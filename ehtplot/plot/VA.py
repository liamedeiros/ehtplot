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

def plot_VA(ax1, array, fig=None, output=None, name=None, norm=True, scale='lin',
btracks=True, font=10.56, colorbar=True, lim_lin=np.array([0,1]), lim_log=False,
norm_num=1, pad=8, M=64, bounds='default', x_label=True, y_label=True, zoom=True,
colorbar_ticks='set', tick_color='w', cb_tick_color='k'):

    """!@brief Makes a plot of a visibility amplitude map.

    This can be used for a single image or for multiple subplots,
    below is an example of how this can be used for a single image:
    @code
    plot_VA(VA_array, name='Visibility Amplitude', output='output_file.pdf')
    @endcode

    This is an example for multiple subplots:

    @code
    fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)
    fig.set_size_inches(12,12)

    plot_VA(VA_array1, fig=fig,ax1=ax1, colorbar=False)
    plot_VA(VA_array2, fig=fig,ax1=ax2, colorbar=False)
    plot_VA(VA_array3, fig=fig,ax1=ax3, colorbar=False)
    plot_VA(VA_array4, fig=fig,ax1=ax4, colorbar=False)

    fig.savefig(file_name, bbox_inches='tight')
    plt.close(fig)
    @endcode

    Note that for multiple subplots you might want to omit colorbars,
    and only include the model name in one of the subplots.

    @param array 2D numpy array of the image to be plotted.

    @param fig the name of the figure where you want to plot your image,
    see the example code above.

    @param ax1 the name of the subplot (where applicable) where you want to plot
    your image, see the example code above.

    @param output optional keyword, default set to None, if not None should be
    a string and  will save the figure to a file with file name equal to output.

    @param name optional keyword, default set to None. If not None must be a
    string and will add a text label to the plot equal to this string.

    @param norm optional keyword, default set to True, if
    True will normalize image so that the maximum is 1,
    if false does not normalize image.

    @param scale optional keyword, default set to 'lin',
    'log' is also supported, this sets the scale of the color map.

    @param btracks optional keyword, default set to True, if True will plot the
    baseline tracks for the EHT over the VA map.

    @param font this is an optional keyword, default is set to 20, this sets
    the font size for the axis labels, and numbers as well as the numbers for
    the color bar.

    @param colorbar optional keyword, default set to True, if True will plot the
    color bar, if False will do nothing, and if set to 'top' will plot colorbar
    on top.

    @param lim_lin optional keyword, default set to np.array([0,1]), this is the
    limits for the color bar if scale='lin'.

    @param lim_log optional keyword, default set to False, this is the limits
    for the color bar if scale='log'.

    @param norm_num optional keyword, default set to 1, this is in case
    normalizing to 1 doesn't give the desired image, you can control a more
    specific normalization with norm_num, for example, if norm_num=1.2, the
    maximum value in the image will be 1.2, but the color bar will go from 0 to
    1 (assuming scale='lin').

    @param pad int, optional keyword, default set to 8, factor by which I want
    to pad my arrays before taking the fft.

    @param M int, optional keyword, default set to 64, size the the array in
    units of \f$ GM/c^2 \f$.

    @param bounds optional keyword, default set to 'default'. If this is set to
    a string will use the default bounds for the x and y axes. Otherwise, this
    variable can be set to a number and the bounds will then be [-bounds,bounds].

    @param x_label optional keyword, default set to True. If True will add a
    label to the x-axis, if False, will not add this label.

    @param y_label optional keyword, default set to True. If True will add a
    label to the y-axis, if False, will not add this label.

    @param zoom optional keyword, default set to True. If set to True will zoom
    in to about 20 \f$ G \lambda \f$ on each side, if not set to True, will leave
    the full array visible, unless bounds is set.

    @param colorbar_ticks optional keyword, default set to 'set'. If set to
    'set' the colorbar ticks will be at [0,0.2,0.4,0.6,0.8,1], if set to 'auto'
    will let matplotlib set the colorbar ticks automatically.

    @param tick_color optional keyword, default set to 'w' will set the color of
    the ticks in the plot.

    @param cb_tick_color optional keyword, default set to 'k' will set the color
    of the ticks for the colobar, as long as colorbar not set to 'top'.

     @returns ax1 if ax1 not given, or the image object if ax1 is given.
    """
    make_fig = False
    if (fig == None) and (ax1 == None):
        make_fig =True
        columnwidth = 3.39441
        fig,(ax1) = plt.subplots(1,1)
        fig.set_size_inches(columnwidth,columnwidth)

    x       = np.shape(array)[0]
    r0      = x*np.sqrt(27)/M # this is the radius of the black hole shadow
    uvpix   = 0.6288/pad
    widthL  = (1/(np.pi*r0))*x*uvpix*pad
    ext     = widthL*4

    if norm == True: array = array/(np.max(array))*norm_num

    plt.set_cmap('gnuplot2')

    if scale == 'lin':
        im1=ax1.imshow(array,extent=[x/2*uvpix,-x/2*uvpix,-x/2*uvpix,x/2*uvpix],vmin=lim_lin[0], vmax=lim_lin[1], origin='lower', interpolation='bilinear')
        if colorbar==True:
            divider1 = make_axes_locatable(ax1)
            cax1     = divider1.append_axes("right", size="7%", pad=0.05)
            if colorbar_ticks == 'auto': cbar1 = plt.colorbar(im1, cax=cax1)
            else: cbar1 = plt.colorbar(im1, cax=cax1, ticks=[0,0.2,0.4,0.6,0.8,1])
            cbar1.ax.tick_params(labelsize=font, color=cb_tick_color,width=1.5, direction='in')
        elif colorbar== 'top':
            divider1 = make_axes_locatable(ax1)
            cax1     = divider1.append_axes("top", size="7%", pad=0.05)
            if colorbar_ticks == 'auto': cbar1    = plt.colorbar(im1,orientation="horizontal", cax=cax1)
            else: cbar1    = plt.colorbar(im1, cax=cax1,orientation="horizontal", ticks=[0,0.2,0.4,0.6,0.8])
            cbar1.ax.tick_params(labelsize=font)#, color='w',width=1.5, direction='in')
            cbar1.ax.xaxis.set_ticks_position('top')
    if scale == 'log':
        if type(lim_log) ==bool: im1=ax1.imshow(array,extent=[x/2*uvpix,-x/2*uvpix,-x/2*uvpix,x/2*uvpix],norm=LogNorm(),origin='lower', interpolation='bilinear')
        else: im1=ax1.imshow(array,extent=[x/2*uvpix,-x/2*uvpix,-x/2*uvpix,x/2*uvpix],norm=LogNorm(vmin=lim_log[0], vmax=lim_log[1]),origin='lower', interpolation='bilinear')
        if colorbar==True:
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
    if x_label==True: ax1.set_xlabel('$u$ (G $\lambda$)',fontsize=font)
    if y_label==True: ax1.set_ylabel('$v$ (G $\lambda$)',fontsize=font)
    if btracks == True:
        path    = __file__.replace('my_plot.pyc', '')
        U, V    = np.load(path+'U.npy'), np.load(path+'V.npy')
        U,V     = U*10**(-6),V*10**(-6)
        ax1.scatter( U, V, c='w', s=2, marker='o',edgecolors='none')
        ax1.scatter(-U,-V, c='w', s=2, marker='o',edgecolors='none')
    ax1.tick_params(axis='both', which='major', labelsize=font, color=tick_color, width=1.5, direction='in')
    if zoom == True:
        if type(bounds) == str:
            ax1.set_xlim([ext,-ext])
            ax1.set_ylim([-ext,ext])
            ax1.set_xticks([-5,0,5])
            ax1.set_yticks([-5,0,5])
            if name != None: ax1.text(9,-9, name, fontsize=font,color='w') #makes the text label
        else:
            ax1.set_xlim([bounds,-bounds])
            ax1.set_ylim([-bounds,bounds])
            if name != None: ax1.text(.9*bounds,-.9*bounds, name, fontsize=font,color='w') #makes the text label
    else:
        ax1.set_yticks(-1*ax1.get_xticks())
        temp = ax1.get_xlim()
        ax1.set_ylim(-1*temp[0], -1*temp[1])
        if name !=None:
            ax1.text(.9*temp[0],-.9*temp[0], name, fontsize=font, color='w') #makes the text label
    if output != None:
        fig.savefig(output, bbox_inches='tight')
        plt.close(fig)
    if make_fig == True:return(ax1)
    else: return(im1)
