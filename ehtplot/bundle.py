# Copyright (C) 2017 Chi-kwan Chan
# Copyright (C) 2017 Steward Observatory
#
# This file is part of mockservation.
#
# Mockservation is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Mockservation is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mockservation.  If not, see <http://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod

class Bundle(ABC):
    """An abstract class to be implemented by data bundle loaders
    """
    @abstractmethod
    def close(self): # must be implemented by subclasses
        pass

    # Bundle is a context manager so it can be used with the `with` statement
    def __enter__():
        return self
    def __exit__(self, exception_type, exception_val, trace):
        self.close()

    # Bundle may conform to the iterator protocal
    def __iter__(self):
        return self
    def __next__(self):
        raise NotImplementedError
