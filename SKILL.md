---
name: ai-camera-vision-pcbs-design-skill-addon
description: Addon to ai-pcb-design-skill (REQUIRED, v1.2.1+) for smart cameras — CMOS/CCD sensor, ISP, AI accelerator, optics, MIPI CSI-2/USB/Ethernet, night vision, power, solar, battery, Wi-Fi/LTE/PoE, storage, IP rating, cybersecurity and privacy. Plus Custom Vision PC (Edge/Workstation/Server) for local image processing. Does NOT work without the base skill. Use when designing a camera or a vision system with an AI.
---

# ai-camera-vision-pcbs-design-skill-addon

**Version:** 0.0.1 — 2026-11-27

**What it is:** an addon skill for designing cameras and vision
systems — smart cameras, industrial cameras, camera traps, robotic
vision, security systems and traffic monitoring with anonymous
statistics — on top of `ai-pcb-design-skill`. It adds only the
camera/vision parts: sensor, ISP, AI accelerator, optics, MIPI
CSI-2, night vision, solar/battery power, storage, thermal,
environment, cybersecurity and privacy. Everything else (spec,
schematic, layout, DRC, BOM, fab) comes from the base skill.

**Who it is for:** the same user as the base skill — a beginner who
designs boards and lets the AI do the drafting, while the human stays
in charge of every decision that matters — now for a camera.

**How to use it:** load the base skill first, then this file. It works
with any AI backend, like the base skill. If a step needs a tool that
does not exist in your environment (for example `kicad-cli`,
`openEMS` or `ElmerSolver`), the skill says so and tells you the
manual alternative — it never pretends a check ran when it did not.

---

## 0. Prerequisite — hard stop: this skill does NOT work alone

Read this section first. Nothing below it applies without it.

1. **This addon REQUIRES `ai-pcb-design-skill` v1.2.1 or newer.**
   Before ANY work, load the base `SKILL.md`, confirm its `name` is
   `ai-pcb-design-skill` and its version is >= 1.2.1.
2. **If the base skill is not loaded / not found, STOP.**
   Do not continue, do not guess, do not work from this file alone.
   Say exactly this and wait for the human:
   > `STOP — missing base skill ai-pcb-design-skill v1.2.1+. This addon does not work without it. Load the base skill first.`
3. **The kit enforces the same stop.** `scripts/run_all.py` and every
   check script call `scripts/require_base.py` first. If the base
   skill is not found, they exit with code `2` (setup missing) and
   run **no** addon check. A missing base is a setup failure, never
   a pass.
4. **Nothing in this addon replaces the base skill.** The base spec
   format, hard rules, gated workflow, routing rules, DRC, BOM,
   trace-width and fab rules still apply in full. This addon only
   *extends* them. If the two disagree, the base skill wins on PCB
   rules, this addon wins only on camera/vision numbers in §3–§10.
5. **A failed base gate stops the addon work too.** If the base spec
   fails `rules_check.py`, or DRC fails, fix the base first. Do not
   proceed to an addon stage on top of a failing base stage.

### 0.1 Hard rules inherited from the base skill

All 10 hard rules of the base skill (§0) apply unchanged, in
particular:

- Never invent a part number, pin, footprint, datasheet value or
  fab limit. If a value cannot be verified, write `UNVERIFIED`
  and cite the file and page where it should be checked.
- **When you do not know a value, ASK the user.** Never invent a
  size, a voltage, a pin assignment or a part. A question costs a
  minute; a wrong guess costs a respin.
- Verify on the web, never from memory. Datasheets and fab limits
  are checked against live sources. Memory is not a source.
- Never disable, filter or loosen a check. A waiver (knowingly
  breaking a rule) is a human decision, written down with a reason.
- The model never decides correctness. The scripts in `scripts/`
  verify the design (exit 0 = pass, 1 = fail, 2 = setup missing).
- Never order, upload or publish anything. The order is placed
  only by the human, manually, with human review.
