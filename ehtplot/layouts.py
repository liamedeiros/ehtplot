# Copyright (C) 2017--2019 Lia Medeiros & Chi-kwan Chan
# Copyright (C) 2017--2019 Steward Observatory
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

from __future__ import division


def divide(pos, n, inrow=True):
    w = pos.x1 - pos.x0
    h = pos.y1 - pos.y0
    if inrow:
        w /= n
        box = lambda i: (pos.x0+i*w, pos.y0, w, h)
    else:
        h /= n
        box = lambda i: (pos.x0, pos.y0+i*h, w, h)
    for i in range(n):
        yield box(i)


def newaxes(fig, box=(0,0,1,1)):
    """Create an axes with hidden axises"""
    ax = fig.add_axes(box)
    ax.axis('off')
    return ax


def getaxes(ax0):
    """Get all axeses, e.g. twinx, from a single axes"""
    axes = [ax0]
    for pair in ax0._twinned_axes:
        if ax0 in pair:
            axes += list(set(pair).difference([ax0]))
    # TODO: ensure that all axes have the same position
    return axes
