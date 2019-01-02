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

def ensure_list(obj, valid=lambda x: True):
    """Convert `obj` to a list if it is not already one"""
    if isinstance(obj, list):
        if all(valid(o) for o in obj):
            return obj
    else:
        if valid(obj):
            return [obj]
    return []


def split_dict(inp, *keyses):
    """Split an input dict into multiple dicts according to lists of keys

    Args:
        ind (dict): input dictionary, usually kwargs
        *keyses (tuple of lists): Variable length argument list that
            contains keys to split.  That is, keyses itself is a tuple
            of lists of keys, and each of keyses[0], keyses[1], ... is
            a list of keys.

    Returns:
        dict or tuple of dicts: If no keyses is provided, return a
            dictionary, which should contain the same key-value pairs
            of `inp`.  Otherwise, return a tuple of dicts that can be
            unwrapped into a form similar to the full argument list.

    Example:
        To illustrate how split_dict() can be used, we provide two
        examples here.  The non-trivial one is:

            $ kwargs = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
            $ keys1  = ['b']
            $ keys2  = ['b', 'c']
            $ d0, d1, d2 = split_dict(kwargs, keys1, keys2)

        `d0`, `d1`, and `d2` above should be `{'a': 1, 'd': 4}`,
        `{'b': 2}`, and `{'b': 2, 'c': 3}`, respectively.

        We desin split_dic() so it is intuitive to use.  A special
        case where no list of keys is passed, which is our second
        exampmle:

            $ d0 = split_dict(kwargs)

        `d0` should contain the same key-value pairs of kwargs.

    """
    out = tuple({} for i in range(len(keyses)+1))

    for k, v in inp.items():
        matched = False
        for i, keys in enumerate(keyses):
            if k in keys:
                matched = True
                out[i+1].update({k: v})
        if not matched:
            out[0].update({k: v})

    return out[0] if keyses == () else out


def getaxes(ax0):
    """Get all axeses, e.g. twinx, from a single axes"""
    axes = [ax0]
    for pair in ax0._twinned_axes:
        if ax0 in pair:
            axes += list(set(pair).difference([ax0]))
    # TODO: ensure that all axes have the same position
    return axes


def getbce(obj, i):
    """Get broadcasted element"""
    if not isinstance(obj, list) or len(obj) == 0:
        return obj
    elif len(obj) == 1:
        return obj[0]
    elif len(obj) > i:
        return obj[i]
    else:
        raise IndexError("failed to broadcast")


def broadcast(args, kwargs):
    """Broadcast values in `args` and `kwargs` to a list of them

    This is a very simple 1D version of numpy's broadcasting mechanism
    for `args` and `kwargs`.  The idea is that we can pass lists or
    objects to a function through `args` and `kwargs`.  If all the
    `args` and `kwargs` have lengths 1 and a unique `n`, then we
    consider they are broadcastable.  This function then returns a
    list of `n` `(args, kwargs)` tuples.

    Args:
        *args (tuple): Variable length argument list that contains
            objects or list of objects.
        **kwargs (dict): Arbitrary keyworded arguments that contains
            objects or list of objects.

    Returns:
        list of objects: As long as the input `args` and `kwargs` are
            broadcastable, this function return a list of `(args,
            kwargs)` tuples.

    """
    values = args + tuple(kwargs.values())
    ns     = set(len(a) for a in values if isinstance(a, list) and len(a) > 1)

    if len(ns) == 0:
        n = 1
    elif len(ns) == 1:
        n = ns.pop()
    else:
        raise ValueError('The parameters have inconsistent vector length')

    return [(tuple(getbce(a, i) for a    in args),
               {k: getbce(v, i) for k, v in kwargs.items()}) for i in range(n)]
