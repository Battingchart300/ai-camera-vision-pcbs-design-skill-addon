"""known_parts.py — verified part tables for the Camera & Vision addon.

Every value here was checked against a live source (see the `source`
field) or is marked UNVERIFIED (None). A part that is NOT in these
tables is NOT automatically wrong — but the validators treat it as
UNVERIFIED and FAIL the spec, because an unverified part must be
checked against its datasheet first (SKILL.md §0 rule 1).

Sources used (2026-11-27):
- Sony IMX477 / Raspberry Pi HQ Camera: Raspberry Pi docs + Mouser
  product brief (4056x3040, 12.3 MP, 1.55 um, rolling shutter,
  4-lane MIPI CSI-2, up to 2.1 Gbps/lane, RAW10/12, 60 fps full-res).
- Sony IMX219 / IMX708 / IMX500 / IMX296 / OV5647: Raspberry Pi
  camera documentation (raspberrypi.com/documentation/accessories/
  camera.html) — resolutions, pixel sizes, shutter types.
- onsemi AR0234: 1920x1200, 3 um, global shutter (kurokesu module
  comparison, 2026).
- MIPI CSI-2 / D-PHY lane rates: MIPI Alliance spec tables —
  D-PHY v1.1 = 1.5, v1.2 = 2.5, v2.0/v2.1 = 4.5 Gbps/lane.
- Rockchip RK3588: 6 TOPS NPU (INT8), 48 MP ISP, MIPI CSI 2x4-lane
  D-PHY v2.0 / 4x2-lane, up to 2.5 Gbps/lane, LPDDR4/4X/5 to 32 GB.
- Raspberry Pi 5 (BCM2712): 2x 4-lane MIPI CSI/DSI, 1.5 Gbps/lane
  (official Raspberry Pi documentation).
- NVIDIA Jetson Orin Nano 8GB: 40 TOPS sparse / 20 TOPS dense INT8,
  8 lanes MIPI CSI-2 D-PHY 2.1 (up to 20 Gbps total), 7/15 W.
"""
import math

# --- Image sensors -------------------------------------------------------
# lanes: max data lanes of the sensor's MIPI CSI-2 port. None = the lane
# count is UNVERIFIED for this part — the validator warns and skips the
# lane-count check instead of guessing.
SENSORS = {
    "IMX477": {
        "maker": "Sony", "width_px": 4056, "height_px": 3040,
        "mp": 12.3, "pixel_um": 1.55, "shutter": "rolling",
        "interface": "MIPI CSI-2", "lanes": 4, "supply_v": 3.3,
        "on_chip_ai": False,
        "source": "Raspberry Pi HQ Camera docs / Mouser product brief",
    },
    "IMX219": {
        "maker": "Sony", "width_px": 3280, "height_px": 2464,
        "mp": 8.0, "pixel_um": 1.12, "shutter": "rolling",
        "interface": "MIPI CSI-2", "lanes": 2, "supply_v": 3.3,
        "on_chip_ai": False,
        "source": "Raspberry Pi camera documentation",
    },
    "IMX708": {
        "maker": "Sony", "width_px": 4608, "height_px": 2592,
        "mp": 11.9, "pixel_um": 1.4, "shutter": "rolling",
        "interface": "MIPI CSI-2", "lanes": 2, "supply_v": 3.3,
        "on_chip_ai": False,
        "source": "Raspberry Pi camera documentation (Camera Module 3)",
    },
    "IMX500": {
        "maker": "Sony", "width_px": 4056, "height_px": 3040,
        "mp": 12.3, "pixel_um": 1.55, "shutter": "rolling",
        "interface": "MIPI CSI-2", "lanes": 4, "supply_v": 3.3,
        "on_chip_ai": True, "ai_tops": None,  # UNVERIFIED: no public TOPS figure
        "source": "Raspberry Pi camera documentation (AI Camera)",
    },
    "IMX296": {
        "maker": "Sony", "width_px": 1456, "height_px": 1088,
        "mp": 1.6, "pixel_um": 3.45, "shutter": "global",
        "interface": "MIPI CSI-2", "lanes": None, "supply_v": 3.3,
        "on_chip_ai": False,
        "source": "Raspberry Pi camera documentation (GS Camera)",
    },
    "OV5647": {
        "maker": "OmniVision", "width_px": 2592, "height_px": 1944,
        "mp": 5.0, "pixel_um": 1.4, "shutter": "rolling",
        "interface": "MIPI CSI-2", "lanes": 2, "supply_v": 3.3,
        "on_chip_ai": False,
        "source": "Raspberry Pi camera documentation (Camera Module v1)",
    },
    "AR0234": {
        "maker": "onsemi", "width_px": 1920, "height_px": 1200,
        "mp": 2.3, "pixel_um": 3.0, "shutter": "global",
        "interface": "MIPI CSI-2", "lanes": None, "supply_v": 3.3,
        "on_chip_ai": False,
        "source": "onsemi / kurokesu module comparison (lane count UNVERIFIED)",
    },
}

