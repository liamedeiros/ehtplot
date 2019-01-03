# Copyright (C) 2019 Lia Medeiros & Chi-kwan Chan
# Copyright (C) 2019 Steward Observatory
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

from .plot  import Plot
from .panel import Panel


def _leaf(plots, args, kwargs):
    return Plot(plots, *args, **kwargs)


def _node(plots, args, kwargs):
    B, K = _broadcast(plots, args, kwargs)
    mk   = _leaf if len(B) == 1 else _node # recursion
    return Panel([mk(p, a, k) for p, a, k in B], **K)
