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

## Color Models and Color Spaces

The "raw" [RGB](https://en.wikipedia.org/wiki/RGB_color_model) and
[CMYK](https://en.wikipedia.org/wiki/CMYK_color_model) [color
models](https://en.wikipedia.org/wiki/Color_model) are
device-dependent.  In order to describe device-independent color,
companies create "standardized" [color
spaces](https://en.wikipedia.org/wiki/Color_space) such as
[sRGB](https://en.wikipedia.org/wiki/SRGB) (standard Red Green Blue by
HP and Microsoft) and [Adobe RGB](https://en.wikipedia.org/wiki/Adobe_RGB_color_space).  A [color
profile](https://en.wikipedia.org/wiki/ICC_profile), either
characterizes a device or a color space, can then be used to
accurately map the color in an image to a device.  sRGB is often the
default image color space for modern softwares.  That is, if we save
an image without a color profile, it is often interpreted as in sRGB
with [gamma](https://en.wikipedia.org/wiki/Gamma_correction) 2.2.

The [CIELAB](https://en.wikipedia.org/wiki/CIELAB_color_space) (== CIE
L\*a\*b\* == Lab) color space, introduced by the [International
Commission on Illumination (ICE)](https://en.wikipedia.org/wiki/International_Commission_on_Illumination)
in 1976, was the first attempt to take into account the the perceptual
aspects of human vision.  Here, L\* is the lightness; a\* and b\* are
the green-red and blue-yellow color components.  The
[CIECAM02](https://en.wikipedia.org/wiki/CIECAM02)
[color appearance model (CAM)](https://en.wikipedia.org/wiki/Color_appearance_model)
published by the CIE in 2002 defines six color appearances:
brightness, lightness, colorfulness, chroma, saturation, and hue.  And
the [iCAM06](https://en.wikipedia.org/wiki/Color_appearance_model#iCAM06)
model is capable of handling spatial appearance phenomena such as
contrast.

It is useful to transform the Cartesian CIELAB color space to the
cylindrical [CIELCh](https://en.wikipedia.org/wiki/CIELAB_color_space#Cylindrical_representation:_CIELCh_or_CIEHLC)
color space which has coordinates L\*, C\*, and h.  The lightness
coordinate L\* is identical to CIELAB.  The chroma (relative
saturation) C\* and hue h (in degree h°) are simply `C* = sqrt(a*^2 +
b*^2)` and `h = atan2(b*, a*)`.

## Color Appearance Parameters

We ignore spatial appearance phenomena and consider only the the six
color appearance parameters defined by CIECAM02.  They can be grouped
into three classes, correspond to the three coordinates of CIELCh:

- [Brightness](https://en.wikipedia.org/wiki/Brightness) and
  [lightness](https://en.wikipedia.org/wiki/Lightness): they are the
  extrinsic and intrinsic "tones" or "values", respectively.

- [Colorfulness](https://en.wikipedia.org/wiki/Colorfulness),
  [chroma](https://en.wikipedia.org/wiki/Colorfulness#Chroma_in_CIE_1976_L*a*b*_and_L*u*v*_color_spaces),
  and [saturation](https://en.wikipedia.org/wiki/Colorfulness#Saturation):
  colorfulness and chroma are, roughly speaking, the extrinsic and
  intrinsic difference between a color and grey of an object,
  respectively.  Saturation is the colorfulness of a color relative to
  its own brightness.

- [Hue](https://en.wikipedia.org/wiki/Hue): "the degree to which a
  stimulus can be described as similar to or different from stimuli
  that are described as red, green, blue, and yellow."  [Q: are the
  CIELCh hue and (s)RGB hue `h_rgb = atan2(sqrt(3) * (G-B), 2*R - G -
  B)` equivalent?]

It is important to note that the above terms can be defined very
differently in different context.  For example, RGB brightness is
defined as `(R + G + B) / 3`, which is completely different than
CIECAM02 brightness.

## Basic Requirements

Without putting in too much details, a good colormap for scientific
image representation should:

- given readers a correct sense on the pixel values (intensities) in
  the image;

- not artificially show features that do not exist;

- not hide features that exist.

## General Guidance

Given the above requirements, at minimal,

- we need to use *perceptually uniform colormaps*

so that the lightness of the colormap is a fair representation of its
pixel values.  Since chrominance is a two-dimensional quantity, we can
use the different dimensions for different purposes.  Being
independent of lightness and chroma and easily recognized,

- *hue can encode additional information* in an image;

- *hue is also ideal in making an image more attractive* without
  interferencing the representation of pixel values.

The other dimension chroma is less recognizable and should not be used
to encode physical information.  Instead,

- *chroma (or saturation) is useful to place focus of an image*
  without affecting the representation of the physical quantities.

Finally, given that human eyes are less sensitive to color in low
light,

- if color is used to encode an additional information in a figure,
  the *colormap may start (or end) at non-zero lightness*.
