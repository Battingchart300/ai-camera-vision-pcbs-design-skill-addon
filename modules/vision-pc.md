# Custom Vision PC

A computer for local image processing — a **conceptual design**,
not a finished production PCB. See SKILL.md §9 for the full rules.

## Categories

| Category | What it is | Typical build |
|---|---|---|
| **Edge Vision PC** | Small computer in/next to the camera | ARM SoC, NPU, LPDDR, low power |
| **Vision Workstation** | Standalone computer | x86/ARM, GPU/NPU, DDR5, NVMe SSD |
| **Vision Server** | Centralized processing of allowed data | Server CPU, ECC RAM, AI accelerators, redundancy |

## Supported areas

Custom motherboard, CPU (ARM / x86 / RISC-V), GPU, NPU, FPGA,
RAM (DDR4 / DDR5 / LPDDR4 / LPDDR5), SSD (NVMe / SATA / eMMC),
networking (Ethernet / Wi-Fi / fiber), PSU, cooling, I/O board,
custom connectors / cables / case, OS (Linux / embedded).

## Link to the PC addon

The motherboard, GPU, FPGA and RAM design lives in
`ai-pc-component-design-skill-addon` — this addon does NOT
duplicate it. It only checks the build's compatibility
(`scripts/vision_pc_check.py`): RAM type vs. CPU, NVMe vs.
interface, PSU headroom (×1.25), cooling capacity, server ECC +
redundant PSU.

## Privacy link

A Vision PC/server that stores raw footage without anonymization
FAILs. Anonymize before central storage (§8) — or keep raw footage
on the camera only.

## Example

`examples/edge_vision_pc.json` — RK3588 Edge Vision PC, passes
all validators.
