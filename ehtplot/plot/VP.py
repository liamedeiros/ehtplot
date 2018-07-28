# Copyright (C) 2018 Lia Medeiros
# Copyright (C) 2018 Steward Observatory
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

def plot_VP(ax1, array, pad=8, M=64,
            name=None,
            btracks=True, colorbar=True,
            white_width=5, interpolation='bilinear',
            x_label=True, y_label=True, zoom=True,
            font=10.56, tick_color='k', cb_tick_color='k'):
    """!@brief Makes a plot of a visibility phase map.

    This can be used for a single image or for multiple subplots,
    below is an example of how this can be used for a single image:
    @code
    fig = Figure(Panel().plot_VP(VP_array,name='Visibility Phase'))
    fig.savefig(file_name)
    @endcode

    This is an example for multiple subplots:

    @code
    pnl1 = Panel().plot_VP(VP_array1, colorbar=False)
    pnl1 = Panel().plot_VP(VP_array2, colorbar=False)
    pnl1 = Panel().plot_VP(VP_array3, colorbar=False)
    pnl1 = Panel().plot_VP(VP_array4, colorbar=False)

    fig = Figure([[pnl1, pnl2], [pnl3, pnl4]])
    fig.savefig(file_name)
    @endcode

    Note that for multiple subplots you might want to omit color bars,
    and only include the model name in one of the subplots.

    @param ax1 the name of the subplot (where applicable) where you
    want to plot your image, see the example code above.

    @param array 2D numpy array of the image to be plotted.

    @param name optional keyword, default set to None. If not None
    must be a string and will add a text label to the plot equal to
    this string.

    @param btracks optional keyword, default set to True, if True will
    plot the baseline tracks for the EHT over the VA map.

    @param font optional keyword, default set to 20, this sets the
    font size for the axis labels, and numbers as well as the numbers
    for the color bar.

    @param colorbar optional keyword, default set to True, if True
    will plot the color bar, if False will do nothing, and if set to
    'top' will plot colorbar on top.

    @param pad int, optional keyword, default set to 8, factor by
    which I want to pad my arrays before taking the fft.

    @param M int, optional keyword, default set to 64, size the the
    array in units of \f$ GM/c^2 \f$.

    @param x_label optional keyword, default set to True. If True will
    add a label to the x-axis, if False, will not add this label..

    @param y_label optional keyword, default set to True. If True will
    add a label to the y-axis, if False, will not add this label.

    @param zoom optional keyword, default set to True. If set to True
    will zoom in to about 20 \f$ G \lambda \f$ on each side, if not
    set to True, will leave the full array visible, unless bounds is
    set.

    @param white_width optional keyword, default set to 5. This will
    control the width of the white border around the black text on the
    plot.

    @param interpolation optional keyword, default set to
    'bilinear'. This will control the type of interpolation that is
    used in the plot, the options are the same as those for
    matplotlib.

    """

    x       = np.shape(array)[0]
    r0      = x*np.sqrt(27)/M # this is the radius of the black hole shadow
    uvpix   = 0.6288/pad
    widthL  = (1/(np.pi*r0))*x*0.6288
    ext     = widthL*4

    array[np.where(array >  np.pi)] = array[np.where(array >  np.pi)]-2.0*np.pi
    array[np.where(array < -np.pi)] = array[np.where(array < -np.pi)]+2.0*np.pi

    plt.set_cmap('hsv')
    im1=ax1.imshow(array,extent=[x/2*uvpix,-x/2*uvpix,-x/2*uvpix,x/2*uvpix],
                   vmin=-np.pi, vmax=np.pi,
                   origin='lower', interpolation=interpolation)
    if colorbar == True:
        divider1 = make_axes_locatable(ax1)
        cax1     = divider1.append_axes("right", size="7%", pad=0.05)
        cbar1    = plt.colorbar(im1, cax=cax1)
        cbar1.ax.tick_params(labelsize=font, color=cb_tick_color, width=1.5, direction='in')
    elif colorbar == 'top':
        divider1 = make_axes_locatable(ax1)
        cax1     = divider1.append_axes("top", size="7%", pad=0.05)
        cbar1    = plt.colorbar(im1,orientation="horizontal", cax=cax1)
        cbar1.ax.tick_params(labelsize=font)#, color='w',width=1.5, direction='in')
        cbar1.ax.xaxis.set_ticks_position('top')
    if x_label == True:
        ax1.set_xlabel('$u$ (G $\lambda$)', fontsize=font)
    if y_label == True:
        ax1.set_ylabel('$v$ (G $\lambda$)', fontsize=font)
    if btracks == True:
        path    = __file__.replace('my_plot.pyc', '')
        U, V    = np.load(path+'U.npy'), np.load(path+'V.npy')
        U,V     = U*10**(-6),V*10**(-6)
        ax1.scatter( U, V, c='k', s=2, marker='o', edgecolors='none')
        ax1.scatter(-U,-V, c='k', s=2, marker='o', edgecolors='none')
    ax1.tick_params(axis='both', which='major',
                    labelsize=font, color=tick_color, width=1.5, direction='in')
    if zoom == True:
        ax1.set_xlim([ext,-ext])
        ax1.set_ylim([-ext,ext])
        ax1.set_xticks([-5,0,5])
        ax1.set_yticks([-5,0,5])
        if name != None:
            txt = ax1.text(9,-9, name, fontsize=font, color='k') #makes the text label
            txt.set_path_effects([PathEffects.withStroke(linewidth=white_width, foreground='w')])
    else:
        ax1.set_yticks(-1*ax1.get_xticks())
        temp = ax1.get_xlim()
        ax1.set_ylim(-1*temp[0], -1*temp[1])
        if name != None:
            txt = ax1.text(.9*temp[0],-.9*temp[0], name, fontsize=font, color='k') #makes the text label
            txt.set_path_effects([PathEffects.withStroke(linewidth=white_width, foreground='w')])
