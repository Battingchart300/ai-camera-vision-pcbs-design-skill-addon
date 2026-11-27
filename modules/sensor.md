# Image Sensor (CMOS/CCD) — critical

The sensor turns light into data. Everything downstream (ISP, link,
AI, storage) is sized from it.

## Choosing

- **Resolution vs. light:** bigger pixels see better in the dark.
  IMX477 (1.55 µm) beats IMX219 (1.12 µm) at night at the same
  resolution. For night work, prefer big pixels over more pixels.
- **Shutter:** rolling shutter is fine for still scenes; a moving
  subject or a fast robot needs a **global shutter** (IMX296,
  AR0234) or the image skews.
- **Interface:** MIPI CSI-2 for a sensor on the board; a USB camera
  is a module, not a sensor choice.
- **IR:** a standard sensor has an IR-cut filter (day only). For
  night vision use a NoIR variant or remove the filter.

## Verified parts

See `references/components.md` and `validators/known_parts.py`:
IMX477, IMX219, IMX708, IMX500, IMX296, OV5647, AR0234.

## Checks

`scripts/sensor_check.py`: part known, resolution matches the
datasheet, lanes in range, interface compatible with the processor.

## Pitfalls

- A sensor with no driver for the SoC is a paperweight — check
  driver support (V4L2 / libcamera) before choosing.
- Full-resolution fps is lower than the headline fps (which is
  usually a binned/cropped mode). Size the link for the mode you
  actually use.
