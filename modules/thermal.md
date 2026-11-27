# Thermal — high

A sealed camera box in summer sun is an oven. Size the heat path
before the box is built.

## Model

Internal temp = ambient max + peak W × thermal resistance (°C/W)
of the enclosure. `thermal_check.py` FAILs over the hottest
component's rating and warns under 10 °C margin. It is an estimate
— for a real number, generate a case with
`simulations/thermal_input.py` and run Elmer FEM.

## Levers

- **Lower peak power:** sleep, slower fps, lighter AI model.
- **Bigger heatsink / heat spreader:** a metal plate to the case
  wall beats a small fin in still air.
- **Lighter color, shade:** a white box in sun runs much cooler
  than a black one. Shade the box if you can.
- **Ventilation:** only if the IP rating allows it (IP66/IP67
  usually does not).

## Checks

`scripts/thermal_check.py`. Operating range must cover the install
site's real temperatures.
