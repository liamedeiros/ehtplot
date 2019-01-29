# Copyright (C) 2017 Lia Medeiros
# Copyright (C) 2017 Steward Observatory
#
# This file is part of ehtplot.
#
# ehtplot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ehtplot is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ehtplot.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import with_statement
from __future__ import absolute_import

from setuptools import setup, find_packages
from codecs     import open
from os         import path
from io         import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ehtplot",
    version="0.9.0",

    description="Plotting functions for EHT",
    long_description=long_description,

    url="https://github.com/liamedeiros/ehtplot",
    author="Lia Medeiros",
    author_email="lia00@email.arizona.edu",
    license="GPLv3+",

    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: "+
            "GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
    ],
    keywords="astronomy plotting",

    packages=find_packages(exclude=["doc*", "test*"]),
    package_data={'ehtplot.theme': ['*.mplstyle'],
                  'ehtplot.color': ['ctabs/*.ctab']},

    install_requires=[
      # "colorspacious",
        "matplotlib",
        "numpy",
        "scipy",
        "scikit-image",
    ],
)
