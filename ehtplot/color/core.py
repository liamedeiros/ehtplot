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

from os.path import dirname, join, splitext, basename
from glob    import glob

import numpy as np

from matplotlib.colors import ListedColormap
from matplotlib.cm     import register_cmap

Nq = 256     # number of quantization levels in a colormap
Nc = 1024    # nubber of quantization levels in a channel (10bit default)
Ns = 1048576 # number of quantization levels in sampling colors during remap

def register(name=None, cmap=None):
    path = dirname(__file__)
    ext  = ".txt"
    if name is None:
        for f in glob(join(path, '*'+ext)):
            register(name=splitext(basename(f))[0]) # recursion
    else:
        if cmap is None:
            ctab = np.loadtxt(join(path, name+ext))
            if ctab.shape[1] == 3:
                ctab = np.append(ctab, np.full((ctab.shape[0], 1), Nc), axis=1)
            cmap = ListedColormap(ctab / (Nc - 1.0))
        register_cmap(name=name, cmap=cmap)
