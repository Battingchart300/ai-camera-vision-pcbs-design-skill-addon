# Design rules

Camera-specific rules on top of the base skill (§4–§7). Where a
number is not given here, take it from the part datasheet or the fab
— never guess.

## MIPI CSI-2 routing

- 85 Ω differential impedance, pairs routed together, over an
  unbroken GND plane. No routing over a plane split.
- Keep pairs short: sensor close to the processor. Every extra
  centimetre of flex costs signal margin.
- Length-match the two wires of a pair; match pairs to each other
  loosely (check the SoC guide for the number).
- 100 Ω is for other interfaces — do not mix it up with the 85 Ω
  of MIPI/PCIe.
- Series resistors / common-mode chokes only when the SoC or
  sensor datasheet asks for them.

## Power

- Separate the sensor's analog rail from the digital rail; a noisy
  sensor supply shows up as stripes in the image.
- Decoupling at the sensor and at the SoC per their datasheets.
- Power sequencing in the datasheet order (sensor last on / first
  off is common — verify per part).
- Size the 5 V / 3.3 V rails for peak current, not average.

## Optics and mechanics

- The lens mount must hold focus: no flex, no play. A loose mount
  is a blurry camera.
- Keep the sensor window clean and the IR-cut filter seated.
- The image circle of the lens must cover the sensor (a lens for a
  1/3" sensor vignettes on a 1/2.3" sensor).
- Leave airflow or a heatsink path for the SoC — a sealed box with
  no thermal path cooks (see §7).

## Pin-by-pin check (mandatory, SKILL.md §11.1)

Every pin of every part, checked against its datasheet: right net,
right voltage, right pull-up/down, no pin floating that must not
float. No handover with an unchecked pin.
