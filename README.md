# Introduction

`ehtplot` is a python module that assists scientists in the [Event
Horizon Telescope (EHT) Collaboration](http://eventhorizontelescope.org)
to create publication quality, elegant, and consistent plots.  It
provides a set of easy-to-use plotting functions for EHT and
Very-Long-Baseline Interferometry (VLBI) specific figures (see the
documentation of the Figure class).  This includes plotting visibility
and images for both synthetic and real data, adding uv-tracks to the
plots, adding the expected event horizon size to the plots, etc.

# Special Features

## Hierarchically Panels

By introducing a logical layer to hierarchically organize subplots and
manage subplot properties, `ehtplot` is capable to combining many
simple plots in a complex figure (see the documentation of the Panel
class).  For example, the following code place multiple figures
side-by-side:

    import ehtplot as ep
    fig = ep.Figure(ep.Panel(image="1.fits"),
                    ep.Panel(image="2.fits"),
                    ep.Panel(image="3.fits"),
                    ep.Panel(image="4.fits"))
    fig.show()

This feature can help generating comparative plots for the [EHT
Imaging Challenge](http://vlbiimaging.csail.mit.edu/imagingchallenge).

## Multiple Themes Rendering

In a typical scientific workflow, a publication quality plot often
goes to multiple places, which may have very different typesetting and
coloring requirements.  For example, a plot first needs to be rendered
clearly and accurately onscreen; then, when exported into vector
graphic formats for publications, the lines need to be visible, the
font sizes of labels should match the caption font size, etc; finally,
important plots also go into talks, where larger fonts and wider lines
are usually preferred; in addition, slides come with different
theme&mdash;dark and light backgrounds&mdash;which may require
changing the color theme in a plot.  In order to make creating these
multi-style-multi-destination figures easy, `ehtplot` is theme based
(see the documentation in "ehtplot/theme.py").  After creating a plot,
its presentation and rendering depend on the user selected targeted
outputs.

    fig.save("figure.eps")
    fig.save("figure-seaborn.eps", style="seaborn")
    fig.save("figure-talk-dark.png", format="talk", theme="dark")

It is straightforward to enable `ehtplot`'s theme even without using
`ehtplot` for plotting.  One simply loads the theme submodule:

    import ehtplot.theme

and all `ehtplot` theme will be registered to `matplotlib`.

## Perceptually Uniform Colormap

We also spent a lot of time to create perceptually uniform colormaps
based on the CAM02-UCS color appearance model.  For more information,
see `ehtplot`'s [color submodule documentation](https://github.com/liamedeiros/ehtplot/blob/docs/docs/COLORMAPS.ipynb).

It is also straightforward to enable `ehtplot`'s colormaps even
without using `ehtplot` for plotting.  One simply loads the color
submodule:

    import ehtplot.color

and all `ehtplot` colormaps will be registered to `matplotlib`.

# Related Links

- [The Event Horizon Telescope](https://eventhorizontelescope.org)
- [EHT Imaging Challenge](http://vlbiimaging.csail.mit.edu/imagingchallenge)
- [ehtplot Documentation](https://liamedeiros.github.io/ehtplot)
- [matplotlib Usage Guide](https://matplotlib.org/tutorials/introductory/usage.html)
