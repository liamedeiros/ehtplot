#!/usr/bin/env python3

import ehtplot as ep
from ehtplot.extra import io

img = ep.Panel(image=io.open("sample", component="pca0"))
row = ep.Panel(img, img, img)
fig = ep.Figure(row, row, inrow=False)

exts = [".png", ".jpg"]

fig.save(["demo-seaborn"+ext for ext in exts], style='seaborn')
fig.save(["demo-ggplot" +ext for ext in exts], style='ggplot')
fig.save(["demo-ehtplot"+ext for ext in exts], style='ehtplot')
fig.save(["demo"        +ext for ext in exts])
