# Camera SoC — integrated camera processors

A system-on-chip with the camera pipeline built in: ISP, video
encode, sometimes an NPU.

## Verified SoCs

| SoC | MIPI lanes | ISP max | NPU | RAM |
|---|---|---|---|---|
| BCM2712 (Pi 5) | 4 (×2 ports) | 12.3 MP | 0 | LPDDR4X |
| BCM2711 (Pi 4) | 2 | 12.3 MP | 0 | LPDDR4 |
| Rockchip RK3588 | 8 | 48 MP | 6 TOPS | LPDDR4/4X/5 |
| Jetson Orin Nano 8GB | 8 | UNVERIFIED | 20 TOPS dense | LPDDR5 |

## Choosing

- **RK3588** for a serious camera: 48 MP ISP + 6 TOPS NPU + 8
  MIPI lanes covers two cameras and on-device AI.
- **BCM2712** for a first camera: cheap, great software
  (libcamera/PiSP), one 12 MP sensor.
- **Jetson Orin Nano** for heavy AI: 20 TOPS dense, but hungrier
  (7–15 W) and pricier.
- **ESP32-S3** is NOT a camera SoC for MIPI: DVP only, no ISP, no
  NPU. Fine for a tiny low-res trap, wrong for anything serious.

## Checks

`sensor_check.py` (lanes, ISP max, TOPS), `interface_check.py`
(lane rate), `vision_pc_check.py` (RAM type/size for Vision PCs).
