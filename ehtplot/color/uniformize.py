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

from scipy.optimize    import bisect, minimize
from colorspacious     import cspace_convert
from matplotlib.colors import ListedColormap
from matplotlib.cm     import get_cmap

from ehtplot.color.core import Nc

cscale = Nc - 1.0

def colortable(cm):
    cm = get_cmap(cm)
    return np.array([cm(i) for i in range(cm.N)])

def lightness(r, g, b, a=1.0):
    return cspace_convert([r, g, b], "sRGB1", "CAM02-UCS")[0]

def uniq(a):
    return a[np.r_[True, a[:-1] != a[1:]]]

def interp(x, xp, yp):
    if xp[0] < xp[-1]:
        return np.interp(x, xp, yp)
    else:
        return np.interp(x, np.flip(xp,0), np.flip(yp,0))

def linearize(cm, JpL=None, JpR=None, save=None):
    ctab = np.array([cm(i) for i in range(cm.N)])
    Jabp = cspace_convert(ctab[:,:3], "sRGB1", "CAM02-UCS")

    Jp = np.linspace(Jabp[ 0,0] if JpL is None else JpL,
                     Jabp[-1,0] if JpR is None else JpR, cm.N)
    ap = interp(Jp, Jabp[:,0], Jabp[:,1])
    bp = interp(Jp, Jabp[:,0], Jabp[:,2])

    carr = cspace_convert(np.stack([Jp,ap,bp], axis=-1), "CAM02-UCS", "sRGB1")
    if save is None:
        return ListedColormap(carr)
    else:
        if carr.shape[1] == 4 and np.all(carr[:,3] == 1.0):
            carr = carr[:,:3]
        np.savetxt(save, np.rint(carr * cscale).astype(int), fmt="%i")

def symmetrize(cm, JpL=None, JpM=None, JpR=None, save=None):
    ctab = np.array([cm(i) for i in range(cm.N)])
    Jabp = cspace_convert(ctab[:,:3], "sRGB1", "CAM02-UCS")

    N = cm.N
    H = N//2
    if JpL is None:
        JpL = Jabp[0,0]
    if JpM is None:
        JpM = Jabp[H,0]
    if JpR is None:
        JpR = Jabp[-1,0]

    if (JpR - JpM) * (JpM - JpL) >= 0.0:
        raise ValueError('colormap does not seem to diverge')

    if JpR > JpM: # v-shape
        b  = min(JpL, JpR)
        Jp = np.absolute(np.linspace(-b, b, N))
    else:           # ^-shape
        b  = JpM - max(JpL, JpR)
        Jp = JpM - np.absolute(np.linspace(-b, b, N))

    apL = interp(Jp[:H], Jabp[:H,0], Jabp[:H,1])
    apR = interp(Jp[H:], Jabp[H:,0], Jabp[H:,1])
    bpL = interp(Jp[:H], Jabp[:H,0], Jabp[:H,2])
    bpR = interp(Jp[H:], Jabp[H:,0], Jabp[H:,2])

    carr = cspace_convert(np.stack([Jp,
                                    np.append(apL, apR),
                                    np.append(bpL, bpR)], axis=-1),
                          "CAM02-UCS", "sRGB1")
    if save is None:
        return ListedColormap(carr)
    else:
        if carr.shape[1] == 4 and np.all(carr[:,3] == 1.0):
            carr = carr[:,:3]
        np.savetxt(save, np.rint(carr * cscale).astype(int), fmt="%i")

def uniformize(cname, N=256):
    Jabp = cspace_convert(colortable(cname)[:,:3], "sRGB1", "CAM02-UCS")
    Jp   = Jabp[:,0]
    sgn  = uniq(np.sign(Jp[1:] - Jp[:-1]).astype(int))

    if np.array_equal(sgn, [1]):
        print(cname, sgn, 'up')
        linearize(get_cmap(cname),         save=cname+'_u.txt')
        linearize(get_cmap(cname), JpR=25, save=cname+'_lu.txt')
    elif np.array_equal(sgn, [-1]):
        print(cname, sgn, 'down')
        linearize(get_cmap(cname),         save=cname+'_u.txt')
        linearize(get_cmap(cname), JpL=25, save=cname+'_lu.txt')
    elif np.array_equal(sgn, [1,-1]):
        print(cname, sgn, 'hill')
        symmetrize(get_cmap(cname),                 save=cname+'_u.txt')
        symmetrize(get_cmap(cname), JpL=25, JpR=25, save=cname+'_lu.txt')
    elif np.array_equal(sgn, [-1,1]):
        print(cname, sgn, 'valley')
        symmetrize(get_cmap(cname),                 save=cname+'_u.txt')
        symmetrize(get_cmap(cname), JpL=25, JpR=25, save=cname+'_lu.txt')
    else:
        print(cname, sgn, '?')

if __name__ == "__main__":
    cnames = [
        'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr',
        'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu',
        'PuBuGn', 'BuGn', 'YlGn', 'binary', 'gist_yarg', 'Wistia',

        'gist_gray', 'gray', 'bone', 'pink', 'summer', 'autumn', 'hot',
        'afmhot', 'gist_heat', 'copper', 'gnuplot2',

        'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn',
        'Spectral', 'coolwarm', 'bwr', 'seismic']

    for cname in cnames:
        uniformize(cname)
