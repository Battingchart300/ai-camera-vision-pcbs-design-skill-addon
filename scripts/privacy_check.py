#!/usr/bin/env python3
"""privacy_check.py — privacy and data-minimization checks.

Privacy is a core rule of this addon, not an afterthought. These are
ERRORS, not warnings:
  * face recognition combined with public-space surveillance
    (recognising strangers / mass surveillance)
  * continuous recording in a public space
  * face recognition running in the cloud (raw faces leave the device)
  * raw video uploaded to the cloud with no on-device processing
  * retention longer than 30 days (data minimization)
  * a camera trap / public camera with no stated recording trigger

Warnings: retention over 14 days; faces not blurred in a public space.

Exit codes: 0 = pass, 1 = fail, 2 = setup missing (base skill / spec).
Standard library only.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import Report, camera_section, check_base_or_exit, load_spec
from validators.types import is_bool, is_int, is_nonempty_str

MAX_RETENTION_DAYS = 30
WARN_RETENTION_DAYS = 14


def main():
    ap = argparse.ArgumentParser(description="Check camera privacy rules.")
    ap.add_argument("spec", help="Camera spec JSON")
    ap.add_argument("--base-skill", default=None, help="Path to ai-pcb-design-skill repo")
    args = ap.parse_args()

    check_base_or_exit(args.base_skill)
    spec, err = load_spec(args.spec)
    report = Report("privacy_check")
    if err:
        print(f"SETUP ERROR: {err}")
        print(f"Audit log: privacy_check=FAIL (setup), exit=2")
        return 2

    cam = camera_section(spec, report)
    if cam is None:
        return report.finish()

    priv = cam.get("privacy")
    if not isinstance(priv, dict):
        report.error("missing 'camera.privacy' object — every camera design "
                     "must state its privacy rules (see SKILL.md §8)")
        return report.finish()

    def flag(name, default=False):
        value = priv.get(name, default)
        if not is_bool(value):
            report.error(f"privacy.{name} must be true/false (got {value!r})")
            return default
        return value

    face_rec = flag("face_recognition", False)
    on_device = flag("on_device_processing", True)
    public_space = flag("public_space_surveillance", False)
    cloud_raw = flag("cloud_upload_raw", False)
    faces_blurred = flag("faces_blurred", False)

    trigger = priv.get("recording_trigger")
    if not is_nonempty_str(trigger):
        report.error("privacy.recording_trigger must name when the camera "
                     "records ('motion', 'schedule', 'continuous', ...)")
        trigger = None
    elif trigger not in ("motion", "schedule", "continuous", "manual", "event"):
        report.error(f"unknown privacy.recording_trigger '{trigger}'")

    retention = priv.get("retention_days")
    if retention is None:
        report.error("privacy.retention_days is missing — state how long "
                     "recordings are kept")
    elif not is_int(retention) or retention < 0:
        report.error(f"privacy.retention_days must be a non-negative integer "
                     f"(got {retention!r} — a boolean is not a day count)")
    else:
        if retention > MAX_RETENTION_DAYS:
            report.error(f"retention {retention} days exceeds the {MAX_RETENTION_DAYS}-day "
                         "minimization limit — keep less, or justify in writing "
                         "why longer storage is needed")
        elif retention > WARN_RETENTION_DAYS:
            report.warning(f"retention {retention} days is long — prefer "
                           f"<= {WARN_RETENTION_DAYS} days unless the use case needs more")

    # --- hard privacy rules ---------------------------------------------------
    if face_rec and public_space:
        report.error("face recognition + public-space surveillance = "
                     "recognising strangers / mass surveillance — NOT ALLOWED. "
                     "Use anonymous statistics (counts, flow) instead, or "
                     "limit recognition to a private space with consent.")
    if face_rec and not on_device:
        report.error("face recognition must run on-device — raw faces must "
                     "not leave the camera to a cloud service.")
    if public_space and trigger == "continuous":
        report.error("continuous recording in a public space = mass "
                     "surveillance — use a motion/event trigger with "
                     "anonymization instead.")
    if cloud_raw and not on_device:
        report.error("raw video uploaded to the cloud with no on-device "
                     "processing — process locally and upload only "
                     "anonymized results (counts, alerts, blurred clips).")
    if public_space and not faces_blurred and not on_device:
        report.warning("public-space camera without face blurring — blur or "
                       "anonymize people in stored footage.")

    # --- vision PC / server link ----------------------------------------------
    vpc = spec.get("vision_pc")
    if isinstance(vpc, dict):
        if vpc.get("stores_raw_footage") is True \
                and vpc.get("anonymized_before_storage") is not True:
            report.error("vision_pc stores raw footage without anonymization "
                         "— anonymize before central storage, or store only "
                         "on the camera (see SKILL.md §8/§9).")

    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