- Never claim a check ran if it did not run.
- Never destroy the user's work. Checkpoint before the first change.
- A failed gate stops the work. Fix the cause, re-run the *same*
  check. If a stage fails 3 times, stop and ask the human.
- The schematic is the design; the layout is only its physical
  implementation.

### 0.2 Privacy is a core rule, not an afterthought

- **Data minimization:** record as little as possible — motion or
  event trigger instead of continuous recording, short retention
  (<= 30 days, prefer <= 14), no audio unless the use case needs it.
- **On-device processing first:** detect, count and classify on the
  camera or the local Vision PC. Upload only anonymized results
  (counts, alerts, blurred clips) — never raw footage of people.
- **No face recognition of strangers, no mass surveillance.**
  Face recognition is allowed only on-device, in a private space,
  for people who consented. Continuous recording of a public space
  is not allowed — use anonymous statistics (counts, flow) instead.
- **No central storage of non-anonymized footage without a reason.**
  A Vision Server stores anonymized data; raw footage stays on the
  camera or is deleted. `scripts/privacy_check.py` enforces this.

---

## 1. Gated workflow — addon stages

Work in stages. Each stage ends in a **gate**. The base workflow
(base §1, stages 0–10) still runs underneath; the addon stages run
*inside* it, mostly between base stages 1–4.

| Stage | Do | Gate |
|---|---|---|
| C0. Prerequisite | Load base skill, confirm version >= 1.2.1. | `scripts/require_base.py` passes. |
| C1. Requirements | Write the camera spec (§2): sensor, processor, optics, interface, power, privacy. | All `scripts/*_check.py`: 0 errors. Human approves the spec. |
| C2. Architecture | Block diagram: sensor + ISP + accelerator + power + storage. Pick parts from datasheets. | Every active part has MPN + datasheet + footprint. |
| C3. Simulation inputs | Generate inputs for SI/thermal/SPICE tools (§10). | Inputs generated; tools report READY or NOT_RUN — never a fake PASS. |
| C4. Schematic + stackup | Base schematic + MIPI routing rules (§5). | Base ERC 0 errors; stackup matches the fab. |
| C5. Layout + checks | Route MIPI first, then power, then the rest. Pin-by-pin check (§11). | `kicad-cli pcb drc`: 0 errors; addon checks 0 errors. |
| C6. Bring-up | First image, focus, night mode, solar/battery test. | Real image captured; night mode works; battery survives a night. Human sign-off. |

**Human review stops:** after the spec (C1), after the architecture
(C2), after the simulation inputs (C3), and before the order (base
stage 10). **Structural changes need the human:** the model never
changes the sensor, the processor, the interface or the power source
without asking.

**Start small, on purpose:** the first working target is one sensor
on a ready-made board (for example a Raspberry Pi 5 + IMX477), not a
custom camera PCB. Only when that captures, streams and survives a
night does the design move to a custom board.

---

## 2. Spec-first — the camera spec

The camera spec **extends** the base spec (`kit/examples/spec.json`
in the base skill). It never replaces it. A board that uses this
addon has both: a base spec (board, parts, nets) **and** a camera
spec (this section). The shipped examples are
`examples/solar_camera_trap.json` and
`examples/industrial_mipi_camera.json`; the JSON Schema is
`schemas/camera-spec.schema.json`.

