# Copyright (C) 2017 Chi-kwan Chan
#
# This file is part of EHTplot.
#
# EHTplot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EHTplot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EHTplot.  If not, see <http://www.gnu.org/licenses/>.

class Panel:
    """The class for hierarchically organize subplots in EHTplot

    The Panel class is the "organization class" that allows EHTplot to
    hierarchically organize subplots and manage subplot properties.
    In each EHTplot Figure, there is always one root Panel instance.
    The root Panel can directly contain a single matplotlib axes or a
    set of subpanels.

    """
    pass
