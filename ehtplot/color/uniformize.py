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

from ehtplot.color.core     import Nc
from ehtplot.color.colormap import colorremap

cscale = Nc - 1.0

def lightness(r, g, b, a=1.0):
    return cspace_convert([r, g, b], "sRGB1", "CAM02-UCS")[0]

def linearize(cm, N=None,
              lmin=None, lmax=None,
              vmin=0.0,  vmax=1.0,
              save=None):
    if N is None:
        N = cm.N
    cm = colorremap(cm)

    def v2l(v):
        return lightness(*cm(v))
    def l2v(l):
        return bisect(lambda v: v2l(v) - l, vmin, vmax)

    L = np.linspace(v2l(vmin) if lmin is None else lmin,
                    v2l(vmax) if lmax is None else lmax, N)

    carr = np.array([cm(l2v(l)) for l in L])
    if save is None:
        return ListedColormap(carr)
    else:
        if carr.shape[1] == 4 and np.all(carr[:,3] == 1.0):
            carr = carr[:,:3]
        np.savetxt(save, np.rint(carr * cscale).astype(int), fmt="%i")

def symmetrize(cm, N=None,
               lmin=None, lmid=None, lmax=None,
               vmin=0.0,  vmid=None, vmax=1.0,
               save=None):
    if N is None:
        N = cm.N
    cm = colorremap(cm)

    def v2l(v):
        return  lightness(*cm(v[0] if isinstance(v, np.ndarray) else v))
    def v2ml(v):
        return -lightness(*cm(v[0] if isinstance(v, np.ndarray) else v))

    if lmin is None: lmin = v2l(vmin)
    if lmid is None: lmid = v2l(0.5 if vmid is None else vmid)
    if lmax is None: lmax = v2l(vmax)

    if (lmax - lmid) * (lmid - lmin) >= 0.0:
        raise ValueError('colormap does not seem to diverge')

    if vmid is None:
        opt  = minimize(v2l if lmax > lmid else v2ml,
                        0.5, method='Nelder-Mead')
        vmid = opt.x[0]
        lmid = v2l(vmid)

    if lmax > lmid: # v-shape
        b = min(lmin, lmax)
        L = np.absolute(np.linspace(-b, b, N))
    else:           # ^-shape
        b = lmid - max(lmin, lmax)
        L = lmid - np.absolute(np.linspace(-b, b, N))

    def l2vL(l):
        try:
            return bisect(lambda v: v2l(v) - l, vmin, vmid)
        except:
            print('Warning: unable to solve for value in l2vL()', l)
            return 0.5 if l > 75 else 0.0
    def l2vR(l):
        try:
            return bisect(lambda v: v2l(v) - l, vmid, vmax)
        except:
            print('Warning: unable to solve for value in l2vR()', l)
            return 0.5 if l > 75 else 1.0

    carr = np.array([cm(l2vL(l)) for l in L[:N//2]] +
                    [cm(l2vR(l)) for l in L[N//2:]])
    if save is None:
        return ListedColormap(carr)
    else:
        if carr.shape[1] == 4 and np.all(carr[:,3] == 1.0):
            carr = carr[:,:3]
        np.savetxt(save, np.rint(carr * cscale).astype(int), fmt="%i")

if __name__ == "__main__":
    lmaps = [
        'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
        'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
        'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
        'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
        'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
        'hot', 'afmhot', 'gist_heat', 'copper']

    smaps = [
        'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
        'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']

    for cm in lmaps:
        print(cm)
        linearize(get_cmap(cm), save=cm+'_u.txt')

    for cm in smaps:
        print(cm)
        symmetrize(get_cmap(cm), save=cm+'_u.txt')