```json
{
  "board": {"name": "Solar Camera Trap", "layers": 4, "fab": "jlcpcb"},
  "camera": {
    "sensor": {"part": "IMX219", "width_px": 3280, "height_px": 2464,
               "lanes": 2, "fps": 10, "bits_per_pixel": 10},
    "processor": {"part": "BCM2712", "platform": "Raspberry Pi 5"},
    "lens": {"focal_length_mm": 3.04, "mount": "M12", "ir_cut": false},
    "interface": {"type": "MIPI CSI-2", "lanes": 2,
                  "lane_rate_gbps": 1.0, "dphy_version": "1.1"},
    "night_vision": {"ir_led_nm": 850, "ir_led_count": 2, "pir": true},
    "power": {"source": "solar+battery", "input_v": 5,
              "avg_w": 0.8, "peak_w": 5.0},
    "solar": {"panel_w": 20, "sun_hours_day": 3.5},
    "battery": {"type": "Li-ion 18650", "capacity_wh": 25.9, "cells": 2},
    "connectivity": {"wifi": true, "lte": false, "ethernet": false, "poe": false},
    "storage": {"type": "microSD", "capacity_gb": 128},
    "thermal": {"ambient_max_c": 40, "max_component_c": 70,
                "thermal_resistance_c_per_w": 5.0},
    "environment": {"ip_rating": "IP66", "operating_c_min": -20, "operating_c_max": 60},
    "security": {"tls": true, "secure_boot": true, "default_password_changed": true},
    "privacy": {"on_device_processing": true, "face_recognition": false,
                "retention_days": 7, "recording_trigger": "motion",
                "faces_blurred": false, "public_space_surveillance": false,
                "cloud_upload_raw": false}
  }
}
```

**Lint the camera spec before drawing anything:**

```bash
python scripts/run_all.py examples/solar_camera_trap.json
# runs require_base, then sensor, interface, energy, privacy,
# thermal checks — and vision_pc_check when the spec has one
```

Errors that stop the work: unknown/invented sensor or processor,
MIPI sensor on a DVP-only processor, a link too narrow for the
stream, a lane rate over the D-PHY cap, an energy deficit (solar
makes less than the camera needs), a battery with under 1 day of
autonomy, a privacy violation, a thermal limit exceeded, a Vision PC
RAM mismatch.

**Rule: nothing is drawn until the base spec has 0 errors AND the
camera spec has 0 errors.** A warning may stay only with a reason
written in a note on the sheet.

---

## 3. Modules

| # | Module | Priority | File | What it covers |
|---|---|---|---|---|
| 1 | Image Sensor (CMOS/CCD) | critical | `modules/sensor.md` | Sensor choice, resolution, shutter, lanes |
| 2 | ISP | critical | `modules/isp.md` | Debayer, HDR, 3DNR, tuning |
| 3 | AI Accelerator (NPU/GPU/TPU/FPGA) | high | `modules/accelerator.md` | On-device inference, TOPS budget |
| 4 | Optical System | high | `modules/optics.md` | Lens, mount, focus, IR-cut |
| 5 | Camera Interface (MIPI CSI-2/USB/Ethernet) | critical | `modules/interface.md` | Link bandwidth, lane math |
| 6 | Night Vision | high | `modules/night-vision.md` | IR 850/940 nm, PIR, NoIR |
| 7 | Power Management | critical | `modules/power.md` | Rails, sequencing, budgets |
| 8 | Solar System | high | `modules/solar.md` | Panel, charge controller, sun hours |
| 9 | Battery Management | critical | `modules/battery.md` | Li-ion/LiFePO4, BMS, autonomy |
| 10 | Connectivity (Wi-Fi/LTE/Ethernet/PoE) | high | `modules/connectivity.md` | Links, PoE budgets, ONVIF/RTSP |
| 11 | Storage (SD/eMMC/SSD) | high | `modules/storage.md` | Card/SSD sizing, wear, retention |
| 12 | Thermal | high | `modules/thermal.md` | Enclosure, heatsink, limits |
| 13 | Environmental / IP rating | high | `modules/environmental.md` | IP66/IP67, temperature, sealing |
| 14 | Cybersecurity | critical | `modules/cybersecurity.md` | TLS, secure boot, passwords, updates |
| 15 | Privacy System | critical | `modules/privacy.md` | Minimization, anonymization, retention |
| 16 | Custom Camera PCB | — | `modules/custom-camera-pcb.md` | The camera's own board (base skill rules apply) |
| 17 | FPGA System | — | `modules/fpga-system.md` | Hardware acceleration with an FPGA |
| 18 | Camera SoC | — | `modules/camera-soc.md` | Integrated camera processors |
| 19 | Solar Management | — | `modules/solar-management.md` | MPPT, charge/discharge control |
| 20 | Networking | — | `modules/networking.md` | Network architecture, protocols |
| 21 | Storage System | — | `modules/storage-system.md` | Local + central storage design |
| 22 | Custom Vision Server | — | `modules/custom-vision-server.md` | Central compute for allowed image data |
| 23 | Cooling System | — | `modules/cooling-system.md` | Passive/active cooling design |
| 24 | Enclosure Design | — | `modules/enclosure-design.md` | Case, mechanics, mounting, sealing |
| 25 | Custom Vision PC | — | `modules/vision-pc.md` | Edge / workstation / server (§9) |

