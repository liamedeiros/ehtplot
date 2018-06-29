#!/usr/bin/env python3

import ehtplot as ep

img = ep.open("sample")
pnl = ep.Panel(image=img)
fig = ep.Figure(pnl)

fig.save("demo-seaborn.png", style='seaborn')
fig.save("demo-ggplot.png",  style='ggplot')
fig.save("demo.png")
