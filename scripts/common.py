#!/usr/bin/env python3
"""common.py — shared helpers for the Camera & Vision addon check scripts.

Every check script: (1) calls require_base first — a missing base
skill is exit 2 and NO check runs; (2) loads the spec JSON (a
non-object root or unreadable file is a clean exit-2 error, never a
traceback); (3) reports errors/warnings and exits 0/1/2.

Standard library only.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

CREDIT = "Made by PTS6845 — https://battingchart300.github.io"


def load_spec(path):
    """Load a spec JSON file. Returns (spec_dict, error_str_or_None)."""
    p = Path(path)
    if not p.is_file():
        return None, f"spec file not found: {path}"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return None, f"spec file unreadable or invalid JSON: {path} ({exc})"
    if not isinstance(data, dict):
        return None, "spec root must be a JSON object, not a list or scalar"
    return data, None


def check_base_or_exit(base_skill):
    """Run the hard base-skill stop. Returns (base_path, base_version)
    or exits the process with code 2."""
    sys.path.insert(0, str(HERE))
    from require_base import find_base_skill

    path, version = find_base_skill(base_skill)
    if path is None:
        print("BASE SKILL MISSING — STOP")
        print("This addon does not work without ai-pcb-design-skill v1.2.1+.")
        print("Load the base skill first. No addon check ran.")
        sys.exit(2)
    if version is None or version < (1, 2, 1):
        have = ".".join(map(str, version)) if version else "unknown"
        print(f"BASE SKILL TOO OLD — STOP: found v{have}, need v1.2.1+")
        sys.exit(2)
    return path, version


class Report:
    """Collects errors and warnings for one check."""

    def __init__(self, name):
        self.name = name
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)
        print(f"   ERROR: {msg}")

    def warning(self, msg):
        self.warnings.append(msg)
        print(f"   WARNING: {msg}")

    def finish(self):
        n_e, n_w = len(self.errors), len(self.warnings)
        status = "PASS" if n_e == 0 else "FAIL"
        print(f"Audit log: {self.name}={status} "
              f"({n_e} errors, {n_w} warnings), exit={0 if n_e == 0 else 1}")
        return 0 if n_e == 0 else 1


def camera_section(spec, report):
    """Return the spec's camera dict, or None (with an error) if missing."""
    cam = spec.get("camera")
    if cam is None:
        report.error("missing 'camera' section — this addon checks a camera spec")
        return None
    if not isinstance(cam, dict):
        report.error("'camera' must be an object")
        return None
    return cam