Scope: industrial cameras, robotic vision, camera traps, traffic
monitoring with anonymous statistics, smart camera systems — not
one camera type only.

---

## 4. Sensor and processor compatibility

Verified parts live in `validators/known_parts.py` — only those
parts pass `sensor_check.py`. Anything else FAILs until its
datasheet is checked and the part is added.

| Sensor | Resolution | Pixel | Shutter | Interface | Lanes |
|---|---|---|---|---|---|
| Sony IMX477 | 4056×3040 (12.3 MP) | 1.55 µm | rolling | MIPI CSI-2 | 4 |
| Sony IMX219 | 3280×2464 (8 MP) | 1.12 µm | rolling | MIPI CSI-2 | 2 |
| Sony IMX708 | 4608×2592 (11.9 MP) | 1.4 µm | rolling | MIPI CSI-2 | 2 |
| Sony IMX500 | 4056×3040 (12.3 MP) | 1.55 µm | rolling | MIPI CSI-2 | 4 |
| Sony IMX296 | 1456×1088 (1.6 MP) | 3.45 µm | global | MIPI CSI-2 | UNVERIFIED |
| OmniVision OV5647 | 2592×1944 (5 MP) | 1.4 µm | rolling | MIPI CSI-2 | 2 |
| onsemi AR0234 | 1920×1200 (2.3 MP) | 3.0 µm | global | MIPI CSI-2 | UNVERIFIED |

| Processor | MIPI lanes | Max lane rate | ISP max | NPU |
|---|---|---|---|---|
| BCM2712 (Raspberry Pi 5) | 4 (×2 ports) | 1.5 Gbps | 12.3 MP | 0 TOPS |
| BCM2711 (Raspberry Pi 4) | 2 | 1.0 Gbps | 12.3 MP | 0 TOPS |
| Rockchip RK3588 | 8 | 2.5 Gbps | 48 MP | 6 TOPS |
| ESP32-S3 | 0 (DVP only) | — | — | 0 TOPS |
| NVIDIA Jetson Orin Nano 8GB | 8 | 2.5 Gbps | UNVERIFIED | 20 TOPS dense |

Rules: the sensor interface must be one the processor accepts (a
MIPI sensor on an ESP32-S3 cannot work — it has DVP only); sensor
lanes <= processor lanes; sensor megapixels <= ISP max; the AI
model's TOPS demand <= the processor's NPU TOPS. Sony IMX500 has
on-chip AI; its TOPS figure is not public — UNVERIFIED, do not quote
a number for it.

---

## 5. Camera interfaces

- **MIPI CSI-2** is the default for a sensor on the same board.
  Data rate = width × height × fps × bits-per-pixel. The link must
  carry it: lanes × lane_rate >= stream rate.
- **D-PHY lane caps (MIPI Alliance):** v1.1 = 1.5, v1.2 = 2.5,
  v2.0/v2.1 = 4.5 Gbps/lane. A declared rate over the cap FAILs.
- **C-PHY** reaches up to 5.7 Gsps per trio — only when the sensor
  and the processor both support it; do not assume it.
