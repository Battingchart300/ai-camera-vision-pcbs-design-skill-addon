# Solar System — high

Panel + charge controller + sun. The panel is sized from the
camera's daily energy, not from hope.

## Sizing

- Daily need = avg W × 24 h. Generation = panel W × sun hours ×
  0.75. Generation must cover the need — `energy_check.py` FAILs a
  deficit.
- Sun hours are site-specific (season, shade, latitude). Take them
  from local solar data. Winter sun hours decide the panel size,
  not summer ones.
- Margin under 25% warns: cloudy days will drain the battery.

## Panel and controller

- Panel: 10–20 W is typical for a camera trap; bigger for a
  always-on camera (which usually should not be solar at all).
- Charge controller: MPPT type, sized for the panel watts and the
  battery chemistry. A PWM controller wastes power.
- Mount the panel facing the sun (south in Europe), tilted, clean
  — dust and shade kill output faster than a small panel does.

## Checks

`scripts/energy_check.py` (generation vs. consumption).
See also `modules/solar-management.md` for the controller side.
