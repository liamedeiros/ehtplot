# Copyright (C) 2019 Chi-kwan Chan
# Copyright (C) 2019 Steward Observatory
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

from ehtplot.color.cmath import transform


def invalid(sRGB):
    return np.logical_or(np.amin(sRGB, -1) < 0,
                         np.amax(sRGB, -1) > 1)


def visualize_colors(ax, Jp=73.16384, L=50):
    N  = 2 * (8*L) + 1
    aP = np.linspace(-L,L,N)
    bP = np.linspace(-L,L,N)
    ap, bp = np.meshgrid(aP, bP)

    Jpapbp = np.array([np.full(N*N, Jp), ap.flatten(), bp.flatten()]).T
    sRGB   = transform(Jpapbp, inverse=True)
    sRGB[invalid(sRGB),:] = 0

    ax.imshow(sRGB.reshape(N,N,3),
              origin='lower',
              extent=[-L,L,-L,L])
    ax.set_xlabel("a'")
    ax.set_ylabel("b'")
