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

    """

    paths = [join(dirname(__file__), "plots")]

    @staticmethod
    def load_plot(plot):
        func = "plot_"+plot
        for path in self.path:
            file = join(path, plot+".py")
            try:
                spec   = iu.spec_from_file_location(func, file)
                module = iu.module_from_spec(spec)
            except:
                continue
            spec.loader.exec_module(module)
            return module.__dict__[func]
        raise ImportError("failed to load \"{}\"".format(plot))

    @staticmethod
    def ensure_callable(plot):
        if isinstance(plot, basestring):
            return self.load_plot(plot)
        elif callable(plot):
            return plot
        else:
            raise TypeError("`plot` must be a string or a callable")

    def __init__(self, plot, *args, **kwargs):
        """Plot initializer

        The Panel class saves the plotter, args, and kwargs so that a
        plot can be redrawn multiple times by calling the class as a
        function.

        """
        self.plot   = self.ensure_callable(plot)
        self.args   = args
        self.kwargs = kwargs

    def __call__(self, ax, *args, **kwargs):
        """Plot realizer

        Realize a plot, i.e., redraw a plot, by combining the saved
        and new kwargs.  If new args is provided, then the realization
        uses the new args.

        """
        if args:
            self.plot(ax, *args,      **{**self.kwargs, **kwargs})
        else:
            self.plot(ax, *self.args, **{**self.kwargs, **kwargs})
