#!/usr/bin/env python3
"""interface_check.py — camera data-interface checks (MIPI CSI-2 / USB / Ethernet).

Checks:
  * interface type matches the sensor's interface
  * data rate math: width*height*fps*bits-per-pixel must fit into
    lanes * lane_rate (a too-narrow link FAILs)
  * declared lane rate <= the D-PHY version cap
    (D-PHY v1.1 = 1.5, v1.2 = 2.5, v2.0/v2.1 = 4.5 Gbps/lane)
  * declared lanes <= processor MIPI lanes
  * USB / Ethernet variants: declared bandwidth must fit the link
  * bool-safe types everywhere (lanes: true is an error, not "1 lane")

Exit codes: 0 = pass, 1 = fail, 2 = setup missing (base skill / spec).
Standard library only.
"""
import argparse
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import Report, camera_section, check_base_or_exit, load_spec
sys.path.insert(0, str(HERE.parent))
from validators.known_parts import DPHY_MAX_GBPS, PROCESSORS, SENSORS
from validators.types import is_int, is_nonempty_str, is_number, is_unverified

# Link capacity (Gbps) for non-MIPI camera interfaces.
LINK_GBPS = {
    "USB 2.0": 0.48, "USB 3.0": 5.0, "USB 3.1": 10.0, "USB 3.2": 20.0,
    "Ethernet 100M": 0.1, "Ethernet 1GbE": 1.0, "Ethernet 2.5GbE": 2.5,
    "Ethernet 10GbE": 10.0,
}


def data_rate_gbps(width, height, fps, bpp):
    """Raw sensor stream: pixels * frames * bits, in Gbps."""
    return width * height * fps * bpp / 1e9


def main():
    ap = argparse.ArgumentParser(description="Check camera data interfaces.")
    ap.add_argument("spec", help="Camera spec JSON")
    ap.add_argument("--base-skill", default=None, help="Path to ai-pcb-design-skill repo")
    args = ap.parse_args()

    check_base_or_exit(args.base_skill)
    spec, err = load_spec(args.spec)
    report = Report("interface_check")
    if err:
        print(f"SETUP ERROR: {err}")
        print(f"Audit log: interface_check=FAIL (setup), exit=2")
        return 2

    cam = camera_section(spec, report)
    if cam is None:
        return report.finish()

    sensor = cam.get("sensor") if isinstance(cam.get("sensor"), dict) else {}
    iface = cam.get("interface")
    if not isinstance(iface, dict):
        report.error("missing 'camera.interface' object")
        return report.finish()
    processor = cam.get("processor") if isinstance(cam.get("processor"), dict) else {}

    itype = iface.get("type")
    if not is_nonempty_str(itype):
        report.error("interface.type must be a non-empty string "
                     "(e.g. 'MIPI CSI-2', 'USB 3.0', 'Ethernet 1GbE')")
        return report.finish()
    if is_unverified(itype):
        report.error("interface.type is UNVERIFIED — name the real interface")
        return report.finish()

    # Sensor resolution/fps/bpp for the bandwidth math. Fall back to the
    # known sensor table when the spec does not repeat them.
    sensor_info = SENSORS.get(sensor.get("part")) if is_nonempty_str(sensor.get("part")) else None
    width = sensor.get("width_px")
    height = sensor.get("height_px")
    fps = sensor.get("fps")
    bpp = sensor.get("bits_per_pixel", 10)
    if width is None and sensor_info is not None:
        width = sensor_info["width_px"]
    if height is None and sensor_info is not None:
        height = sensor_info["height_px"]
    if not is_int(width) or not is_int(height):
        report.error("cannot compute bandwidth: sensor width_px/height_px "
                     "must be integers (declare them or use a known sensor)")
        return report.finish()
    if fps is None:
        report.error("cannot compute bandwidth: sensor.fps is missing")
        return report.finish()
    if not is_number(fps) or fps <= 0:
        report.error(f"sensor.fps must be a positive number (got {fps!r})")
        return report.finish()
    if not is_int(bpp) or bpp not in (8, 10, 12, 14, 16):
        report.error(f"sensor.bits_per_pixel must be 8/10/12/14/16 (got {bpp!r})")
        return report.finish()

    rate = data_rate_gbps(width, height, fps, bpp)
    report.warning(f"sensor stream: {width}x{height} @ {fps} fps, {bpp} bpp "
                   f"= {rate:.2f} Gbps raw")

    if itype == "MIPI CSI-2":
        if sensor_info is not None and sensor_info["interface"] != "MIPI CSI-2":
            report.error(f"interface is MIPI CSI-2 but sensor "
                         f"{sensor.get('part')} uses {sensor_info['interface']}")
        lanes = iface.get("lanes")
        lane_rate = iface.get("lane_rate_gbps")
        dphy = str(iface.get("dphy_version", "1.2"))
        if not is_int(lanes):
            report.error(f"interface.lanes must be an integer (got {lanes!r} "
                         "— a boolean is not a lane count)")
            return report.finish()
        if lanes <= 0 or lanes > 4:
            report.error(f"interface.lanes={lanes} out of range (1-4)")
            return report.finish()
        if not is_number(lane_rate) or lane_rate <= 0:
            report.error(f"interface.lane_rate_gbps must be a positive number "
                         f"(got {lane_rate!r})")
            return report.finish()
        cap = DPHY_MAX_GBPS.get(dphy)
        if cap is None:
            report.error(f"unknown dphy_version '{dphy}' (known: "
                         f"{', '.join(sorted(DPHY_MAX_GBPS))})")
        elif lane_rate > cap:
            report.error(f"lane_rate {lane_rate} Gbps exceeds the D-PHY "
                         f"v{dphy} cap of {cap} Gbps/lane")
        capacity = lanes * lane_rate
        needed = math.ceil(rate / lane_rate) if lane_rate else 99
        if needed > lanes:
            report.error(f"link too narrow: stream needs {rate:.2f} Gbps = "
                         f"{needed} lanes at {lane_rate} Gbps/lane, but only "
                         f"{lanes} lanes declared ({capacity:.2f} Gbps)")
        elif needed == lanes:
            report.warning("link is exactly full — no headroom for blanking "
                           "overhead or a faster mode")
        proc_info = PROCESSORS.get(processor.get("part")) \
            if is_nonempty_str(processor.get("part")) else None
        if proc_info is not None and lanes > proc_info["mipi_lanes"]:
            report.error(f"interface uses {lanes} MIPI lanes but processor "
                         f"{processor.get('part')} provides "
                         f"{proc_info['mipi_lanes']}")
        if proc_info is not None and lane_rate > proc_info["mipi_max_gbps"]:
            report.error(f"lane_rate {lane_rate} Gbps exceeds what processor "
                         f"{processor.get('part')} receives "
                         f"({proc_info['mipi_max_gbps']} Gbps/lane)")
    elif itype in LINK_GBPS:
        capacity = LINK_GBPS[itype]
        if rate > capacity:
            report.error(f"link too narrow: stream needs {rate:.2f} Gbps but "
                         f"{itype} carries at most {capacity} Gbps")
        elif rate > 0.8 * capacity:
            report.warning(f"link is over 80% full ({rate:.2f} of {capacity} Gbps)")
    else:
        report.error(f"unknown interface.type '{itype}' (known: MIPI CSI-2, "
                     f"{', '.join(sorted(LINK_GBPS))})")

    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
