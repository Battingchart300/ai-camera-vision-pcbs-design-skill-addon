# Night Vision — high

Seeing in the dark: IR illumination + an IR-sensitive sensor + a
wake trigger.

## IR illumination

- **850 nm:** longer range, faint red glow (visible if you look at
  the LEDs). The default for camera traps and security.
- **940 nm:** invisible, shorter range. Use it where the glow
  would give the camera away or disturb animals.
- Match the LED wavelength to the sensor: a sensor with an IR-cut
  filter sees almost no IR. Night mode needs NoIR or a switchable
  filter.

## Wake

- **PIR sensor:** wakes the camera on warm motion. The main energy
  saver in a trap — the SoC sleeps until something moves.
- **Always-on night mode:** only for mains/PoE cameras; a solar
  trap cannot afford it.

## Spec fields

`night_vision: {ir_led_nm, ir_led_count, pir}`. LED count 0 means
no IR illumination (day-only camera or external illuminator).

## Checks

No script checks night vision — verify on a real dark night: range,
even illumination (no hot spot in the middle), no IR reflection
from the enclosure window back into the lens.
