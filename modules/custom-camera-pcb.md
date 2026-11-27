# Custom Camera PCB

The camera's own board — when a ready-made board is not enough.

## When to build one

- The sensor, the SoC and the optics do not fit on any ready-made
  board, or the enclosure forces a custom shape.
- Otherwise: start on a ready-made board (Pi 5 + camera module)
  and move to a custom PCB only after the system works (SKILL.md
  §1: start small).

## Rules

- The base skill designs the board: spec, schematic, layout, DRC,
  BOM, fab (base §1–§11). This addon adds only the camera rules
  (MIPI routing, sensor power, optics mounting).
- Sensor placement is fixed by the optics (lens mount, focal
  distance) — place the sensor first, everything else follows.
- MIPI pairs routed first, shortest, 85 Ω (references/design-rules.md).
- Pin-by-pin check before handover (SKILL.md §11.1).

## Design status

A custom camera PCB starts as a **conceptual design**. It becomes
a **simulated design** when the SI/thermal inputs have real tool
results, and a **physically verified design** only after a built
board captures a real image.
