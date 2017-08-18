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

    In a typical scientific workflow, a publication quality figure
    often goes to multiple places, which can have very different
    typesetting requirements.  For example, a figure first needs to be
    rendered clearly and accurately onscreen; then, when exported into
    vector graph formats in order to be included in publications, the
    lines need to be visible, the font sizes of label and tickmarks
    should match the caption font size, etc; finally, important
    figures also go into talks, where larger fonts and wider line are
    usually preferred, in addition, slides come with different
    theme---dark and light backgrounds---which may require changing
    the color theme in a figure.

    EHTplot is designed to make creating multi-style-multi-destination
    easy.  The whole library is theme based.  After creating a figure,
    its presentation and rendering depends on the targeted output.
    For example, the same figure appearing in a jupyter notebook has
    smaller fonts than its png version, which is often used in slides.

    set_theme() is used to set the default themes for these different
    situations.

    Args:
        screen: the theme(s) used for rendering on screen
        vector: the theme(s) used for exporting to vector graphics formats
        raster: the theme(s) used for exporting to raster (bitmap) formats

    """
    pass
