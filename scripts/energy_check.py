#!/usr/bin/env python3
"""energy_check.py — energy balance for (solar) cameras.

Checks:
  * solar generation (panel W * sun hours * 0.75 usable) covers the
    daily consumption (avg W * 24 h) — otherwise an energy deficit
  * battery autonomy: capacity Wh / daily consumption >= min days
  * peak power <= the power source's budget (PoE / USB-C / DC)
  * battery capacity is a positive number; solar panel / sun hours
    are positive numbers when solar is declared
  * a camera with no power source at all FAILs
  * bool-safe types everywhere

A mains/PoE camera has no solar and no battery — those checks are
simply skipped for it. A solar camera trap needs both.

Exit codes: 0 = pass, 1 = fail, 2 = setup missing (base skill / spec).
Standard library only.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import Report, camera_section, check_base_or_exit, load_spec
sys.path.insert(0, str(HERE.parent))
from validators.known_parts import POWER_SOURCES, SOLAR_EFFICIENCY
from validators.types import is_nonempty_str, is_number, is_unverified


def main():
    ap = argparse.ArgumentParser(description="Check camera energy balance.")
    ap.add_argument("spec", help="Camera spec JSON")
    ap.add_argument("--base-skill", default=None, help="Path to ai-pcb-design-skill repo")
    args = ap.parse_args()

    check_base_or_exit(args.base_skill)
    spec, err = load_spec(args.spec)
    report = Report("energy_check")
    if err:
        print(f"SETUP ERROR: {err}")
        print(f"Audit log: energy_check=FAIL (setup), exit=2")
        return 2

    cam = camera_section(spec, report)
    if cam is None:
        return report.finish()

    power = cam.get("power")
    if not isinstance(power, dict):
        report.error("missing 'camera.power' object")
        return report.finish()

    avg_w = power.get("avg_w")
    peak_w = power.get("peak_w")
    if not is_number(avg_w) or avg_w <= 0:
        report.error(f"power.avg_w must be a positive number of watts (got {avg_w!r})")
        return report.finish()
    if not is_number(peak_w) or peak_w <= 0:
        report.error(f"power.peak_w must be a positive number of watts (got {peak_w!r})")
        return report.finish()
    if peak_w < avg_w:
        report.error(f"power.peak_w ({peak_w} W) is below power.avg_w ({avg_w} W)")

    daily_wh = avg_w * 24
    report.warning(f"daily consumption: {avg_w} W avg * 24 h = {daily_wh:.1f} Wh/day")

    source = power.get("source")
    if not is_nonempty_str(source):
        report.error("power.source must name the supply "
                     "('USB-C 5V/3A', 'PoE 802.3af', 'solar+battery', ...)")
        return report.finish()
    if is_unverified(source):
        report.error("power.source is UNVERIFIED — name the real supply")
        return report.finish()

    # --- peak power vs the source budget -----------------------------------
    budget = POWER_SOURCES.get(source)
    if source == "solar+battery":
        budget = None  # limited by battery discharge — checked via autonomy
    elif budget is None:
        report.warning(f"power.source '{source}' is not a known source — "
                       "peak-power budget not checked (verify the datasheet)")
    if budget is not None and peak_w > budget:
        report.error(f"peak power {peak_w} W exceeds the {source} budget "
                     f"of {budget} W")

    # --- solar generation ---------------------------------------------------
    solar = cam.get("solar")
    battery = cam.get("battery")
    if solar is not None:
        if not isinstance(solar, dict):
            report.error("'camera.solar' must be an object")
            return report.finish()
        panel_w = solar.get("panel_w")
        sun_h = solar.get("sun_hours_day")
        if not is_number(panel_w) or panel_w <= 0:
            report.error(f"solar.panel_w must be a positive number (got {panel_w!r})")
        elif not is_number(sun_h) or sun_h <= 0 or sun_h > 24:
            report.error(f"solar.sun_hours_day must be 0-24 (got {sun_h!r})")
        else:
            generated = panel_w * sun_h * SOLAR_EFFICIENCY
            report.warning(f"solar: {panel_w} W * {sun_h} h * {SOLAR_EFFICIENCY} "
                           f"= {generated:.1f} Wh/day")
            if generated < daily_wh:
                report.error(f"energy deficit: solar makes {generated:.1f} Wh/day "
                             f"but the camera needs {daily_wh:.1f} Wh/day "
                             "(bigger panel, more sun, or lower avg power)")
            elif generated < daily_wh * 1.25:
                report.warning("solar margin under 25% — cloudy days will "
                               "drain the battery")

    # --- battery autonomy ----------------------------------------------------
    if battery is not None:
        if not isinstance(battery, dict):
            report.error("'camera.battery' must be an object")
            return report.finish()
        cap_wh = battery.get("capacity_wh")
        if not is_number(cap_wh) or cap_wh <= 0:
            report.error(f"battery.capacity_wh must be a positive number (got {cap_wh!r})")
        else:
            min_days = cam.get("min_autonomy_days", 1)
            if not is_number(min_days) or min_days <= 0:
                report.error(f"min_autonomy_days must be a positive number "
                             f"(got {min_days!r})")
            else:
                autonomy = cap_wh / daily_wh
                report.warning(f"battery autonomy: {cap_wh} Wh / "
                               f"{daily_wh:.1f} Wh/day = {autonomy:.1f} days")
                if autonomy < min_days:
                    report.error(f"battery too small: {autonomy:.1f} days of "
                                 f"autonomy, need at least {min_days} day(s) "
                                 "(bigger battery or lower avg power)")
    elif solar is not None:
        report.error("solar panel declared but no 'camera.battery' — a solar "
                     "camera needs a battery for the night")

    if solar is None and battery is None and source == "solar+battery":
        report.error("power.source is 'solar+battery' but no solar/battery "
                     "sections are declared")

    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
