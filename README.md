# ai-camera-vision-pcbs-design-skill-addon

Addon to `ai-pcb-design-skill` for designing smart cameras — image
sensors, ISP, AI accelerators, MIPI CSI-2, night vision, solar and
battery power, storage, thermal, cybersecurity and privacy-first
vision systems.

**Version:** 0.0.1 — 2026-11-27

> **Requires `ai-pcb-design-skill` v1.2.1+.** This addon does NOT
> work without the base skill. If the base skill is not loaded, STOP:
> `STOP — missing base skill ai-pcb-design-skill v1.2.1+. This addon does not work without it. Load the base skill first.`

## What it covers

Smart cameras, industrial cameras, camera traps, robotic vision,
security systems and traffic monitoring with anonymous statistics —
privacy-first throughout: data minimization, on-device processing,
no face recognition of strangers, no mass surveillance.

Modules (see `SKILL.md` §3): Image Sensor, ISP, AI Accelerator,
Optical System, Camera Interface (MIPI CSI-2 / USB / Ethernet),
Night Vision, Power Management, Solar System, Battery Management,
Connectivity, Storage, Thermal, Environmental / IP rating,
Cybersecurity, Privacy System — plus Custom Camera PCB, FPGA
System, Camera SoC, Solar Management, Networking, Storage System,
Custom Vision Server, Cooling System, Enclosure Design and
Custom Vision PC (Edge / Workstation / Server).

## Quickstart

```bash
# 1. Load the base skill first (ai-pcb-design-skill v1.2.1+)
# 2. Run all checks on an example:
python scripts/run_all.py examples/solar_camera_trap.json
python scripts/run_all.py examples/industrial_mipi_camera.json
python scripts/run_all.py examples/edge_vision_pc.json

# 3. Run the tests:
PYTHONPATH=$HOME/.local/lib/python3.12/site-packages python3 -m pytest tests/ -q
```

## Layout

| Path | What is in it |
|---|---|
| `SKILL.md` | The skill: rules, workflow, modules, checks |
| `modules/` | One file per module (25 modules) |
| `references/` | Architecture, components, interfaces, design rules, safety, standards |
| `scripts/` | Validators: `require_base`, `sensor_check`, `interface_check`, `energy_check`, `privacy_check`, `thermal_check`, `vision_pc_check`, `run_all` |
| `validators/` | Verified part tables + bool-safe type guards |
| `schemas/` | JSON Schema for the camera spec |
| `templates/` | Spec templates (start here for your own design) |
| `examples/` | 3 passing examples + 7 regression fixtures (must FAIL) |
| `simulations/` | Input generators for Elmer FEM / openEMS / ngspice (inputs only, never fake results) |
| `benchmarks/` | Theoretical estimates (labeled ESTIMATE, never measured) |
| `tests/` | pytest suite (91 tests) |
| `.github/workflows/` | CI: Python 3.10–3.13, pytest + validators on all examples |

## Rules that matter

- **Never invent a part, pin, datasheet value or standard.** Unknown
  value = `UNVERIFIED` + ask the user. An invented part FAILs the
  validators.
- **Privacy is core:** on-device first, retention <= 30 days, no
  face recognition of strangers, no central raw footage.
- **The skill cannot simulate.** It generates simulation inputs;
  a missing tool is `NOT_RUN`, never a fake PASS.
- **Design status is stated:** conceptual / simulated / physically
  verified — never call a concept "verified".

## Changelog

### v0.0.1 — 2026-11-27

First release: 15 priority modules + 9 extra modules + Custom
Vision PC, 6 validators + `run_all`, 3 passing examples, 7
regression fixtures, 91 pytest tests, CI on Python 3.10–3.13.

---

*Made by PTS6845 — https://battingchart300.github.io*
