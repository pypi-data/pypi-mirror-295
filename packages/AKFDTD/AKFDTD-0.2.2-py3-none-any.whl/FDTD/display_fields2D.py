from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, CheckButtons
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from .commons import cmap_spectral, wavelength_to_colormap, pause


DEBUG = True


class DisplayFields2D:
    N_cycles = 500

    # accumulation_type:
    # 0: the absolute value of the Poynting vector
    # 1: the x-component of the Poynting vector
    # 2: the y-component of the Poynting vector
    accumulation_type = 0

    def __init__(self, fields2D,
                 displayed_wavelengths=(1., 5., 10.),
                 displayed_slit_widths=(1., 5., 10.),
                 slit_func=lambda x: None,
                 show_Poynting: bool = False, show_PML: bool = False, show_xy: bool = False):
        self.fields2D = fields2D
        self.show_Poynting = show_Poynting
        self.show_PML = show_PML
        self.show_xy = show_xy
        self.slit_func = slit_func

        wavelength_min, wavelength_init, wavelength_max = displayed_wavelengths
        # Normalize the wavelength to be between 0 and 1 for colormap
        self.norm = mcolors.Normalize(vmin=wavelength_min, vmax=wavelength_max)

        slit_width_min, slit_width_init, slit_width_max = displayed_slit_widths

        # create a matplotlib window to display the 2D field distribution, the output field intensity,
        # and two sliders (for wavelength and for slit width)
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(5, 7))

        # display fields
        x = self.fields2D.get_x(self.show_PML)
        y = self.fields2D.get_y(self.show_PML)

        self.start_update()

        if self.show_Poynting:
            cm = wavelength_to_colormap(wavelength_init, self.norm)

            out_field = self.fields2D.get_accumulate_S(show_PML=self.show_PML)
            self.im1 = self.ax1.imshow(
                out_field,
                extent=(y.min(), y.max(), x.max(), x.min()),
                cmap=cm,
                origin='upper',
                vmin=0, vmax=1
            )
        else:
            out_field = self.fields2D.get_Ez(self.show_PML)
            self.im1 = self.ax1.imshow(
                out_field,
                extent=(y.min(), y.max(), x.max(), x.min()),
                cmap='RdBu',
                origin='upper',
                vmin=-2, vmax=2
            )
        # Add a title and labels
        self.ax1.set_xlabel('y-axis')
        self.ax1.set_ylabel('x-axis')

        if self.show_xy:
            out_field = self.fields2D.get_Ez(self.show_PML)
            self.im2, = self.ax2.plot(x, abs(out_field[:, self.fields2D.Ny // 2 + 2]))
            self.ax2.set_xlabel('x-axis')
        else:
            out_field = self.fields2D.get_out_intensity(self.show_PML)
            self.im2, = self.ax2.plot(y, out_field)
            self.ax2.set_xlim(y.min(), y.max())
            # ax2.set_ylim(0, 1.6)
            self.ax2.set_xlabel('y-axis')
        self.ax2.set_ylabel('intensity')

        self.ax1.set_position([0.1, 0.5, 0.8, 0.45])  # [left, bottom, width, height]
        out = self.ax1.get_position()
        self.ax2.set_position([out.x0, 0.27, out.x1 - out.x0, 0.15])

        # Create a slider axis and slider widget
        slider_ax1 = plt.axes([0.2, 0.1, 0.6, 0.05], facecolor='lightgoldenrodyellow')
        self.wavelength_slider = Slider(slider_ax1, 'wavelength', wavelength_min, wavelength_max, valinit=wavelength_init)
        # Create an array representing the colormap gradient
        gradient = np.linspace(wavelength_min, wavelength_max, cmap_spectral.N).reshape(1, -1)  # 1D gradient
        slider_ax1.imshow(gradient, aspect='auto', cmap=cmap_spectral, extent=[wavelength_min, wavelength_max, 0, 1])
        self.wavelength_slider.poly.set_facecolor(cmap_spectral(self.norm(wavelength_init)))
        # Connect the slider to the update function
        self.wavelength_slider.on_changed(self.slider_update_wavelength)

        slider_ax2 = plt.axes([0.2, 0.05, 0.6, 0.05], facecolor='lightgoldenrodyellow')
        self.slitwidth_slider = Slider(slider_ax2, 'slit width', slit_width_min, slit_width_max, valinit=slit_width_init)
        # Connect the slider to the update function
        self.slitwidth_slider.on_changed(self.slider_update_slit_width)

        # Create a CheckButtons widget
        poynting_ax = plt.axes([0.03, 0.16, 0.4, 0.04])  # Position for the checkbox
        self.poynting_check = CheckButtons(poynting_ax, ['display energy flow'], [self.show_Poynting])
        # Connect the CheckButtons widget with the toggle function
        self.poynting_check.on_clicked(self.toggle_poynting)

        # Animation setup
        self.ani = FuncAnimation(self.fig, self.update, frames=100, interval=5)

    def show(self):
        """
        display matplotlib plot
        """
        plt.show()
        # plt.pause(0)

    def update_ax1(self):
        """
        update ax1
        """
        if self.show_Poynting:
            out_field = self.fields2D.get_accumulate_S(self.show_PML)
            if out_field is not None:
	            self.im1.set_data(out_field)
                # Autoscale to update color limits if needed
                # self.im1.autoscale()
        else:
            out_field = self.fields2D.get_Ez(self.show_PML)
            # out_field = fields.get_Sx(show_PML)
            self.im1.set_data(out_field)

    def update_ax2(self):
        """
        update ax2
        """
        self.im2.set_ydata(self.fields2D.get_out_intensity(self.show_PML))

        self.ax2.relim()  # Recalculate limits based on new data
        self.ax2.autoscale_view()  # Rescale the view

    def update(self, n):
        """
        Time-stepping loop
        """
        self.fields2D.update()
        if self.show_Poynting:
            if self.fields2D.n_step % self.fields2D.Nt == 0:
                # check calculation saturation
                if self.fields2D.dS < 10:
                    self.ani.event_source.stop()  # Pause the animation
                else:
                    self.update_ax1()
            self.update_ax2()
        else:
            self.update_ax1()
            if self.fields2D.n_step % self.fields2D.Nt == 0:
                self.update_ax2()

    def start_update(self):
        if DEBUG:
            print("start_update")

        if self.show_Poynting:
            # Update the fields until saturation
            self.fields2D.set_accumulate_S(accumulation_type=self.accumulation_type)
            self.fields2D.start_until(None)
            self.fields2D.do_n(self.fields2D.Nt)
        else:
            self.fields2D.set_accumulate_S(accumulation_type=-1)
            self.fields2D.start_until(self.N_cycles)

    @pause
    def slider_update_wavelength(self, val):
        """
        Update wavelength slider
        """
        if self.show_Poynting:
            # Update the colormap
            new_cmap = wavelength_to_colormap(val, self.norm)
            self.im1.set_cmap(new_cmap)

        # Get the color from the colormap
        color = cmap_spectral(self.norm(val))
        self.wavelength_slider.poly.set_facecolor(color)

        # Update the wavelength
        self.fields2D.set_wavelength(wavelength=val)
        # Update the fields
        self.start_update()
        self.update_ax1()
        
    @pause
    def slider_update_slit_width(self, val):
        # change slit
        self.slit_func(val)
        # Update the fields
        self.start_update()
        self.update_ax1()

    @pause
    def toggle_poynting(self, label):
        """
        Define the function to toggle the visibility of the plot lines
        """
        status = self.poynting_check.get_status()  # Get the status of the checkboxes
        if status[0]:
            self.show_Poynting = True
            self.fields2D.set_accumulate_S(accumulation_type=self.accumulation_type)
            self.fields2D.do_n(self.fields2D.Nt)
            new_cmap = wavelength_to_colormap(self.fields2D.wavelength, self.norm)
            # Update the colormap
            self.im1.set_cmap(new_cmap)
            self.update_ax1()
        else:
            self.show_Poynting = False
            self.im1.set_cmap('RdBu')  # Update the colormap
            self.im1.set_clim(-2, 2)
