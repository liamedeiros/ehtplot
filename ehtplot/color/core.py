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

from matplotlib.colors import ListedColormap
from matplotlib.cm     import register_cmap

from ehtplot.color.ctab import list_ctab, load_ctab


def unmodified(name):
    chars = set("0123456789flus")
    return "_" not in name or not set(name.rsplit("_", 1)[1]) <= chars


def register(name=None, cmap=None, path=None):
    if name is None:
        # Self-call to register all colormaps in "ehtplot/color/"
        for name in list_ctab(path=path):
            register(name=name, cmap=cmap, path=path)
    else:
        if cmap is None:
            cmap = ListedColormap(load_ctab(name, path=path))

        # Register the colormap
        register_cmap(name=name, cmap=cmap)

        # Register the reversed colormap
        register_cmap(name=name + ("_r" if unmodified(name) else "r"),
                      cmap=cmap.reversed())
