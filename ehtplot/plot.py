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

def plot(type):
    dir, name = type.split('_', 1)

    file   = dirname(__file__) + "/" + dir + "/" + name + ".py"
    spec   = iu.spec_from_file_location(type, file)
    module = iu.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.__dict__[type]
