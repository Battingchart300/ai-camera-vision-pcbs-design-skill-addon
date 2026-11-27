#!/usr/bin/env python3
"""sensor_check.py — sensor <-> processor compatibility.

Checks:
  * sensor part is a known, verified part (an invented part FAILs;
    "UNVERIFIED" as a part name FAILs)
  * processor part is a known, verified part
  * sensor interface matches what the processor accepts
    (e.g. a MIPI sensor on an ESP32-S3, which has DVP only, FAILs)
  * sensor lanes <= processor MIPI lanes
  * sensor resolution <= processor ISP max megapixels
  * AI model NPU demand <= processor NPU TOPS
  * bool-safe types everywhere (lanes: true is an error, not "1 lane")

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
from validators.known_parts import PROCESSORS, SENSORS
from validators.types import is_int, is_nonempty_str, is_number, is_unverified


def main():
    ap = argparse.ArgumentParser(description="Check sensor-processor compatibility.")
    ap.add_argument("spec", help="Camera spec JSON")
    ap.add_argument("--base-skill", default=None, help="Path to ai-pcb-design-skill repo")
    args = ap.parse_args()

    check_base_or_exit(args.base_skill)
    spec, err = load_spec(args.spec)
    report = Report("sensor_check")
    if err:
        print(f"SETUP ERROR: {err}")
        print(f"Audit log: sensor_check=FAIL (setup), exit=2")
        return 2

    cam = camera_section(spec, report)
    if cam is None:
        return report.finish()

    sensor = cam.get("sensor")
    if not isinstance(sensor, dict):
        report.error("missing 'camera.sensor' object")
        return report.finish()
    processor = cam.get("processor")
    if not isinstance(processor, dict):
        report.error("missing 'camera.processor' object")
        return report.finish()

    # --- sensor part ------------------------------------------------------
    part = sensor.get("part")
    if not is_nonempty_str(part):
        report.error("sensor.part must be a non-empty part name string")
        sensor_info = None
    elif is_unverified(part):
        report.error("sensor.part is UNVERIFIED — check the sensor datasheet "
                     "and name the exact part before designing")
        sensor_info = None
    else:
        sensor_info = SENSORS.get(part)
        if sensor_info is None:
            report.error(f"sensor.part '{part}' is not a known verified part "
                         "— invented or unlisted sensor (check the datasheet "
                         "and add it to validators/known_parts.py first)")

    # --- processor part ----------------------------------------------------
    proc_part = processor.get("part")
    if not is_nonempty_str(proc_part):
        report.error("processor.part must be a non-empty part name string")
        proc_info = None
    elif is_unverified(proc_part):
        report.error("processor.part is UNVERIFIED — name the exact SoC/CPU")
        proc_info = None
    else:
        proc_info = PROCESSORS.get(proc_part)
        if proc_info is None:
            report.error(f"processor.part '{proc_part}' is not a known verified "
                         "part — invented or unlisted SoC (check the datasheet "
                         "and add it to validators/known_parts.py first)")

    # --- declared resolution vs the sensor's real resolution ---------------
    if sensor_info is not None:
        for field, real in (("width_px", sensor_info["width_px"]),
                            ("height_px", sensor_info["height_px"])):
            declared = sensor.get(field)
            if declared is not None:
                if not is_int(declared):
                    report.error(f"sensor.{field} must be an integer "
                                 f"(got {declared!r})")
                elif declared != real:
                    report.error(f"sensor.{field}={declared} does not match "
                                 f"{part}: real value is {real} (datasheet)")
        declared_mp = sensor.get("resolution_mp")
        if declared_mp is not None:
            if not is_number(declared_mp):
                report.error(f"sensor.resolution_mp must be a number (got {declared_mp!r})")
            elif abs(declared_mp - sensor_info["mp"]) > 0.15:
                report.error(f"sensor.resolution_mp={declared_mp} does not match "
                             f"{part}: real value is {sensor_info['mp']} MP")

    # --- sensor lanes -------------------------------------------------------
    sensor_lanes = sensor.get("lanes")
    if sensor_lanes is not None:
        if not is_int(sensor_lanes):
            report.error(f"sensor.lanes must be an integer number of lanes "
                         f"(got {sensor_lanes!r} — a boolean is not a lane count)")
        elif sensor_lanes <= 0 or sensor_lanes > 4:
            report.error(f"sensor.lanes={sensor_lanes} out of range (1-4)")
        elif sensor_info is not None and sensor_info["lanes"] is not None \
                and sensor_lanes > sensor_info["lanes"]:
            report.error(f"sensor.lanes={sensor_lanes} exceeds what {part} "
                         f"provides ({sensor_info['lanes']} lanes)")
    elif sensor_info is not None and sensor_info["lanes"] is None:
        report.warning(f"lane count for {part} is UNVERIFIED — confirm "
                       "against the datasheet before routing")

    # --- fps ----------------------------------------------------------------
    fps = sensor.get("fps")
    if fps is not None:
        if not is_number(fps) or fps <= 0:
            report.error(f"sensor.fps must be a positive number (got {fps!r})")

    # --- processor compatibility --------------------------------------------
    if sensor_info is not None and proc_info is not None:
        if sensor_info["interface"] not in proc_info["interfaces"]:
            report.error(f"incompatible: sensor {part} uses "
                         f"{sensor_info['interface']} but processor "
                         f"{proc_part} accepts only "
                         f"{', '.join(proc_info['interfaces'])} "
                         "(e.g. MIPI sensor on a DVP-only MCU cannot work)")
        if sensor_info["interface"] == "MIPI CSI-2" and sensor_lanes is not None \
                and is_int(sensor_lanes):
            if sensor_lanes > proc_info["mipi_lanes"]:
                report.error(f"incompatible: sensor needs {sensor_lanes} MIPI "
                             f"lanes but {proc_part} provides "
                             f"{proc_info['mipi_lanes']}")
        if proc_info["isp_max_mp"] is not None \
                and sensor_info["mp"] > proc_info["isp_max_mp"]:
            report.error(f"incompatible: sensor is {sensor_info['mp']} MP but "
                         f"the {proc_part} ISP handles at most "
                         f"{proc_info['isp_max_mp']} MP")
        elif proc_info["isp_max_mp"] is None and proc_info["isp"]:
            report.warning(f"ISP max resolution for {proc_part} is UNVERIFIED "
                           "— confirm the sensor fits the ISP before designing")

    # --- AI accelerator demand ----------------------------------------------
    ai = cam.get("ai")
    if isinstance(ai, dict):
        need = ai.get("npu_tops_required")
        if need is not None:
            if not is_number(need) or need < 0:
                report.error(f"ai.npu_tops_required must be a non-negative "
                             f"number (got {need!r})")
            elif proc_info is not None and need > proc_info["npu_tops"]:
                report.error(f"incompatible: AI model needs {need} TOPS but "
                             f"{proc_part} provides {proc_info['npu_tops']} TOPS "
                             "(pick a lighter model or a stronger accelerator)")

    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
