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

from .plot    import Plot
from .helpers import ensure_list, split_dict, getbce, broadcast

class Panel:
    """The "node" class for hierarchically organizing subplots in ehtplot

    The Panel class is the "organization class" that allows ehtplot to
    hierarchically organize subplots and manage subplot properties.
    In each ehtplot Figure, there is always one root Panel instance.
    The root Panel can directly contain a single matplotlib axes or a
    set of subpanels.

    Attributes:
        _prop_keys (list of strings): List of graphics keywords used
            by Panel to create a panel.

    """

    _prop_keys = ['inrow', 'title']

    @classmethod
    def split_args(cls, args):
        l, c = [], 0
        for a in args:
            a = ensure_list(a, lambda p: isinstance(p, Panel) or
                                         Plot.isplotable(p))
            if a:
                l += a
            else:
                break
            c += 1
        return args[c:], l

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
        # Smart argument transform
        args,   plots            = self.split_args(args)
        kwargs, kwplots, kwprops = split_dict(kwargs, Plot.plot_keys,
                                                      self._prop_keys)
        # The actual constructor
        self.plots   = []
        self.kwprops = {'inrow': True}
        self.kwprops.update(kwprops)

        # Add and create Panels and Plots
        allargses = broadcast(args, kwargs)
        n         = len(allargses)
        Make      = Plot if n == 1 else Panel

        for p in plots:
            if isinstance(p, (Panel, Plot)):
                self.plots += [p]
                continue # done for this `p`
            for args, kwargs in allargses:
                self.plots += [Make(p, *args, **kwargs)]

        for p, d in kwplots.items():
            for i, (args, kwargs) in enumerate(allargses):
                self.plots += [Make(p, getbce(d, i), *args, **kwargs)]

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
        w = pos.x1 - pos.x0
        h = pos.y1 - pos.y0

        if n_plots == 0:
            ax.axis('off')
        if n_panels != 0:
            if self.kwprops['inrow']:
                w /= n_panels
            else:
                h /= n_panels

        for i, p in enumerate(self.plots):
            if isinstance(p, Plot):
                p(ax, *args, **kwargs)
                # Steal title from matplotlib Axes and put it in ehtplot Panel
                title = ax.get_title()
                if title is not None:
                    self.kwprops['title'] = title
                    ax.set_title(None)
            elif isinstance(p, Panel):
                if self.kwprops['inrow']:
                    subax = fig.add_axes([pos.x0+i*w, pos.y0, w, h])
                else:
                    subax = fig.add_axes([pos.x0, pos.y0+i*h, w, h])
                if i == 0:
                    ax0 = subax
                p(subax, *args, **kwargs)

        # This panel is left-most
        if pos.x0 < w:
            pass
        else:
            ax0.set_yticklabels([])
            ax0.yaxis.label.set_visible(False)

        # This panel is right-most
        if 1.0 - pos.x1 < w:
            pass

        # This panel is at bottom
        if pos.y0 < h:
            pass
        else:
            ax0.set_xticklabels([])
            ax0.xaxis.label.set_visible(False)

        # This panel is at top
        if 1.0 - pos.y1 < h:
            pass

        # Take care of panel title
        if 'title' in self.kwprops:
            if len(self.plots) <= 1 or not self.kwprops['inrow']:
                if 1.0 - pos.y1 < h: # top
                    ax0.set_title(self.kwprops['title'])
                else:
                    pass # do nothing
            else:
                ax0.set_ylabel(self.kwprops['title'])
