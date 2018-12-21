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

def adjust_sequential(Jabp, roundup=None):
    Jp = Jabp[:,0]

    Jplower = min(Jp[0], Jp[-1])
    if roundup is not None:
        Jplower = np.ceil(Jplower / roundup) * roundup

    return adjust(Jabp, Jplower=Jplower)

def adjust_divergent(Jabp, roundup=None):
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

def pre(cname):
    return transform(get_ctab(get_cmap(cname)))

def post(Jabp, cls, roundup, fname):
    adjust = globals()['adjust_'+cls]
    save_ctab(transform(adjust(Jabp, roundup), inverse=True), fname)
    print("    Rounded up to {}; saved to \"{}\"".format(roundup, fname))

def modify(cname, roundup, fname):
    Jabp = pre(cname)
    cls  = classify(Jabp)

    print("----------------")
    print(cls + " colormap " + cname)

    if cls == 'unknown':
        print("    Do nothing, no modification is made")
    else:
        print("    Jp in [{:.2f}, {:.2f}]". format(Jabp[0,0], Jabp[-1,0]))
        post(Jabp, cls, roundup, fname)

    return Jabp, cls

def modify_many(category, cnames, roundups, postfix=None):
    if roundups is None:
        roundups = []
    elif not isinstance(roundups, list):
        roundups = [roundups]

    print("================")
    print(category)

    for cname in cnames:
        Jabp, cls = modify(cname, None, cname+"_u.txt")
        for roundup in roundups:
            if postfix is None or len(roundups) > 1:
                fname = "{}_{:.0f}u.txt".format(cname, roundup)
            else:
                fname = "{}_{}u.txt".format(cname, postfix)
            post(Jabp, cls, roundup, fname)

if __name__ == "__main__":
    matplotlib_cmap_sets = {
        # Monotomically decreasing lightness
        'one-color decreasing': (
            ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds'],
            100.0/3),
        'two-color decreasing': (
            ['OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'BuGn', 'YlGn'],
            100.0/3),
        'three-color decreasing': (
            ['YlOrBr', 'YlOrRd', 'YlGnBu', 'PuBuGn'],
            100.0/3),
        'misc decreasing': (
            ['binary', 'gist_yarg', 'Wistia'],
            None),

        # Monotomically increasing lightness
        'boring increasing': (
            ['gist_gray', 'gray', 'bone', 'pink'],
            None),
        'seasons increasing': (
            ['summer', 'autumn'],
            None),
        'redish increasing': (
            ['hot', 'afmhot', 'gist_heat', 'copper'],
            None),
        'misc increasing': (
            ['gnuplot2', 'cubehelix'],
            None),

        # Divergent "hill" colormaps
        'two-color hill': (
            ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu'],
            40.0),
        'three-color hill': (
            ['RdYlBu', 'RdYlGn'],
            40.0),
        'misc hill': (
            ['Spectral', 'coolwarm', 'bwr', 'seismic'],
            None),
        }

    for category, (cnames, roundups) in matplotlib_cmap_sets.items():
        modify_many(category, cnames, roundups, 'l')
