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
from .commons import damping_profile, cupy_check, avoid_PML1D, avoid_PML2D, avoid_PML3D
from math import ceil


is_DEBUG = False
is_DEBUG = True


class EM3D:
    """
    Python object designed for simple 3D finite difference time domain (FDTD) simulation in open space.
    Allows slit diffraction testing
    """
    def __init__(self,
                 Lx: float = 20., Ly: float = 20., Lz: float = 20.,
                 Nx: int = 100, Ny: int = 101, Nz: int = 102,
                 wavelength: float = 3,
                 exponential_PML: bool=True, use_CuPy: bool=True,
                 pml_width: int = 20, sigma_max = 5, pml_p: int = 2
                 ):
        """
        Object constuctor
        :param Lx: is the x dimension of the simulation domain
        :param Ly: is the y dimension of the simulation domain
        :param Lz: is the z dimension of the simulation domain
        :param Nx: is the number of sampling points along the x axis
        :param Ny: is the number of sampling points along the y axis
        :param Nz: is the number of sampling points along the z axis
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
        self.Exy = None
        self.Exz = None
        self.Ex = None
        self.Eyz = None
        self.Eyx = None
        self.Ey = None
        self.Ezx = None
        self.Ezy = None
        self.Ez = None
        self.Hx = None
        self.Hxy = None
        self.Hxz = None
        self.Hy = None
        self.Hyz = None
        self.Hyx = None
        self.Hz = None
        self.Hzx = None
        self.Hzy = None
        # domain parameters
        self.Lx = None
        self.Ly = None
        self.Lz = None
        self.Nx = None
        self.Ny = None
        self.Nz = None
        self.dx = None
        self.dy = None
        self.dz = None
        self.x = None
        self.y = None
        self.z = None
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
        self.exp_sE_z = None
        self.exp_sH_x = None
        self.exp_sH_y = None
        self.exp_sH_z = None
        self.sE_x = None
        self.sE_y = None
        self.sE_z = None
        self.sH_x = None
        self.sH_y = None
        self.sH_z = None
        # Incoming wave parameters
        self.wavelength = None
        self.k = None
        self.omega = None
        # Wave velocity
        self.c = 1

        self.init_domain(Lx, Ly, Lz, Nx, Ny, Nz)
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

    def init_domain(self, Lx, Ly, Lz, Nx, Ny, Nz):
        """
        Init domain
        :param Lx: is the x dimension of the simulation domain
        :param Ly: is the y dimension of the simulation domain
        :param Lz: is the z dimension of the simulation domain
        :param Nx: is the number of sampling points along the x axis
        :param Ny: is the number of sampling points along the y axis
        :param Nz: is the number of sampling points along the z axis
        """
        # domain size
        self.Lx = Lx
        self.Ly = Ly
        self.Lz = Lz

        # number of grid points
        self.Nx = Nx
        self.Ny = Ny
        self.Nz = Nz

        self.dx = self.Lx / self.Nx  # grid spacing in x direction
        self.dy = self.Ly / self.Ny  # grid spacing in y direction
        self.dz = self.Lz / self.Nz  # grid spacing in z direction
        if self.use_CuPy:
            self.dx = self.xp.array([self.dx], dtype=self.dtype)
            self.dy = self.xp.array([self.dy], dtype=self.dtype)
            self.dz = self.xp.array([self.dz], dtype=self.dtype)

    def Courant(self):
        """
        The convergence condition by Courant–Friedrichs–Lewy (stability criterion of difference scheme)
        :return: time step
        """
        return 1 / (self.c * self.xp.sqrt(1 / self.dx ** 2 + 1 / self.dy ** 2 + 1 / self.dz ** 2))

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
        sigmaE_z = self.xp.zeros(self.Nz, dtype=self.dtype)
        sigmaH_x = self.xp.zeros(self.Nx - 1, dtype=self.dtype)
        sigmaH_y = self.xp.zeros(self.Ny - 1, dtype=self.dtype)
        sigmaH_z = self.xp.zeros(self.Nz - 1, dtype=self.dtype)

        i_pml = self.xp.arange(1, self.pml_width+1, dtype=self.dtype)
        sigmaE_x[range(self.pml_width-1, -1, -1)]\
            = sigmaE_y[range(self.pml_width-1, -1, -1)]\
            = sigmaE_z[range(self.pml_width-1, -1, -1)]\
            = sigmaE_x[-self.pml_width:]\
            = sigmaE_y[-self.pml_width:]\
            = sigmaE_z[-self.pml_width:]\
            = damping_profile(i_pml, self.pml_width, self.sigma_max, self.pml_p)
        
        sigmaH_x[range(self.pml_width-1, -1, -1)]\
            = sigmaH_y[range(self.pml_width-1, -1, -1)]\
            = sigmaH_z[range(self.pml_width-1, -1, -1)]\
            = sigmaH_x[-self.pml_width:]\
            = sigmaH_y[-self.pml_width:]\
            = sigmaH_z[-self.pml_width:]\
            = damping_profile(i_pml - 0.5, self.pml_width, self.sigma_max, self.pml_p)

        C = 1 / 2 # in dt units
        sE_x = sigmaE_x[1:-1, self.xp.newaxis, self.xp.newaxis] * C
        sH_x = sigmaH_x[:, self.xp.newaxis, self.xp.newaxis] * C
        sE_y = sigmaE_y[self.xp.newaxis, 1:-1, self.xp.newaxis] * C
        sH_y = sigmaH_y[self.xp.newaxis, :, self.xp.newaxis] * C
        sE_z = sigmaE_z[self.xp.newaxis, self.xp.newaxis, 1:-1] * C
        sH_z = sigmaH_z[self.xp.newaxis, self.xp.newaxis, :] * C

        if self.exponential_PML:
            self.exp_sE_x = self.xp.exp(-sE_x)
            self.exp_sH_x = self.xp.exp(-sH_x)
            self.exp_sE_y = self.xp.exp(-sE_y)
            self.exp_sH_y = self.xp.exp(-sH_y)
            self.exp_sE_z = self.xp.exp(-sE_z)
            self.exp_sH_z = self.xp.exp(-sH_z)
        else:
            self.sE_x = sE_x
            self.sH_x = sH_x
            self.sE_y = sE_y
            self.sH_y = sH_y
            self.sE_z = sE_z
            self.sH_z = sH_z

    def init_fields(self):
        """
        Init fields (Yee mesh)
        """
        self.n_step = 0

        # x-components of the electric field (1, 2)
        self.Exy = self.xp.zeros((self.Nx-1, self.Ny, self.Nz), dtype=self.dtype)
        self.Exz = self.xp.zeros((self.Nx-1, self.Ny, self.Nz), dtype=self.dtype)
        self.Ex = self.Exy - self.Exz

        # y-components of the electric field (1, 2)
        self.Eyz = self.xp.zeros((self.Nx, self.Ny-1, self.Nz), dtype=self.dtype)
        self.Eyx = self.xp.zeros((self.Nx, self.Ny-1, self.Nz), dtype=self.dtype)
        self.Ey = self.Eyz - self.Eyx

        # z-component of the electric field (1, 2)
        self.Ezx = self.xp.zeros((self.Nx, self.Ny, self.Nz-1), dtype=self.dtype)
        self.Ezy = self.xp.zeros((self.Nx, self.Ny, self.Nz-1), dtype=self.dtype)
        self.Ez = self.Ezx - self.Ezy

        # x-component of the magnetic field (1, 2)
        self.Hxy = self.xp.zeros((self.Nx-2, self.Ny-1, self.Nz-1), dtype=self.dtype)
        self.Hxz = self.xp.zeros((self.Nx-2, self.Ny-1, self.Nz-1), dtype=self.dtype)
        self.Hx = self.Hxz - self.Hxy

        # y-component of the magnetic field (1, 2)
        self.Hyz = self.xp.zeros((self.Nx-1, self.Ny-2, self.Nz-1), dtype=self.dtype)
        self.Hyx = self.xp.zeros((self.Nx-1, self.Ny-2, self.Nz-1), dtype=self.dtype)
        self.Hy = self.Hyx - self.Hyz

        # z-component of the magnetic field (1, 2)
        self.Hzx = self.xp.zeros((self.Nx-1, self.Ny-1, self.Nz-2), dtype=self.dtype)
        self.Hzy = self.xp.zeros((self.Nx-1, self.Ny-1, self.Nz-2), dtype=self.dtype)
        self.Hz = self.Hzy - self.Hzx

    def create_grid(self):
        """
        Create grid
        """
        self.x = self.xp.linspace(-self.Lx/2, self.Lx/2, self.Nx, dtype=self.dtype)
        self.y = self.xp.linspace(-self.Ly/2, self.Ly/2, self.Ny, dtype=self.dtype)
        self.z = self.xp.linspace(-self.Lz/2, self.Lz/2, self.Nz, dtype=self.dtype)
        # X, Y, Z = self.xp.meshgrid(x, y, z, indexing="ij")

    def update_E(self):
        """
        Updating the electric field components over one simulation cycle.
        """
        # Update Ex => dHy_dz - dHz_dy
        dHy_dz = (self.C / self.dz) * self.xp.diff(self.Hy, axis=2)
        dHz_dy = (self.C / self.dy) * self.xp.diff(self.Hz, axis=1)
        if self.exponential_PML:
            wx = self.exp_sE_x
            wy = self.exp_sE_y
            wz = self.exp_sE_z
            self.Exy[:, 1:-1, 1:-1] = wz * (wz * self.Exy[:, 1:-1, 1:-1] + dHy_dz)
            self.Exz[:, 1:-1, 1:-1] = wy * (wy * self.Exz[:, 1:-1, 1:-1] + dHz_dy)
        else:
            self.Exy[:, 1:-1, 1:-1] = ((1 - self.sE_z) * self.Exy[:, 1:-1, 1:-1] + dHy_dz) / (1 + self.sE_z)
            self.Exz[:, 1:-1, 1:-1] = ((1 - self.sE_y) * self.Exz[:, 1:-1, 1:-1] + dHz_dy) / (1 + self.sE_y)

        self.Ex = self.Exy - self.Exz

        # Update Ey => dHz_dx - dHx_dz
        dHz_dx = (self.C / self.dx) * self.xp.diff(self.Hz, axis=0)
        dHx_dz = (self.C / self.dz) * self.xp.diff(self.Hx, axis=2)
        if self.exponential_PML:
            self.Eyz[1:-1, :, 1:-1] = wx * (wx * self.Eyz[1:-1, :, 1:-1] + dHz_dx)
            self.Eyx[1:-1, :, 1:-1] = wz * (wz * self.Eyx[1:-1, :, 1:-1] + dHx_dz)
        else:
            self.Eyz[1:-1, :, 1:-1] = ((1 - self.sE_x) * self.Eyz[1:-1, :, 1:-1] + dHz_dx) / (1 + self.sE_x)
            self.Eyx[1:-1, :, 1:-1] = ((1 - self.sE_z) * self.Eyx[1:-1, :, 1:-1] + dHx_dz) / (1 + self.sE_z)

        self.Ey = self.Eyz - self.Eyx

        # Update Ez => dHx_dy - dHy_dx
        dHx_dy = (self.C / self.dy) * self.xp.diff(self.Hx, axis=1)
        dHy_dx = (self.C / self.dx) * self.xp.diff(self.Hy, axis=0)
        if self.exponential_PML:
            self.Ezx[1:-1, 1:-1, :] = wy * (wy * self.Ezx[1:-1, 1:-1, :] + dHx_dy)
            self.Ezy[1:-1, 1:-1, :] = wx * (wx * self.Ezy[1:-1, 1:-1, :] + dHy_dx)
        else:
            self.Ezx[1:-1, 1:-1, :] = ((1 - self.sE_y) * self.Ezx[1:-1, 1:-1, :] + dHx_dy) / (1 + self.sE_y)
            self.Ezy[1:-1, 1:-1, :] = ((1 - self.sE_x) * self.Ezy[1:-1, 1:-1, :] + dHy_dx) / (1 + self.sE_x)

        self.Ez = self.Ezx - self.Ezy

    def update_H(self):
        """
        Updating the magnetic field components over one simulation cycle.
        """
        # Update Hx => -(dEy_dz - dEz_dy)
        dEy_dz = (self.C / self.dz) * self.xp.diff(self.Ey[1:-1, :, :], axis=2)
        dEz_dy = (self.C / self.dy) * self.xp.diff(self.Ez[1:-1, :, :], axis=1)
        if self.exponential_PML:
            wx = self.exp_sH_x
            wy = self.exp_sH_y
            wz = self.exp_sH_z
            self.Hxy = wz * (wz * self.Hxy + dEy_dz)
            self.Hxz = wy * (wy * self.Hxz + dEz_dy)
        else:
            self.Hxy= ((1 - self.sH_z) * self.Hxy + dEy_dz) / (1 + self.sH_z)
            self.Hxz = ((1 - self.sH_y) * self.Hxz + dEz_dy) / (1 + self.sH_y)

        self.Hx = self.Hxz - self.Hxy

        # Update Hy => -(dEz_dx - dEx_dz)
        dEz_dx = (self.C / self.dx) * self.xp.diff(self.Ez[:, 1:-1, :], axis=0)
        dEx_dz = (self.C / self.dz) * self.xp.diff(self.Ex[:, 1:-1, :], axis=2)
        if self.exponential_PML:
            self.Hyz = wx * (wx * self.Hyz + dEz_dx)
            self.Hyx = wz * (wz * self.Hyx + dEx_dz)
        else:
            self.Hyz = ((1 - self.sH_x) * self.Hyz + dEz_dx) / (1 + self.sH_x)
            self.Hyx = ((1 - self.sH_z) * self.Hyx + dEx_dz) / (1 + self.sH_z)

        self.Hy = self.Hyx - self.Hyz

        # Update Hz => -(dEz_dx - dEx_dz)
        dEx_dy = (self.C / self.dy) * self.xp.diff(self.Ex[:, :, 1:-1], axis=1)
        dEy_dx = (self.C / self.dx) * self.xp.diff(self.Ey[:, :, 1:-1], axis=0)
        if self.exponential_PML:
            self.Hzx = wy * (wy * self.Hzx + dEx_dy)
            self.Hzy = wx * (wx * self.Hzy + dEy_dx)
        else:
            self.Hzx = ((1 - self.sH_y) * self.Hzx + dEx_dy) / (1 + self.sH_y)
            self.Hzy = ((1 - self.sH_x) * self.Hzy + dEy_dx) / (1 + self.sH_x)

        self.Hz = self.Hzy - self.Hzx

    def update_output(self):
        """
        accumulate field intensity over one period of the incoming wave
        """
        self.I_tmp += self.Ez[self.out_pos, :, :] ** 2
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
            3 accumulation the z-component of the Poynting vector
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
        elif accumulation_type == 3:
            self.accumulate = True
            self.S_func = self._get_Sz
        self.S_tmp *= 0
        self.count = 0
        self.S = None

    @cupy_check
    @avoid_PML3D
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
        self.Ez[ix, 2:-2, 2:-2] += self.xp.sin(wt) / (self.omega * self.dt)

    def add_incident_wave_Hy(self):
        """
        add incoming wave
        """
        wt = self.omega * self.n_step * self.dt
        ix = self.pml_width + 1
        self.Hy[ix, 2:-2, 2:-2] += self.xp.sin(wt) / (self.omega * self.dt)

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
    @avoid_PML1D
    def get_z(self, show_PML: bool=False):
        """
        Get the z coordinate
        :param show_PML: with or without the PML region
        :return: y coordinate
        """
        return self.z

    @cupy_check
    @avoid_PML3D
    def get_Ex(self, show_PML: bool=False):
        """
        Get the x-component of the electric field
        :param show_PML: with or without the PML region
        :return: the z-component of the electric field
        """
        return self.Ex

    @cupy_check
    @avoid_PML3D
    def get_Ey(self, show_PML: bool=False):
        """
        Get the y-component of the electric field
        :param show_PML: with or without the PML region
        :return: the z-component of the electric field
        """
        return self.Ey

    @cupy_check
    @avoid_PML3D
    def get_Ez(self, show_PML: bool=False):
        """
        Get the z-component of the electric field
        :param show_PML: with or without the PML region
        :return: the z-component of the electric field
        """
        return self.Ez

    @cupy_check
    @avoid_PML3D
    def get_Hx(self, show_PML: bool=False):
        """
        Get the x-component of the magnetic field
        :param show_PML: with or without the PML region
        :return: the z-component of the magnetic field
        """
        return self.Hx

    @cupy_check
    @avoid_PML3D
    def get_Hy(self, show_PML: bool=False):
        """
        Get the y-component of the magnetic field
        :param show_PML: with or without the PML region
        :return: the z-component of the magnetic field
        """
        return self.Hy

    @cupy_check
    @avoid_PML3D
    def get_Hz(self, show_PML: bool=False):
        """
        Get the z-component of the magnetic field
        :param show_PML: with or without the PML region
        :return: the z-component of the magnetic field
        """
        return self.Hz

    @cupy_check
    @avoid_PML2D
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
        return (self.Ey[1:-1, 1:, 1:-1] * (self.Hz[1:, 1:, :] + self.Hz[:-1, 1:, :])
                +self.Ey[1:-1, :-1, 1:-1] * (self.Hz[1:, :-1, :] + self.Hz[:-1, :-1, :])
                -self.Ez[1:-1, 1:-1, 1:] * (self.Hy[1:, :, 1:] + self.Hy[:-1, :, 1:])
                -self.Ez[1:-1, 1:-1, :-1] * (self.Hy[1:, :, :-1] + self.Hy[:-1, :, :-1])) / 4

    def _get_Sy(self):
        """
        Get the y-component of the Poynting vector
        :return: the y-component of the Poynting vector (in CUDA if cupy is used)
        """
        return (self.Ez[1:-1, 1:-1, 1:] * (self.Hx[:, 1:, 1:] + self.Hx[:, :-1, 1:])
                +self.Ez[1:-1, 1:-1, :-1] * (self.Hx[:, 1:, :-1] + self.Hx[:, :-1, :-1])
                -self.Ex[1:, 1:-1, 1:-1] * (self.Hz[1:, 1:, :] + self.Hz[1:, :-1, :])
                -self.Ex[:-1, 1:-1, 1:-1] * (self.Hz[:-1, 1:, :] + self.Hz[:-1, :-1, :])) / 4

    def _get_Sz(self):
        """
        Get the z-component of the Poynting vector
        :return: the z-component of the Poynting vector (in CUDA if cupy is used)
        """
        return (self.Ex[1:, 1:-1, 1:-1] * (self.Hy[1:, :, 1:] + self.Hy[1:, :, :-1])
                +self.Ex[:-1, 1:-1, 1:-1] * (self.Hy[:-1, :, 1:] + self.Hy[:-1, :, :-1])
                -self.Ey[1:-1, 1:, 1:-1] * (self.Hx[:, 1:, 1:] + self.Hx[:, 1:, :-1])
                -self.Ey[1:-1, :-1, 1:-1] * (self.Hx[:, :-1, 1:] + self.Hx[:, :-1, :-1])) / 4

    def _get_S(self):
        """
        Get the absolute value of the Poynting vector
        :return: the absolute value of the Poynting vector
        """
        return self.xp.sqrt(self._get_Sx()**2 + self._get_Sy()**2 + self._get_Sz()**2)

    @cupy_check
    @avoid_PML3D
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
        :condition_func: f(x,y,z) to set zeros
        """
        X, Y, Z = self.xp.meshgrid((self.x[1:] + self.x[:-1]) / 2, self.y, self.z, indexing="ij")
        cond_x = condition_func(X, Y, Z)
        X, Y, Z = self.xp.meshgrid(self.x, (self.y[1:] + self.y[:-1]) / 2, self.z, indexing="ij")
        cond_y = condition_func(X, Y, Z)
        X, Y, Z = self.xp.meshgrid(self.x, self.y, (self.z[1:] + self.z[:-1]) / 2, indexing="ij")
        cond_z = condition_func(X, Y, Z)

        def apply_PEC_slit(self):
            self.Ex[cond_x] = 0
            self.Ey[cond_y] = 0
            self.Ez[cond_z] = 0

        self.apply_PEC = lambda self=self: apply_PEC_slit(self)
