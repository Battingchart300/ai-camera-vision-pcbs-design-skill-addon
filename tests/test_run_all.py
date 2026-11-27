"""Integration tests — run_all.py on the shipped examples and fixtures."""
from pathlib import Path

from helpers import BASE_SKILL, ROOT, run_script

EXAMPLES = ROOT / "examples"


def _run_all(spec):
    return run_script("run_all.py", str(spec), "--base-skill", str(BASE_SKILL))


def test_solar_camera_trap_passes():
    code, out = _run_all(EXAMPLES / "solar_camera_trap.json")
    assert code == 0, out
    assert "run_all=PASS" in out
    assert "Made by PTS6845" in out


def test_industrial_mipi_camera_passes():
    code, out = _run_all(EXAMPLES / "industrial_mipi_camera.json")
    assert code == 0, out
    assert "run_all=PASS" in out


def test_edge_vision_pc_passes_with_vision_pc_check():
    code, out = _run_all(EXAMPLES / "edge_vision_pc.json")
    assert code == 0, out
    assert "vision_pc_check" in out
    assert "run_all=PASS" in out


def test_missing_base_is_exit_2():
    code, out = run_script("run_all.py", str(EXAMPLES / "solar_camera_trap.json"),
                           "--base-skill", "/tmp/no-such-base")
    assert code == 2, out
    assert "STOP" in out


# --- regression fixtures: every one must FAIL run_all -----------------------

def test_regression_incompatible_sensor():
    code, out = _run_all(EXAMPLES / "regression_incompatible_sensor.json")
    assert code == 1, out


def test_regression_invented_part():
    code, out = _run_all(EXAMPLES / "regression_invented_part.json")
    assert code == 1, out


def test_regression_privacy_violation():
    code, out = _run_all(EXAMPLES / "regression_privacy_violation.json")
    assert code == 1, out


def test_regression_energy_deficit():
    code, out = _run_all(EXAMPLES / "regression_energy_deficit.json")
    assert code == 1, out


def test_regression_vision_pc_ram_mismatch():
    code, out = _run_all(EXAMPLES / "regression_vision_pc_ram_mismatch.json")
    assert code == 1, out


def test_regression_bool_lanes():
    code, out = _run_all(EXAMPLES / "regression_bool_lanes.json")
    assert code == 1, out


def test_regression_unverified_sensor():
    code, out = _run_all(EXAMPLES / "regression_unverified_sensor.json")
    assert code == 1, out


def test_array_root_is_exit_2(tmp_path):
    bad = tmp_path / "array.json"
    bad.write_text("[1, 2, 3]", encoding="utf-8")
    code, out = run_script("sensor_check.py", str(bad), "--base-skill", str(BASE_SKILL))
    assert code == 2, out
    assert "Traceback" not in out
