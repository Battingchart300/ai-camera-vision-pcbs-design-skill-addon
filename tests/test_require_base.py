"""Tests for scripts/require_base.py — the hard base-skill dependency."""
import shutil
from pathlib import Path

from helpers import BASE_SKILL, ROOT, run_script

SCRIPTS = ROOT / "scripts"


def test_base_found_at_sibling_path():
    code, out = run_script("require_base.py", "--base-skill", str(BASE_SKILL))
    assert code == 0, out
    assert "Base skill OK" in out
    assert "ai-pcb-design-skill v1.2.6" in out


def test_missing_base_is_exit_2(tmp_path):
    code, out = run_script("require_base.py", "--base-skill", str(tmp_path / "nope"))
    assert code == 2, out
    assert "BASE SKILL MISSING" in out


def test_misnamed_base_is_exit_2(tmp_path):
    # A directory whose SKILL.md frontmatter names the addon itself
    # must NOT pass as the base skill (exact-name check).
    fake = tmp_path / "fake-base"
    fake.mkdir()
    (fake / "SKILL.md").write_text(
        "---\nname: ai-pc-component-design-skill-addon\n---\n\n"
        "**Version:** 0.3.5 — 2026-11-25\n",
        encoding="utf-8",
    )
    code, out = run_script("require_base.py", "--base-skill", str(fake))
    assert code == 2, out


def test_too_old_base_is_exit_2(tmp_path):
    fake = tmp_path / "old-base"
    fake.mkdir()
    (fake / "SKILL.md").write_text(
        "---\nname: ai-pcb-design-skill\n---\n\n**Version:** 1.2.0 — 2026-11-24\n",
        encoding="utf-8",
    )
    code, out = run_script("require_base.py", "--base-skill", str(fake))
    assert code == 2, out
    assert "TOO OLD" in out


def test_explicit_path_is_authoritative(tmp_path):
    # An explicit wrong path must NOT fall through to the real base skill.
    code, out = run_script("require_base.py", "--base-skill", str(tmp_path / "nope"))
    assert code == 2, out
    assert "No addon check ran" in out or "BASE SKILL MISSING" in out
