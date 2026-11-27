"""Tests for scripts/energy_check.py — solar/battery energy balance."""
from pathlib import Path

from helpers import load_example, run_check, write_spec

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_trap_passes():
    code, out = run_check("energy_check.py", EXAMPLES / "solar_camera_trap.json")
    assert code == 0, out
    assert "energy_check=PASS" in out


def test_industrial_passes():
    code, out = run_check("energy_check.py", EXAMPLES / "industrial_mipi_camera.json")
    assert code == 0, out


def test_energy_deficit_fails():
    code, out = run_check("energy_check.py", EXAMPLES / "regression_energy_deficit.json")
    assert code == 1, out
    assert "energy deficit" in out


def test_battery_too_small_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["battery"]["capacity_wh"] = 5.0  # 5 / 19.2 = 0.26 days
    code, out = run_check("energy_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "autonomy" in out


def test_peak_over_poe_budget_fails(tmp_path):
    spec = load_example("industrial_mipi_camera.json")
    spec["camera"]["power"]["peak_w"] = 30.0  # PoE 802.3at budget is 25.5 W
    code, out = run_check("energy_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "exceeds" in out


def test_solar_without_battery_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    del spec["camera"]["battery"]
    code, out = run_check("energy_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "battery" in out


def test_negative_avg_power_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["power"]["avg_w"] = -1
    code, out = run_check("energy_check.py", write_spec(tmp_path, spec))
    assert code == 1, out


def test_nan_power_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["power"]["avg_w"] = float("nan")
    code, out = run_check("energy_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
