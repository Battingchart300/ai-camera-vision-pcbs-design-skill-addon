"""Tests for scripts/thermal_check.py — thermal limits."""
from pathlib import Path

from helpers import load_example, run_check, write_spec

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_trap_passes():
    code, out = run_check("thermal_check.py", EXAMPLES / "solar_camera_trap.json")
    assert code == 0, out


def test_industrial_passes():
    code, out = run_check("thermal_check.py", EXAMPLES / "industrial_mipi_camera.json")
    assert code == 0, out


def test_overheating_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["thermal"]["thermal_resistance_c_per_w"] = 10.0  # 40 + 50 = 90 > 70
    code, out = run_check("thermal_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "thermal limit exceeded" in out


def test_small_margin_warns_but_passes(tmp_path):
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["thermal"]["thermal_resistance_c_per_w"] = 5.5  # 40 + 27.5 = 67.5, margin 2.5
    code, out = run_check("thermal_check.py", write_spec(tmp_path, spec))
    assert code == 0, out
    assert "margin only" in out


def test_missing_thermal_section_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    del spec["camera"]["thermal"]
    code, out = run_check("thermal_check.py", write_spec(tmp_path, spec))
    assert code == 1, out


def test_ambient_over_operating_range_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["thermal"]["ambient_max_c"] = 70  # operating range tops at 60
    spec["camera"]["thermal"]["max_component_c"] = 125  # keep the limit itself OK
    code, out = run_check("thermal_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "operating range" in out
