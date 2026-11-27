"""Tests for schemas/camera-spec.schema.json — required keys and types.

A small hand-rolled checker driven by the schema file itself (no
jsonschema dependency): it walks the schema's `required` lists and
`type` declarations and checks the shipped examples against them.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schemas" / "camera-spec.schema.json").read_text())


def _check(instance, schema, path, problems):
    if "type" in schema:
        want = schema["type"]
        got = ("object" if isinstance(instance, dict)
               else "integer" if isinstance(instance, int) and not isinstance(instance, bool)
               else "number" if isinstance(instance, (int, float)) and not isinstance(instance, bool)
               else "boolean" if isinstance(instance, bool)
               else "string" if isinstance(instance, str)
               else "array" if isinstance(instance, list) else "null")
        if want == "number" and got in ("integer", "number"):
            pass
        elif got != want:
            problems.append(f"{path}: expected {want}, got {got}")
            return
    if schema.get("type") == "object" and isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                problems.append(f"{path}: missing required key '{key}'")
        for key, sub in schema.get("properties", {}).items():
            if key in instance:
                _check(instance[key], sub, f"{path}.{key}", problems)
    if "enum" in schema and instance not in schema["enum"]:
        problems.append(f"{path}: {instance!r} not in {schema['enum']}")


def _validate(name):
    spec = json.loads((ROOT / "examples" / name).read_text())
    problems = []
    _check(spec, SCHEMA, "$", problems)
    return problems


def test_schema_file_is_valid_json():
    assert SCHEMA["title"] == "Camera & Vision Addon Spec"
    assert SCHEMA["required"] == ["board", "camera"]


def test_solar_camera_trap_matches_schema():
    assert _validate("solar_camera_trap.json") == []


def test_industrial_camera_matches_schema():
    assert _validate("industrial_mipi_camera.json") == []


def test_edge_vision_pc_matches_schema():
    assert _validate("edge_vision_pc.json") == []


def test_schema_catches_missing_required_key():
    spec = json.loads((ROOT / "examples" / "solar_camera_trap.json").read_text())
    del spec["camera"]["privacy"]
    problems = []
    _check(spec, SCHEMA, "$", problems)
    assert any("privacy" in p for p in problems)


def test_schema_catches_wrong_type():
    spec = json.loads((ROOT / "examples" / "solar_camera_trap.json").read_text())
    spec["camera"]["sensor"]["fps"] = "fast"
    problems = []
    _check(spec, SCHEMA, "$", problems)
    assert any("fps" in p for p in problems)
