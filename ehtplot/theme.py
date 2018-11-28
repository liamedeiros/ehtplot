# Copyright (C) 2017--2018 Lia Medeiros & Chi-kwan Chan
# Copyright (C) 2017--2018 Steward Observatory
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

import matplotlib as mpl
import os

def get_themes(style):
    """Getting a theme for ehtplot

    get_themes() is used to get the theme for rendering to screen,
    export to vector graphics formats (such as eps and pdf), and
    export to raster/bitmap formats (such as jpg and png).

    In principle, we can have a ehtplot Theme class to manage themes.
    This seems overkill at the moment and we simply use a plain python
    dictionary to store themes for now.

    Args:
        style: matplotlib style

    """

    file = os.path.join(os.path.dirname(__file__), style+".mplstyle")
    if os.path.isfile(file):
        return mpl.rc_params_from_file(file, use_default_template=False)
    else:
        return style