# --- Processors / SoCs ----------------------------------------------------
# mipi_lanes: total data lanes the SoC can receive. isp_max_mp: max sensor
# megapixels the built-in ISP handles (None = UNVERIFIED). npu_tops:
# INT8 TOPS, dense figure where a sparse figure also exists.
PROCESSORS = {
    "BCM2712": {
        "platform": "Raspberry Pi 5", "mipi_lanes": 4, "mipi_ports": 2,
        "mipi_max_gbps": 1.5, "isp": True, "isp_max_mp": 12.3,
        "npu_tops": 0, "interfaces": ["MIPI CSI-2"],
        "ram": ["LPDDR4X"], "pcie": True, "max_ram_gb": 16,
        "source": "Raspberry Pi 5 documentation (RP1, 2x 4-lane 1.5 Gbps)",
    },
    "BCM2711": {
        "platform": "Raspberry Pi 4", "mipi_lanes": 2, "mipi_ports": 1,
        "mipi_max_gbps": 1.0, "isp": True, "isp_max_mp": 12.3,
        "npu_tops": 0, "interfaces": ["MIPI CSI-2"],
        "ram": ["LPDDR4"], "pcie": False, "max_ram_gb": 8,
        "source": "Raspberry Pi 4 documentation (2-lane CSI-2, 1 Gbps/lane)",
    },
    "RK3588": {
        "platform": "Rockchip RK3588 SBC/SoM", "mipi_lanes": 8,
        "mipi_ports": 2, "mipi_max_gbps": 2.5, "isp": True,
        "isp_max_mp": 48, "npu_tops": 6, "interfaces": ["MIPI CSI-2"],
        "ram": ["LPDDR4", "LPDDR4X", "LPDDR5"], "pcie": True,
        "max_ram_gb": 32,
        "source": "Rockchip RK3588 datasheet (6 TOPS NPU, 48 MP ISP)",
    },
    "ESP32-S3": {
        "platform": "Espressif ESP32-S3", "mipi_lanes": 0, "mipi_ports": 0,
        "mipi_max_gbps": 0, "isp": False, "isp_max_mp": None,
        "npu_tops": 0, "interfaces": ["DVP"],
        "ram": ["PSRAM", "SRAM"], "pcie": False, "max_ram_gb": 0,
        "source": "Espressif ESP32-S3 datasheet (DVP camera interface, no MIPI CSI-2)",
    },
    "Jetson Orin Nano": {
        "platform": "NVIDIA Jetson Orin Nano 8GB", "mipi_lanes": 8,
        "mipi_ports": 2, "mipi_max_gbps": 2.5, "isp": True,
        "isp_max_mp": None, "npu_tops": 20,
        "interfaces": ["MIPI CSI-2"],
        "ram": ["LPDDR5"], "pcie": True, "max_ram_gb": 8,
        "source": "NVIDIA Jetson Orin Nano datasheet (20 TOPS dense / 40 sparse INT8, 8 lanes D-PHY 2.1, 20 Gbps total)",
    },
}

# --- MIPI D-PHY lane-rate caps (MIPI Alliance) -----------------------------
DPHY_MAX_GBPS = {"1.1": 1.5, "1.2": 2.5, "2.0": 4.5, "2.1": 4.5}

# --- Vision PC CPUs (extends PROCESSORS with generic entries) --------------
# A generic CPU is allowed but always warns: verify the exact part
# against its datasheet before ordering.
VISION_CPUS = {
    "RK3588": dict(PROCESSORS["RK3588"], verified=True),
    "BCM2712": dict(PROCESSORS["BCM2712"], verified=True),
    "BCM2711": dict(PROCESSORS["BCM2711"], verified=True),
    "Jetson Orin Nano": dict(PROCESSORS["Jetson Orin Nano"], verified=True),
    "x86_64-generic": {
        "platform": "generic x86-64 CPU", "ram": ["DDR4", "DDR5"],
        "pcie": True, "max_ram_gb": 128, "verified": False,
        "source": "generic — verify exact CPU against its datasheet",
    },
    "RISC-V-generic": {
        "platform": "generic RISC-V CPU", "ram": ["DDR4", "LPDDR4"],
        "pcie": True, "max_ram_gb": None, "verified": False,
        "source": "generic — verify exact CPU against its datasheet",
    },
}

# --- Power sources ----------------------------------------------------------
# max_w: power available to the camera at the load (after the standard's
# own losses). PoE figures are the powered-device budgets, not the
# power-sourcing-equipment figures.
POWER_SOURCES = {
    "USB-C 5V/3A": 15.0,
    "USB-C PD 20W": 20.0,
    "PoE 802.3af": 12.95,
    "PoE 802.3at": 25.5,
    "PoE 802.3bt type 3": 51.0,
    "12V DC barrel": 24.0,
    "battery-only": None,  # limited by battery discharge, checked elsewhere
}

SOLAR_EFFICIENCY = 0.75  # panel rating -> usable Wh (wiring, charge controller, heat)
