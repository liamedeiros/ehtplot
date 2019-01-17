#!/usr/bin/env python3
#
# Copyright (C) 2018--2019 Chi-kwan Chan
# Copyright (C) 2018--2019 Steward Observatory
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

from ehtplot.color.cmap import ehtrainbow, ehtuniform
from ehtplot.color.ctab import path, ext, get_ctab, save_ctab

save_ctab(get_ctab(ehtrainbow()),      path+"/ehtrainbow"+ext)
save_ctab(get_ctab(ehtrainbow(Jp=25)), path+"/ehtrainbow_25"+ext)
save_ctab(get_ctab(ehtrainbow(Jp=50)), path+"/ehtrainbow_50"+ext)
save_ctab(get_ctab(ehtrainbow(Jp=75)), path+"/ehtrainbow_75"+ext)

save_ctab(get_ctab(ehtuniform()),                          path+"/ehthot"+ext)
save_ctab(get_ctab(ehtuniform(hpL='blue', hpR='skyblue')), path+"/ehtcold"+ext)
