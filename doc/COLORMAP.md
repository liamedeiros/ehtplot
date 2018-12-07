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
accurately map the color in an image to a device.

The [CIELAB](https://en.wikipedia.org/wiki/CIELAB_color_space) (also
CIE L\*a\*b\*, hereafter Lab) color space, introduced by the
[International Commission on Illumination
(ICE)](https://en.wikipedia.org/wiki/International_Commission_on_Illumination)
in 1976, was the first attempt to take into account the the perceptual
aspects of human vision.  Here, L\* is the lightness; a\* and b\* are
the green-red and blue-yellow color components.  The
[CIECAM02](https://en.wikipedia.org/wiki/CIECAM02) [color appearance
model (CAM)](https://en.wikipedia.org/wiki/Color_appearance_model)
published by the CIE in 2002 defines six color appearances:
brightness, lightness, colorfulness, chroma, saturation, and hue.  And
the
[iCAM06](https://en.wikipedia.org/wiki/Color_appearance_model#iCAM06)
model is capable of handling spatial appearance phenomena such as
contrast.

It is useful to transform the Cartesian Lab color space to the
cylindrical [CIELCh](https://en.wikipedia.org/wiki/CIELAB_color_space#Cylindrical_representation:_CIELCh_or_CIEHLC)
(hereafter LCh) color space which has coordinates L\*, C\*, and h.
The lightness coordinate L\* is identical to Lab.  The chroma
(relative saturation) C\* and hue h (in degree h°) are simply `C* =
sqrt(a*^2 + b*^2)` and `h = atan2(b*, a*)`.

## Color Appearance Parameters

We ignore spatial appearance phenomena and consider only the the six
color appearance parameters defined by CIECAM02.  They can be grouped
into three classes, correspond to the three coordinates of LCh:

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
representation of a scale image should:

1. give the readers a correct sense on the scale values (intensities)
   in the image;

2. not artificially show features that do not exist;

3. not intentionally hide features that exist;

4. be effective in communicating scientific messages;

5. be device-independent.

## General Guidance

In response to the above requirements, at minimal,

- we need to use *perceptually uniform colormaps*

so that the lightness of the color in an image is a fair
representation of its scale values.  While visual perception is a
complex science, the Lab lightness L\* should serve us as a good
approximation for generating perceptually uniform colormaps.  In fact,
linearity in L\* is used as the working definition of Perceptually
Uniform Sequential colormaps by
[matplotlib](https://matplotlib.org/users/colormaps.html).

Since chrominance is a two-dimensional quantity, we can use the
different dimensions for different purposes.  Being independent of
lightness and chroma and easily recognized,

- *hue can encode an additional physical quantity* in an image (when
  used in this way, the change of hue should be linearly proportional
  to the quantity);

- *hue is also ideal in making an image more attractive* without
  interferencing the representation of pixel values.

The other dimension chroma is less recognizable and should not be used
to encode physical information.  Since sRGB is only a subset of the
Lab colorspace, there are human regonizable color that are not
displayable.  In order to accurately represent the physical
quantities,

- if a color is not displayable, one should preserve its lightness L\*
  and hue h, and adjust its chroma.

If we adopt Eva Lubbe's formula `S = C* / sqrt(C*^2 + L*^2)`,

- *saturation is useful to place focus of an image* without affecting
  the representation of the physical quantities.

Given that human eyes are less sensitive to color in low light,

- if color is used to encode an additional physical quantity in a
  figure, the *colormap may start (or end) at non-zero lightness*.

Finally, sRGB is often the default image color space for modern
softwares.  That is, if we save an image without a color profile, it
is often interpreted as in sRGB with [gamma](https://en.wikipedia.org/wiki/Gamma_correction) 2.2.
Therefore, we should

- convert colormaps to sRGB with gamma 2.2, and then save the
  resulting images without any color profile.
