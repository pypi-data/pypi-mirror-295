# pip install AKFDTD
from FDTD.fdtd2D import EM2D
from FDTD.display_fields2D import DisplayFields2D


if __name__ == "__main__":
    # display PML region
    show_PML = False
    # show_PML = True

    # display absolute value of the Poynting vector
    show_Poynting = True
    # show_Poynting = False

    # display of the field distribution along the center of the calculation area
    show_xy = False
    # show_xy = True

    # incoming plane wave wavelength
    wavelength_init = 3
    wavelength_min = 1
    wavelength_max = 5

    # simulation domain
    Lx = 30
    Ly = 20
    # Nx = 300
    # Ny = 201
    Nx = 200
    Ny = 151

    # slit width
    slit_width_init = 3
    slit_width_min = 1
    slit_width_max = 10
    slit_position_init = -Lx/2 + 8
    slit_screen_thickness = 0.5

    # create FDTD domain and initialize fields3D
    fields = EM2D(Lx=Lx, Ly=Ly, Nx=Nx, Ny=Ny, wavelength=wavelength_init)

    # set single rectangular slit
    def slit_func(hy):
        x0 = slit_position_init
        hx = slit_screen_thickness
        y0 = 0
        condition_func = lambda x, y: (x0 - hx/2 < x) & (x< x0 + hx/2) & ((y0 - hy/2 > y) | (y > y0 + hy/2))
        fields.set_slit(condition_func)

    slit_func(slit_width_init)

    # Initial condition
    N_cycles = 500
    N_cycles = 1

    display_fields = DisplayFields2D(
        fields,
        displayed_wavelengths=(wavelength_min, wavelength_init, wavelength_max),
        displayed_slit_widths=(slit_width_min, slit_width_init, slit_width_max),
        slit_func=slit_func,
        show_Poynting=show_Poynting, show_PML=show_PML, show_xy=show_xy)
    display_fields.N_cycles = N_cycles
    display_fields.show()
