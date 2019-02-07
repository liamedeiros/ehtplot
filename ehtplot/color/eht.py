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
from ehtplot.color.ctab import _path, ext, get_ctab, save_ctab

def save_cmap(cm, name):
    save_ctab(get_ctab(cm), _path+"/"+name+ext)

save_cmap(ehtrainbow(),      "ehtrainbow")
save_cmap(ehtrainbow(Jp=25), "ehtrainbow_25")
save_cmap(ehtrainbow(Jp=50), "ehtrainbow_50")
save_cmap(ehtrainbow(Jp=75), "ehtrainbow_75")

save_cmap(ehtrainbow(Cp='minmax'),        "ehtrainbow_f")
save_cmap(ehtrainbow(Cp='minmax', Jp=25), "ehtrainbow_25f")
save_cmap(ehtrainbow(Cp='minmax', Jp=50), "ehtrainbow_50f")
save_cmap(ehtrainbow(Cp='minmax', Jp=75), "ehtrainbow_75f")

save_cmap(ehtuniform(),                            "ehtorange")
save_cmap(ehtuniform(hpL='blue',   hpR='skyblue'), "ehtblue")
save_cmap(ehtuniform(hpL='indigo', hpR='violet'),  "ehtviolet")
