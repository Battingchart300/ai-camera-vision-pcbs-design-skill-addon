# Components

Only verified parts are listed. A part not listed here is not
automatically wrong — but it FAILs `sensor_check.py` until its
datasheet is checked and it is added to `validators/known_parts.py`.

## Image sensors (verified)

| Part | Resolution | Pixel | Shutter | Lanes | Source |
|---|---|---|---|---|---|
| Sony IMX477 | 4056×3040 | 1.55 µm | rolling | 4 | Raspberry Pi HQ Camera docs |
| Sony IMX219 | 3280×2464 | 1.12 µm | rolling | 2 | Raspberry Pi camera docs |
| Sony IMX708 | 4608×2592 | 1.4 µm | rolling | 2 | Raspberry Pi Camera Module 3 |
| Sony IMX500 | 4056×3040 | 1.55 µm | rolling | 4 | Raspberry Pi AI Camera (AI TOPS UNVERIFIED) |
| Sony IMX296 | 1456×1088 | 3.45 µm | global | UNVERIFIED | Raspberry Pi GS Camera |
| OmniVision OV5647 | 2592×1944 | 1.4 µm | rolling | 2 | Raspberry Pi Camera Module v1 |
| onsemi AR0234 | 1920×1200 | 3.0 µm | global | UNVERIFIED | onsemi / module comparison |

## Processors / SoCs (verified)

| Part | MIPI lanes | Max lane rate | ISP max | NPU | RAM |
|---|---|---|---|---|---|
| BCM2712 (Pi 5) | 4 (×2 ports) | 1.5 Gbps | 12.3 MP | 0 | LPDDR4X |
| BCM2711 (Pi 4) | 2 | 1.0 Gbps | 12.3 MP | 0 | LPDDR4 |
| Rockchip RK3588 | 8 | 2.5 Gbps | 48 MP | 6 TOPS | LPDDR4/4X/5 |
| ESP32-S3 | 0 (DVP only) | — | — | 0 | PSRAM/SRAM |
| Jetson Orin Nano 8GB | 8 | 2.5 Gbps | UNVERIFIED | 20 TOPS dense | LPDDR5 |

## Lenses and optics

- **M12 (S-mount):** small, fixed lenses for compact cameras
  (focal 3.04 mm on IMX219 stock, 2.75–6 mm common).
- **CS-mount / C-mount:** interchangeable lenses, HQ Camera
  (IMX477). C-mount needs a 5 mm adapter ring on a CS mount.
- **IR-cut filter:** standard on day cameras; remove it (NoIR) for
  night/IR sensitivity. Removing it is irreversible on most modules.
- **Autofocus:** IMX708 (Camera Module 3) has motorised autofocus
  (10 cm to infinity); IMX219/IMX477 are manual focus.

## Night vision

- IR LEDs: **850 nm** (faint red glow, longer range) or **940 nm**
  (invisible, shorter range). Match the LED wavelength to the
  sensor's IR sensitivity (check the datasheet — NoIR needed).
- PIR sensor: wakes the camera on motion; the main energy saver
  in a camera trap.

## Power and battery

- 18650 Li-ion: 3.7 V nominal, ~2.6–3.5 Ah per cell — use the cell
  datasheet. 2 cells = 25.9 Wh at 3.5 Ah.
- LiFePO4: safer outdoors, better in cold; lower energy density.
- PoE: 802.3af = 12.95 W, 802.3at = 25.5 W, 802.3bt type 3 = 51 W
  at the powered device.
- Solar charge controller: MPPT type; size it for the panel watts.

## Storage

- microSD: cheap, wears out — pick endurance-rated cards for
  continuous recording; check write speed against the encoder bitrate.
- eMMC: soldered, more reliable than a card slot outdoors.
- NVMe SSD: for industrial cameras and Vision PCs (needs PCIe).
