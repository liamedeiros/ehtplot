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

## Color Models and Color Appearance Models

The "raw" RGB and CMYK color models are device-dependent.  In order to
describe device-independent color, companies "standarize" color spaces
and create sRGB (standard Red Green Blue by HP and Microsoft) and
Adobe RGB.

A color profile, either characterizes a device or a color space, can
then be used to accurately map the color in an image to a device.
sRGB is often the default image color space for modern softwares.
That is, if we save an image without a color profile, it is often
interperted as in sRGB with gamma 2.2.

The CIELAB (== CIE L*a*b* == Lab) color space, introduced by the
International Commission on Illumination (ICE) in 1976, was the first
attempt to take into account the the perceptual aspects of human
vision.  Here, L* is the lightness and a* and b* are the green-red and
blue-yellow color components.  The CIECAM02 color appearance model
(CAM) published by the CIE in 2002 defines six color appearances:
brightness, lightness, colorfulness, chroma, saturation, and hue.  And
the iCAM06 model is capable of handling spatial appearance phenomena
such as contrast.

It is useful to transform the Cartesian CIELAB color space to the
cylindrical CIELCh color space which has coordinates L*, C*, and h.
The lightness coordinate L* is identical to CIELAB.  The chroma
(relative saturation) C* and hue h (in degree h°) are simply `C* =
sqrt(a*^2 + b*^2)` and `h = atan2(b*, a*)`.

## Color Apperance Parameters

We completely ignore spatial appearance phenomena and consider only
the the six color appearance parameters defined by CIECAM02.  They can
be grouped into three classes, correspond to the three coordinates of
CIELCh:

- Brightness and lightness: they are the extrinsic and intrinsic
  "tones" or "values", respectively.

- Colorfulness, chroma, and saturation: colorfulness and chroma are,
  roughly speaking, the extrinsic and intrinsic difference between a
  color and grey of an object, respectively.  Saturation is the
  colorfulness of a color relative to its own brightness.

- Hue: "the degree to which a stimulus can be described as similar to
  or different from stimuli that are described as red, green, blue,
  and yellow."  [Q: are the CIELCh hue and (s)RGB hue `h_rgb =
  atan2(sqrt(3) * (G-B), 2*R - G - B)` equivalent?]
