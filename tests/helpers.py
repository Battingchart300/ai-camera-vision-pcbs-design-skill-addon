"""Shared helpers for the addon tests."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
EXAMPLES = ROOT / "examples"
BASE_SKILL = ROOT.parent / "ai-pcb-design-skill"


def run_script(name, *args):
    """Run a check script as a subprocess. Returns (exit_code, stdout)."""
    cmd = [sys.executable, str(SCRIPTS / name), *map(str, args)]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


def run_check(name, spec_path, *extra):
    """Run a check script on a spec, always with the real base skill."""
    return run_script(name, spec_path, "--base-skill", str(BASE_SKILL), *extra)


def load_example(name):
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def write_spec(tmp_path, spec, name="spec.json"):
    p = tmp_path / name
    p.write_text(json.dumps(spec), encoding="utf-8")
    return p
