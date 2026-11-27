#!/usr/bin/env python3
"""run_all.py — run every Camera & Vision addon check, base skill first.

Order: require_base.py -> sensor_check.py -> interface_check.py ->
energy_check.py -> privacy_check.py -> thermal_check.py ->
vision_pc_check.py (only when the spec has a vision_pc section).
A missing kit script is a setup failure (exit 2), never a silent
PASS — every step is verified to exist before it runs.
Exit codes: 0 = all pass, 1 = a check failed, 2 = setup missing
(including: base skill missing, kit script missing, spec unreadable).
Standard library only.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXAMPLE = HERE.parent / "examples" / "solar_camera_trap.json"
# Credit line (v0.0.1): printed once, as the last line, in the
# audit-log footer. No online check, no popup, no behaviour change.
CREDIT = "Made by PTS6845 — https://battingchart300.github.io"
# Every script run_all depends on. Checked up front:
# a missing check must FAIL, never silently pass.
CHECKS = ["require_base.py", "sensor_check.py", "interface_check.py",
          "energy_check.py", "privacy_check.py", "thermal_check.py",
          "vision_pc_check.py"]


def run(cmd, label):
    print(f"--- {label}: {' '.join(cmd)}")
    r = subprocess.run(cmd)
    print(f"--- {label}: exit={r.returncode}")
    return r.returncode


def main():
    ap = argparse.ArgumentParser(description="Run all Camera & Vision addon checks.")
    ap.add_argument("spec", nargs="?", default=str(EXAMPLE), help="Camera spec JSON")
    ap.add_argument("--base-skill", default=None, help="Path to ai-pcb-design-skill repo")
    args = ap.parse_args()

    missing = [name for name in CHECKS if not (HERE / name).is_file()]
    if missing:
        for name in missing:
            print(f"ERROR: missing script: scripts/{name} — cannot run checks.")
        print("Audit log: run_all=FAIL (missing script), exit=2")
        return 2

    py = sys.executable
    base_args = ["--base-skill", args.base_skill] if args.base_skill else []
    spec_args = [args.spec]

    code = run([py, str(HERE / "require_base.py")] + base_args, "require_base")
    if code != 0:
        print("run_all: STOP — base skill missing. No addon check ran.")
        print(f"Audit log: run_all=FAIL (require_base), exit={code}")
        return code

    has_vision_pc = False
    try:
        has_vision_pc = "vision_pc" in json.loads(Path(args.spec).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass

    for script in ["sensor_check.py", "interface_check.py", "energy_check.py",
                   "privacy_check.py", "thermal_check.py"]:
        label = script[:-3]
        code = run([py, str(HERE / script)] + spec_args + base_args, label)
        if code != 0:
            print(f"Audit log: run_all=FAIL ({label}), exit={code}")
            return code

    if has_vision_pc:
        code = run([py, str(HERE / "vision_pc_check.py")] + spec_args + base_args,
                   "vision_pc_check")
        if code != 0:
            print("Audit log: run_all=FAIL (vision_pc_check), exit=1")
            return code
        print("Audit log: run_all=PASS (require_base, sensor_check, "
              "interface_check, energy_check, privacy_check, thermal_check, "
              "vision_pc_check), exit=0")
    else:
        print("Audit log: run_all=PASS (require_base, sensor_check, "
              "interface_check, energy_check, privacy_check, thermal_check), exit=0")
    return 0


if __name__ == "__main__":
    code = main()
    print(CREDIT)
    sys.exit(code)
