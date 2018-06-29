#!/usr/bin/env python3

import ehtplot as ep

img = ep.open("sample")
pnl = ep.Panel(image=img, pixsize=1)
fig = ep.Figure(pnl)

fig.show(style='ggplot')
fig.save(style='default', "demo.png")
fig.save(style='seaborn', "demo-seaborn.png")
