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

from colorspacious import cspace_convert

def interp(x, xp, yp):
    if xp[0] < xp[-1]:
        return np.interp(x, xp, yp)
    else:
        return np.interp(x, np.flip(xp,0), np.flip(yp,0))

def extrema(a):
    da =  a[1:] -  a[:-1]
    xa = da[1:] * da[:-1]
    return np.argwhere(xa <= 0.0)[:,0]+1

def transform(ctab, src='sRGB1', dst='CAM02-UCS', inverse=False):
    out = ctab.copy()
    if not inverse:
        out[:,:3] = cspace_convert(out[:,:3], src, dst)
    else:
        out[:,:3] = cspace_convert(out[:,:3], dst, src)
    return out

def classify(Jabp):
    N = Jabp.shape[0]
    x = extrema(Jabp[:,0])
    if len(x) == 0:
        return 'sequential'
    elif len(x) == 1 and x[0] in {(N+1)//2-1, N//2}:
        return 'divergent'
    else:
        return 'unknown'

def uniformize(Jabp, JpL=None, JpR=None, Jplower=None, Jpupper=None):
    if JpL is None: JpL = Jabp[ 0,0]
    if JpR is None: JpR = Jabp[-1,0]

    if Jplower is not None: JpL, JpR = max(JpL, Jplower), max(JpR, Jplower)
    if Jpupper is not None: JpL, JpR = min(JpL, Jpupper), min(JpR, Jpupper)

    out = Jabp.copy()
    out[:,0] = np.linspace(JpL, JpR, out.shape[0])
    out[:,1] = interp(out[:,0], Jabp[:,0], Jabp[:,1])
    out[:,2] = interp(out[:,0], Jabp[:,0], Jabp[:,2])

    return out

def desaturate(Jabp):
    out = Jabp.copy()
    s = np.linspace(0.0, np.sqrt(0.5), num=out.shape[0])
    s = s / np.sqrt(1.0 - s * s)
    if Jabp[0,0] > Jabp[-1,0]:
        s = np.flip(s)
    out[:,1] *= s
    out[:,2] *= s
    return out

def adjust_sequential(Jabp, roundup=None):
    Jp = Jabp[:,0]

    Jplower = min(Jp[0], Jp[-1])
    if roundup is not None:
        Jplower = np.ceil(Jplower / roundup) * roundup

    return uniformize(Jabp, Jplower=Jplower)

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

    L = uniformize(Jabp[:h+1,:], Jplower=Jplower, Jpupper=Jpupper)
    R = uniformize(Jabp[H:,  :], Jplower=Jplower, Jpupper=Jpupper)
    return np.append(L, R[N%2:,:], axis=0)