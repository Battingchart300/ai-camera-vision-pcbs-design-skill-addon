"""Tests for scripts/vision_pc_check.py — Custom Vision PC builds."""
from pathlib import Path

from helpers import load_example, run_check, write_spec

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_edge_vision_pc_passes():
    code, out = run_check("vision_pc_check.py", EXAMPLES / "edge_vision_pc.json")
    assert code == 0, out
    assert "vision_pc_check=PASS" in out


def test_ram_mismatch_fails():
    code, out = run_check("vision_pc_check.py", EXAMPLES / "regression_vision_pc_ram_mismatch.json")
    assert code == 1, out
    assert "RAM mismatch" in out


def test_nvme_without_pcie_fails(tmp_path):
    spec = load_example("edge_vision_pc.json")
    spec["vision_pc"]["storage"] = {"type": "NVMe", "interface": "SATA", "capacity_gb": 256}
    code, out = run_check("vision_pc_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "PCIe" in out


def test_psu_too_small_fails(tmp_path):
    spec = load_example("edge_vision_pc.json")
    spec["vision_pc"]["psu"] = {"watts": 10}  # peak 12 W * 1.25 = 15 W needed
    code, out = run_check("vision_pc_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "PSU too small" in out


def test_cooling_too_weak_fails(tmp_path):
    spec = load_example("edge_vision_pc.json")
    spec["vision_pc"]["cooling"] = {"capacity_w": 5, "type": "passive"}
    code, out = run_check("vision_pc_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "cooling too weak" in out


def test_server_needs_ecc_and_redundant_psu(tmp_path):
    spec = load_example("edge_vision_pc.json")
    spec["vision_pc"]["category"] = "server"
    code, out = run_check("vision_pc_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "ECC RAM" in out
    assert "redundant PSU" in out


def test_server_with_ecc_and_redundant_psu_passes(tmp_path):
    spec = load_example("edge_vision_pc.json")
    spec["vision_pc"].update({"category": "server", "ecc_ram": True,
                              "redundant_psu": True,
                              "cpu": {"part": "x86_64-generic", "ram_type": "DDR5", "ram_gb": 64},
                              "psu": {"watts": 100}, "power": {"peak_w": 60},
                              "cooling": {"capacity_w": 65, "type": "active"}})
    code, out = run_check("vision_pc_check.py", write_spec(tmp_path, spec))
    assert code == 0, out


def test_ram_over_cpu_max_fails(tmp_path):
    spec = load_example("edge_vision_pc.json")
    spec["vision_pc"]["cpu"]["ram_gb"] = 64  # RK3588 max is 32 GB
    code, out = run_check("vision_pc_check.py", write_spec(tmp_path, spec))
    assert code == 1, out


def test_unknown_category_fails(tmp_path):
    spec = load_example("edge_vision_pc.json")
    spec["vision_pc"]["category"] = "supercomputer"
    code, out = run_check("vision_pc_check.py", write_spec(tmp_path, spec))
    assert code == 1, out


def test_generic_cpu_warns_but_passes(tmp_path):
    spec = load_example("edge_vision_pc.json")
    spec["vision_pc"]["cpu"] = {"part": "x86_64-generic", "ram_type": "DDR5", "ram_gb": 32}
    spec["vision_pc"]["cooling"] = {"capacity_w": 15, "type": "active"}
    code, out = run_check("vision_pc_check.py", write_spec(tmp_path, spec))
    assert code == 0, out
    assert "generic" in out


def test_no_vision_pc_section_passes_with_warning(tmp_path):
    code, out = run_check("vision_pc_check.py", EXAMPLES / "solar_camera_trap.json")
    assert code == 0, out
    assert "nothing to check" in out


def test_bool_ram_gb_fails(tmp_path):
    spec = load_example("edge_vision_pc.json")
    spec["vision_pc"]["cpu"]["ram_gb"] = True
    code, out = run_check("vision_pc_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
