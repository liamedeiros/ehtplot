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

from matplotlib.colors import ListedColormap

from .adjust import transform
from .ctab   import save_ctab

Nq = 256 # number of quantization levels in a colormap

def new_cmap(N=Nq, darkest=15.0, lightest=95.0):
    v  = np.linspace(0, 1, num=N)

    Jp = np.linspace(darkest, lightest, num=N)
    hp = np.clip(np.linspace(-15.0, 105.0, num=N), 30.0, 90.0) * (np.pi/180.0)
    Cp = 30 * (1 - (2*v-1)**4)

    Jabp = np.stack([Jp, Cp * np.cos(hp), Cp * np.sin(hp)], axis=-1)
    sRGB = transform(Jabp, inverse=True)
    return ListedColormap(np.clip(sRGB, 0, 1))
