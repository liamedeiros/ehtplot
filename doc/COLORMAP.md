# Color Map

## Introduction

The Event Horizon Telescope (EHT) is a Very-long-baseline
interferometry (VLBI) experiment aiming at capture of the first
pictures of black holes.  While an image worth a thousand words, the
interpretation of an image is subjective.  The presentation of an
image can strongly affect how human eyes identify features.  This is
especially true for two-dimensional intensity maps, where the value of
each pixel is represented by a color.  A poorly chosen colormap
between values and colors can fool the human eyes to, e.g., pick out
non-existing features, or to hide important features.

In order to present the resulting images of the EHT as accurate as
possible, we take into account how human eyes work and provide a few
guidance on the colormap usages in different situations.

## General Guidance

Without putting in too much details, the requirements of a good
colormap for scientific image representation should:

- Given readers a correct sense on the pixel values (intensities) in
  the image.
- Not artificially show features that do not exist.
- Not hide features that exist.

Therefore, it is clear that, at minimal, we need:

- Perceptually uniform colormaps

Given that human eyes are less senstive to color in low light:

- If color provides important information in a figure, the colormap
  may start at gray instead of black.
