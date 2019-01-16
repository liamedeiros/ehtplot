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

from ehtplot.color.core import register

# Note that "cmath.py" requires the optional library "colorspacious"
# and hence is not imported by default.  We use matplotlib's core-
# pattern here and only import the necessary symbols in "core.py" to
# avoid namespace pollution.
#
# from ehtplot.color.cmap   import *
# from ehtplot.color.ctab   import *
# from ehtplot.color.cmath  import *
# from ehtplot.color.modify import *
# from ehtplot.color.view   import *


register()
