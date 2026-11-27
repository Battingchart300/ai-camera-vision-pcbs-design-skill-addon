# ISP (Image Signal Processor) — critical

The ISP turns the sensor's RAW data into a usable image: debayer,
exposure, white balance, noise reduction, HDR, tone mapping.

## Choosing

- **Built-in ISP** (PiSP on Pi 5, RK3588 48 MP ISP, NVIDIA ISP on
  Jetson) is the default — it is tuned for the vendor's sensors.
- **No ISP** (ESP32-S3, raw sensor on an FPGA) means the software
  or the FPGA does the work — slower, and tuning is your job.
- **ISP max megapixels** must cover the sensor (RK3588: 48 MP;
  BCM2712: 12.3 MP). Over it FAILs `sensor_check.py`.

## What to set

- Exposure / gain limits for day and night modes.
- HDR mode where the scene has bright and dark areas at once
  (IMX708 HDR video, IMX477 DOL-HDR).
- 3DNR (temporal noise reduction) for night video — it costs
  latency, so keep it light on a robot.
- Tuning: a sensor without tuning for the ISP looks wrong (colour,
  exposure). Use the vendor tuning or budget time to make one.

## Checks

ISP max MP is checked in `sensor_check.py`. Tuning quality is not
checkable by a script — verify with a real captured image.
