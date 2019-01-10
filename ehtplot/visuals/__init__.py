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

pass

# This file is meant to be empty.  We actually do not want to make
# `ehtplot.visuals` a package.  Instead, we want it to be a simple
# directory that contains visualization/plotting source codes that is
# loaded dynamically.  Nevertheless, since python2 does not support
# `importlib.util`, we are forced to find a work around using the more
# portable `importlib.import_module()` function.  Hence, we are forced
# to introduce this "__init__.py" to turn `ehtplot.visuals` a package.
