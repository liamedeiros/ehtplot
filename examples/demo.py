#!/usr/bin/env python3

import ehtplot as ep
from ehtplot.extra import io

img = ep.Panel(image=io.open("sample"))
row = ep.Panel(subpanels=[img, img, img])
fig = ep.Figure([row, row], inrow=False)

fig.save("demo-seaborn.png", style='seaborn')
fig.save("demo-ggplot.png",  style='ggplot')
fig.save("demo-ehtplot.png", style='ehtplot')
fig.save("demo.png")
