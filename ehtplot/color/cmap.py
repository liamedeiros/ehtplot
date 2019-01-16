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
from __future__ import division

import numpy as np

from matplotlib.colors import ListedColormap

from ehtplot.color.adjust import transform, symmetrize
from ehtplot.color.ctab   import get_ctab, save_ctab

Nq = 256 # number of quantization levels in a colormap


def max_chroma(Jp, hp,
               Cpmin=0.0, Cpmax=64.0,
               eps=1024*np.finfo(np.float).eps,
               clip=True):
    Jpmin  = 5.54015251457561e-22
    Jpminv = 3.797300335885588 # obtained by using 4096 h' values
    Jpmaxv = 98.98016717524226 # obtained by using 4096 h' values
    Jpmax  = 99.99871678107648

    if clip:
       Jp = np.clip(Jp, Jpminv, Jpmaxv)

    if np.any(Jp < Jpmin)  or np.any(Jp > Jpmax):
       raise ValueError("J' out of range.")

    if np.any(Jp < Jpminv) or np.any(Jp > Jpmaxv):
       raise ValueError(
           "J' is out of range such that the corresponding sRGB colorspace "+
           "is offset and C' == 0 is no longer a valid assumption.")

    CpU = np.full(len(Jp), Cpmax)
    CpL = np.full(len(Jp), Cpmin)

    for i in range(64):
        Cp = 0.5 * (CpU + CpL)

        # Fix when we hit machine precision
        need_fix = Cp == CpU
        Cp[need_fix] = CpL[need_fix]

        Jpapbp = np.stack([Jp, Cp * np.cos(hp), Cp * np.sin(hp)], axis=-1)
        sRGB   = transform(Jpapbp, inverse=True)
        edge   = 2.0 * np.amax(abs(sRGB - 0.5), -1)

        if 1.0 - eps <= np.min(edge) and np.max(edge) <= 1.0:
            break

        I = edge >= 1.0
        CpU[ I] = Cp[ I]
        CpL[~I] = Cp[~I]
    else:
        raise ArithmeticError("WARNING: max_chroma() has not fully converged")

    return Cp


def ehtcmap(N=Nq,
            Jpmin=15.0, Jpmax=95.0,
            Cpmin= 0.0, Cpmax=64.0,
            hpmin=None, hpmax=90.0,
            hp=None,
            **kwargs):
    name = kwargs.pop('name', "new eht colormap")

    Jp = np.linspace(Jpmin, Jpmax, num=N)
    if hp is None:
        if hpmin is None:
            hpmin = hpmax - 60.0
        q  = 0.25 * (hpmax - hpmin)
        hp = np.clip(np.linspace(hpmin-3*q, hpmax+q, num=N), hpmin, hpmax)
    elif callable(hp):
        hp = hp(np.linspace(0.0, 1.0, num=N))
    hp *= np.pi/180.0
    Cp = max_chroma(Jp, hp, Cpmin=Cpmin, Cpmax=Cpmax)

    Jpapbp = np.stack([Jp, Cp * np.cos(hp), Cp * np.sin(hp)], axis=-1)
    Jpapbp = symmetrize(Jpapbp, **kwargs)
    sRGB   = transform(Jpapbp, inverse=True)
    return ListedColormap(np.clip(sRGB, 0, 1), name=name)


def linseg(x, sarr):
    """Compute a discontinues linear segmented array from x and sarr"""
    y = np.zeros(len(x))
    for i in range(len(sarr) - 1):
        xL = sarr[i][0]
        xR = sarr[i+1][0]
        yL = sarr[i][2]
        yR = sarr[i+1][1]
        iL = np.searchsorted(x, xL, side='left')
        iR = np.searchsorted(x, xR, side='right')
        y[iL:iR] = np.linspace(yL, yR, iR-iL)
    return y


def getCp(ctab):
    Jpapbp = transform(ctab)
    return np.sqrt(Jpapbp[:,1] * Jpapbp[:,1] + Jpapbp[:,2] * Jpapbp[:,2])


def mergecmap(cmplist, **kwargs):
    """Merge color maps

    An inelegant function to merge a list of existing colormaps into
    one.

    TODO: design a more elegant interface.

    """
    name   = kwargs.pop('name', "new eht colormap")
    matchC = kwargs.pop('matchC', False)

    ctabs = []
    for cmp in cmplist:
        ctab = get_ctab(cmp['name'])
        if cmp.get('revert'):
            ctab = ctab[::-1]
        ctabs += [ctab]

    if matchC:
        n   = len(ctabs[0])
        mCp = getCp(ctabs[0])
        for ctab in ctabs[1:]:
            if len(ctab) != n:
                raise ValueError("Fail to match chroma; "+
                                 "colormap seguments have different lengths")
            mCp = np.minimum(mCp, getCp(ctab))

        for i in range(len(ctabs)):
            Jpapbp = transform(ctabs[i])
            Cp   = np.sqrt(Jpapbp[:,1] * Jpapbp[:,1] + Jpapbp[:,2] * Jpapbp[:,2])
            f    = mCp / (Cp + 1.0e-32)
            Jpapbp[:,1] *= f
            Jpapbp[:,2] *= f
            ctabs[i] = transform(Jpapbp, inverse=True)

    ctab = [crow for ctab in ctabs for crow in ctab] # flattern list of list
    return ListedColormap(np.clip(ctab, 0, 1), name=name)


def ehtrainbow(N=Nq,
               Jp=73.16377142857142, # maximizing minimal Cp for all hue
               Cp=None,
               hp0=32.1526953043875, # offset the hue so that value==0 is red
               **kwargs):
    """Create a perceptually uniform rainbow colormap"""
    name = kwargs.pop('name', "new eht colormap")

    hp = np.linspace(np.pi / 180 * (hp0),
                     np.pi / 180 * (hp0+360), Nq, endpoint=False)

    if Cp is None:
        Cp = min(max_chroma(np.full(len(hp), Jp), hp))

    ap = Cp * np.cos(hp)
    bp = Cp * np.sin(hp)

    Jpapbp = np.array([np.full(len(hp), Jp), ap, bp]).T
    sRGB   = transform(Jpapbp, inverse=True)

    return ListedColormap(sRGB, name=name)
