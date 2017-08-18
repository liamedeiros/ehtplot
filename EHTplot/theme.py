# Copyright (C) 2017 Chi-kwan Chan
#
# This file is part of EHTplot.
#
# EHTplot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EHTplot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EHTplot.  If not, see <http://www.gnu.org/licenses/>.

def set_theme(screen='crystal',        # e.g., jupyter notebook
              vector='ApJ',            # e.g., eps and pdf for journals
              raster=['dark-on-white', # e.g., for talks
                      'light-on-black'] ):
    """Setting the global theme for EHTplot

    set_theme() is used to set the default themes for rendering to
    screen, export to vector graphics formats (such as eps and pdf),
    and export to raster/bitmap formats (such as jpg and png).  Each
    of the arguments can be a single string of an array of strings.
    In the later case, multiple figures will be rendered and/or
    exported.

    Args:
        screen: the theme(s) used for rendering on screen
        vector: the theme(s) used for exporting to vector graphics formats
        raster: the theme(s) used for exporting to raster (bitmap) formats

    """
    pass
