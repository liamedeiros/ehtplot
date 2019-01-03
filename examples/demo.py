#!/usr/bin/env python3

import ehtplot as eht
from ehtplot.extra import io

img = io.open("sample", component="pca0")
fig = eht.plot(['image', 'image'], [[img, img, img]])

exts = [".png", ".jpg"]
fig.save(["demo-seaborn"+ext for ext in exts], style='seaborn')
fig.save(["demo-ggplot" +ext for ext in exts], style='ggplot')
fig.save(["demo-ehtplot"+ext for ext in exts], style='ehtplot')
fig.save(["demo"        +ext for ext in exts])
