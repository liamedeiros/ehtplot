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

from matplotlib.colors import ListedColormap, is_color_like, to_rgba

from ehtplot.color.cmath import transform, symmetrize, max_chroma, deltaE
from ehtplot.color.ctab  import get_ctab, save_ctab

Nq = 256 # number of quantization levels in a colormap


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
               Jp=73.16384, # maximizing minimal Cp for all hue
               Cp=None,
               hp0=32.1526953043875, # offset the hue so that value==0 is red
               eps=1024*np.finfo(np.float).eps,
               **kwargs):
    """Create a perceptually uniform rainbow colormap"""
    name = kwargs.pop('name', "new eht colormap")

    hp = np.linspace(np.pi / 180 * (hp0),
                     np.pi / 180 * (hp0+360), Nq+1)
    Jp = np.full(len(hp), Jp)

    if Cp is not None:
        if Cp == 'minmax':
            Cp = min(max_chroma(Jp, hp))

        ap = Cp * np.cos(hp)
        bp = Cp * np.sin(hp)

        Jpapbp = np.array([np.full(len(hp), Jp), ap, bp]).T
        sRGB   = transform(Jpapbp[:-1,:], inverse=True)

        return ListedColormap(sRGB, name=name)

    Cp = max_chroma(Jp, hp)
    ap = Cp * np.cos(hp)
    bp = Cp * np.sin(hp)
    dE = np.sqrt((Jp[1:]-Jp[:-1])**2 +
                 (ap[1:]-ap[:-1])**2 +
                 (bp[1:]-bp[:-1])**2)
    cE = np.concatenate(([0], np.cumsum(dE)))

    for i in range(256):
        cE_new = np.linspace(0, max(cE), len(cE))
        hp_new = np.interp(cE_new, cE, hp)
        Cp_new = max_chroma(Jp, hp_new)

        if np.max(abs(Cp - Cp_new)) < eps:
            break

        Cp = Cp_new
        hp = hp_new

        ap = Cp * np.cos(hp)
        bp = Cp * np.sin(hp)
        dE = np.sqrt((Jp[1:]-Jp[:-1])**2 +
                     (ap[1:]-ap[:-1])**2 +
                     (bp[1:]-bp[:-1])**2)
        cE = np.concatenate(([0], np.cumsum(dE)))
    else:
        print("WARNING: ehtuniform() has not fully converged")

    Jpapbp = np.array([Jp, ap, bp]).T
    sRGB   = transform(Jpapbp[:-1,:], inverse=True)
    return ListedColormap(np.clip(sRGB, 0, 1), name=name)


def gethue(color):
    """Get the hue of a color"""
    if isinstance(color, float):
        return color

    if is_color_like(color):
        RGB = to_rgba(color)[:3]
    else:
        raise ValueError("color is not color like")

    Jp, ap, bp = transform(np.array([RGB]))[0]
    hp = np.arctan2(bp, ap) * 180 / np.pi
    print("Decode color \"{}\"; h' = {}".format(color, hp))
    return hp


def ehtuniform(N=Nq,
               JpL=6.25,    JpR=93.75, # consistent with 17 quantize levels
               CpL=0.0,     CpR=64.0,
               hpL='coral', hpR='gold', hpD=None,
               eps=1024*np.finfo(np.float).eps,
               **kwargs):
    """Create a perceptually uniform colormap"""
    name = kwargs.pop('name', "new eht colormap")

    hpL = gethue(hpL) * np.pi / 180.0
    hpR = gethue(hpR) * np.pi / 180.0
    if hpD is None:
        dhp = hpR - hpL
        while dhp < 0:
            dhp += 2 * np.pi
        while dhp > 2 * np.pi:
            dhp -= 2 * np.pi
        hpD = +1 if dhp < np.pi else -1
    if (hpR - hpL) * hpD < 0.0:
        hpR += hpD * 2.0 * np.pi

    Jp = np.linspace(JpL, JpR, N)
    hp = np.linspace(hpL, hpR, N-2)
    Cp = max_chroma(Jp[1:-1], hp)

    Cp = np.concatenate(([CpL], Cp, [CpR]))
    hp = np.concatenate(([hpL], hp, [hpR]))

    ap = Cp * np.cos(hp)
    bp = Cp * np.sin(hp)
    dE = np.sqrt((Jp[1:]-Jp[:-1])**2 +
                 (ap[1:]-ap[:-1])**2 +
                 (bp[1:]-bp[:-1])**2)
    cE = np.concatenate(([0], np.cumsum(dE)))

    for i in range(256):
        cE_new = np.linspace(0, max(cE), len(cE))
        hp_new = np.interp(cE_new, cE, hp)
        Cp_new = np.interp(cE_new, cE, Cp)

        if hpD > 0:
            edgeL = hp_new <= hpL
            edge  = np.logical_and(hpL < hp_new, hp_new < hpR)
            edgeR = hpR <= hp_new
        else:
            edgeL = hp_new >= hpL
            edge  = np.logical_and(hpL > hp_new, hp_new > hpR)
            edgeR = hpR >= hp_new

        Cp_tmp         = max_chroma(Jp[edge], hp_new[edge])
        Cp_new[edgeL] *= Cp_tmp[ 0] / Cp_new[edge][ 0]
        Cp_new[edgeR] *= Cp_tmp[-1] / Cp_new[edge][-1]
        Cp_new[edge]   = Cp_tmp

        if np.max(abs(Cp - Cp_new)) < eps:
            break

        Cp = Cp_new
        hp = hp_new

        ap = Cp * np.cos(hp)
        bp = Cp * np.sin(hp)
        dE = np.sqrt((Jp[1:]-Jp[:-1])**2 +
                     (ap[1:]-ap[:-1])**2 +
                     (bp[1:]-bp[:-1])**2)
        cE = np.concatenate(([0], np.cumsum(dE)))
    else:
        print("WARNING: ehtuniform() has not fully converged")

    Jpapbp = np.array([Jp, ap, bp]).T
    sRGB   = transform(Jpapbp, inverse=True)
    return ListedColormap(np.clip(sRGB, 0, 1), name=name)
