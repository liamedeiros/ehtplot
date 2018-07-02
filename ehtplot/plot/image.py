# Copyright (C) 2018 Lia Medeiros
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

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm

def plot_image(ax1, array,
               spin=None, theta=60.0, name=None, norm=True, scale='lin',
               colorbar=True, norm_num=1, lim_lin=np.array([0,1]), lim_log=False,
               flip_x=False, horz=False, M=64, x_label=True, y_label=True,
               colorbar_ticks='set', circle_width=1,
               zoom=True, tick_color='w', cb_tick_color='k'):
    """!@brief Makes a plot of an image.

    This can be used for a single image or for multiple subplots,
    below is an example of how this can be used for a single image:
    @code
    fig = Figure(Panel().plot_image(image_array, spin=.9, name='Model B'))
    fig.savefig(file_name)
    @endcode

    This is an example for multiple subplots:

    @code
    pnl1 = Panel().plot_image(image_array1, spin=.9, colorbar=False)
    pnl2 = Panel().plot_image(image_array2, spin=.9, colorbar=False)
    pnl3 = Panel().plot_image(image_array3, spin=.9, colorbar=False)
    pnl4 = Panel().plot_image(image_array4, spin=.9, colorbar=False)

    fig = Figure([[pnl1, pnl2], [pnl3, pnl4]])
    fig.savefig(file_name)
    @endcode

    Note that for multiple subplots you might want to omit color bars,
    and only include the model name in one of the subplots.

    @param ax1 optional keyword, default set to None this keyword is
    closely tied with fig, either they both must be None or
    neither. If None will create a figure of size columnwidth by
    columnwidth with one subplot. If not None this should be the name
    of the subplot (where applicable) where you want to plot your
    image, see the example code above.

    @param array 2D numpy array of the image to be plotted.

    @param spin optional keyword, default set to None. If None, will
    not draw a circle over the image, if not None will draw the black
    hole shadow calculated analytically for a kerr black hole with
    black hole spin given by this parameter and the inclination of the
    observer given by the parameter theta.

    @param theta optional keyword, default set to 60.0 degrees. This
    is the inclination of the observer relative to the black hole in
    degrees, used to analytically calculate the shape and position of
    the black hole shadow see also spin.

    @param name optional keyword, default set to None. If not None
    must be a string and will add a text label to the plot equal to
    this string.

    @param norm optional keyword, default set to True, if True will
    normalize image so that the maximum is 1, if false does not
    normalize image.

    @param scale optional keyword, default set to 'lin', 'log' is also
    supported, this sets the scale of the color map.

    @param font this is an optional keyword, default is set to 10.56
    because this is the size of the font in the emulate ApJ 2-column
    latex format, this sets the font size for the axis labels, and
    numbers as well as the numbers for the color bar.

    @param colorbar optional keyword, default set to True, if True
    will plot the color bar, if False will do nothing, and if set to
    'top' will plot colorbar on top.

    @param norm_num optional keyword, default set to 1, this is in
    case normalizing to 1 doesn't give the desired image, you can
    control a more specific normalization with norm_num, for example,
    if norm_num=1.2, the maximum value in the image will be 1.2, but
    the color bar will go from 0 to 1 (assuming scale='lin').

    @param lim_lin optional keyword, default set to np.array([0,1]),
    this is the limits for the color bar if scale='lin'.

    @param lim_log optional keyword, default set to False, this is the
    limits for the color bar if scale='log'.

    @param flip_x optional keyword, default set to False. if set to
    True will flip the array in the left-right direction.

    @param horz optional keyword, default set to False, sometimes I
    want to plot the images transposed so that we can compare
    different orientations, this will move the red circle accordingly.

    @param M int, optional keyword, default set to 64, size the array
    in units of \f$ GM/c^2 \f$.

    @param x_label optional keyword, default set to True. If True will
    add a label to the x-axis, if False, will not add this label.

    @param y_label optional keyword, default set to True. If True will
    add a label to the y-axis, if False, will not add this label.

    @param colorbar_ticks optional keyword, default set to 'set'. If
    set to 'set' the colorbar ticks will be at [0,0.2,0.4,0.6,0.8,1],
    if set to 'auto' will let matplotlib set the colorbar ticks
    automatically.

    @param circle_width optional keyword, default set to 1. This
    controls the line-width of the circle that corresponds to the
    black hole shadow, see also spin.

    @param zoom optional keyword, default set to True. If set to True
    will zoom in to about 20 \f$ GM/c^2 \f$ on each side, if not set
    to True, will leave the full array visible.

    @param tick_color optional keyword, default set to 'w' will set
    the color of the ticks in the plot.

    @param cb_tick_color optional keyword, default set to 'k' will set
    the color of the ticks for the colobar, as long as colorbar not
    set to 'top'.

    """

    x = np.shape(array)[0]
    r0      = x*np.sqrt(27)/M # this is the radius of the black hole shadow
    r0M     = r0*M/x # this gives the BH shadow in units of GM/c**2
    if norm == True: array = array/(np.max(array))*norm_num

    plt.set_cmap('gnuplot2')
    if scale == 'lin':
        if flip_x == True:
            array = np.fliplr(array)
            im1   = ax1.imshow(array, extent=[M/2.0,-M/2.0,-M/2.0,M/2.0],vmin=lim_lin[0], vmax=lim_lin[1], origin='lower', interpolation='bilinear')
        else:
            im1   = ax1.imshow(array, extent=[-M/2.0,M/2.0,-M/2.0,M/2.0],vmin=lim_lin[0], vmax=lim_lin[1], origin='lower', interpolation='bilinear')
        if colorbar==True:
            divider1 = make_axes_locatable(ax1)
            cax1     = divider1.append_axes("right", size="7%", pad=0.05)
            if colorbar_ticks == 'auto': cbar1    = plt.colorbar(im1, cax=cax1)
            else: cbar1    = plt.colorbar(im1, cax=cax1, ticks=[0,0.2,0.4,0.6,0.8,1])
            cbar1.ax.tick_params(labelsize=font, color=cb_tick_color,width=1, direction='in')
        elif colorbar== 'top':
            divider1 = make_axes_locatable(ax1)
            cax1     = divider1.append_axes("top", size="7%", pad=0.05)
            if colorbar_ticks == 'auto': cbar1    = plt.colorbar(im1,orientation="horizontal", cax=cax1)
            else: cbar1    = plt.colorbar(im1, cax=cax1,orientation="horizontal", ticks=[0,0.2,0.4,0.6,0.8])
            cbar1.ax.tick_params(labelsize=font)#, color='w',width=1.5, direction='in')
            cbar1.ax.xaxis.set_ticks_position('top')
    elif scale == 'log':
        if type(lim_log) ==bool:
            if flip_x == True:
                array = np.fliplr(array)
                im1=ax1.imshow(array, extent=[M/2.0,-M/2.0,-M/2.0,M/2.0], norm=LogNorm()                                , origin='lower', interpolation='bilinear')
            else:
                im1=ax1.imshow(array, extent=[-M/2.0,M/2.0,-M/2.0,M/2.0], norm=LogNorm()                                , origin='lower', interpolation='bilinear')
        else:
            if flip_x == True:
                array = np.fliplr(array)
                im1=ax1.imshow(array, extent=[M/2.0,-M/2.0,-M/2.0,M/2.0], norm=LogNorm(vmin=lim_log[0], vmax=lim_log[1]), origin='lower', interpolation='bilinear')
            else:
                im1=ax1.imshow(array, extent=[-M/2.0,M/2.0,-M/2.0,M/2.0], norm=LogNorm(vmin=lim_log[0], vmax=lim_log[1]), origin='lower', interpolation='bilinear')
        if colorbar==True:
            divider1 = make_axes_locatable(ax1)
            cax1     = divider1.append_axes("right", size="7%", pad=0.05)
            cbar1    = plt.colorbar(im1, cax=cax1)
            cbar1.ax.xaxis.set_ticks_position('top')
            cbar1.ax.tick_params(labelsize=font, color=cb_tick_color, direction='in')
        elif colorbar== 'top':
            divider1 = make_axes_locatable(ax1)
            cax1     = divider1.append_axes("top", size="7%", pad=0.05)
            cbar1    = plt.colorbar(im1,orientation="horizontal", cax=cax1)
            cbar1.ax.tick_params(labelsize=font)#, color='w',width=1.5, direction='in')
            cbar1.ax.xaxis.set_ticks_position('top')
    ax1.tick_params(axis='both', which='major', labelsize=font, color=tick_color,width=1.5, direction='in')

    if flip_x == False:
        if zoom == True: # flip_x = False, zoom=True
            ax1.set_xlim([-r0M*2, r0M*2])
            ax1.set_ylim([-r0M*2, r0M*2])
            ax1.set_xticks([-10,-5,0,5,10])
            ax1.set_yticks([-10,-5,0,5,10])
            if name != None:
                ax1.text(-9,-9, name, fontsize=font, color='w') #makes the text label
        else:# flip_x = False, zoom=False
            ax1.set_yticks(ax1.get_xticks())
            ax1.set_ylim(ax1.get_xlim())
            if name !=None:
                ax1.text(-0.47*M,-0.47*M, name, fontsize=font, color='w') #makes the text label
    elif zoom == True: # flip_x = True, zoom=True
        ax1.set_xlim([r0M*2, -r0M*2])
        ax1.set_ylim([-r0M*2, r0M*2])
        ax1.set_xticks([10,5,0,-5,-10])
        ax1.set_yticks([-10,-5,0,5,10])
        if name != None:
            ax1.text(9,-9, name, fontsize=font, color='w') #makes the text label
    elif zoom == False:# flip_x = True, zoom=False
        ax1.set_yticks(-1*ax1.get_xticks())
        temp = ax1.get_xlim()
        ax1.set_ylim(-1*temp[0], -1*temp[1])
        if name !=None:
                ax1.text(0.47*M,-0.47*M, name, fontsize=font, color='w') #makes the text label

    if x_label==True: ax1.set_xlabel('X ($GMc^{-2}$)',fontsize=font)
    if y_label==True: ax1.set_ylabel('Y ($GMc^{-2}$)',fontsize=font)
    if spin != None:
        make_circle_kerr(ax1,spin,i=theta,circle_width=circle_width)
