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

import matplotlib.pyplot as plt
from .theme import *
from .panel import *

class Figure:
    """The "head" class for hierarchically organizing panels in ehtplot

    The Figure class is the "outermost container" in ehtplot.  An
    ehtplot Figure can be rendered on screen and exported to files.
    Logically, an ehtplot Figure always contains a single root ehtplot
    Panel instance, although the root Panel can have multiple
    subpanels in it.  See the documentation of the ehtplot Panel class
    for details.

    """

    def __init__(self, root, *args, **kwargs):
        if not isinstance(root, Panel):
            self.panel = Panel(subpanels=root, *args, **kwargs)
        elif args is None and kwargs is None:
            self.panel = root
        else:
            raise ValueError('no argument allowed when passing ehtplot.Panel')

    def __call__(self, *args, **kwargs):
        style = kwargs.pop('style', None)
        fig = plt.figure()
        ax  = fig.add_axes([0, 0, 1, 1])
        with plt.style.context(get_themes(style)):
            self.panel(ax, *args, **kwargs)
        return fig

    def show(self, *args, **kwargs):
        self(*args, **kwargs).show()

    def draw(self, *args, **kwargs):
        self(*args, **kwargs).canvas.draw_idle()

    def save(self, file, *args, **kwargs):
        self(*args, **kwargs).savefig(file)
