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

from os.path import basename, dirname, join, splitext
from glob import glob
import importlib.util as iu

import numpy as np


class Plot:
    """The Plot class has similar behavior compare to a function closure

    The Plot class saves the plotting function, arguments, and
    keyworded arguments together so that a plot can be redrawn.  Its
    behavior is very similar to a function closure.  The only
    difference is that the keyworded arguments can be modified at
    "plot time".

    Attributes:
        paths (list of strings): A list of paths used by Plot to look
            up plotting functions.
        plot_keys (list of strings): A list of valid names that can be
            loaded into plotting functions.

    """
    paths     = [join(dirname(__file__), "plots")]
    plot_keys = [splitext(basename(f))[0]
                 for p in paths for f in glob(join(p, "*.py"))]

    @classmethod
    def _load(cls, plotable, prefix="plot_", ext=".py"):
        """Load a plotting function from directories listed in Plot.paths."""
        func_name = prefix+plotable
        for path in cls.paths:
            file_name = join(path, plotable+ext)
            try:
                spec   = iu.spec_from_file_location(func_name, file_name)
                module = iu.module_from_spec(spec)
            except:
                continue # try next path
            spec.loader.exec_module(module)
            return module.__dict__[func_name]
        raise ImportError("failed to load \"{}\"".format(plotable))


    @classmethod
    def _prepare(cls, p):
        """Convert a generic plotable to a callable."""
        return p if callable(p) else cls._load(p)


    @classmethod
    def isplotable(cls, p):
        """Check if the argument can be used as a Plot or Plots"""
        # Numpy wants to do everything pointwisely so we take it out
        # as a special case---numpy arrays are not plotable.
        if isinstance(p, np.ndarray):
            return False
        else:
            return callable(p) or (p in cls.plot_keys)


    def __init__(self, plotable, *args, **kwargs):
        """Plot initializer

        The Panel class saves the plotting function, args, and kwargs
        so that a plot can be redrawn multiple times by calling the
        class as a function.

        Args:
            plotable (Plot, callable, or plot key): A variable that
                describes the plotting functions.  It can be a Plot, a
                callable, or a plot key, i.e., anything that returns a
                True from isplotable().
            *args (tuple): Variable length argument list that is
                passed to the plotting function when realizing an
                instance of Plot.
            **kwargs (dict): Arbitrary keyworded arguments that are
                passed to the plotting function when realizing an
                instance of Plot.

        Attributes:
            plot (callable): The plotting function generated from the
                `plotable` argument.
            props (tuple): The default arguments when realizing an
                instance of Plot.
            kwprops (dict): The default keywords when realizing an
                instance of Plot.

        """
        self.plot    = self._prepare(plotable)
        self.props   = args
        self.kwprops = kwargs


    def __call__(self, ax, *args, **kwargs):
        """Plot realizer

        Realize a plot by combining the saved and new arguments.  The
        realization uses the new `args` list if it is provided, and
        uses the saved attribute otherwise.  Saved and new `kwargs`
        are always combined.

        Args:
            ax (matplotlib.axis.Axes): A matplotlib Axes for Plot to
                draw/render/realize on.
            *args (tuple): Variable length argument list that
                overrides the saved on when realizing an instance of
                Plot.
            **kwargs (dict): Arbitrary keyworded arguments that are
                passed to the plotting function the when realizing an
                instance of Plot.

        """
        props   = args if args else self.props
        kwprops = {**self.kwprops, **kwargs}
        return self.plot(ax, *props, **kwprops)

    def draw(self, ax, *args, **kwargs):
        """Plot drawer/renderer

        Draw or render a plot by combining the saved and new
        arguments.  This function is identical to `Plot.__call__()`.
        It matches Panel.draw() in order to do recursion with duck
        typing.

        Args:
            ax (matplotlib.axis.Axes): A matplotlib Axes for Plot to
                draw/render/realize on.
            *args (tuple): Variable length argument list that
                overrides the saved on when realizing an instance of
                Plot.
            **kwargs (dict): Arbitrary keyworded arguments that are
                passed to the plotting function the when realizing an
                instance of Plot.

        """
        return self(ax, *args, **kwargs)
