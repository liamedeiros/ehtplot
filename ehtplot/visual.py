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

from os.path import basename, dirname, join, splitext
from glob import glob

try:
    import importlib.util as iu
except ImportError:
    import importlib as il

import numpy as np

from ehtplot.helpers import merge_dict


class Visual(object):
    """The Visual class has similar behavior compare to a function closure

    The Visual class saves the visualizing function, arguments, and
    keyworded arguments together so that a "visual" can be redrawn.
    Its behavior is very similar to a function closure.  The only
    difference is that the arguments and keyworded arguments can be
    overridden/modified at "draw time".

    Attributes:
        paths (list of strings): A list of paths used by Visual to
            look up visualizing
        visuals (list of strings): A list of valid names that can be
            loaded into visualizing functions.

    """
    paths   = [join(dirname(__file__), "visuals")]
    visuals = [splitext(basename(f))[0]
               for p in paths for f in glob(join(p, "*.py"))]

    @classmethod
    def _load_from_file(cls, visual, prefix="visualize_", ext=".py"):
        """Load a visualizing function from directories in `Visual.paths`."""
        func_name = prefix+visual
        for path in cls.paths:
            file_name = join(path, visual+ext)
            try:
                spec   = iu.spec_from_file_location(func_name, file_name)
                module = iu.module_from_spec(spec)
            except:
                continue # try next path
            spec.loader.exec_module(module)
            return module.__dict__[func_name]
        raise ImportError("failed to load \"{}\"".format(visual))


    @classmethod
    def _load_from_pkg(cls, visual, prefix="visualize_", pkg="visuals"):
        """Load a visualizing function from `ehtplot.visuals`"""
        func_name = prefix+visual
        parent    = ".".join(__name__.split(".")[:-1])
        pkg_name  = ".".join([parent, pkg, visual])
        return il.import_module(pkg_name).__dict__[func_name]


    @classmethod
    def _load(cls, visual):
        """Load a visualizing function."""
        try:
            iu # exists if we are using python3
        except NameError:
            return cls._load_from_pkg(visual)  # python2 fallback
        else:
            return cls._load_from_file(visual) # python3


    @classmethod
    def _prepare(cls, p):
        """Convert a generic visualable to a callable."""
        return p if callable(p) else cls._load(p)


    @classmethod
    def isvisualable(cls, p):
        """Check if the argument can be used as a Visual or Visuals"""
        # Numpy wants to do everything pointwisely so we take it out
        # as a special case---numpy arrays are not visualable.
        if isinstance(p, np.ndarray):
            return False
        else:
            return callable(p) or (p in cls.visuals)


    def __init__(self, visualable, *args, **kwargs):
        """Visual initializer

        The Visual class saves the visualizing function, args, and
        kwargs so that a visual can be redrawn multiple times by
        calling the class as a function.

        Args:
            visualable (Visual, callable, or visual key): A variable
                that describes the visualizing functions.  It can be a
                Visual, a callable, or a visual key, i.e., anything
                that returns a True from isvisualable().  Note that
                "visualable" is not a typo here: it is not something
                that's visualizable.  Instead, it is something that
                can be turned into a visual.
            *args (tuple): Variable length argument list that is
                passed to the visualizing function when realizing an
                instance of Visual.
            **kwargs (dict): Arbitrary keyworded arguments that are
                passed to the visualizing function when realizing an
                instance of Visual.

        Attributes:
            visual (callable): The visualizing function generated from
                the `visualable` argument.
            props (tuple): The default arguments when realizing an
                instance of Visual.
            kwprops (dict): The default keywords when realizing an
                instance of Visual.

        """
        self.visual  = self._prepare(visualable)
        self.props   = args
        self.kwprops = kwargs


    def update(self, *args, **kwargs):
        """Update internal properties"""
        self.props   = args if args else self.props
        self.kwprops.update(kwargs)
        return self


    def __call__(self, ax, *args, **kwargs):
        """Visual realizer

        Realize a visual by combining the saved and new arguments.
        The realization uses the new `args` list if it is provided,
        and uses the saved attribute otherwise.  Saved and new
        `kwargs` are always combined.

        Args:
            ax (matplotlib.axis.Axes): A matplotlib Axes for Visual to
                draw/render/realize on.
            *args (tuple): Variable length argument list that
                overrides the saved on when realizing an instance of
                Visual.
            **kwargs (dict): Arbitrary keyworded arguments that are
                passed to the visualizing function the when realizing
                an instance of Visual.

        """
        props   = args if args else self.props
        kwprops = merge_dict(self.kwprops, kwargs)
        return self.visual(ax, *props, **kwprops)


    def draw(self, ax, *args, **kwargs):
        """Visual drawer/renderer

        Draw or render a visual by combining the saved and new
        arguments.  This function is identical to `Visual.__call__()`.
        It matches Panel.draw() in order to do recursion with duck
        typing.

        Args:
            ax (matplotlib.axis.Axes): A matplotlib Axes for Visual to
                draw/render/realize on.
            *args (tuple): Variable length argument list that
                overrides the saved on when realizing an instance of
                Visual.
            **kwargs (dict): Arbitrary keyworded arguments that are
                passed to the visualizing function the when realizing
                an instance of Visual.

        """
        return self(ax, *args, **kwargs)
