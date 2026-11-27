# Privacy System — critical

Privacy is a core rule of this addon (§0.2, SKILL.md §8), not a
feature to add later.

## Rules (enforced by `scripts/privacy_check.py`)

- **Minimize:** motion/event trigger, not continuous recording;
  retention <= 30 days (prefer <= 14).
- **Process on-device:** detection and counting happen on the
  camera or the local Vision PC.
- **Upload results, not people:** counts, alerts, blurred clips.
  Raw video to the cloud with no local processing FAILs.
- **No face recognition of strangers, no mass surveillance:**
  face recognition + public space FAILs; continuous recording in a
  public space FAILs.
- **No central raw footage:** a Vision PC/server that stores raw
  footage without anonymization FAILs.

## Design guidance

- Prefer anonymous statistics: how many, which direction, how
  fast — not who.
- Blur faces in stored footage by default where people can appear.
- A camera in a public space, a workplace, or a neighbour's
  property needs a legal basis and usually a sign (GDPR in the EU).
  The skill checks the design, not the law — the human checks the
  law before installing.
- Every camera design states its privacy rules in the spec
  (`camera.privacy`). A design with no privacy section FAILs.
