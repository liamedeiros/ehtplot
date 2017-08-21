# Copyright (C) 2017 Chi-kwan Chan
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

def set_themes(style='ehtplot',
               screen='crystal',        # e.g., jupyter notebook
               vector='ApJ',            # e.g., eps and pdf for journals
               raster=['dark-on-white', # e.g., for talks
                       'light-on-black'] ):
    """Setting the global themes for ehtplot

    set_themes() is used to set the default themes for rendering to
    screen, export to vector graphics formats (such as eps and pdf),
    and export to raster/bitmap formats (such as jpg and png).  Each
    of the arguments can be a single string of an array of strings.
    In the later case, multiple figures will be rendered and/or
    exported.

    In principle, we can have a ehtplot Theme class to manage themes.
    This seems overkill at the moment and we simply use a plain python
    dictionary to store themes for now.

    Args:
        screen: the theme(s) used for rendering on screen
        vector: the theme(s) used for exporting to vector graphics formats
        raster: the theme(s) used for exporting to raster (bitmap) formats

    """
    file = os.path.join(os.path.dirname(__file__), style+".mplstyle")
    if os.path.isfile(file):
        style = mpl.rc_params_from_file(file, use_default_template=False)
    mpl.style.use(style)
