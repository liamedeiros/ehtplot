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
from os.path import dirname

def load(method):
    dir, name = method.split('_', 1)

    file   = dirname(__file__) + "/" + dir + "/" + name + ".py"
    spec   = iu.spec_from_file_location("plot_image", file)
    module = iu.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.__dict__[method]

class Panel:
    """The "node" class for hierarchically organizing subplots in ehtplot

    The Panel class is the "organization class" that allows ehtplot to
    hierarchically organize subplots and manage subplot properties.
    In each ehtplot Figure, there is always one root Panel instance.
    The root Panel can directly contain a single matplotlib axes or a
    set of subpanels.

    """

    def __init__(self, *args, **kwargs):
        self.subpanels = kwargs.pop('subpanels', [])
        self.inrow     = kwargs.pop('inrow', True)
        self.plots     = []

        image = kwargs.pop('image', None)
        if image is not None:
            self.plot_image(image, *args, **kwargs)

    def __call__(self, ax, **kwargs):
        # TODO: **kwargs is passed recursively down to the subpanel
        # leaves.  However, there is not a clear to actually use them
        # for now.
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
                panel(fig.add_axes([pos.x0+i*w, pos.y0, w, h]), **kwargs)
        else:
            h = (pos.y1 - pos.y0) / len(self.subpanels)
            w =  pos.x1 - pos.x0
            for i, panel in enumerate(self.subpanels):
                panel(fig.add_axes([pos.x0, pos.y0+i*h, w, h]), **kwargs)

    def __getattr__(self, method):
        def stage(*args, **kwargs):
            func = load(method)
            def plot(ax):
                func(ax, *args, **kwargs)
            self.plots += [plot]
        return stage

    def __iter__(self):
        return iter(self.subpanels)
