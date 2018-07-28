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

def plot_VA(ax1, array, pad=8, M=64,
            name=None, norm=True, scale='lin',
            btracks=True, colorbar=True,
            lim_lin=np.array([0,1]), lim_log=False, norm_num=1,
            bounds='default', x_label=True, y_label=True, zoom=True,
            font=10.56, colorbar_ticks='set', tick_color='w', cb_tick_color='k'):
    """!@brief Makes a plot of a visibility amplitude map.

    This can be used for a single image or for multiple subplots,
    below is an example of how this can be used for a single image:
    @code
    fig = Figure(Panel().plot_VA(VA_array, name='Visibility Amplitude'))
    fig.savefig(file_name)
    @endcode

    This is an example for multiple subplots:

    @code
    pnl1 = Panel().plot_VA(VA_array1, colorbar=False)
    pnl1 = Panel().plot_VA(VA_array2, colorbar=False)
    pnl1 = Panel().plot_VA(VA_array3, colorbar=False)
    pnl1 = Panel().plot_VA(VA_array4, colorbar=False)

    fig = Figure([[pnl1, pnl2], [pnl3, pnl4]])
    fig.savefig(file_name)
    @endcode

    Note that for multiple subplots you might want to omit colorbars,
    and only include the model name in one of the subplots.

    @param ax1 the name of the subplot (where applicable) where you
    want to plot your image, see the example code above.

    @param array 2D numpy array of the image to be plotted.

    @param name optional keyword, default set to None. If not None must be a
    string and will add a text label to the plot equal to this string.

    @param norm optional keyword, default set to True, if
    True will normalize image so that the maximum is 1,
    if false does not normalize image.

    @param scale optional keyword, default set to 'lin', 'log' is also
    supported, this sets the scale of the color map.

    @param btracks optional keyword, default set to True, if True will
    plot the baseline tracks for the EHT over the VA map.

    @param font this is an optional keyword, default is set to 20,
    this sets the font size for the axis labels, and numbers as well
    as the numbers for the color bar.

    @param colorbar optional keyword, default set to True, if True
    will plot the color bar, if False will do nothing, and if set to
    'top' will plot colorbar on top.

    @param lim_lin optional keyword, default set to np.array([0,1]),
    this is the limits for the color bar if scale='lin'.

    @param lim_log optional keyword, default set to False, this is the
    limits for the color bar if scale='log'.

    @param norm_num optional keyword, default set to 1, this is in
    case normalizing to 1 doesn't give the desired image, you can
    control a more specific normalization with norm_num, for example,
    if norm_num=1.2, the maximum value in the image will be 1.2, but
    the color bar will go from 0 to 1 (assuming scale='lin').

    @param pad int, optional keyword, default set to 8, factor by
    which I want to pad my arrays before taking the fft.

    @param M int, optional keyword, default set to 64, size the the
    array in units of \f$ GM/c^2 \f$.

    @param bounds optional keyword, default set to 'default'. If this
    is set to a string will use the default bounds for the x and y
    axes. Otherwise, this variable can be set to a number and the
    bounds will then be [-bounds,bounds].

    @param x_label optional keyword, default set to True. If True will
    add a label to the x-axis, if False, will not add this label.

    @param y_label optional keyword, default set to True. If True will
    add a label to the y-axis, if False, will not add this label.

    @param zoom optional keyword, default set to True. If set to True
    will zoom in to about 20 \f$ G \lambda \f$ on each side, if not
    set to True, will leave the full array visible, unless bounds is
    set.

    @param colorbar_ticks optional keyword, default set to 'set'. If
    set to 'set' the colorbar ticks will be at [0,0.2,0.4,0.6,0.8,1],
    if set to 'auto' will let matplotlib set the colorbar ticks
    automatically.

    @param tick_color optional keyword, default set to 'w' will set
    the color of the ticks in the plot.

    @param cb_tick_color optional keyword, default set to 'k' will set
    the color of the ticks for the colobar, as long as colorbar not
    set to 'top'.

    """

    x       = np.shape(array)[0]
    r0      = x*np.sqrt(27)/M # this is the radius of the black hole shadow
    uvpix   = 0.6288/pad
    widthL  = (1/(np.pi*r0))*x*uvpix*pad
    ext     = widthL*4

    if norm == True:
        array = array/(np.max(array))*norm_num

    if scale == 'lin':
        im1=ax1.imshow(array,extent=[x/2*uvpix,-x/2*uvpix,-x/2*uvpix,x/2*uvpix],
                       vmin=lim_lin[0], vmax=lim_lin[1],
                       origin='lower', interpolation='bilinear')
        if colorbar == True:
            divider1 = make_axes_locatable(ax1)
            cax1     = divider1.append_axes("right", size="7%", pad=0.05)
            if colorbar_ticks == 'auto':
                cbar1 = plt.colorbar(im1, cax=cax1)
            else:
                cbar1 = plt.colorbar(im1, cax=cax1, ticks=[0,0.2,0.4,0.6,0.8,1])
            cbar1.ax.tick_params(labelsize=font, color=cb_tick_color,width=1.5, direction='in')
        elif colorbar == 'top':
            divider1 = make_axes_locatable(ax1)
            cax1     = divider1.append_axes("top", size="7%", pad=0.05)
            if colorbar_ticks == 'auto': cbar1    = plt.colorbar(im1,orientation="horizontal", cax=cax1)
            else: cbar1    = plt.colorbar(im1, cax=cax1,orientation="horizontal", ticks=[0,0.2,0.4,0.6,0.8])
            cbar1.ax.tick_params(labelsize=font)#, color='w',width=1.5, direction='in')
            cbar1.ax.xaxis.set_ticks_position('top')
    if scale == 'log':
        if type(lim_log) == bool:
            im1=ax1.imshow(array,extent=[x/2*uvpix,-x/2*uvpix,-x/2*uvpix,x/2*uvpix],
                           norm=LogNorm(),
                           origin='lower', interpolation='bilinear')
        else:
            im1=ax1.imshow(array,extent=[x/2*uvpix,-x/2*uvpix,-x/2*uvpix,x/2*uvpix],
                           norm=LogNorm(vmin=lim_log[0], vmax=lim_log[1]),
                           origin='lower', interpolation='bilinear')
        if colorbar == True:
            divider1 = make_axes_locatable(ax1)
            cax1     = divider1.append_axes("right", size="7%", pad=0.05)
            cbar1    = plt.colorbar(im1, cax=cax1)
            cbar1.ax.tick_params(labelsize=font, color=cb_tick_color, direction='in')
        elif colorbar== 'top':
            divider1 = make_axes_locatable(ax1)
            cax1     = divider1.append_axes("top", size="7%", pad=0.05)
            cbar1    = plt.colorbar(im1,orientation="horizontal", cax=cax1)
            cbar1.ax.tick_params(labelsize=font)#, color=
            cbar1.ax.xaxis.set_ticks_position('top')
    if x_label == True:
        ax1.set_xlabel('$u$ (G $\lambda$)',fontsize=font)
    if y_label == True:
        ax1.set_ylabel('$v$ (G $\lambda$)',fontsize=font)
    if btracks == True:
        path    = __file__.replace('my_plot.pyc', '')
        U, V    = np.load(path+'U.npy'), np.load(path+'V.npy')
        U,V     = U*10**(-6),V*10**(-6)
        ax1.scatter( U, V, c='w', s=2, marker='o',edgecolors='none')
        ax1.scatter(-U,-V, c='w', s=2, marker='o',edgecolors='none')
    ax1.tick_params(axis='both', which='major',
                    labelsize=font, color=tick_color, width=1.5, direction='in')
    if zoom == True:
        if type(bounds) == str:
            ax1.set_xlim([ext,-ext])
            ax1.set_ylim([-ext,ext])
            ax1.set_xticks([-5,0,5])
            ax1.set_yticks([-5,0,5])
            if name != None:
                ax1.text(9,-9, name, fontsize=font,color='w') #makes the text label
        else:
            ax1.set_xlim([bounds,-bounds])
            ax1.set_ylim([-bounds,bounds])
            if name != None:
                ax1.text(.9*bounds,-.9*bounds, name, fontsize=font,color='w') #makes the text label
    else:
        ax1.set_yticks(-1*ax1.get_xticks())
        temp = ax1.get_xlim()
        ax1.set_ylim(-1*temp[0], -1*temp[1])
        if name !=None:
            ax1.text(.9*temp[0],-.9*temp[0], name, fontsize=font, color='w') #makes the text label
