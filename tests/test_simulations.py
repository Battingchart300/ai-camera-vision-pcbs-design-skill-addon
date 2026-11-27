"""Tests for simulations/ — input generators only, never fake results."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIMS = ROOT / "simulations"
SPEC = ROOT / "examples" / "solar_camera_trap.json"


def _run(script, outdir):
    r = subprocess.run([sys.executable, str(SIMS / script), str(SPEC), str(outdir)],
                       capture_output=True, text=True, cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


def test_thermal_input_writes_sif_and_reports_not_run(tmp_path):
    code, out = _run("thermal_input.py", tmp_path)
    assert code == 0, out
    sif = tmp_path / "thermal.sif"
    assert sif.is_file()
    text = sif.read_text()
    assert "UNVERIFIED" in text
    assert "Heat Equation" in text
    # No simulation ran here: the tool is not installed in this env.
    assert "NOT_RUN" in out
    assert "no simulation was run" in out


def test_si_input_writes_xml_and_reports_not_run(tmp_path):
    code, out = _run("si_input.py", tmp_path)
    assert code == 0, out
    xml = tmp_path / "mipi_pair.xml"
    assert xml.is_file()
    assert "85" in xml.read_text()
    assert "NOT_RUN" in out


def test_spice_input_writes_deck_and_reports_not_run(tmp_path):
    code, out = _run("spice_input.py", tmp_path)
    assert code == 0, out
    deck = tmp_path / "power_rail.spice"
    assert deck.is_file()
    assert "UNVERIFIED" in deck.read_text()
    assert "NOT_RUN" in out


def test_bad_spec_is_exit_2(tmp_path):
    r = subprocess.run([sys.executable, str(SIMS / "thermal_input.py"),
                        "/tmp/no-such-spec.json", str(tmp_path)],
                       capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 2
