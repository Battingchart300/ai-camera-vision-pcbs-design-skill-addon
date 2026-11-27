# Cooling System

Passive and active cooling for cameras and Vision PCs.

## Passive (preferred for cameras)

- Heatsink + heat spreader to the case wall; the case itself is
  the heatsink in a metal enclosure.
- Works when peak power is low (a few watts) and the ambient is
  moderate. No moving parts, no noise, nothing to fail.
- In a sealed IP66 box, the heat path is: chip -> spreader ->
  case wall -> outside air. Every interface in that chain needs
  thermal paste/pad — a dry joint is a broken path.

## Active (Vision PC / workstation / server)

- Fan + heatsink when passive cannot keep up. Size the fan for
  peak power, not average.
- Dust kills fans outdoors: filter the intake or use a sealed
  design with an external heatsink.
- A fan failure must not kill the system: thermal throttling +
  an alert, not a silent overheat.

## Checks

`scripts/thermal_check.py` (enclosure estimate) and
`scripts/vision_pc_check.py` (cooling capacity >= peak power).
For a real number, run the thermal simulation (§10).
