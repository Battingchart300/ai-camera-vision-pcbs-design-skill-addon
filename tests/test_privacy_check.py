"""Tests for scripts/privacy_check.py — privacy / data minimization."""
from pathlib import Path

from helpers import load_example, run_check, write_spec

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_trap_passes():
    code, out = run_check("privacy_check.py", EXAMPLES / "solar_camera_trap.json")
    assert code == 0, out
    assert "privacy_check=PASS" in out


def test_industrial_passes():
    code, out = run_check("privacy_check.py", EXAMPLES / "industrial_mipi_camera.json")
    assert code == 0, out


def test_privacy_violation_fails():
    code, out = run_check("privacy_check.py", EXAMPLES / "regression_privacy_violation.json")
    assert code == 1, out
    assert "mass surveillance" in out


def test_face_recognition_in_public_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["privacy"].update({"face_recognition": True,
                                      "public_space_surveillance": True})
    code, out = run_check("privacy_check.py", write_spec(tmp_path, spec))
    assert code == 1, out


def test_face_recognition_on_device_private_passes(tmp_path):
    # Face recognition of the owner's own household, on-device, is allowed.
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["privacy"].update({"face_recognition": True,
                                      "on_device_processing": True,
                                      "public_space_surveillance": False})
    code, out = run_check("privacy_check.py", write_spec(tmp_path, spec))
    assert code == 0, out


def test_retention_over_30_days_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["privacy"]["retention_days"] = 90
    code, out = run_check("privacy_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "minimization" in out


def test_bool_retention_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["privacy"]["retention_days"] = True
    code, out = run_check("privacy_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "boolean" in out


def test_raw_cloud_upload_without_local_processing_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["privacy"].update({"cloud_upload_raw": True,
                                      "on_device_processing": False})
    code, out = run_check("privacy_check.py", write_spec(tmp_path, spec))
    assert code == 1, out


def test_missing_privacy_section_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    del spec["camera"]["privacy"]
    code, out = run_check("privacy_check.py", write_spec(tmp_path, spec))
    assert code == 1, out


def test_vision_pc_raw_storage_fails(tmp_path):
    spec = load_example("edge_vision_pc.json")
    spec["vision_pc"]["stores_raw_footage"] = True
    spec["vision_pc"]["anonymized_before_storage"] = False
    code, out = run_check("privacy_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "anonymize" in out
