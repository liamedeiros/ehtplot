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

from matplotlib.cm import get_cmap

from ehtplot.color.ctab   import get_ctab, save_ctab, path, ext
from ehtplot.color.adjust import transform, classify, adjust_sequential, adjust_divergent

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

def modify_many(category, cnames, roundups, prefix=path, postfix=None):
    if roundups is None:
        roundups = []
    elif not isinstance(roundups, list):
        roundups = [roundups]

    print("================")
    print(category)

    for cname in cnames:
        Jabp, cls = modify(cname, None, path+"/"+cname+"_u"+ext)
        for roundup in roundups:
            if postfix is None or len(roundups) > 1:
                fname = "{}/{}_{:.0f}u{}".format(path, cname, roundup, ext)
            else:
                fname = "{}/{}_{}u{}".format(path, cname, postfix, ext)
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

        # Manual adjustments
        'EHT demos': (
            ['gray', 'hot', 'afmhot', 'gist_heat'],
            [10.0, 20.0, 30.0, 40.0, 50.0])
        }

    for category, (cnames, roundups) in matplotlib_cmap_sets.items():
        modify_many(category, cnames, roundups, 'l')