- **USB:** USB 2.0 = 0.48, USB 3.0 = 5, USB 3.1 = 10, USB 3.2 = 20
  Gbps. A stream over the link capacity FAILs.
- **Ethernet:** 100M / 1GbE / 2.5GbE / 10GbE. RTSP/ONVIF on top.
- Control goes over I2C (CCI) — 100 kHz / 400 kHz / 1 MHz — never
  over the MIPI data lanes.
- Keep MIPI traces short, 85 Ω differential, over an unbroken GND
  plane (base skill §7). A long flex cable needs a re-driver or a
  slower lane rate — verify, do not assume.

---

## 6. Power, solar and battery

- **Budget first:** avg watts × 24 h = daily Wh. Peak watts must
  fit the source budget: USB-C 5V/3A = 15 W, PoE 802.3af = 12.95 W
  at the device, 802.3at = 25.5 W, 802.3bt type 3 = 51 W.
- **Solar:** generation = panel W × sun hours × 0.75 (wiring,
  charge controller, heat). Generation must cover daily use — a
  deficit FAILs. Sun hours are site-specific: measure or take them
  from local solar data, never guess. Margin under 25% warns.
- **Battery:** autonomy = capacity Wh / daily Wh, at least 1 day
  (set `min_autonomy_days` higher for winter). A solar camera with
  no battery FAILs. Li-ion 18650 = 3.7 V nominal, ~2.6–3.5 Ah per
  cell (use the cell datasheet, not a round number). LiFePO4 is
  safer outdoors and handles cold better; a BMS is mandatory.
- **Sleep matters:** a camera trap lives on its duty cycle. PIR
  wake + short clips beat continuous recording by 10× or more on
  energy. State the duty cycle in the spec; `avg_w` must already
  include it.
- **Sequencing:** sensor, ISP and SoC rails in the datasheet order
  (base skill §6.1). A wrong order can damage the sensor.

---

## 7. Thermal and environment

- **Estimate:** internal temp = ambient max + peak W × thermal
  resistance (°C/W) of the enclosure. Over the hottest component's
  rating FAILs; margin under 10 °C warns. This is an estimate, not
  a simulation — see §10.
- **Sealed boxes cook:** an IP66/IP67 camera trap in summer sun
  easily hits 60–70 °C inside. A heatsink, a lighter color, shade,
  or lower peak power are the levers. Dark enclosures in direct sun
  are a thermal trap.
- **IP ratings (IEC 60529):** IP66 = dust-tight + powerful water
  jets; IP67 = dust-tight + 1 m immersion for 30 min. IP66 is
  enough for rain; IP67 is for flooding risk. State the rating in
  the spec and seal every cable entry.
- **Operating range:** the spec's `operating_c_min/max` must cover
  the install site's real temperatures, including the ambient max
  used in the thermal check.

---

## 8. Privacy and security

Privacy rules (enforced by `scripts/privacy_check.py`):

- Retention over 30 days FAILs. Over 14 days warns.
- Face recognition + public-space surveillance FAILs.
- Face recognition outside the device (cloud) FAILs.
- Continuous recording in a public space FAILs.
- Raw video to the cloud with no on-device processing FAILs.
- A camera with no `privacy` section at all FAILs.
- A Vision PC/server that stores raw footage without
  anonymization FAILs.

Security rules:

- TLS on every network service; no plain HTTP admin, no open RTSP
  without auth. Default passwords must be changed
  (`security.default_password_changed: true`).
- Secure boot where the SoC supports it; signed firmware updates.
- No hard-coded credentials in firmware, no debug UART left open
  on a shipped board.
- Keep a software update path: a camera that cannot be patched is
  a camera that will be owned.

Legal note (not legal advice): recording people is regulated —
  in the EU by the GDPR and national law. A camera in a public
  space, a workplace, or a neighbour's property needs a legal basis
  and usually a sign. The skill checks the design, not the law —
  the human checks the law before installing.

