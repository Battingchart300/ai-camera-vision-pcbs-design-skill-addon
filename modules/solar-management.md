# Solar Management

The controller side of solar power: MPPT, charge/discharge control,
low-power sleep.

## MPPT charge controller

- MPPT (maximum power point tracking) beats PWM — it takes more
  energy from the same panel, especially in cold/bright conditions.
- Size the controller for the panel watts and the battery chemistry
  (Li-ion vs. LiFePO4 charge profiles differ — the wrong profile
  kills the battery).
- A controller with a load output that cuts off at low battery
  protects the cells from deep discharge.

## Energy discipline

- The camera sleeps between events. Sleep current is a spec value:
  measure it, do not assume microamps.
- PIR wake first, SoC wake second: the PIR sips power, the SoC
  does not.
- Winter decides: size panel and battery for the worst month, not
  the average (see solar.md).

## Checks

`scripts/energy_check.py`: generation vs. consumption, autonomy.
The controller's own efficiency is inside the 0.75 solar factor —
if the controller datasheet says otherwise, use its number.
