#!/usr/bin/env python3
#
# Copyright (C) 2018 Chi-kwan Chan
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

import numpy as np

from matplotlib.colors import ListedColormap
from matplotlib.cm     import get_cmap

from ehtplot.color.ctab   import get_ctab, save_ctab
from ehtplot.color.adjust import transform, interp, linearize

def uniq(a):
    return a[np.r_[True, a[:-1] != a[1:]]]

def symmetrize(Jabp, JpL=None, JpM=None, JpR=None):
    N = Jabp.shape[0]
    H = (N-1)//2
    if JpL is None:
        JpL = Jabp[0,0]
    if JpM is None:
        JpM = Jabp[H,0]
    if JpR is None:
        JpR = Jabp[-1,0]

    if JpR > JpM: # v-shape
        b = min(JpL, JpR)
        L = linearize(Jabp[:H,:], JpL=b,   JpR=JpM)
        R = linearize(Jabp[H:,:], JpL=JpM, JpR=b)
    else:         # ^-shape
        b = max(JpL, JpR)
        L = linearize(Jabp[:H,:], JpL=b,   JpR=JpM)
        R = linearize(Jabp[H:,:], JpL=JpM, JpR=b)

    return np.append(L, R, axis=0)

def uniformize(cname, N=256, Jplower=None, postfix=None):
    cmap = get_cmap(cname)
    Jabp = transform(get_ctab(cmap))
    Jp   = Jabp[:,0]
    sgn  = uniq(np.sign(Jp[1:] - Jp[:-1]).astype(int))

    if len(sgn) == 1:
        print(cname, sgn, "monotonic")
        ctab = linearize(Jabp, Jplower=Jplower)
    elif np.array_equal(sgn, [1,-1]):
        print(cname, sgn, "hill")
        ctab = symmetrize(Jabp, JpL=Jplower, JpR=Jplower)
    elif np.array_equal(sgn, [-1,1]):
        print(cname, sgn, "valley")
        ctab = symmetrize(Jabp, JpM=Jplower)
    else:
        print(cname, sgn, "?")

    save_ctab(transform(ctab, inverse=True), cname+"_"+postfix+".txt")

if __name__ == "__main__":
    cnames = [
        # Monotomically decreasing lightness
        'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr',
        'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu',
        'PuBuGn', 'BuGn', 'YlGn', 'binary', 'gist_yarg', 'Wistia',
        # Monotomically increasing lightness
        'gist_gray', 'gray', 'bone', 'pink', 'summer', 'autumn', 'hot',
        'afmhot', 'gist_heat', 'copper', 'gnuplot2', 'cubehelix',
        # Diverge colormaps
        'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn',
        'Spectral', 'coolwarm', 'bwr', 'seismic']

    for cname in cnames:
        uniformize(cname,             postfix='u')
        uniformize(cname, Jplower=25, postfix='lu')
