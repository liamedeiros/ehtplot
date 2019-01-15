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

from __future__ import absolute_import

from ehtplot.visual  import Visual
from ehtplot.panel   import Panel
from ehtplot.figure  import Figure
from ehtplot.helpers import ensure_list, split_tuple, split_dict


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


def _broadcast(visuals, args, kwargs):
    """Broadcast values in `visuals`, `args` and `kwargs` to list of them

    This is a very simple 1D version of numpy's broadcasting
    mechanism.  The idea is that we can pass lists or objects to a
    function through `visuals`, `args` and `kwargs`.  If all of them
    have lengths 1 and a unique `n`, then we consider they are
    broadcastable.  This function then returns a list of `n`
    `(visuals, args, kwargs)` tuples.

    Args:
        visuals (Panel, callable, valid visual key, or list): Panel,
            callable, or valid visual key, or a list of them.
        *args (tuple): Variable length argument list that contains
            objects or list of objects.
        **kwargs (dict): Arbitrary keyworded arguments that contains
            objects or list of objects.

    Returns:
        list of objects: As long as the input `visuals`, `args`, and
            `kwargs` are broadcastable, this function return a list of
            `(visuals, args, kwargs)` tuples.
        dict: A dictionary containing keyworded arguments for the
            Panel.

    """
    kwargs, kwprops = split_dict(kwargs, Panel._prop_keys)

    values = (visuals,) + args + tuple(kwargs.values())
    ns     = set(len(a) for a in values if isinstance(a, list) and len(a) > 1)

    if len(ns) == 0:
        n = 1
    elif len(ns) == 1:
        n = ns.pop()
    else:
        raise ValueError("The parameters have inconsistent vector lengths")

    return ([(_getbce(visuals, i),
        tuple(_getbce(a, i)  for a    in args),
     dict((k, _getbce(v, i)) for k, v in kwargs.items())) for i in range(n)],
            kwprops)


def _leaf(visuals, args, kwargs, level=0):
    """End point of recursive Panel constructions"""
    if isinstance(visuals, Panel):
        return visuals.update(*args, **kwargs), level
    else:
        return Visual(visuals, *args, **kwargs), level


def _node(visuals, args, kwargs, level=0):
    """Recursive part of recursive Panel constructions"""
    B, K = _broadcast(visuals, args, kwargs)
    mk   = _leaf if len(B) == 1 and Visual.isvisualable(B[0][0]) else _node # recursion
    N, L = zip(*(mk(p, a, k, level+1) for p, a, k in B))
    if level+1 < max(L)-1:
        K['inrow'] = False
    return Panel(N, **K), max(L)


def panel(*args, **kwargs):
    """Starting point of recursive Panel constructions"""
    args, visuals = split_tuple(args, Panel.ispanelable, Visual.isvisualable)
    if not visuals:
        kwargs, kwvisuals = split_dict(kwargs, Visual.visuals)
        if kwvisuals:
            visuals =  list(ensure_list(k) for k in kwvisuals.keys())
            args    = (list(kwvisuals.values()),) + args
    p, _ = _node(visuals, args, kwargs)
    return p


def plot(*args, **kwargs):
    """Smart plot generation "frontend" of `ehtplot`"""
    kwargs, kwprops = split_dict(kwargs, Figure._prop_keys)
    return Figure(panel(*args, **kwargs), **kwprops)
