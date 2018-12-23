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

    """

    _propkeys = ['figsize', 'dpi', 'facecolor', 'edgecolor', 'frameon']

    def __init__(self, *args, **kwargs):
        """Figure initializer

        The Figure class can be initialized in two different ways.
        The first way takes a single argument with type Panel, or a
        single list of one Panel:

            fig = Figure( p0 )
            fig = Figure([p0])

        this makes `p0` the built-in root panel of `fig`.  The second
        way takes arbitrary arguments and keywards,

            fig = Figure( p0, p1, ...,  arg0, ..., kw0=..., ...)
            fig = Figure([p0, p1, ...], arg0, ..., kw0=..., ...)

        As long as the number of panel is not one, Figure will
        automatically create a Panel class with the arguments and
        keywords.  That this, the above statements are equvilient to

            fig = Figure(Panel( p0, p1, ...,  arg0, ..., kw0=..., ...))
            fig = Figure(Panel([p0, p1, ...], arg0, ..., kw0=..., ...))

        If there is only one panel and none zero additional arguments
        and keywords, the initializer will raise a type error.

        Args:
            *args (tuple): Variable length argument list that is used
                to determine what way a Figure is initialized.  If it
                is a ehtplot.Panel or a list containing a single
                ehtplot.Panel, then *args becomes the root panel of
                the instantized Figure (if such a case, not kwargs is
                allowed).  Otherwise, it is a variable length argument
                list passed to create the root panel.
            **kwargs (dict): If Figure is initialized in the second
                way, then this is an arbitrary keyword arguments
                passed to create the root panel.

        Attributes:
            panel (ehtplot.Panel): The root panel.
            kwprops (dict): The default keywords when creating a figure.

        """
        self.props = {}

        args,   plots   = Panel.split_args(args)
        kwargs, kwprops = split_dict(kwargs, self._propkeys)

        self.props.update(kwprops)

        if len(plots) == 1 and isinstance(plots[0], Panel):
            if not args and not kwargs:
                self.panel = plots[0]
            else:
                raise ValueError("no argument or keyword is allowed when "+
                                 "passing a single ehtplot.Panel argument")
        else:
            self.panel = Panel(*(tuple(plots)+args), **kwargs)

    def __call__(self, *args, **kwargs):
        """Figure realizer

        The Figure class only keeps track of a root panel.  It does
        not contain an actual matplotlib Figure instance.  Whenever a
        drawing needs to be made, Figure creates a new matplotlib
        Figure in order to render the figure.

        Args:
            *args (tuple): Variable length argument list that is
                passed to the root panel when realizing an instance of
                Plot.
            **kwargs (dict): Arbitrary keyword arguments that are
                passed to the root panel the when realizing an
                instance of Plot.

        """
        kwargs, kwprops = split_dict(kwargs, self._propkeys)
        fig = plt.figure(**{**self.props, **kwprops})
        ax  = fig.add_axes([0, 0, 1, 1])
        with plt.style.context(kwargs.pop('style', 'ehtplot')):
            self.panel(ax, *args, **kwargs)
        return fig

    def show(self, *args, **kwargs):
        """Show the Figure"""
        self(*args, **kwargs).show()

    def draw(self, *args, **kwargs):
        """Draw the Figure"""
        self(*args, **kwargs).canvas.draw_idle()

    def save(self, files, *args, **kwargs):
        """Save the Figure"""
        for file in ensure_list(files):
            self(*args, **kwargs).savefig(file)
