# FPGA System — hardware acceleration

An FPGA for the parts a SoC cannot do: custom sensor interfaces,
line-rate preprocessing, deterministic low latency.

## When to use one

- A sensor interface the SoC does not have (odd lane counts,
  parallel sensors, multi-camera sync).
- Preprocessing at line rate (debayer, HDR merge) before the SoC.
- Deterministic latency a CPU/GPU cannot promise.

## Rules

- The FPGA design itself (RTL, timing, board) is done with the PC
  component addon (`ai-pc-component-design-skill-addon`) — this
  addon does NOT duplicate it. Link, do not copy.
- An FPGA is not a shortcut around a missing driver: the SoC still
  needs to talk to the FPGA (PCIe, MIPI, or a parallel bus).
- Power and thermal: an FPGA doing real work is hot. Budget it in
  `thermal_check.py` like any other load.
- Simulation first (Verilator) before synthesis — same rule as the
  PC addon.

## Checks

Interface and power rules of this addon apply (MIPI, energy,
thermal). The FPGA's own timing is checked by its own tools, not
by this addon.
