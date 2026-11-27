#!/usr/bin/env python3
"""thermal_check.py — thermal limits for camera hardware.

Simple steady-state model: internal temperature = ambient max +
peak power * thermal resistance of the enclosure. It FAILs when the
result exceeds the hottest component's rating, and warns when the
margin is under 10 C.

This is an estimate, not a simulation: the skill cannot run a thermal
simulation (see simulations/ — it only generates inputs and calls the
tool). A missing simulation tool is reported NOT_RUN, never a PASS.

Exit codes: 0 = pass, 1 = fail, 2 = setup missing (base skill / spec).
Standard library only.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import Report, camera_section, check_base_or_exit, load_spec
from validators.types import is_number

WARN_MARGIN_C = 10.0


def main():
    ap = argparse.ArgumentParser(description="Check camera thermal limits.")
    ap.add_argument("spec", help="Camera spec JSON")
    ap.add_argument("--base-skill", default=None, help="Path to ai-pcb-design-skill repo")
    args = ap.parse_args()

    check_base_or_exit(args.base_skill)
    spec, err = load_spec(args.spec)
    report = Report("thermal_check")
    if err:
        print(f"SETUP ERROR: {err}")
        print(f"Audit log: thermal_check=FAIL (setup), exit=2")
        return 2

    cam = camera_section(spec, report)
    if cam is None:
        return report.finish()

    thermal = cam.get("thermal")
    if not isinstance(thermal, dict):
        report.error("missing 'camera.thermal' object")
        return report.finish()
    power = cam.get("power") if isinstance(cam.get("power"), dict) else {}

    ambient = thermal.get("ambient_max_c")
    max_c = thermal.get("max_component_c")
    rth = thermal.get("thermal_resistance_c_per_w")
    peak_w = power.get("peak_w")

    if not is_number(ambient):
        report.error(f"thermal.ambient_max_c must be a number (got {ambient!r})")
        return report.finish()
    if not is_number(max_c):
        report.error(f"thermal.max_component_c must be a number (got {max_c!r})")
        return report.finish()
    if not is_number(rth) or rth <= 0:
        report.error(f"thermal.thermal_resistance_c_per_w must be a positive "
                     f"number (got {rth!r}) — measure it or take the "
                     "enclosure maker's value, never guess")
        return report.finish()
    if not is_number(peak_w) or peak_w <= 0:
        report.error(f"power.peak_w must be a positive number (got {peak_w!r})")
        return report.finish()

    rise = peak_w * rth
    internal = ambient + rise
    margin = max_c - internal
    report.warning(f"thermal estimate: {ambient} C ambient + {peak_w} W * "
                   f"{rth} C/W = {internal:.1f} C internal "
                   f"(limit {max_c} C, margin {margin:.1f} C) — ESTIMATE, "
                   "not a simulation")
    if internal > max_c:
        report.error(f"thermal limit exceeded: {internal:.1f} C internal > "
                     f"{max_c} C component rating (bigger heatsink, lower "
                     "power, or a cooler enclosure)")
    elif margin < WARN_MARGIN_C:
        report.warning(f"thermal margin only {margin:.1f} C (< {WARN_MARGIN_C} C) "
                       "— consider a heatsink or lower peak power")

    # Operating range must cover the declared ambient.
    env = cam.get("environment") if isinstance(cam.get("environment"), dict) else {}
    op_min = env.get("operating_c_min")
    op_max = env.get("operating_c_max")
    if is_number(op_min) and is_number(op_max):
        if ambient > op_max:
            report.error(f"ambient_max_c ({ambient} C) exceeds the declared "
                         f"operating range (up to {op_max} C)")

    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
