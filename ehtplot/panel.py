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

from .plot import plot

try:
    basestring
except NameError:
    basestring = str # so that we can always test strings as in python2

def arePanels(l):
    return isinstance(l, list) and all(isinstance(x, Panel) for x in l)

def pickPanels(args):
    if args and arePanels(args[0]):
        return args[0], args[1:]
    else:
        c = 0
        for a in args:
            if isinstance(a, Panel):
                c += 1
            else:
                break
        return list(args[:c]), args[c:]

class Panel:
    """The "node" class for hierarchically organizing subplots in ehtplot

    The Panel class is the "organization class" that allows ehtplot to
    hierarchically organize subplots and manage subplot properties.
    In each ehtplot Figure, there is always one root Panel instance.
    The root Panel can directly contain a single matplotlib axes or a
    set of subpanels.

    """

    types = ['image']

    def __init__(self, *args, **kwargs):
        """Panel initializer

        The Panel class can be initialized with both subpanels and
        plots.  To create subpanels, pass multiple arguments with type
        Panel or a list of Panels:

            pnl = Panel( p1, p2, ...,  arg1, arg2, ..., kw1=..., kw2=..., ...)
            pnl = Panel([p1, p2, ...], arg1, arg2, ..., kw1=..., kw2=..., ...)

        this makes `p1`, `p2`, etc the subpanel of `pnl`.  To create
        plots, one can pass the data with proper keywords, e.g.,

            pnl = Panel(image=img_array)

        """
        panels, args = pickPanels(args)
        self.inrow = kwargs.pop('inrow', True)

        self.plots     = []
        self.subpanels = panels

        for type in self.types:
            if type in kwargs:
                self.stage('plot_'+type, kwargs.pop(type), *args, **kwargs)

    def __call__(self, ax):
        if not self.plots:
            ax.axis('off')
        for plot in self.plots:
            plot(ax)

        if not self.subpanels:
            return
        fig = ax.figure
        pos = ax.get_position()
        if self.inrow:
            h =  pos.y1 - pos.y0
            w = (pos.x1 - pos.x0) / len(self.subpanels)
            for i, panel in enumerate(self.subpanels):
                panel(fig.add_axes([pos.x0+i*w, pos.y0, w, h]))
        else:
            h = (pos.y1 - pos.y0) / len(self.subpanels)
            w =  pos.x1 - pos.x0
            for i, panel in enumerate(self.subpanels):
                panel(fig.add_axes([pos.x0, pos.y0+i*h, w, h]))

    def __getattr__(self, attr):
        return lambda *args, **kwargs: self.stage(attr, *args, **kwargs)

    def __iter__(self):
        return iter(self.subpanels)

    def stage(self, type, *args, **kwargs):
        if isinstance(type, basestring):
            type = plot(type)
        if not callable(type):
            raise TypeError('type should be a callable')
        self.plots += [lambda ax: type(ax, *args, **kwargs)]
