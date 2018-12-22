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

from .core import register

# Note that "adjust.py" requires the optional library "colorspacious"
# and hence is not always imported.  We use matplotlib's core-pattern
# and here and only import the necessary symbols to avoid namespace
# pollution.
try:
    import colorspacious
except ImportError:
    #print("`colorspacious` not found; "+
    #      "only limited function of `ehtplot.color` is available.")
    pass
else:
    print("`colorspacious` found; `ehtplot.color` is fully loaded.")
    from .adjust import transform, classify, uniformize, desaturate
    from .cmap   import new_cmap
    from .ctab   import get_ctab
    from .modify import modify

register()
