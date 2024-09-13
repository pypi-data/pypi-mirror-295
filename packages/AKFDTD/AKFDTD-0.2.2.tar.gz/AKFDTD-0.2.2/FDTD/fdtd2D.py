try:
    import cupy as cp
    # Check if CUDA is available
    if cp.cuda.is_available():
        print("CUDA is available.")
    else:
        raise ImportError("CUDA is not available. Falling back to NumPy.")
except ImportError as e:
    print(e)
    import numpy as np
    print("Using NumPy. To use CuPy install it first: pip install cupy-cuda12x")

import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.animation import FuncAnimation
from timeit import default_timer as timer
from .commons import damping_profile, cupy_check, avoid_PML1D, avoid_PML2D
from math import ceil


is_DEBUG = False
is_DEBUG = True


class EM2D:
    """
    Python object designed for simple 2D finite difference time domain (FDTD) simulation in open space.
    Allows slit diffraction testing
    """
    def __init__(self,
                 Lx: float = 20., Ly: float = 20.,
                 Nx: int = 200, Ny: int = 201,
                 wavelength: float = 3,
                 exponential_PML: bool=True, use_CuPy: bool=True,
                 pml_width: int = 20, sigma_max = 5, pml_p: int = 2
                 ):
        """
        Object constuctor
        :param Lx: is the x dimension of the simulation domain
        :param Ly: is the y dimension of the simulation domain
        :param Nx: is the number of sampling points along the x axis
        :param Ny: is the number of sampling points along the y axis
        :param wavelength: is the wavelength of the incoming wave.
        :param exponential_PML: selecting a PML update scheme
        :param use_CuPy: use CUDA if exist
        :param pml_width: is the number of points used for the PML width
        :param sigma_max: is the maximum sigma value for PML (in  1 / dt units)
        :param pml_p: is the order of sigma function
        """

        if use_CuPy and 'cp' in globals():
            self.xp = cp
            self.use_CuPy = True
            print("Using CuPy.")
        else:
            if 'numpy' not in globals():
                import numpy as np
            self.xp = np
            self.use_CuPy = False

        self.exponential_PML = exponential_PML

        self.dtype = self.xp.float32

        # function to apply PEC condition (for example, a slit)
        self.apply_PEC = lambda: None

        # field components
        self.Ezx = None
        self.Ezy = None
        self.Ez = None
        self.Hx = None
        self.Hy = None
        # domain parameters
        self.Lx = None
        self.Ly = None
        self.Nx = None
        self.Ny = None
        self.dx = None
        self.dy = None
        self.x = None
        self.y = None
        # time step
        self.n_step = 0
        # time parameters
        self.Nt = None #  number of cycles in one period of the incoming wave
        self.dt = None
        # PML parameters
        self.pml_width = None
        self.sigma_max = None
        self.pml_p = None
        # PML coefficient for the fields calculations
        self.exp_sE_x = None
        self.exp_sE_y = None
        self.exp_sH_x = None
        self.exp_sH_y = None
        self.sE_x = None
        self.sE_y = None
        self.sH_x = None
        self.sH_y = None
        # Incoming wave parameters
        self.wavelength = None
        self.k = None
        self.omega = None
        # Wave velocity
        self.c = 1

        self.init_domain(Lx, Ly, Nx, Ny)
        self.create_grid()
        self.set_PML(pml_width, sigma_max, pml_p)

        self.set_wavelength(wavelength)

        # self.init_fields()
        # accumulator of the absolute value of the field intensity at the end of the wave propagation at out_pos
        self.out_pos = -self.pml_width - 2
        self.I_tmp = 0
        self.I_out = None
        # accumulator of the absolute value of the Poynting vector
        self.accumulate: bool = False
        self.count = 0
        self.S_func = lambda x: None
        self.S_tmp = 0
        self.S = None
        self.dS = 1e5

    def set_wavelength(self, wavelength):
        """
        Set the wavelength for incoming wave and the time step relative to one period of the incoming wave and taking into account the Courant condition
        :param wavelength: is the wavelength of the incoming wave.
        """
        # Wavelength of the incident wave
        self.wavelength = wavelength
        # λ = c / f -> f = c / λ
        # Wave number
        self.k = 2 * self.xp.pi / self.wavelength
        # Angular frequency
        self.omega = self.c * self.k

        # update dt
        # T = λ / c
        T = self.wavelength / self.c
        dt0 = 0.75 * self.Courant()
        self.Nt = ceil(T / dt0)
        self.dt = T / self.Nt
        # print(f"{self.dt/self.Courant()}")

        self.C = self.dt/self.c
        if self.use_CuPy:
            self.C = self.xp.array([self.C], dtype=self.dtype)

    def init_domain(self, Lx, Ly, Nx, Ny):
        """
        Init domain
        :param Lx: is the x dimension of the simulation domain
        :param Ly: is the y dimension of the simulation domain
        :param Nx: is the number of sampling points along the x axis
        :param Ny: is the number of sampling points along the y axis
        """
        # domain size
        self.Lx = Lx
        self.Ly = Ly

        # number of grid points
        self.Nx = Nx
        self.Ny = Ny

        self.dx = self.Lx / self.Nx  # grid spacing in x direction
        self.dy = self.Ly / self.Ny  # grid spacing in y direction
        if self.use_CuPy:
            self.dx = self.xp.array([self.dx], dtype=self.dtype)
            self.dy = self.xp.array([self.dy], dtype=self.dtype)

    def Courant(self):
        """
        The convergence condition by Courant–Friedrichs–Lewy (stability criterion of difference scheme)
        :return: time step
        """
        return 1 / (self.c * self.xp.sqrt(1 / self.dx ** 2 + 1 / self.dy ** 2))

    def set_PML(self, pml_width: int = 20, sigma_max = 1, pml_p: int = 2):
        """
        Init PML parameters
        :param pml_width: is the number of points used for the PML width
        :param sigma_max: is the maximum sigma value for PML (in  1 / dt units)
        :param pml_p: is the order of sigma function
        """
        self.pml_width = pml_width
        self.sigma_max = sigma_max
        self.pml_p = pml_p
        self.init_PML()

    def init_PML(self):
        """
        Init PML (Yee mesh)
        """
        # PML damping profiles
        sigmaE_x = self.xp.zeros(self.Nx, dtype=self.dtype)
        sigmaE_y = self.xp.zeros(self.Ny, dtype=self.dtype)
        sigmaH_x = self.xp.zeros(self.Nx - 1, dtype=self.dtype)
        sigmaH_y = self.xp.zeros(self.Ny - 1, dtype=self.dtype)

        i_pml = self.xp.arange(1, self.pml_width+1, dtype=self.dtype)
        sigmaE_x[range(self.pml_width-1, -1, -1)]\
            = sigmaE_y[range(self.pml_width-1, -1, -1)]\
            = sigmaE_x[-self.pml_width:]\
            = sigmaE_y[-self.pml_width:]\
            = damping_profile(i_pml, self.pml_width, self.sigma_max, self.pml_p)
        
        sigmaH_x[range(self.pml_width-1, -1, -1)]\
            = sigmaH_y[range(self.pml_width-1, -1, -1)]\
            = sigmaH_x[-self.pml_width:]\
            = sigmaH_y[-self.pml_width:]\
            = damping_profile(i_pml - 0.5, self.pml_width, self.sigma_max, self.pml_p)

        C = 1 / 2 # in dt units
        sE_x = sigmaE_x[1:-1, self.xp.newaxis] * C
        sH_x = sigmaH_x[:, self.xp.newaxis] * C
        sE_y = sigmaE_y[self.xp.newaxis, 1:-1] * C
        sH_y = sigmaH_y[self.xp.newaxis, :] * C

        if self.exponential_PML:
            self.exp_sE_x = self.xp.exp(-sE_x)
            self.exp_sH_x = self.xp.exp(-sH_x)
            self.exp_sE_y = self.xp.exp(-sE_y)
            self.exp_sH_y = self.xp.exp(-sH_y)
        else:
            self.sE_x = sE_x
            self.sH_x = sH_x
            self.sE_y = sE_y
            self.sH_y = sH_y

    def init_fields(self):
        """
        Init fields (Yee mesh)
        """
        self.n_step = 0

        # z-components of the electric field (1, 2)
        self.Ezx = self.xp.zeros((self.Nx, self.Ny), dtype=self.dtype)
        self.Ezy = self.xp.zeros((self.Nx, self.Ny), dtype=self.dtype)
        self.Ez = self.Ezx - self.Ezy

        # x-component of the magnetic field
        self.Hx = self.xp.zeros((self.Nx-2, self.Ny-1), dtype=self.dtype)
        # y-component of the magnetic field
        self.Hy = self.xp.zeros((self.Nx-1, self.Ny-2), dtype=self.dtype)

    def create_grid(self):
        """
        Create grid
        """
        self.x = self.xp.linspace(-self.Lx/2, self.Lx/2, self.Nx, dtype=self.dtype)
        self.y = self.xp.linspace(-self.Ly/2, self.Ly/2, self.Ny, dtype=self.dtype)

    def update_E(self):
        """
        Updating the electric field components over one simulation cycle.
        """
        # Update Ez => dHx_dy - dHy_dx
        dHx_dy = (self.C / self.dy) * self.xp.diff(self.Hx, axis=1)
        dHy_dx = (self.C / self.dx) * self.xp.diff(self.Hy, axis=0)
        if self.exponential_PML:
            wx = self.exp_sE_x
            wy = self.exp_sE_y
            self.Ezx[1:-1, 1:-1] = wy * (wy * self.Ezx[1:-1, 1:-1] + dHx_dy)
            self.Ezy[1:-1, 1:-1] = wx * (wx * self.Ezy[1:-1, 1:-1] + dHy_dx)
        else:
            self.Ezx[1:-1, 1:-1] = ((1 - self.sE_y) * self.Ezx[1:-1, 1:-1] + dHx_dy) / (1 + self.sE_y)
            self.Ezy[1:-1, 1:-1] = ((1 - self.sE_x) * self.Ezy[1:-1, 1:-1] + dHy_dx) / (1 + self.sE_x)

        self.Ez = self.Ezx - self.Ezy

    def update_H(self):
        """
        Updating the magnetic field components over one simulation cycle.
        """
        # Update Hx => -(0 - dEz_dy)
        dEz_dy = (self.C / self.dy) * self.xp.diff(self.Ez[1:-1, :], axis=1)
        dEz_dx = (self.C / self.dx) * self.xp.diff(self.Ez[:, 1:-1], axis=0)
        if self.exponential_PML:
            wx = self.exp_sH_x
            wy = self.exp_sH_y
            self.Hx = wy * (wy * self.Hx + dEz_dy)
            self.Hy = wx * (wx * self.Hy - dEz_dx)
        else:
            self.Hx = ((1 - self.sH_y) * self.Hx + dEz_dy) / (1 + self.sH_y)
            self.Hy = ((1 - self.sH_x) * self.Hy - dEz_dx) / (1 + self.sH_x)

    def update_output(self):
        """
        accumulate field intensity over one period of the incoming wave
        """
        self.I_tmp += self.Ez[self.out_pos, :] ** 2
        if self.n_step % self.Nt == 0:
            self.I_out = self.I_tmp / self.Nt
            self.I_tmp *= 0

    def update_S(self):
        """
        accumulate energy (the absolute value of the Poynting vector) over one period of the incoming wave
        """
        tmp = self.S_func()
        if self.count == self.Nt:
            self.S_tmp = (self.S_tmp + tmp / 2) / self.Nt
            if self.S is not None:
                self.dS = self.xp.linalg.norm(self.S - self.S_tmp)
                print(f"dS = {self.dS:.5g}")
            self.S = self.S_tmp.copy()
            self.S_tmp = tmp / 2
            self.count = 0
        else:
            self.S_tmp += tmp
        self.count += 1


    def update(self):
        """
        Updating fields over time (one simulation cycle).
        """
        self.n_step += 1

        # (electric field components)
        self.update_E()

        # Incident wave
        # self.add_incident_wave_Ez()

        # Define the slit in the PEC boundary
        self.apply_PEC()

        # (magnetic field components)
        self.update_H()

        # Incident wave
        self.add_incident_wave_Hy()

        # accumulate field intensity over one period of the incoming wave
        self.update_output()

        # accumulate energy
        if self.accumulate:
            self.update_S()

    def set_accumulate_S(self, accumulation_type: int = 0):
        """
        Initialize the Poynting vector components to accumulated along one period of the incoming wave
        :param accumulation_type: use accumulation type:
            -1 no accumulation
            0 accumulation the absolute value of the Poynting vector
            1 accumulation the x-component of the Poynting vector
            2 accumulation the y-component of the Poynting vector
        """
        if accumulation_type == -1:
            self.accumulate = False
        elif accumulation_type == 0:
            self.accumulate = True
            self.S_func = self._get_S
        elif accumulation_type == 1:
            self.accumulate = True
            self.S_func = self._get_Sx
        elif accumulation_type == 2:
            self.accumulate = True
            self.S_func = self._get_Sy
        self.S_tmp *= 0
        self.count = 0
        self.S = None

    @cupy_check
    @avoid_PML2D
    def get_accumulate_S(self, show_PML: bool = True):
        """
        return accumulated the Poynting vector components
        """
        return self.S

    def add_incident_wave_Ez(self):
        """
        add incoming wave
        """
        wt = self.omega * self.n_step * self.dt
        ix = self.pml_width + 1
        self.Ez[ix, 2:-2] += self.xp.sin(wt) / (self.omega * self.dt)

    def add_incident_wave_Hy(self):
        """
        add incoming wave
        """
        wt = self.omega * self.n_step * self.dt
        ix = self.pml_width + 1
        self.Hy[ix, 2:-2] += self.xp.sin(wt)

    def do_n(self, N_cycles):
        """
        Performing N_cycles simulation cycles.
        """
        if is_DEBUG:
            start = timer()

        for _ in range(N_cycles):
            self.update()

        if is_DEBUG:
            execution = timer()-start
            print(f"Calculation time {execution:.4f} s (one cycle: {execution / N_cycles*1000:.4f} ms))")

    def start_until(self, N_cycles=300):
        """
        Performing simulations until fields saturation
        :param show_PML: with or without the PML region
        :return: accumulated absolute value of the Poynting vector
        """
        # clear previous simulations
        self.init_fields()

        if N_cycles is not None:
            self.do_n(N_cycles)
        else:
            # number of cycles for wave propagation along the x-axis from the start to the end of calculation area
            N_t = ceil(2 * (self.Lx - 2 * self.dx * self.pml_width) / self.wavelength)
            self.do_n(N_t * self.Nt)

    @cupy_check
    @avoid_PML1D
    def get_x(self, show_PML: bool=False):
        """
        Get the x coordinate
        :param show_PML: with or without the PML region
        :return: x coordinate
        """
        return self.x

    @cupy_check
    @avoid_PML1D
    def get_y(self, show_PML: bool=False):
        """
        Get the y coordinate
        :param show_PML: with or without the PML region
        :return: y coordinate
        """
        return self.y

    @cupy_check
    @avoid_PML2D
    def get_Ez(self, show_PML: bool=False):
        """
        Get the z-component of the electric field
        :param show_PML: with or without the PML region
        :return: the z-component of the electric field
        """
        return self.Ez

    @cupy_check
    @avoid_PML2D
    def get_Hx(self, show_PML: bool=False):
        """
        Get the x-component of the magnetic field
        :param show_PML: with or without the PML region
        :return: the z-component of the magnetic field
        """
        return self.Hx

    @cupy_check
    @avoid_PML2D
    def get_Hy(self, show_PML: bool=False):
        """
        Get the y-component of the magnetic field
        :param show_PML: with or without the PML region
        :return: the z-component of the magnetic field
        """
        return self.Hy

    @cupy_check
    @avoid_PML1D
    def get_out_intensity(self, show_PML: bool=False):
        """
        Get out intensity at the end of wave propagation along the x-axis
        :param show_PML: with or without the PML region
        :return: intensity
        """
        return self.I_out

    def _get_Sx(self):
        """
        Get the x-component of the Poynting vector
        :return: the x-component of the Poynting vector (in CUDA if cupy is used)
        """
        return -self.Ez[1:-1, 1:-1] * (self.Hy[1:, :] + self.Hy[:-1, :]) / 2

    def _get_Sy(self):
        """
        Get the y-component of the Poynting vector
        :return: the y-component of the Poynting vector (in CUDA if cupy is used)
        """
        return self.Ez[1:-1, 1:-1] * (self.Hx[:, 1:] + self.Hx[:, :-1]) / 2

    def _get_S(self):
        """
        Get the absolute value of the Poynting vector
        :return: the absolute value of the Poynting vector
        """
        return self.xp.sqrt(self._get_Sx()**2 + self._get_Sy()**2)

    @cupy_check
    @avoid_PML2D
    def get_S(self, show_PML: bool=False):
        """
        Get the absolute value of the Poynting vector with transfer to CPU if need
        :param show_PML: with or without the PML region
        :return: the absolute value of the Poynting vector
        """
        return self._get_S()

    def set_slit(self, condition_func):
        """
        Set slit(s) by condition function
        :condition_func: f(x,y) to set zeros
        """
        X, Y = self.xp.meshgrid(self.x, self.y, indexing="ij")

        cond = condition_func(X, Y)

        def apply_PEC_slit(self):
            self.Ez[cond] = 0
        self.apply_PEC = lambda self=self: apply_PEC_slit(self)
