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

from .plot import *

try:
    basestring
except NameError:
    basestring = str # so that we can always test strings as in python2

_plots = ['image']
_props = ['inrow', 'title']

def loadable(a):
    return isinstance(a, basestring) and (a in _plots)

def validarg(a):
    return isinstance(a, (Panel, Plot)) or callable(a) or loadable(a)

def validlist(l):
    return isinstance(l, list) and all(validarg(a) for a in l)

def splitargs(args):
    l, c = [], 0
    for a in args:
        if validlist(a):
            l += a
        elif validarg(a):
            l += [a]
        else:
            break
        c += 1
    return l, args[c:]

def splitkwargs(kwargs):
    a, b, c = {}, {}, {}
    for k, v in kwargs.items():
        if k in _plots:
            a.update({k: v})
        elif k in _props:
            b.update({k: v})
        else:
            c.update({k: v})
    return a, b, c

class Panel:
    """The "node" class for hierarchically organizing subplots in ehtplot

    The Panel class is the "organization class" that allows ehtplot to
    hierarchically organize subplots and manage subplot properties.
    In each ehtplot Figure, there is always one root Panel instance.
    The root Panel can directly contain a single matplotlib axes or a
    set of subpanels.

    """

    def __init__(self, *args, **kwargs):
        """Panel initializer

        The Panel class can be initialized with both subpanels and
        plots.  To create subpanels, pass multiple arguments with type
        Panel or a list of Panels:

            pnl = Panel( p0, p1, ...,  arg0, ..., kw0=..., ...)
            pnl = Panel([p0, p1, ...], arg0, ..., kw0=..., ...)

        this makes `p0`, `p1`, etc the subpanel of `pnl`.  To create
        plots, one can pass the data with proper keywords, e.g.,

            pnl = Panel(image=img_array)

        """
        self.props = {'inrow': True}
        self.plots = []

        plots,            args   = splitargs(args)
        kwplots, kwprops, kwargs = splitkwargs(kwargs)

        self.props.update(kwprops)

        for p in plots:
            if isinstance(p, (Panel, Plot)):
                self.plots += [p]
            else:
                self.stage(p, *args, **kwargs)
        for k, v in kwplots.items():
            self.stage(k, v, *args, **kwargs)

    def __call__(self, ax, *args, **kwargs):
        """Panel realizer

        Realize (replot) all plots in the `self.plots[]` array and
        then recursively realize all panels in the `self.subpanels[]`
        array.

        """
        n_plots  = len([p for p in self.plots if isinstance(p, Plot)])
        n_panels = len([p for p in self.plots if isinstance(p, Panel)])

        fig = ax.figure
        pos = ax.get_position()
        ax0 = ax
        i = 0
        j = 0
        w = pos.x1 - pos.x0
        h = pos.y1 - pos.y0

        if n_plots == 0:
            ax.axis('off')
        if n_panels != 0:
            if self.props['inrow']:
                w /= n_panels
            else:
                h /= n_panels

        for p in self.plots:
            if isinstance(p, Plot):
                p(ax, *args, **kwargs)
                # Steal title from matplotlib Axes and put it in ehtplot Panel
                title = ax.get_title()
                if title is not None:
                    self.props['title'] = title
                    ax.set_title(None)
            elif isinstance(p, Panel):
                subax = fig.add_axes([pos.x0+i*w, pos.y0+j*h, w, h])
                p(subax, *args, **kwargs)
                if i == 0 and j == 0:
                    ax0 = subax
                if self.props['inrow']:
                    i += 1
                else:
                    j += 1

        if 'title' in self.props:
            if len(self.plots) <= 1 or not self.props['inrow']:
                if 1.0 - pos.y1 >= h:
                    pass # most likely *not* the top row; do nothing
                else:
                    ax0.set_title(self.props['title'])
            else:
                ax0.set_ylabel(self.props['title'])

    def __getattr__(self, attr):
        return lambda *args, **kwargs: self.stage(attr, *args, **kwargs)

    def __iter__(self):
        return iter(self.subpanels)

    def stage(self, plot, *args, **kwargs):
        self.plots += [Plot(plot, *args, **kwargs)]
