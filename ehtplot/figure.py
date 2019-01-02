# Copyright (C) 2017--2019 Lia Medeiros & Chi-kwan Chan
# Copyright (C) 2017--2019 Steward Observatory
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

import matplotlib.pyplot as plt

from .panel   import Panel
from .helpers import ensure_list, split_dict


class Figure:
    """The "head" class for hierarchically organizing panels in ehtplot

    The Figure class is the "outermost container" in ehtplot.  An
    ehtplot Figure can be rendered on screen and exported to files.
    Logically, an ehtplot Figure always contains a single root ehtplot
    Panel instance, although the root Panel can have multiple
    subpanels in it.  See the documentation of the ehtplot Panel class
    for details.

    Attributes:
        _prop_keys (list of strings): List of graphics keywords used by
            Figure to create a figure.

    """
    _prop_keys = ['style',
                  'figsize', 'dpi', 'facecolor', 'edgecolor', 'frameon']


    def __init__(self, panel, **kwargs):
        """Figure initializer

        The Figure class takes a single argument with type Panel:

            fig = Figure(pnl, kw0=..., kw1=..., ...)

        this makes `pnl` the built-in root panel of `fig`.

        Args:
            panel (ehtplot.Panel): The root panel of the Figure.
            **kwargs (dict): If Figure is initialized in the second
                way, then this is an arbitrary keyworded arguments
                passed to create the root panel.

        Attributes:
            panel (ehtplot.Panel): The root panel of the Figure.
            kwprops (dict): The default keywords for creating a
                figure.

        """
        self.panel   = panel
        self.kwprops = {'style': 'ehtplot', **kwargs}


    def __call__(self, *args, **kwargs):
        """Figure drawer/renderer/realizer

        The Figure class only keeps track of a root panel.  It does
        not contain an actual matplotlib Figure instance.  Whenever a
        figure needs to be created, Figure creates a new matplotlib
        Figure in order to drew/rendered/realized the figure.

        Args:
            *args (tuple): Variable length argument list that is
                passed to the root panel.
            **kwargs (dict): Arbitrary keyworded arguments that are
                split into properties of the figure and the panel.

        """
        kwargs, kwprops = split_dict(kwargs, self._prop_keys)
        kwprops = {**self.kwprops, **kwprops}

        style = kwprops.pop('style')
        fig   = plt.figure(**kwprops)
        with plt.style.context(style):
            ax = fig.add_axes([0, 0, 1, 1])
            self.panel(ax, *args, **kwargs) # TODO: how to handle returned
                                            # variable from self.panel()
        return fig


    def show(self, *args, **kwargs):
        """Show the Figure"""
        self(*args, **kwargs).show()


    def draw(self, *args, **kwargs):
        """Draw the Figure"""
        self(*args, **kwargs).canvas.draw_idle()


    def save(self, files, *args, **kwargs):
        """Save the Figure"""
        fig = self(*args, **kwargs)
        for file in ensure_list(files):
            fig.savefig(file)
