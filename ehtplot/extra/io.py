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
import os
import inspect


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


class MultipleImplementationError(Exception):
    pass


def fullname(cls):
    return cls.__module__ + "." + cls.__name__


def open(name, *args, **kwargs):
    """Open a data file/bundle for mockservation according to extensions

    Args:
        name:    Name of the data file/bundle

    Returns:
        A handle for the opened data file/bundle

    Raises:
        NameError:    Invalid data file/bundle name

    Examples:
        >>> import mockservation as mock
        >>> handle = mock.open("data_file.raw")

    """
    if os.path.isdir(name):
        open_x = open_bundle # open_bundle() have been implemented; see below
    elif os.path.isfile(name):
        _, x = os.path.splitext(name)
        try:
            open_x = globals()["open_{}".format(x.strip("."))]
        except Exception as e:
            e.args = ("{}() is not implemented; "
                      "failed to open \"{}\"".format(e.args[0], name))
            raise
    else:
        raise NameError("path \"{}\" is invalid".format(name))

    return open_x(name, *args, **kwargs)


def open_bundle(name, *args, **kwargs):
    """Open a folder as a data bundle

    Args:
        name:    Name of the data bundle

    Returns:
        A handle for the opened data bundle

    Raises:
        ImportError:    Data bundle does not provide a loader

    Examples:
        >>> import mockservation as mock
        >>> handle = mock.open_bundle("data_bundle")

    """
    abcname = fullname(Bundle)

    for loader_name in ["loader.py",
                        ".loader.py",
                        ".mockservation/loader.py"]:
        full_name = "{}/{}".format(name, loader_name)
        if os.path.isfile(full_name):
            import importlib.util as iu
            spec   = iu.spec_from_file_location("loader", full_name)
            loader = iu.module_from_spec(spec)
            spec.loader.exec_module(loader)

            mk = [obj for _, obj in inspect.getmembers(loader, inspect.isclass)
                      if abcname in [fullname(c) for c in obj.__bases__]]
            if not mk:
                return loader.load(name, *args, **kwargs)
            if len(mk) == 1:
                return mk[0](name, *args, **kwargs)

            raise MultipleImplementationError(
                "{} subclasses of {} are implemented for data bundle \"{}\"".
                format(len(mk), abcname, name))

    raise ImportError("loader not found in data bundle \"{}\"".format(name))
