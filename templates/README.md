# Templates

Start from a template and change the values to your design. Both
templates are the shipped examples, so they PASS the validators as
they are — change one thing at a time and re-run `run_all.py`.

| Template | Based on | For |
| --- | --- | --- |
| `camera-spec.template.json` | solar camera trap | Battery/solar cameras, camera traps |
| `vision-pc-spec.template.json` | Edge Vision PC | A camera with a local Vision PC build |

Fields you MUST change for your own design (never leave a value you
did not verify):

- `camera.sensor.part` — exact sensor part (must be in
  `validators/known_parts.py`, or add it with its datasheet first)
- `camera.processor.part` — exact SoC (same rule)
- `camera.lens.*` — focal length, mount, IR-cut
- `camera.power.*` — measure avg/peak power, do not guess
- `camera.solar.*` / `camera.battery.*` — panel watts, sun hours at
  the install site, battery Wh
- `camera.thermal.thermal_resistance_c_per_w` — from the enclosure
  maker or a measurement, never a guess
- `camera.privacy.*` — the privacy rules for YOUR install site
- `vision_pc.*` — CPU, RAM type/size, storage, PSU, cooling

Values you do not know: write `UNVERIFIED` and ask — the validators
will FAIL the spec until the value is real (SKILL.md §0 rule 2).
