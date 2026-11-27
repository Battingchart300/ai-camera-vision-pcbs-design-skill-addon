# Simulations — inputs only, never results

This addon **cannot simulate**. It generates input files for real
simulation tools and calls them. A missing tool is reported
`NOT_RUN` or `BLOCKED` — never a fake PASS, and no verification claim
is made without evidence (SKILL.md §10).

| Generator | Tool | Input it writes |
| --- | --- | --- |
| `thermal_input.py` | Elmer FEM (`ElmerSolver`) | `.sif` heat-equation case: enclosure, sensor + SoC as heat sources, ambient from the spec |
| `si_input.py` | openEMS | XML case: one MIPI CSI-2 differential pair, 85 ohm target, D-PHY lane rate from the spec |
| `spice_input.py` | ngspice / LTspice | `.spice` netlist skeleton: input rail, buck converter model, decoupling caps |

Usage:

```bash
python simulations/thermal_input.py examples/solar_camera_trap.json out/
python simulations/si_input.py examples/industrial_mipi_camera.json out/
python simulations/spice_input.py examples/industrial_mipi_camera.json out/
```

Each generator prints one status line:

- `READY — <tool> found, run it manually` (the tool exists; the
  generator does NOT run the simulation itself — the human runs it
  and reads the real result)
- `NOT_RUN — <tool> not installed` (install the tool, then re-run)

Material values in the generated inputs (thermal conductivity,
dielectric constant, loss tangent) are marked `UNVERIFIED` unless the
spec states a measured value — take them from the enclosure / PCB
material datasheet before trusting any result.
