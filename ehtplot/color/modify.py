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
from ehtplot.color.adjust import transform, classify, adjust

def modify_sequential(Jabp, roundup):
    Jp = Jabp[:,0]

    Jplower = min(Jp[0], Jp[-1])
    if roundup is not None:
        Jplower = np.ceil(Jplower / roundup) * roundup

    return adjust(Jabp, Jplower=Jplower)

def modify_divergent(Jabp, roundup):
    Jp = Jabp[:,0]
    N  = Jabp.shape[0]
    h  = (N+1)//2-1 # == H-1 if even; == H if odd
    H  = N//2

    if Jp[1] > Jp[0]: # hill
        Jplower = max(Jp[0], Jp[-1])
        Jpupper = min(Jp[h], Jp[H])
    else: # valley
        Jplower = max(Jp[h], Jp[H])
        Jpupper = min(Jp[0], Jp[-1])
    if roundup is not None:
        Jplower = np.ceil(Jplower / roundup) * roundup

    L = adjust(Jabp[:h+1,:], Jplower=Jplower, Jpupper=Jpupper)
    R = adjust(Jabp[H:,  :], Jplower=Jplower, Jpupper=Jpupper)
    return np.append(L, R[N%2:,:], axis=0)

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

        Jabp = transform(get_ctab(get_cmap(cname)))
        cls  = classify(Jabp)

        print("Working on {} colormap \"{}\":".format(cls, cname))
        if cls == 'unknown':
            print("do nothing, no modification is made")
            continue
        else:
            print("modifying the colormap")
            modify = globals()['modify_'+cls]

        save_ctab(transform(modify(Jabp, None), inverse=True), cname+'_u.txt')
        save_ctab(transform(modify(Jabp, 25),   inverse=True), cname+'_lu.txt')
