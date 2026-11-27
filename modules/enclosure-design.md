# Enclosure Design

Case, mechanics, mounting, sealing. The enclosure is part of the
camera, not packaging.

## Design

- **Material:** UV-stable plastic or metal for outdoors; metal
  doubles as a heatsink (see cooling-system.md).
- **Sealing:** IP66/IP67 needs sealed cable entries (glands),
  a seated gasket, and screws torqued evenly. A warped lid leaks.
- **Lens window:** glass, clean, with an IR-transparent window
  for night mode. A plastic window that fogs or scratches ruins
  the image.
- **Mounting:** the mount holds in wind and snow; the screws and
  the pole are part of the design (see safety.md).

## Outputs

- `.step` for the 3D model, `.stl` for printed parts
  (SKILL.md §13). Print a prototype, fit the board, then order
  the real case.
- Condensation: a sealed box that breathes through a bad seal
  fogs the lens. A vent or desiccant helps where the IP rating
  allows it.

## Checks

No script checks the enclosure — verify by inspection and by a
water test before the camera goes outside.
