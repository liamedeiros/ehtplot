#!/usr/bin/env python3

import ehtplot as ep

img = ep.open("sample")

fig = ep.Figure()
fig.plot_image(img, pixsize=1)

ep.set_themes('seaborn')
fig.savefig("demo-seaborn.png")

ep.set_themes('default')
fig.savefig("demo.png")
