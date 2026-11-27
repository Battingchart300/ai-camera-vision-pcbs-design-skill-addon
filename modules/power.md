# Power Management — critical

Rails, sequencing, budgets. A camera that browns out on IR-on is a
camera that misses the event.

## Rails

- Sensor analog rail separate from digital; SoC core, I/O, sensor,
  IR LEDs, storage each sized for their own peak.
- Size for **peak** current (IR LEDs on + recording + Wi-Fi
  transmitting at once), not average.
- Decoupling at every load per the part datasheets.

## Sequencing

- Rails in the datasheet order. Sensor and SoC sequencing wrong =
  a dead sensor or a boot that never finishes.

## Sources and budgets

| Source | Budget at the device |
|---|---|
| USB-C 5V/3A | 15 W |
| USB-C PD 20W | 20 W |
| PoE 802.3af | 12.95 W |
| PoE 802.3at | 25.5 W |
| PoE 802.3bt type 3 | 51 W |
| Solar + battery | battery discharge (see energy_check) |

## Checks

`scripts/energy_check.py`: peak vs. source budget, daily balance,
battery autonomy.
