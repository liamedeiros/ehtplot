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

def interp(x, xp, yp):
    if xp[0] < xp[-1]:
        return np.interp(x, xp, yp)
    else:
        return np.interp(x, np.flip(xp,0), np.flip(yp,0))

def linearizeJp(Jabp, JpL=None, JpR=None):
    if JpL is None: JpL = Jabp[ 0,0]
    if JpR is None: JpR = Jabp[-1,0]
    out = Jabp.copy()
    out[:,0] = np.linspace(JpL, JpR, out.shape[0])
    out[:,1] = interp(out[:,0], Jabp[:,0], Jabp[:,1])
    out[:,2] = interp(out[:,0], Jabp[:,0], Jabp[:,2])
    return out
