#!/usr/bin/env python3

import ehtplot as ep

img = ep.Panel(image=ep.open("sample"))
row = ep.Panel([img, img, img])
fig = ep.Figure([row, row], inrow=False)

fig.save("demo-seaborn.png", style='seaborn')
fig.save("demo-ggplot.png",  style='ggplot')
fig.save("demo-ehtplot.png", style='ehtplot')
fig.save("demo.png")