---

## 9. Custom Vision PC — local image processing computer

A Vision PC is a **conceptual design** for a computer that processes
image data locally (not a finished production PCB). It links to the
PC component addon (`ai-pc-component-design-skill-addon`) for the
motherboard, GPU, FPGA and RAM design — **this addon does NOT
duplicate that content**; it only checks the build's compatibility.
`scripts/vision_pc_check.py` validates the `vision_pc` section of a
spec (example: `examples/edge_vision_pc.json`).

| Category | What it is | Typical build |
|---|---|---|
| **Edge Vision PC** | Small computer inside / next to the camera | ARM SoC, NPU, LPDDR, low power |
| **Vision Workstation** | Standalone computer | x86/ARM, GPU/NPU, DDR5, NVMe SSD |
| **Vision Server** | Centralized processing of allowed image data | Server CPU, ECC RAM, AI accelerators, redundant systems |

Supported areas: custom motherboard, CPU (ARM / x86 / RISC-V),
GPU, NPU, FPGA, RAM (DDR4 / DDR5 / LPDDR4 / LPDDR5), SSD
(NVMe / SATA / eMMC), networking (Ethernet / Wi-Fi / fiber), PSU,
cooling, I/O board, custom connectors / cables / case, OS
(Linux / embedded).

Compatibility rules (enforced by the validator):

- RAM type must match the CPU (RK3588 takes LPDDR4/4X/5 — DDR5
  FAILs; BCM2712 takes LPDDR4X; x86 takes DDR4/DDR5).
- RAM size <= the CPU's max (RK3588: 32 GB).
- NVMe storage needs a PCIe interface.
- PSU watts >= peak power × 1.25 headroom.
- Cooling capacity >= peak power.
- A **server** needs ECC RAM and a redundant PSU (both are errors
  when missing).
- Privacy link: a server that stores raw footage without
  anonymization FAILs — anonymize before central storage, or keep
  raw footage on the camera only (§8).

---

## 10. Simulations — the skill cannot simulate

The skill **cannot** run a signal-integrity, electromagnetic or
thermal simulation. It only **generates inputs and calls the tool**:

| Tool | What the skill does |
|---|---|
| openEMS | `simulations/si_input.py` writes a MIPI pair case |
| Elmer FEM | `simulations/thermal_input.py` writes a heat case |
| ngspice / LTspice | `simulations/spice_input.py` writes a power-rail deck |

Each generator prints exactly one status:

- `READY` — the tool is installed; run it manually and read its output.
- `NOT_RUN` — the tool is not installed; no simulation ran.
- `BLOCKED` — the tool exists but cannot run (missing input, license, mesh).

**A missing tool is never a PASS.** No verification claim is made
without evidence: a simulation result counts only when the tool
actually ran and its output was read. Material values in generated
inputs are UNVERIFIED placeholders until taken from a datasheet.

---

## 11. Workflows

### 11.1 Component → schematic → layout → pin-by-pin check

(inspired by the tunestechtips workflow)

1. **Pick the parts** — sensor, processor, lens, power, storage —
   each with a datasheet. No part without a datasheet.
2. **Draw the schematic** in KiCad from the spec (§2).
3. **Lay out the board** in KiCad (multi-pass placement, §11.2).
4. **Pin-by-pin check (mandatory before handover):** go through
   every pin of every part — sensor, processor, power, connectors
   — and check it against the datasheet: connected to the right net,
   right voltage, right pull-up/down, no pin left floating that
   must not float. The check is done pin by pin, not by sampling.
   A board is not handed over with an unchecked pin.

### 11.2 One prompt → finished board: multi-pass placement, batched routing

(inspired by the protoflow.ai workflow — a procedure, not a claim
that the skill does this by itself)

1. **Placement in passes:** pass 1 = sensor + lens mount + MIPI
   connector (fixed by optics); pass 2 = processor + RAM; pass 3 =
   power; pass 4 = connectors and the rest. Re-run DRC after every
   pass.
