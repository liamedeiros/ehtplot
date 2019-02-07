#!/usr/bin/env python3
#
# Copyright (C) 2018--2019 Chi-kwan Chan
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
from __future__ import print_function
from __future__ import with_statement

import re
from io import open

from matplotlib.cm import get_cmap

from ehtplot.color.ctab  import get_ctab, save_ctab, _path, ext
from ehtplot.color.cmath import transform, classify, symmetrize
from ehtplot.color.cmath import adjust_sequential, adjust_divergent


def pre(cname):
    return transform(get_ctab(get_cmap(cname)))


def post(Jpapbp, cls, roundup, fname):
    adjust = globals()["adjust_"+cls]

    Jpapbp = adjust(Jpapbp, roundup)
    save_ctab(transform(Jpapbp, inverse=True), fname+ext)
    print("    Rounded up to {}; saved to \"{}\"".format(roundup, fname+ext))

    Jpapbp = symmetrize(Jpapbp, bitonic=True, diffuse=False)
    save_ctab(transform(Jpapbp, inverse=True), fname+"s"+ext)
    print("    Symmetrized; saved to \"{}\"".format(fname+"s"+ext))


def modify(cname, roundup, fname):
    Jpapbp = pre(cname)
    cls  = classify(Jpapbp)

    print("----------------")
    print(cls + " colormap " + cname)

    if cls == 'unknown':
        print("    Do nothing, no modification is made")
    else:
        print("    Jp in [{:.2f}, {:.2f}]". format(Jpapbp[0,0], Jpapbp[-1,0]))
        post(Jpapbp, cls, roundup, fname)

    return Jpapbp, cls


def modify_many(category, cnames, roundups, prefix=_path, postfix=None):
    if roundups is None:
        roundups = []
    elif not isinstance(roundups, list):
        roundups = [roundups]

    print("================")
    print(category)

    for cname in cnames:
        Jpapbp, cls = modify(cname, None, prefix+"/"+cname+"_u")
        for roundup in roundups:
            if postfix is None or len(roundups) > 1:
                fname = "{}/{}_{:.0f}u".format(prefix, cname, roundup)
            else:
                fname = "{}/{}_{}u".format(prefix, cname, postfix)
            post(Jpapbp, cls, roundup, fname)


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
