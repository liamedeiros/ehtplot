#!/usr/bin/env python3

import ehtplot as ep

img = ep.open("sample")

fig = ep.Figure()
fig.plot_image(img, pixsize=1)
fig.fig.savefig("demo.jpg")
