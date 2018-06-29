# Copyright (C) 2017--2018 Lia Medeiros & Chi-kwan Chan
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

class Panel:
    """The "node" class for hierarchically organizing subplots in ehtplot

    The Panel class is the "organization class" that allows ehtplot to
    hierarchically organize subplots and manage subplot properties.
    In each ehtplot Figure, there is always one root Panel instance.
    The root Panel can directly contain a single matplotlib axes or a
    set of subpanels.

    """

    def __init__(self, subpanels=None, image=None):
        self.subpanels = [] if subpanels is None else subpanels
        self.plots     = []

        if image is not None:
            self.plot_image(image)

    def __iter__(self):
        return iter(self.subpanels)

    def __call__(self, ax):
        for plot in self.plots:
            plot(ax)

        if not self.subpanels:
            return
        fig = ax.figure
        pos = ax.get_position()
        h   =  pos.y1 - pos.y0
        w   = (pos.x1 - pos.x0) / len(self.subpanels)
        for i, panel in enumerate(self.subpanels):
            panel(fig.add_axes([pos.x0+i*w, pos.y0, w, h]))

    def plot_image(self, img):
        def plot(ax):
            ax.imshow(img)
        self.plots += [plot]
