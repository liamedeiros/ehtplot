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

By introducing a logical layer to hierarchically organize subplots and
manage subplot properties, `ehtplot` is capible to combining many
simple plots to a complex figure (see the documentation of the Panel
class).  This feature helps to generate comparative plots for the [EHT
Imaging Challenge](http://vlbiimaging.csail.mit.edu/imagingchallenge).

In a typical scientific workflow, a publication quality plot often
goes to multiple places, which can have very different typesetting and
coloring requirements.  For example, a plot first needs to be rendered
clearly and accurately onscreen; then, when exported into vector graph
formats in order to be included in publications, the lines need to be
visible, the font sizes of labels and tickmarks should match the
caption font size, etc; finally, important plots also go into talks,
where larger fonts and wider lines are usually preferred; in addition,
slides come with different theme&mdash;dark and light
backgrounds&mdash;which may require changing the color theme in a
plot.  In order to make creating these multi-style-multi-destination
figures easy, `ehtplot` is theme based (see the documentation in
"ehtplot/theme.py").  After creating a plot, its presentation and
rendering depend on the user selected targeted outputs.

# Related Links

- [The Event Horizon Telescope](https://eventhorizontelescope.org)
- [EHT Imaging Challenge](http://vlbiimaging.csail.mit.edu/imagingchallenge)
- [ehtplot Documentation](https://liamedeiros.github.io/ehtplot)
- [matplotlib Usage Guide](https://matplotlib.org/tutorials/introductory/usage.html)
