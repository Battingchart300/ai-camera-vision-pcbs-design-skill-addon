"""Tests for scripts/interface_check.py — data-interface bandwidth."""
from pathlib import Path

from helpers import load_example, run_check, write_spec
from interface_check import data_rate_gbps

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_data_rate_math():
    # 1920x1080 @ 30 fps, 10 bpp = 0.62208 Gbps
    assert abs(data_rate_gbps(1920, 1080, 30, 10) - 0.62208) < 1e-6
    # 4056x3040 @ 30 fps, 10 bpp = 3.699072 Gbps
    assert abs(data_rate_gbps(4056, 3040, 30, 10) - 3.699072) < 1e-6


def test_trap_passes(tmp_path):
    code, out = run_check("interface_check.py", EXAMPLES / "solar_camera_trap.json")
    assert code == 0, out


def test_industrial_passes(tmp_path):
    code, out = run_check("interface_check.py", EXAMPLES / "industrial_mipi_camera.json")
    assert code == 0, out


def test_link_too_narrow_fails(tmp_path):
    spec = load_example("industrial_mipi_camera.json")
    spec["camera"]["interface"]["lanes"] = 1  # needs 3 at 1.5 Gbps/lane
    code, out = run_check("interface_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "too narrow" in out


def test_lane_rate_over_dphy_cap_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["interface"]["lane_rate_gbps"] = 2.5  # D-PHY v1.1 caps at 1.5
    code, out = run_check("interface_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "D-PHY" in out


def test_bool_lanes_fails(tmp_path):
    code, out = run_check("interface_check.py", EXAMPLES / "regression_bool_lanes.json")
    assert code == 1, out
    assert "boolean" in out


def test_lanes_over_processor_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["interface"]["lanes"] = 4
    spec["camera"]["sensor"]["lanes"] = 4
    # BCM2712 has 4 lanes total, so use a 2-lane processor instead:
    spec["camera"]["processor"] = {"part": "BCM2711", "platform": "Raspberry Pi 4"}
    spec["camera"]["sensor"] = {"part": "IMX477", "width_px": 4056, "height_px": 3040,
                                "lanes": 4, "fps": 30, "bits_per_pixel": 10}
    spec["camera"]["interface"]["lane_rate_gbps"] = 1.0
    code, out = run_check("interface_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "provides 2" in out


def test_usb_link_too_narrow_fails(tmp_path):
    spec = load_example("industrial_mipi_camera.json")
    spec["camera"]["interface"] = {"type": "USB 2.0"}
    code, out = run_check("interface_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "too narrow" in out


def test_unknown_interface_fails(tmp_path):
    spec = load_example("solar_camera_trap.json")
    spec["camera"]["interface"]["type"] = "Thunderbolt 9"
    code, out = run_check("interface_check.py", write_spec(tmp_path, spec))
    assert code == 1, out
    assert "unknown interface" in out
