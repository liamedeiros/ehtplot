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

from __future__ import absolute_import
from __future__ import with_statement

from contextlib import contextmanager

import matplotlib        as mpl
import matplotlib.pyplot as plt

from ehtplot.panel   import Panel
from ehtplot.helpers import ensure_list, split_dict, merge_dict
from ehtplot.layouts import newaxes


class Figure(object):
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
    _default_kwprops = {'style': 'ehtplot'}
    _prop_keys = (list(_default_kwprops.keys()) +
                  ['figsize', 'dpi', 'facecolor', 'edgecolor', 'frameon'])

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
        self.kwprops = merge_dict(self._default_kwprops, kwargs)


    def update(self, **kwargs):
        """Update internal properties"""
        self.kwprops.update(kwargs)
        return self


    @contextmanager
    def __call__(self, **kwargs):
        """Figure realizer

        The Figure class only keeps track of a root panel.  It does
        not contain an actual matplotlib Figure instance.  Whenever a
        figure needs to be created, Figure creates a new matplotlib
        Figure in order to drew/rendered/realized the figure.

        Args:

            **kwargs (dict): Arbitrary Figure-specific keyworded
                arguments that are used to construct the matplotlib
                Figure.

        """
        kwprops = merge_dict(self.kwprops, kwargs)
        style   = kwprops.pop('style')

        with mpl.rc_context():
            mpl.rcdefaults()
            plt.style.use(style)

            imode = mpl.is_interactive()
            if imode:
                plt.ioff()

            fig = plt.figure(**kwprops)
            ax  = newaxes(fig)
            yield fig, ax

            if imode:
                plt.ion()


    def draw(self, *args, **kwargs):
        """Figure drawer/renderer

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
        kwprops = merge_dict(self.kwprops, kwprops)

        with self(**kwprops) as (fig, ax):
            self.panel.draw(ax, *args, **kwargs)

        return fig


    def show(self, *args, **kwargs):
        """Show the Figure"""
        fig = self.draw(*args, **kwargs)
        fig.show()


    def save(self, files, *args, **kwargs):
        """Save the Figure"""
        fig = self.draw(*args, **kwargs)
        for file in ensure_list(files):
            fig.savefig(file)
