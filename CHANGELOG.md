# Changelog — ai-camera-vision-pcbs-design-skill-addon

## v0.0.1 — 2026-11-27

First release (local only, not published).

- 15 priority modules (sensor, ISP, AI accelerator, optics,
  interface, night vision, power, solar, battery, connectivity,
  storage, thermal, environmental, cybersecurity, privacy) + 9
  extra modules (Custom Camera PCB, FPGA System, Camera SoC, Solar
  Management, Networking, Storage System, Custom Vision Server,
  Cooling System, Enclosure Design) + Custom Vision PC (Edge /
  Workstation / Server, linked to ai-pc-component-design-skill-addon,
  no duplicated content).
- Validators: `require_base` (hard stop, exit 2), `sensor_check`
  (sensor-processor compatibility), `interface_check` (MIPI
  bandwidth, D-PHY caps), `energy_check` (solar/battery balance),
  `privacy_check` (data minimization, no mass surveillance),
  `thermal_check` (thermal limits), `vision_pc_check` (RAM/CPU,
  NVMe/PCIe, PSU, cooling, server ECC/redundancy), `run_all`.
- Verified part tables: Sony IMX477/219/708/500/296, OV5647,
  AR0234; BCM2712/2711, RK3588, ESP32-S3, Jetson Orin Nano;
  D-PHY caps 1.5/2.5/4.5 Gbps/lane. All values web-verified.
- Examples: solar camera trap, industrial MIPI camera, Edge Vision
  PC — all PASS. 7 regression fixtures — all FAIL (incompatible
  sensor, invented part, privacy violation, energy deficit, Vision
  PC RAM mismatch, boolean lanes, UNVERIFIED sensor).
- Simulations: Elmer FEM / openEMS / ngspice input generators only
  (NOT_RUN when the tool is missing, never a fake PASS).
- Benchmarks: theoretical estimates only (labeled ESTIMATE).
- Tests: 91 pytest tests, all passing.
- CI: Python 3.10–3.13 on ubuntu-latest (3.9 dropped — EOL, no
  setup-python on Ubuntu 26.04).
- Credit: "Made by PTS6845 — https://battingchart300.github.io"
  in SKILL.md, README.md and the scripts.
