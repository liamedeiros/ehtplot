# Copyright (C) 2017 Lia Medeiros
#
# This file is part of EHTplot.
#
# EHTplot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EHTplot is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EHTplot.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
from codecs     import open
from os         import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README"), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="EHTplot",
    version="0.9.0",
    description="Plotting functions for EHT",
    long_description=long_description,

    url="https://github.com/liamedeiros/EHTplot",
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
)
