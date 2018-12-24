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

import importlib.util as iu
from os.path import join, dirname

try:
    basestring
except NameError:
    basestring = str # so that we can always test strings as in python2

class Plot:
    """The Plot class has similar behavior compare to a function closure

    The Plot class saves the plotting function, arguments, and
    keywords together so that a plot can be redrawn.  Its behavior is
    very similar to a funciton closure.  The only difference is that
    the keyworded arguments can be modified at "plot time".

    Attributes:
        _prop_keys (list of strings): List of paths used by Plot to
            look up plotting functions.

    """

    paths = [join(dirname(__file__), "plots")]

    @classmethod
    def load_plot(cls, plot):
        """Load a plotting function from directories in Plot.paths."""
        func = "plot_"+plot
        for path in cls.paths:
            file = join(path, plot+".py")
            try:
                spec   = iu.spec_from_file_location(func, file)
                module = iu.module_from_spec(spec)
            except:
                continue
            spec.loader.exec_module(module)
            return module.__dict__[func]
        raise ImportError("failed to load \"{}\"".format(plot))

    @classmethod
    def ensure_callable(cls, plot):
        """Convert `plot` to callable when possible."""
        if isinstance(plot, basestring):
            return cls.load_plot(plot)
        elif callable(plot):
            return plot
        else:
            raise TypeError("`plot` must be a string or a callable")

    def __init__(self, plot, *args, **kwargs):
        """Plot initializer

        The Panel class saves the plotting function, args, and kwargs
        so that a plot can be redrawn multiple times by calling the
        class as a function.

        Args:
            plot (string or callable): Name of the plotting function
                or the plotting function itself.
            *args (tuple): Variable length argument list that is
                passed to the plotting function when realizing an
                instance of Plot.
            **kwargs (dict): Arbitrary keyword arguments that are
                passed to the plotting function when realizing an
                instance of Plot.

        Attributes:
            plot (callable): The plotting function
            props (tuple): The default arguments when realizing an
                instance of Plot.
            kwprops (dict): The default keywords when realizing an
                instance of Plot.

        """
        # Smart argument transform
        plot = self.ensure_callable(plot)

        # The actual constructor
        self.plot    = plot
        self.props   = args
        self.kwprops = kwargs

    def __call__(self, ax, *args, **kwargs):
        """Plot drawer/renderer/realizer

        Realize, i.e., draw or render, a plot by combining the saved
        and new arguments.  The realization uses the new `args` list
        if it is provided, and uses the saved attribute otherwise.
        Saved and new `kwargs` are always combined.

        Args:
            ax (matplotlib.axis.Axes): A matplotlib Axes for Plot to
                realize/draw on.
            *args (tuple): Variable length argument list that
                overrides the saved on when realizing an instance of
                Plot.
            **kwargs (dict): Arbitrary keyword arguments that are
                passed to the plotting function the when realizing an
                instance of Plot.

        """
        # Smart argument transform
        props   = args if args else self.props
        kwprops = {**self.kwprops, **kwargs}

        # The actual plot realization
        self.plot(ax, *props, *kwprops)
