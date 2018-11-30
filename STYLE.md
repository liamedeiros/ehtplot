# EHT Data Visualization Style Guide

## Background

This style guide helps the Event Horizon Telescope (EHT) creates
consistent plots and images across the whole collaboration.  It
summarizes a set of choices and recommandataions for plotting and
visualizing data.

## Using `matplotlib` Style

Since version 1.4 (released in August 2014), matplotlib introduce a
`style` module to manage stylesheets.  This allows users to select
different plotting styles by a single command

    plt.style.use(['dark_background', 'presentation'])

We strongly encourage matplotlib users in the EHT collaboration (EHTC)
to take advantage of the matplotlib style module.  Specifically, if a
plotting styles, e.g., linewidth, needs to be adjust *globally*, user
should consider setting

    lines.linewidth : 3

instead of setting it manually in a function call

    plt.plot(x, y, linewidth=3)
