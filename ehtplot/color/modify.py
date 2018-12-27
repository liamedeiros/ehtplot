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

import re

from matplotlib.cm import get_cmap

from ehtplot.color.ctab   import get_ctab, save_ctab, path, ext
from ehtplot.color.adjust import transform, classify, symmetrize, adjust_sequential, adjust_divergent

def pre(cname):
    return transform(get_ctab(get_cmap(cname)))

def post(Jabp, cls, roundup, fname):
    adjust = globals()["adjust_"+cls]

    Jabp = adjust(Jabp, roundup)
    save_ctab(transform(Jabp, inverse=True), fname+ext)
    print("    Rounded up to {}; saved to \"{}\"".format(roundup, fname+ext))

    Jabp = symmetrize(Jabp, bitonic=True, diffuse=False)
    save_ctab(transform(Jabp, inverse=True), fname+"s"+ext)
    print("    Symmetrized; saved to \"{}\"".format(fname+"s"+ext))

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
        Jabp, cls = modify(cname, None, path+"/"+cname+"_u")
        for roundup in roundups:
            if postfix is None or len(roundups) > 1:
                fname = "{}/{}_{:.0f}u".format(path, cname, roundup)
            else:
                fname = "{}/{}_{}u".format(path, cname, postfix)
            post(Jabp, cls, roundup, fname)

if __name__ == "__main__":
    with open("modify.cfg") as file:
        for line in file:
            line = re.sub(r"([ ,:]) +", r"\1", line.strip())
            if line == "" or  line[0] == "#":
                continue

            temp = line.split(":", 2)

            category = temp[0]
            cnames   = temp[1].split(",")
            if len(temp) > 2:
                roundups = [eval(s) for s in temp[2].split(",")]
            else:
                roundups = None

            modify_many(category, cnames, roundups, postfix="l")
