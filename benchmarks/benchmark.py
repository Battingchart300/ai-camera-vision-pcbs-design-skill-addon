#!/usr/bin/env python3
"""benchmark.py — theoretical estimates from a camera spec.

Every number printed is an ESTIMATE (labelled as such), computed from
the spec and the verified tables. Nothing here is a measurement: a
measured benchmark needs the real board, sensor and workload.

Estimates: sensor stream rate, link utilization, NPU utilization,
storage days, solar autonomy. Exit 0 on success, 2 on a bad spec.
Standard library only.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from common import load_spec

# UNVERIFIED placeholder: H.265 1080p30 motion-clip bitrate.
# Measure the real encoder bitrate on the board and replace it.
H265_MBPS_1080P30 = 10.0


def main():
    ap = argparse.ArgumentParser(description="Compute theoretical estimates for a camera spec.")
    ap.add_argument("spec", help="Camera spec JSON")
    args = ap.parse_args()

    spec, err = load_spec(args.spec)
    if err:
        print(f"ERROR: {err}")
        return 2
    cam = spec.get("camera", {})
    sensor = cam.get("sensor", {})
    iface = cam.get("interface", {})
    proc = cam.get("processor", {})
    power = cam.get("power", {})
    storage = cam.get("storage", {})
    solar = cam.get("solar")
    battery = cam.get("battery")

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from validators.known_parts import PROCESSORS

    print("Benchmark ESTIMATES (not measured) — "
          f"{spec.get('board', {}).get('name', 'unnamed camera')}")
    width = sensor.get("width_px", 0)
    height = sensor.get("height_px", 0)
    fps = sensor.get("fps", 0)
    bpp = sensor.get("bits_per_pixel", 10)
    rate = width * height * fps * bpp / 1e9
    print(f"  sensor stream: {rate:.2f} Gbps (ESTIMATE)")
    lanes = iface.get("lanes", 0)
    lane_rate = iface.get("lane_rate_gbps", 0)
    if lanes and lane_rate:
        util = rate / (lanes * lane_rate) * 100
        print(f"  link utilization: {util:.0f}% of {lanes * lane_rate:.1f} Gbps (ESTIMATE)")
    ai = cam.get("ai", {})
    need = ai.get("npu_tops_required")
    proc_info = PROCESSORS.get(proc.get("part", ""))
    if need is not None and proc_info is not None and proc_info["npu_tops"]:
        print(f"  NPU utilization: {need / proc_info['npu_tops'] * 100:.0f}% "
              f"of {proc_info['npu_tops']} TOPS (ESTIMATE)")
    cap_gb = storage.get("capacity_gb")
    if cap_gb:
        # Scale the 1080p30 bitrate by pixel count; duty cycle 10% default.
        pixels = max(width * height, 1)
        mbps = H265_MBPS_1080P30 * pixels / (1920 * 1080)
        duty = 0.10
        gb_per_day = mbps / 8 * 86400 * duty / 1000
        days = cap_gb / gb_per_day if gb_per_day else 0
        print(f"  storage: ~{days:.0f} days on {cap_gb} GB at 10% duty cycle "
              "(ESTIMATE, bitrate UNVERIFIED placeholder)")
    if solar and battery:
        daily = power.get("avg_w", 0) * 24
        autonomy = battery.get("capacity_wh", 0) / daily if daily else 0
        print(f"  solar autonomy: {autonomy:.1f} days without sun (ESTIMATE)")
    print("End of estimates — measure on real hardware before quoting numbers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
