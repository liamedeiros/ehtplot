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

import matplotlib.pyplot as plt
from .panel import *

class Figure:
    """The "head" class for hierarchically organizing panels in ehtplot

    The Figure class is the "outermost container" in ehtplot.  An
    ehtplot Figure can be rendered on screen and exported to files.
    Logically, an ehtplot Figure always contains a single root ehtplot
    Panel instance, although the root Panel can have multiple
    subpanels in it.  See the documentation of the ehtplot Panel class
    for details.

    """

    def __init__(self, *args, **kwargs):
        """Figure initializer

        The Figure class can be initialized in two different ways.
        The first way takes a single argument with type Panel, or a
        single list of one Panel:

            fig = Figure( p0 )
            fig = Figure([p0])

        this makes `pnl` the builtin panel of `fig`.  The second way
        takes arbitrary arguments and keywards,

            fig = Figure( p0, p1, ...,  arg0, ..., kw0=..., ...)
            fig = Figure([p0, p1, ...], arg0, ..., kw0=..., ...)

        As long as the number of panel is not one, Figure will
        automatically create a Panel class with the arguments and
        keywords.  That this, the above statements are equvilient to

            fig = Figure(Panel( p0, p1, ...,  arg0, ..., kw0=..., ...))
            fig = Figure(Panel([p0, p1, ...], arg0, ..., kw0=..., ...))

        If there is only one panel and none zero additional arguments
        and keywords, the initializer will raise a type error.

        """
        plots, args = splitargs(args)

        if len(plots) == 1 and isinstance(plots[0], Panel):
            if not args and not kwargs:
                self.panel = plots[0]
            else:
                raise TypeError("no argument or keyword is allowed when "+
                                "passing a single ehtplot.Panel argument")
        else:
            self.panel = Panel(*(tuple(plots)+args), **kwargs)

    def __call__(self, *args, **kwargs):
        """Figure realizer

        The Figure class only keeps track of a root panel.  It does
        not contain a actual matplotlib Figure instance.  Whenever a
        drawing needs to be made, Figure creates a new matplotlib
        Figure in order to render the figure.

        """
        fig = plt.figure()
        ax  = fig.add_axes([0, 0, 1, 1])
        with plt.style.context(kwargs.pop('style', 'ehtplot')):
            self.panel(ax, *args, **kwargs)
        return fig

    def show(self, *args, **kwargs):
        self(*args, **kwargs).show()

    def draw(self, *args, **kwargs):
        self(*args, **kwargs).canvas.draw_idle()

    def save(self, file, *args, **kwargs):
        self(*args, **kwargs).savefig(file)
