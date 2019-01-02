# Copyright (C) 2018 Chi-kwan Chan
# Copyright (C) 2018 Steward Observatory
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

import numpy as np
from skimage.morphology import skeletonize


def rebin(arr, shape=[32, 32]):
    reshape = (shape[0], arr.shape[0]//shape[0],
               shape[1], arr.shape[1]//shape[1])
    return arr.reshape(reshape).mean(-1).mean(1)


def translate_threshold(img, threshold=0.5):
    threshold *= np.sum(img)
    s = np.sort(img.flatten())
    i = np.searchsorted(np.cumsum(s), threshold, side="left")
    return s[i]


def metroize(img, mgrid=32, threshold=0.5):
    threshold = translate_threshold(img, threshold=threshold)
    img = skeletonize(img > threshold)
    img = skeletonize(rebin(img, [mgrid, mgrid]) > 0)
    return img


def plot_metroized(ax, img, **kwargs):
    img = metroize(img, **kwargs)

    sh = img.shape
    s0 = sh[0]
    s1 = sh[1]
    for i in range(sh[0]):
        for j in range(sh[1]):
            if img[i,j] == 0.0: continue

            c = 0
            for ii in [i-1,i,i+1]:
                for jj in [j-1,j,j+1]:
                    if ii == i and jj == j:
                        continue
                    if ii < 0 or ii >= s0:
                        continue
                    if jj < 0 or jj >= s1:
                        continue
                    if img[ii,jj] > 0.0:
                        if ii != i and jj != j:
                            if img[ii,j] > 0.0 or img[i,jj] > 0.0:
                                continue
                        ax.plot([j,(jj-j)/2+j], s1-np.array([i,(ii-i)/2+i]),
                                color='k')
                        c += 1
            if c == 0:
                ax.plot([j], [s1-i], marker='.', color='k')

    ax.set_xlim([0, sh[1]])
    ax.set_ylim([0, sh[0]])
    ax.tick_params(axis='both', which='both',
                   top=False, bottom=False, labelbottom=False,
                   left=False, right=False, labelleft=False)
