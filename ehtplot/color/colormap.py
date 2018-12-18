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

from colorspacious     import cspace_convert
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from ehtplot.color.core import Nq, Ns

def colormap(N=Nq,
            darkest=0.0, lightest=100.0,
            saturation=None, hue=None):
    f  = np.linspace(0, 1, num=N)

    s  = np.sqrt(0.5) if saturation is None else saturation(f)
    hp = 0.0          if hue        is None else hue(f)
    Jp = darkest + f * (lightest - darkest)
    Cp = Jp * s / np.sqrt(1.0 - s*s)

    Jabp = np.stack([Jp, Cp * np.cos(hp), Cp * np.sin(hp)], axis=-1)
    sRGB = np.clip(cspace_convert(Jabp, "CAM02-UCS", "sRGB1"), 0, 1)
    return ListedColormap(sRGB)
