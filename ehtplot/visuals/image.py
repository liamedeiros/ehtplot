# Copyright (C) 2018--2019 Lia Medeiros
# Copyright (C) 2018--2019 Steward Observatory
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

from __future__ import absolute_import
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm


def add_scale(ax, label='$50 \mu $arcsec', length=10, color='gold', padding=0.15, end_factor=0.015,font=10.56, lw=1):
    lims   = ax.get_xlim()
    factor = (lims[1] -lims[0]) * padding
    ends   = (lims[1] -lims[0]) * end_factor
    ax.hlines(lims[0]+factor, lims[0]+factor, lims[0]+factor+length, color=color, lw=lw)
    ax.vlines(lims[0]+factor, lims[0]+factor-ends, lims[0]+factor+ends, color=color, lw=lw)
    ax.vlines(lims[0]+factor+length, lims[0]+factor-ends, lims[0]+factor+ends, color=color, lw=lw)
    if label != None:
        ax.text((lims[0]+factor)+1.5,(lims[0]+factor)*.95, label, fontsize=font, color=color)


def visualize_image(ax, img, name=None,
               imgsz=None, pxsz=None, zoom=True, unit='$GMc^{-2}$', length_scale=None,
               norm=1, scale='lin', vlim=None, colorbar=True):
    """!@brief Makes a plot of an image.

    This can be used for a single image or for multiple subplots,
    below is an example of how this can be used for a single image:
    @code
    fig = Figure(Panel().visualize_image(image_array, name='Model B'))
    fig.savefig(file_name)
    @endcode

    This is an example for multiple subplots:

    @code
    fig = Figure([[pnl1, pnl2], [pnl3, pnl4]])
    fig.savefig(file_name)
    @endcode

    Note that for multiple subplots you might want to omit color bars,
    and only include the model name in one of the subplots.

    @param ax optional keyword, default set to None this keyword is
    closely tied with fig, either they both must be None or
    neither. If None will create a figure of size columnwidth by
    columnwidth with one subplot. If not None this should be the name
    of the subplot (where applicable) where you want to plot your
    image, see the example code above.

    @param img 2D numpy array of the image to be plotted.

    @param name optional keyword, default set to None. If not None
    must be a string and will add a text label to the plot equal to
    this string.

    @param imgsz float, optional keyword, default set to 64, size of
    the array in units of \f$ GM/c^2 \f$.

    @param zoom optional keyword, default set to True. If set to True
    will zoom in to about 20 \f$ GM/c^2 \f$ on each side, if not set
    to True, will leave the full array visible.

    @param unit optional keyword, default set to `GM/c^2`.

    @param length_scale optional keyword, default set to True.

    @param norm optional keyword, default set to 1, this is in case
    normalizing to 1 doesn't give the desired image, you can control a
    more specific normalization with norm_num, for example, if
    norm_num=1.2, the maximum value in the image will be 1.2, but the
    color bar will go from 0 to 1 (assuming scale='lin').

    @param scale optional keyword, default set to 'lin', 'log' is also
    supported, this sets the scale of the color map.

    @param vlim optional keyword, default set to [0, 1], this is the
    limits for the color bar.

    @param colorbar optional keyword, default set to True.

    """
    if imgsz is not None and pxsz is not None:
        raise ValueError("imgsz and pxsz cannot be set simultaneously")
    elif pxsz is not None:
        imgsz = img.shape[0] * pxsz
    elif imgsz is None:
        imgsz = 64
    bb = [-0.5*imgsz, 0.5*imgsz, -0.5*imgsz, 0.5*imgsz]

    if norm is not False:
        img *= norm / np.max(img)

    if scale == 'lin':
        if vlim is None:
            vlim = [0, 1]
        scale_kwargs = {'vmin': vlim[0], 'vmax': vlim[1]}
    elif scale == 'log':
        scale_kwargs = {'norm': (LogNorm() if vlim is None else
                                 LogNorm(vmin=vlim[0], vmax=vlim[1]))}

    im = ax.imshow(img, extent=bb, **scale_kwargs)
    ax.tick_params(axis='both', which='major', width=1.5)

    if zoom is True: # flip_x = False, zoom=True
        r0 = np.sqrt(27) # BH shadow in units of GM/c**2
        ax.set_xlim([-2 * r0, 2 * r0])
        ax.set_xticks([-10, -5, 0, 5, 10])

    ax.set_ylim(ax.get_xlim())
    ax.set_yticks(ax.get_xticks())
    if name is not None:
        ax.text(0.26,0.26, name, color='w', transform=ax.transAxes)

    if length_scale is None: #decide base on unit
        length_scale = unit.endswith('arcsec')

    if length_scale:
        ax.set_axis_off()
        add_scale(ax)
    else:
        ax.set_xlabel('X ({})'.format(unit))
        ax.set_ylabel('Y ({})'.format(unit))

    if colorbar is True:
        colorbar = 'top'

    if colorbar is not False:
        if colorbar == 'top' or colorbar =='bottom':
            orientation = 'horizontal'
        else:
            orientation = 'vertical'

        divider = make_axes_locatable(ax)
        cax     = divider.append_axes(colorbar, size='7%', pad=0.05)
        cbar    = plt.colorbar(im, cax=cax, orientation=orientation)
        cbar.ax.xaxis.set_ticks_position(colorbar)
