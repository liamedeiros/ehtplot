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

from math import sqrt, degrees
import numpy as np

from scipy.optimize import bisect, minimize

from colormath.color_objects     import LabColor, LCHabColor, sRGBColor
from colormath.color_conversions import convert_color

from matplotlib.colors import ListedColormap
from matplotlib.cm     import get_cmap

def convert(i, N,
            darkest=0.0, lightest=1.0,
            saturation=None, hue=None):
    f = i / (N - 1.0)

    s = sqrt(0.5) if saturation is None else saturation(f)
    h = 0.0       if hue        is None else hue(f)

    l = darkest + f * (lightest-darkest)
    c = l*s / sqrt(1.0 - s*s)

    lch = LCHabColor(100.0 * l, 100 * c, degrees(h))
    rgb = convert_color(lch, sRGBColor)

    return [rgb.clamped_rgb_r,
            rgb.clamped_rgb_g,
            rgb.clamped_rgb_b]

def colormap(N=256, **kwargs):
    return ListedColormap([convert(i, N, **kwargs) for i in range(N)])

def lightness(r, g, b, a=1.0):
    return convert_color(sRGBColor(r, g, b), LabColor).lab_l

def linearize(cm, N=256,
              lmin=None, lmax=None,
              vmin=0.0,  vmax=1.0,
              save=None):
    def v2l(v):
        return lightness(*cm(v))
    def l2v(l):
        return bisect(lambda v: v2l(v) - l, vmin, vmax)

    L = np.linspace(v2l(vmin) if lmin is None else lmin,
                    v2l(vmax) if lmax is None else lmax, N)

    carr = [cm(l2v(l)) for l in L]
    if save is None:
        return ListedColormap(carr)
    else:
        np.savetxt(save, carr)

def symmetrize(cm, N=256,
               lmin=None, lmid=None, lmax=None,
               vmin=0.0,  vmid=None, vmax=1.0,
               save=None):
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
            print(l)
            return 100.0
    def l2vR(l):
        try:
            return bisect(lambda v: v2l(v) - l, vmid, vmax)
        except:
            print(l)
            return 100.0

    carr = ([cm(l2vL(l)) for l in L[:N//2]] +
            [cm(l2vR(l)) for l in L[N//2:]])
    if save is None:
        return ListedColormap(carr)
    else:
        np.savetxt(save, carr)

if __name__ == "__main__":
    linearize(get_cmap('afmhot'), save='ehthot.txt')
    symmetrize(get_cmap('RdBu'),  save='ehtRdBu.txt')
