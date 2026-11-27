"""Tests for benchmarks/benchmark.py — estimates only, never measured."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "benchmarks" / "benchmark.py"


def _run(spec):
    r = subprocess.run([sys.executable, str(BENCH), str(spec)],
                       capture_output=True, text=True, cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


def test_trap_benchmark_labels_estimates():
    code, out = _run(ROOT / "examples" / "solar_camera_trap.json")
    assert code == 0, out
    assert "ESTIMATE" in out
    assert "not measured" in out
    assert "sensor stream" in out
    assert "solar autonomy" in out


def test_industrial_benchmark_reports_link_utilization():
    code, out = _run(ROOT / "examples" / "industrial_mipi_camera.json")
    assert code == 0, out
    assert "link utilization" in out
    assert "NPU utilization" in out


def test_bad_spec_is_exit_2():
    code, out = _run("/tmp/no-such-spec.json")
    assert code == 2, out
