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
from .helpers import split_dict
from .layouts import getaxes, newaxes


class Panel:
    """The "node" class for hierarchically organizing plots in ehtplot

    The Panel class is the "container" that allows ehtplot to
    hierarchically organize subpanels and subplots, and to manage
    their properties.

    Attributes:
        _default_kwprops (dict): Default keyworded properties used by
            Panel to create a panel.
        _prop_keys (dict_keys): Keys of _default_kwprops.

    """
    _default_kwprops = {'inrow': True, 'title': None}
    _prop_keys = _default_kwprops.keys()


    @classmethod
    def ispanelable(cls, p):
        """Check if the argument can be used in a Panel"""
        # Numpy wants to do everything pointwisely so we take it out
        # as a special case---numpy arrays are not panelable.
        if isinstance(p, np.ndarray):
            return False
        else:
            return (isinstance(p, list) and
                    all(map(lambda q: isinstance(q, (cls, Plot)), p)))


    def __init__(self, panelable, **kwargs):
        """Panel initializer

        The Panel class is the "node class" that allows ehtplot to
        hierarchically organize subpanels and subplots, and to manage
        their properties.

        Args:
            panelable (list): A list that contains subpanels and/or
                subplots.
            **kwargs (dict): Arbitrary keyworded arguments that are
                passed to the subaxes constructor when realizing an
                instance of Panel.

        Attributes:
            panels (list): A list of subpanels, subplots, or list of
                them generated from the `args` argument.
            kwprops (dict): The default keywords used in creating
                subaxeses when realizing an instance of Panel.

        """
        self.panels  = panelable
        self.kwprops = {**self._default_kwprops, **kwargs}


    def __call__(self, ax, **kwargs):
        """Panel realizer

        Realize a panel to a generator of matplotlib subaxeses by
        combining the saved and new arguments.  It accepts the same
        keyworded arguments as Plot.__init__().  Therefore, its
        argument list matches Plot.__init__() with `panelable`
        replaced by `ax`.

        Args:
            ax (matplotlib.axis.Axes): A matplotlib Axes for Panel's
                subaxeses to realize on.
            **kwargs (dict): Arbitrary Panel-specific keyworded
                arguments that are used to construct the subaxeses.

        """
        kwprops = {**self.kwprops, **kwargs}

        fig = ax.figure

        n_panels = list(map(type, self.panels)).count(Panel)
        if n_panels:
            pos = ax.get_position()
            w   = pos.x1 - pos.x0
            h   = pos.y1 - pos.y0
            if kwprops['inrow']:
                w /= n_panels
            else:
                h /= n_panels

        i = 0
        for p in self.panels:
            if isinstance(p, Panel):
                if kwprops['inrow']:
                    yield newaxes(fig, [pos.x0+i*w, pos.y0, w, h])
                else:
                    yield newaxes(fig, [pos.x0, pos.y0+i*h, w, h])
                i += 1
            else:
                ax.axis('on')
                yield ax


    def draw(self, ax, *args, **kwargs):
        """Panel drawer/renderer

        Draw or render a Panel by combining the saved and new
        arguments.  Its argument list is designed to match Plot.draw()
        so that a Panel and Plot draw in the same way.  This duck
        typing allows Panel to draw all its subpanels and subplots
        recusively.  Saved and new panel properties are combined to
        create subaxeses.  The passed `args` and non-Panel-specific
        keyworded arguments are passed recusively to the subpanels and
        eventially to some ehtplot Plots.

        Args:
            ax (matplotlib.axis.Axes): A matplotlib Axes for Panel to
                draw/render on.
            *args (tuple): Variable length argument list that is
                eventually passed to some ehtplot Plots.
            **kwargs (dict): Arbitrary keyworded arguments that are
                split into Panel-specific and non-Panel-specific
                keyworded arguments.  The Panel-specific ones are used
                to construct the subaxeses, while others are
                eventually passed to some ehtplot Plots.

        """
        kwargs, kwprops = split_dict(kwargs, self._prop_keys)
        kwprops = {**self.kwprops, **kwprops}
        return [p.draw(a, *args, **kwargs)
                for p, a in zip(self.panels, self(ax, **kwprops))]
