"""Tests for scripts/sensor_check.py — sensor <-> processor compatibility."""
from pathlib import Path

from helpers import load_example, run_check, write_spec

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
TRAP = "solar_camera_trap.json"
IND = "industrial_mipi_camera.json"


def test_trap_passes(tmp_path):
    code, out = run_check("sensor_check.py", EXAMPLES / TRAP)
    assert code == 0, out
    assert "sensor_check=PASS" in out


def test_industrial_passes(tmp_path):
    code, out = run_check("sensor_check.py", EXAMPLES / IND)
    assert code == 0, out


def test_incompatible_sensor_fails(tmp_path):
    spec = EXAMPLES / "regression_incompatible_sensor.json"
    code, out = run_check("sensor_check.py", spec)
    assert code == 1, out
    assert "incompatible" in out
    assert "DVP" in out or "MIPI" in out


def test_invented_part_fails(tmp_path):
    spec = EXAMPLES / "regression_invented_part.json"
    code, out = run_check("sensor_check.py", spec)
    assert code == 1, out
    assert "IMX9999" in out


def test_unverified_part_fails(tmp_path):
    spec = EXAMPLES / "regression_unverified_sensor.json"
    code, out = run_check("sensor_check.py", spec)
    assert code == 1, out
    assert "UNVERIFIED" in out


def test_wrong_resolution_fails(tmp_path):
    spec = load_example(TRAP)
    spec["camera"]["sensor"]["width_px"] = 9999
    code, out = run_check("sensor_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "does not match" in out


def test_bool_lanes_fails(tmp_path):
    spec = load_example(TRAP)
    spec["camera"]["sensor"]["lanes"] = True
    code, out = run_check("sensor_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "boolean" in out


def test_too_many_sensor_lanes_fails(tmp_path):
    spec = load_example(TRAP)
    spec["camera"]["sensor"]["lanes"] = 4  # IMX219 provides 2
    code, out = run_check("sensor_check.py", write_spec(tmp_path, spec))
    assert code == 1, out


def test_npu_demand_over_processor_fails(tmp_path):
    spec = load_example(TRAP)
    spec["camera"]["ai"] = {"model": "heavy-detector", "npu_tops_required": 5}
    code, out = run_check("sensor_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "TOPS" in out


def test_missing_sensor_fails(tmp_path):
    spec = load_example(TRAP)
    del spec["camera"]["sensor"]
    code, out = run_check("sensor_check.py", write_spec(tmp_path, spec))
    assert code == 1, out


def test_missing_base_is_exit_2(tmp_path):
    from helpers import run_script
    spec = write_spec(tmp_path, load_example(TRAP))
    code, out = run_script("sensor_check.py", spec, "--base-skill", "/tmp/no-such-base")
    assert code == 2, out
    assert "BASE SKILL MISSING" in out
