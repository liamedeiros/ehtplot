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

from .plot    import Plot
from .panel   import Panel
from .helpers import split_dict


def _getbce(obj, i):
    """Get broadcasted element"""
    if not isinstance(obj, list) or len(obj) == 0:
        return obj
    elif len(obj) == 1:
        return obj[0]
    elif len(obj) > i:
        return obj[i]
    else:
        raise IndexError("failed to broadcast")


def _broadcast(plots, args, kwargs):
    """Broadcast values in `plots`, `args` and `kwargs` to list of them

    This is a very simple 1D version of numpy's broadcasting
    mechanism.  The idea is that we can pass lists or objects to a
    function through `plots`, `args` and `kwargs`.  If all of them
    have lengths 1 and a unique `n`, then we consider they are
    broadcastable.  This function then returns a list of `n` `(plots,
    args, kwargs)` tuples.

    Args:
        plots (Panel, callable, or valid plot key): Panel, callable,
            or valid plot key, or a list of them.
        *args (tuple): Variable length argument list that contains
            objects or list of objects.
        **kwargs (dict): Arbitrary keyworded arguments that contains
            objects or list of objects.

    Returns:
        list of objects: As long as the input `plots`, `args`, and
            `kwargs` are broadcastable, this function return a list of
            `(plots, args, kwargs)` tuples.
        dict: A dictionary containing keyworded arguments for the
            Panel.

    """
    kwargs, kwprops = split_dict(kwargs, Panel._prop_keys)

    values = (plots,) + args + tuple(kwargs.values())
    ns     = set(len(a) for a in values if isinstance(a, list) and len(a) > 1)

    if len(ns) == 0:
        n = 1
    elif len(ns) == 1:
        n = ns.pop()
    else:
        raise ValueError('The parameters have inconsistent vector lengths')

    return ([(_getbce(plots, i),
        tuple(_getbce(a,     i) for a    in args),
          {k: _getbce(v,     i) for k, v in kwargs.items()}) for i in range(n)],
            kwprops)


def _leaf(plots, args, kwargs):
    return Plot(plots, *args, **kwargs)


def _node(plots, args, kwargs):
    B, K = _broadcast(plots, args, kwargs)
    mk   = _leaf if len(B) == 1 else _node # recursion
    return Panel([mk(p, a, k) for p, a, k in B], **K)
