# Copyright (C) 2018 Chi-kwan Chan
# Copyright (C) 2018 Steward Observatory
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

import numpy as np
from ehtplot.color import vis as ev

def plot_cmap(ax1, cmap):
    ctab = ev.get_ctab(cmap)  # get the colormap as a color table in sRGB
    Jabp = ev.transform(ctab) # transform color table into CAM02-UCS colorspace

    Jp = Jabp[:,0]
    ap = Jabp[:,1]
    bp = Jabp[:,2]

    Cp = np.sqrt(ap * ap + bp * bp)
    hp = np.arctan2(bp, ap) * 180 / np.pi
    v  = np.linspace(0.0, 1.0, len(Jp))

    ax1.set_title(cmap)
    ax1.set_xlabel("Value")

    ax2 = ax1.twinx()
    ax1.set_ylim(0,   100)
    ax1.set_ylabel("J' & C' (0-100)")
    ax2.set_ylim(-180,180)
    ax2.set_ylabel("h' (degrees)")

    ax1.scatter(v, Jp, color=ctab)
    ax1.plot   (v, Cp, c='k', linestyle='--')
    ax2.scatter(v[::15], hp[::15], s=12, c='k')
