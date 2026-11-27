# Safety

## Electrical safety

- Mains-powered cameras (PoE injectors, 12 V adapters) keep mains
  away from the board: use a certified adapter, never build a
  mains supply into the camera.
- Battery: a BMS is mandatory for Li-ion/LiFePO4 (overcharge,
  over-discharge, short-circuit, temperature). No BMS = no build.
- A damaged Li-ion cell (swollen, hot, punctured) is a fire risk:
  take it outside, do not charge it, do not puncture it further.
- Fuse the battery input. Size the fuse for the wire and the load.

## IR / optical safety

- IR LEDs at 850/940 nm are invisible or nearly invisible — never
  stare into them at close range, and never point a high-power IR
  illuminator at people at close range. Keep the LED power in the
  datasheet range.
- No lasers in this addon. A laser illuminator or LiDAR is a
  separate safety case (eye safety class) — do not add one without
  its own review.

## Outdoor installation

- Mounting must hold in wind and snow: check the mount, the screws
  and the pole. A falling camera hurts people and kills the camera.
- Lightning: an outdoor PoE camera needs surge protection on the
  Ethernet run; a camera on a tall pole needs a proper ground.
- Sealing: every cable entry sealed to the IP rating (see §7).
  Water inside the box kills the board slowly.

## Safety-critical hardware

A camera that watches a road, a worksite, or a place where people
can be hurt if it fails is safety-relevant: it needs expert review
before it is built (SKILL.md §12). The skill's checks are not a
substitute for that review.
