# Copyright (C) 2017 Lia Medeiros
#
# This file is part of ehtplot.
#
# ehtplot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ehtplot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ehtplot.  If not, see <http://www.gnu.org/licenses/>.

import numpy             as np
import matplotlib        as mpl
import matplotlib.pyplot as plt
import pkg_resources     as pr

from matplotlib              import cm, colors, rcParams
from matplotlib.colors       import LogNorm
from matplotlib.ticker       import MultipleLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable

class Figure(mpl.figure.Figure):
    """The main class of ehtplot that enhances matplotlib's Figure.

    The Figure class is the "outermost container" in ehtplot that
    inherits matplotlib's Figure class.  An ehtplot Figure can be
    rendered on screen and exported to files.  Logically, an ehtplot
    Figure always contains a single root ehtplot Panel instance,
    although the root Panel can have multiple subpanels in it.  See
    the documentation of the ehtplot Panel class for details.

    Attributes:
        axs:       matplotlib axes
        fontsz:    font size
        count:     number of subplots
        size:      size is in (x, y)

    """

    def __init__(self,
                 subplots=(1,1), size=None,
                 fontsz=10, **kwargs):
        """Construct the ehtplot Figure class.

        ... long description ...

        Args:
            subplots: subplots is (row, column)
            size: size is in (x, y)
            fontsz: font size

        """
        textwidth   = 7.1     # in inch; for full width figure in ApJ
        columnwidth = 3.39375 # in inch; for half width figure in ApJ

        if size is None:
            w    = columnwidth if subplots[1] == 1 else textwidth
            size = (w, w / subplots[1] * subplots[0])

        super(Figure, self).__init__(figsize=size, **kwargs)
        self.set_canvas(mpl.backends.backend_agg.FigureCanvasAgg(self))

        axs = self.subplots(subplots[0], subplots[1])
        if subplots[0] == 1 and subplots[1] == 1:
            axs = np.array([axs])
        self.axs = axs.reshape(subplots)

        self.fontsz = fontsz
        self.count  = 0
        self.size   = size

    def plot_image(self,
                   array, pixsize, axis=None, norm=True, scale='lin',
                   colorbar=True, limits=(0, 1), colormap='gnuplot2',
                   zoom=False, labelx='auto', labely='auto'):
        """!@brief Makes a plot of an image.

        This can be used for a single image or for multiple subplots,
        below is an example of how this can be used for a single
        image:

        @code
        fig,(ax1) = plt.subplots(1,1)
        fig.set_size_inches(6,6)

        plot_image(image_array, fig, ax1, m)

        fig.savefig(file_name, bbox_inches='tight')
        plt.close(fig)
        @endcode

        This is an example for multiple subplots:

        @code
        fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)
        fig.set_size_inches(12,12)

        plot_image(image_array1, fig,ax1, m, colorbar=False)
        plot_image(image_array2, fig,ax2, m, colorbar=False, model_text=False)
        plot_image(image_array3, fig,ax3, m, colorbar=False, model_text=False)
        plot_image(image_array4, fig,ax4, m, colorbar=False, model_text=False)

        fig.savefig(file_name, bbox_inches='tight')
        plt.close(fig)
        @endcode

        Note that for multiple subplots you might want to omit color
        bars, and only include the model name in one of the subplots.

        @param array 2D numpy array of the image to be plotted

        @param pixsize pixel size of the image

        @param axis the subplot (where applicable) where you want to
        plot your image, see the example code above

        @param norm optional keyword, default set to True, if True
        will normalize image so that the maximum is 1, if false does
        not normalize image

        @param scale optional keyword, default set to 'lin', 'log' is
        also supported, this sets the scale of the color map

        @param colorbar optional keyword, default set to True, if True
        will plot the color bar

        @param colormap optional keyword, default set to 'gnuplot2',
        this sets the color map of the image and color bar

        @param limits optional keyword, default set to (0, 1), this
        sets limits for the color if scale='lin'

        @param zoom optional keyword, default set to True, when True
        will zoom the plot in to the photon ring

        @param labelx optional keyword, default set to True, when True
        will plot the x-axis label

        @param labely optional keyword, default set to True, when True
        will plot the y-axis label

        @returns 0

        """
        n_row = self.axs.shape[0]
        n_col = self.axs.shape[1]
        if axis is None:
            i   = self.count %  n_col # column
            j   = self.count // n_col # row
            ax1 = self.axs[j%n_row, i]
            self.count = self.count + 1
        else:
            ax1 = axis
        fontsz = self.fontsz
        x = array.shape[0]
        if norm == True:
            array = array / np.max(array)
        plt.set_cmap(colormap)
        if scale == 'lin':
            im1 = ax1.imshow(array,
                             extent=[-x / 2. * pixsize, x / 2. * pixsize,
                                     -x / 2. * pixsize, x / 2. * pixsize],
                             vmin=limits[0], vmax=limits[1],
                             origin='lower', interpolation='bilinear', aspect=1)
            if colorbar == True:
                divider1 = make_axes_locatable(ax1)
                cax1     = divider1.append_axes("right", size="7%", pad=0.05)
                cbar1    = plt.colorbar(im1, cax=cax1,
                                        ticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
                cbar1.ax.tick_params(labelsize=fontsz)
                self.set_size_inches(self.size[0], self.size[1] * .8)

        if scale == 'log':
            im1 = ax1.imshow(array,
                             extent=[-x / 2. * pixsize, x / 2. * pixsize,
                                     -x / 2. * pixsize, x / 2. * pixsize],
                             LogNorm=(),
                             origin='lower', interpolation='bilinear')
            if colorbar == True:
                divider1 = make_axes_locatable(ax1)
                cax1     = divider1.append_axes("right", size="7%", pad=0.05)
                cbar1    = plt.colorbar(im1, cax=cax1)
                cbar1.ax.tick_params(labelsize=fontsz)
                self.set_size_inches(self.size[0], self.size[1] * .8)
        if labelx is None:
            pass
        elif labelx == 'force':
            ax1.set_xlabel('X ($GMc^{-2}$)', fontsize=fontsz, labelpad=0)
        elif labelx == 'auto':
            if j == (n_row - 1):
                ax1.set_xlabel('X ($GMc^{-2}$)', fontsize=fontsz, labelpad=0)
        else:
            ax1.set_xlabel(labelx, fontsize=fontsz, labelpad=0)

        if labely is None:
            pass
        elif labely == 'force':
            ax1.set_ylabel('Y ($GMc^{-2}$)', fontsize=fontsz, labelpad=-6)
        elif labely == 'auto':
            if i == 0:
                ax1.set_ylabel('Y ($GMc^{-2}$)', fontsize=fontsz, labelpad=-6)
        else:
            ax1.set_ylabel(labely, fontsize=fontsz, labelpad=-6)

        ax1.tick_params(axis='both', which='major',
                        labelsize=fontsz, color='w', width=1.5)
        if zoom == True:
            r0 = np.sqrt(27)  # this gives the BH shadow in units of GM/c**2
            ax1.set_xlim([-r0 * 2, r0 * 2])
            ax1.set_ylim([-r0 * 2, r0 * 2])
            ax1.set_xticks([-10, -5, 0, 5, 10])
            ax1.set_yticks([-10, -5, 0, 5, 10])

        return 0
