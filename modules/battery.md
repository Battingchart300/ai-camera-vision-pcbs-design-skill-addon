# Battery Management — critical

The battery is what keeps the camera alive at night and in bad
weather. No BMS = no build.

## Choosing

- **Li-ion 18650:** 3.7 V nominal, ~2.6–3.5 Ah per cell (use the
  cell datasheet). 2 cells ≈ 25.9 Wh at 3.5 Ah. Good energy
  density, needs a BMS and a fuse.
- **LiFePO4:** safer, better in cold, longer life, lower density.
  The right choice for an outdoor camera that stays out all year.
- **Lead-acid:** only for a fixed install with mains charging —
  heavy, and it hates deep discharge.

## Rules

- A BMS is mandatory: overcharge, over-discharge, short-circuit,
  temperature cutoff. Fuse the battery input.
- Autonomy = capacity Wh / daily Wh, at least 1 day
  (`min_autonomy_days` — set higher for winter). Checked by
  `energy_check.py`.
- Cold kills capacity: a Li-ion cell at -20 °C gives a fraction of
  its rated Wh. Size for winter, or heat the battery (which costs
  energy too).
- A swollen, hot or punctured Li-ion cell is a fire risk: outside,
  do not charge, do not puncture further.
