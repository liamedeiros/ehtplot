#!/usr/bin/env python3

from matplotlib.cm import get_cmap
from ehtplot.color import linearize, symmetrize

linearize(get_cmap('afmhot'), save='ehthot.txt')
symmetrize(get_cmap('RdBu'),  save='ehtRdBu.txt')
