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

from colormath.color_objects     import LCHabColor, sRGBColor
from colormath.color_conversions import convert_color

from matplotlib.colors import ListedColormap

def convert(i, N,
            darkest=0.0, saturation=None, hue=None):
    f = i / (N - 1.0)

    s = sqrt(0.5) if saturation is None else saturation(f)
    h = 0.0       if hue        is None else hue(f)

    l = darkest + f * (1.0-darkest)
    c = l*s / sqrt(1.0 - s*s)

    lch = LCHabColor(100.0 * l, 100 * c, degrees(h))
    rgb = convert_color(lch, sRGBColor)

    return [rgb.clamped_rgb_r,
            rgb.clamped_rgb_g,
            rgb.clamped_rgb_b]

def colormap(N=256, **kwargs):
    return ListedColormap([convert(i, N, **kwargs) for i in range(N)])