2. **Routing in batches:** batch 1 = MIPI pairs first (shortest,
   matched, 85 Ω); batch 2 = power; batch 3 = everything else.
   Run DRC after every batch.
3. **Target: 0 DRC errors.** A batch that adds a DRC error is
   reworked before the next batch starts — errors are never left
   to "fix at the end".

---

## 12. Quality rules

- **Design status is always stated:** a design is a *conceptual
  design*, a *simulated design*, or a *physically verified design*.
  Never call a conceptual design "verified" — it is not.
- **ERC, DRC and DFM checks run automatically whenever the tools
  are available** (KiCad CLI, base skill checks, addon checks). When
  a tool is missing, the report says so — a skipped check is a gap,
  not a pass.
- **Every error, warning and UNVERIFIED parameter is logged** in
  the audit log. Nothing is silently dropped.
- **Hardware revisions and backward compatibility:** every board
  revision gets a version (v1.0, v1.1, ...), a changelog entry, and
  a note on what changed and whether old firmware / old enclosures
  still fit. A breaking change is called out, never hidden.
- **Safety-critical hardware needs expert review.** A camera that
  watches a road, a worksite, or a place where people can be hurt
  if it fails is safety-relevant: a second pair of qualified eyes
  reviews the design before it is built. The skill's checks are not
  a substitute.
- **Prefer anonymization, local processing and data minimization**
  in every camera design (§0.2, §8) — including Vision PC and
  Vision Server builds (§9).

---

## 13. Output formats

The skill supports these outputs (produced by the base skill, KiCad,
and the addon scripts together):

`.kicad_pcb`, `.kicad_sch`, `.kicad_pro`, `.step`, `.stl`, `.gbr`,
`.drl`, `.csv` (BOM), `.json`, `.yaml`, `.md`, `.pdf`, `.spice`, `.zip`

- `.kicad_*` — KiCad project files (base skill).
- `.step` / `.stl` — 3D model / enclosure print files.
- `.gbr` / `.drl` — Gerber + drill files for the fab.
- `.csv` — BOM. `.json` / `.yaml` — specs, configs, reports.
- `.md` / `.pdf` — review reports and documentation.
- `.spice` — simulation decks from `simulations/` (§10).
- `.zip` — the fab pack (Gerbers + drill + BOM + CPL).

---

## 14. Engines note

A proposal listed 14 "engines" (Architecture, Component, Schematic,
PCB, Routing, Signal Integrity, Power Integrity, Thermal,
Simulation, Mechanical, Connector, Compatibility, Firmware,
Manufacturing, Security, Validation, Documentation, Cost,
Benchmark). **Those are NOT built here.** The core skill (the base
`ai-pcb-design-skill`) already provides them as its workflow and
checks — this addon only *uses* them for camera designs. Do not
re-implement them in this addon.

---

## 15. Checks

| Script | What it checks | Run |
|---|---|---|
| `scripts/require_base.py` | Base skill present, name exact, version >= 1.2.1 | first, always |
| `scripts/sensor_check.py` | Sensor ↔ processor compatibility | `run_all.py` |
| `scripts/interface_check.py` | Link bandwidth, D-PHY caps | `run_all.py` |
| `scripts/energy_check.py` | Solar / battery energy balance | `run_all.py` |
| `scripts/privacy_check.py` | Privacy rules, data minimization | `run_all.py` |
| `scripts/thermal_check.py` | Thermal limits (estimate) | `run_all.py` |
| `scripts/vision_pc_check.py` | Vision PC build compatibility | when spec has `vision_pc` |
| `scripts/run_all.py` | All of the above, in order | `python scripts/run_all.py <spec>` |

Exit codes everywhere: `0` = pass, `1` = fail, `2` = setup missing
(base skill, spec, or script). A check that did not run is never a
pass.

---

*Made by PTS6845 — https://battingchart300.github.io*
