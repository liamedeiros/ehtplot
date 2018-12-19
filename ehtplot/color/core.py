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
from matplotlib.cm     import register_cmap

from ehtplot.color.ctab import list_ctab, load_ctab

Nq = 256  # number of quantization levels in a colormap

def register(name=None, cmap=None):
    if name is None:
        # Self-call to register all colormaps in "ehtplot/color/"
        for name in list_ctab():
            register(name=name, cmap=cmap)
    else:
        # Set up and register the colormap
        if cmap is None:
            cmap = ListedColormap(load_ctab(name))
        register_cmap(name=name, cmap=cmap)

        # Set up and register the reversed colormap
        if "_" not in name or not set(name.rsplit("_", 1)[1]) <= set("lu"):
            rname = name + "_r"
        else:
            rname = name + "r"
        register_cmap(name=rname, cmap=cmap.reversed())
