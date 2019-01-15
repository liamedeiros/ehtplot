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

import numpy as np

from ehtplot.visual  import Visual
from ehtplot.helpers import split_dict, merge_dict
from ehtplot.layouts import divide, newaxes, getaxes


class Panel(object):
    """The "node" class for hierarchically organizing visuals in ehtplot

    The Panel class is the "container" that allows ehtplot to
    hierarchically organize subpanels and subvisuals, and to manage
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
        if isinstance(p, list):
            return all(map(cls.ispanelable, p)) # Check elements with recursion

        # Numpy wants to do everything pointwisely so we take it out
        # as a special case---numpy arrays are not panelable.
        if isinstance(p, np.ndarray):
            return False
        else:
            return isinstance(p, cls) or Visual.isvisualable(p)


    def __init__(self, panelable, **kwargs):
        """Panel initializer

        The Panel class is the "node class" that allows ehtplot to
        hierarchically organize subpanels and subvisuals, and to
        manage their properties.

        Args:
            panelable (list): A list that contains subpanels and/or
                subvisuals.
            **kwargs (dict): Arbitrary keyworded arguments that are
                passed to the subaxes constructor when realizing an
                instance of Panel.

        Attributes:
            panels (list): A list of subpanels, subvisuals, or list of
                them generated from the `args` argument.
            kwprops (dict): The default keywords used in creating
                subaxeses when realizing an instance of Panel.

        """
        self.panels  = panelable
        self.kwprops = merge_dict(self._default_kwprops, kwargs)


    def update(self, **kwargs):
        """Update internal properties"""
        self.kwprops.update(kwargs)
        return self


    def __call__(self, ax, **kwargs):
        """Panel realizer

        Realize a panel to a generator of matplotlib subaxeses by
        combining the saved and new arguments.  It accepts the same
        keyworded arguments as Visual.__init__().  Therefore, its
        argument list matches Visual.__init__() with `panelable`
        replaced by `ax`.

        Args:
            ax (matplotlib.axis.Axes): A matplotlib Axes for Panel's
                subaxeses to realize on.
            **kwargs (dict): Arbitrary Panel-specific keyworded
                arguments that are used to construct the subaxeses.

        """
        kwprops = merge_dict(self.kwprops, kwargs)

        box = divide(ax.get_position(),
                     list(map(type, self.panels)).count(Panel),
                     inrow=kwprops['inrow'])

        for p in self.panels:
            if isinstance(p, Panel):
                subax = newaxes(ax.figure, next(box))
                yield subax
            else:
                ax.axis('on')
                yield ax


    def draw(self, ax, *args, **kwargs):
        """Panel drawer/renderer

        Draw or render a Panel by combining the saved and new
        arguments.  Its argument list is designed to match
        Visual.draw() so that a Panel and Visual draw in the same way.
        This duck typing allows Panel to draw all its subpanels and
        subvisuals recusively.  Saved and new panel properties are
        combined to create subaxeses.  The passed `args` and
        non-Panel-specific keyworded arguments are passed recusively
        to the subpanels and eventially to some ehtplot Visuals.

        Args:
            ax (matplotlib.axis.Axes): A matplotlib Axes for Panel to
                draw/render on.
            *args (tuple): Variable length argument list that is
                eventually passed to some ehtplot Visuals.
            **kwargs (dict): Arbitrary keyworded arguments that are
                split into Panel-specific and non-Panel-specific
                keyworded arguments.  The Panel-specific ones are used
                to construct the subaxeses, while others are
                eventually passed to some ehtplot Visuals.

        """
        kwargs, kwprops = split_dict(kwargs, self._prop_keys)
        kwprops = merge_dict(self.kwprops, kwprops)
        return [p.draw(a, *args, **kwargs)
                for p, a in zip(self.panels, self(ax, **kwprops))]
