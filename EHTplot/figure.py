# Copyright (C) 2017 Lia Medeiros                                                                             
#                                                                                                             
# This file is part of EHTplot.                                                                               
#                                                                                                             
# EHTplot is free software: you can redistribute it and/or modify                                             
# it under the terms of the GNU General Public License as published by                                        
# the Free Software Foundation, either version 3 of the License, or                                           
# (at your option) any later version.                                                                         
#                                                                                                             
# EHTplot is distributed in the hope that it will be useful,                                                  
# but WITHOUT ANY WARRANTY; without even the implied warranty of                                              
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                               
# GNU General Public License for more details.                                                                
#                                                                                                             
# You should have received a copy of the GNU General Public License                                           
# along with EHTplot.  If not, see <http://www.gnu.org/licenses/>.  

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors, rcParams
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
from matplotlib.ticker import MultipleLocator


class Figure:
    def __init__(self, subplots=(1,1), size=None, font=10, sharex=False, sharey=False):
        '''
        subplots is (row, column) but size is (x,y)
        '''
        
        textwidth=7.1
        columnwidth=3.39375
        if size is None:
            w = columnwidth if subplots[1]==1 else textwidth
            size = (w, w/subplots[1]*subplots[0])
        self.fig, self.axs = plt.subplots(subplots[0], subplots[1], sharex=sharex, sharey=sharey, figsize=size)      
