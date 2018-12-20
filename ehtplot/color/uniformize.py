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

def extrema(a):
    da =  a[1:] -  a[:-1]
    xa = da[1:] * da[:-1]
    return np.argwhere(xa <= 0.0)[:,0]+1

def uniformize(cname, N=256, Jplower=None, postfix=None):
    cmap = get_cmap(cname)
    Jabp = transform(get_ctab(cmap))
    Jp   = Jabp[:,0]
    x    = extrema(Jp)

    if len(x) == 0:
        print(cname, x, "monotonic")
        ctab = linearize(Jabp, Jplower=Jplower)
    elif len(x) == 1 and x[0] in {(N+1)//2-1, N//2}:
        print(cname, x, "divergent")
        L = linearize(Jabp[:(N+1)//2,:], Jplower=Jplower)
        R = linearize(Jabp[N//2:,    :], Jplower=Jplower)
        ctab = np.append(L, R[N%2:,:], axis=0)
    else:
        print(cname, x, "?")

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
