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

from .plot    import Plot
from .helpers import split_dict, getaxes


class Panel:
    """The "node" class for hierarchically organizing subpanels in ehtplot

    The Panel class is the "node class" that allows ehtplot to
    hierarchically organize subpanels and subplots, and to manage
    their properties.

    Attributes:
        _prop_keys (list of strings): List of graphics keywords used
            by Panel to create a panel.

    """
    _prop_keys = ['inrow', 'title']


    @classmethod
    def _prepare(cls, p):
        """Convert a generic panelable to a list."""
        return p if isinstance(p, list) else [p]


    @classmethod
    def ispanelable(cls, p):
        """Check if the argument can be used as a Panel or Panels"""
        # Recur to self if p is a list
        if isinstance(p, list):
            return all(map(cls.ispanelable, p))
        # Numpy wants to do everything pointwisely so we take it out
        # as a special case---numpy arrays are not panelable.
        if isinstance(p, np.ndarray):
            return False
        else:
            return isinstance(p, (Panel, Plot))


    def __init__(self, panelable, **kwargs):
        """Panel initializer

        The Panel class is the "node class" that allows ehtplot to
        hierarchically organize subpanels and subplots, and to manage
        their properties.

        Args:
            *args (tuple): Variable length argument list that contains
                subpanels, subplots, or list of them, i.e., anything
                that returns a True from ispanelable().
            **kwargs (dict): Arbitrary keyworded arguments that are
                passed to the subaxes constructor when realizing an
                instance of Panel.

        Attributes:
            panels (list): A list of subpanels, subplots, or list of
                them generated from the `args` argument.
            kwprops (dict): The default keywords used in creating
                subaxeses when realizing an instance of Panel.

        """
        self.panels  = self._prepare(panelable)
        self.kwprops = {'inrow': True, **kwargs}


    def __call__(self, ax, *args, **kwargs):
        """Panel drawer/renderer/realizer

        Realize, i.e., draw or render, a panel by combining the saved
        and new arguments.  Its argument list is designed to match
        Plot.__call__() so that a Panel and Plot called in the same
        way.  This duck typing allows Panel to realize all its
        subpanels and subplots recusively.  Saved and new panel
        properties are combined to create subaxeses.  The passed
        `args` and non-panel-specific keyworded arguments are passed
        recusively to the subpanels and eventially to some ehtplot
        Plots.

        Args:
            ax (matplotlib.axis.Axes): A matplotlib Axes for Panel to
                draw/render/realize on.
            *args (tuple): Variable length argument list that is
                eventually passed to some ehtplot Plots.
            **kwargs (dict): Arbitrary keyworded arguments that are
                split into panel-specific and non-panel-specific
                keyworded arguments.  The panel-specific ones are used
                to construct the subaxeses, while others are
                eventually passed to some ehtplot Plots.

        """
        kwargs, kwprops = split_dict(kwargs, self._prop_keys)
        kwprops = {**self.kwprops, **kwprops}

        n_plots, n_panels = 0, 0
        for p in self.panels:
            if isinstance(p, Panel):
                n_panels += 1
            else:
                n_plots  += 1

        fig = ax.figure
        pos = ax.get_position()
        axF = ax
        axL = ax

        w = pos.x1 - pos.x0
        h = pos.y1 - pos.y0

        if n_plots == 0:
            ax.axis('off')
        if n_panels != 0:
            if self.kwprops['inrow']:
                w /= n_panels
            else:
                h /= n_panels

        out = []
        i   = 0
        for p in self.panels:
            if isinstance(p, Panel):
                if self.kwprops['inrow']:
                    subax = fig.add_axes([pos.x0+i*w, pos.y0, w, h])
                else:
                    subax = fig.add_axes([pos.x0, pos.y0+i*h, w, h])
                if i == 0:
                    axF = subax
                if i == n_plots-1:
                    axL = subax
                out += [p(subax, *args, **kwargs)]
                i   += 1
            else:
                out += [p(ax, *args, **kwargs)]
                # Steal title from matplotlib Axes and put it in ehtplot Panel
                title = ax.get_title()
                if title is not None:
                    self.kwprops['title'] = title
                    ax.set_title(None)

        axes = getaxes(axF)

        # This panel is left-most
        if pos.x0 < w:
            pass
        else:
            axF.set_yticklabels([])
            axF.yaxis.label.set_visible(False)

        # This panel is right-most
        if 1.0 - pos.x1 < w:
            pass

        # This panel is at bottom
        if pos.y0 < h:
            pass
        else:
            axF.set_xticklabels([])
            axF.xaxis.label.set_visible(False)

        # This panel is at top
        if 1.0 - pos.y1 < h:
            pass

        # Take care of panel title
        if 'title' in self.kwprops:
            if len(self.panels) <= 1 or not self.kwprops['inrow']:
                if 1.0 - pos.y1 < h: # top
                    axF.set_title(self.kwprops['title'])
                else:
                    pass # do nothing
            else:
                axF.set_ylabel(self.kwprops['title'])

        return out
