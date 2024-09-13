from functools import wraps
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


# Damping profiles
def damping_profile(x, width, max_value, p_pml):
    """
    Damping profile.
    """
    return max_value * (x / width)**p_pml


def cupy_check(func):
    def wrapper(self, *args, **kwargs):
        out = func(self, *args, **kwargs)
        if self.use_CuPy and out is not None:
            return out.get()  # Transfer to CPU
        return out
    return wrapper


def avoid_PML1D(func):
    def wrapper(self, show_PML, *args, **kwargs):
        out = func(self, show_PML, *args, **kwargs)
        if out is not None:
            if show_PML:
                return out
            return out[self.pml_width:-self.pml_width]
    return wrapper


def avoid_PML2D(func):
    def wrapper(self, show_PML, *args, **kwargs):
        out = func(self, show_PML, *args, **kwargs)
        if out is not None:
            if show_PML:
                return out
            return out[self.pml_width:-self.pml_width, self.pml_width:-self.pml_width]
    return wrapper


def avoid_PML3D(func):
    def wrapper(self, show_PML, *args, **kwargs):
        out = func(self, show_PML, *args, **kwargs)
        if out is not None:
            if show_PML:
                return out
            return out[
                   self.pml_width:-self.pml_width,
                   self.pml_width:-self.pml_width,
                   self.pml_width:-self.pml_width
                   ]
    return wrapper


## Display functions
# Create a colormap from red to blue
cmap_spectral = plt.colormaps.get_cmap('Spectral_r')

def wavelength_to_colormap(wavelength, norm):
    # Normalize the wavelength
    norm_wavelength = norm(wavelength)
    # Get the color from the colormap
    color = cmap_spectral(norm_wavelength)[:-1]
    colors = [(0, 0, 0), color, (1, 1, 1)]  # Black -> Color
    n_bins = 100  # Number of bins for interpolation
    cmap_name = 'black2color'
    return LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)


def pause(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.ani.event_source.stop()  # Pause the animation
        out = func(self, *args, **kwargs)
        self.ani.event_source.start()  # Resume the animation
        return out
    return wrapper


