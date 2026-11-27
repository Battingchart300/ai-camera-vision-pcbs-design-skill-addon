"""Unit tests for the bool-safe type guards (validators/types.py).

Python treats True as 1 — a naive isinstance(x, int) lets
`lanes: true` pass as "1 lane". These guards must never do that.
"""
from validators.types import is_bool, is_int, is_nonempty_str, is_number, is_unverified


def test_is_int_rejects_bool():
    assert is_int(2) is True
    assert is_int(True) is False
    assert is_int(False) is False
    assert is_int(2.0) is False
    assert is_int("2") is False


def test_is_number_rejects_bool_nan_inf():
    assert is_number(2) is True
    assert is_number(2.5) is True
    assert is_number(True) is False
    assert is_number(float("nan")) is False
    assert is_number(float("inf")) is False
    assert is_number("2") is False


def test_is_nonempty_str():
    assert is_nonempty_str("IMX477") is True
    assert is_nonempty_str("") is False
    assert is_nonempty_str("   ") is False
    assert is_nonempty_str(42) is False


def test_is_unverified_case_insensitive():
    assert is_unverified("UNVERIFIED") is True
    assert is_unverified("unverified") is True
    assert is_unverified("IMX477") is False
    assert is_unverified(None) is False


def test_is_bool():
    assert is_bool(True) is True
    assert is_bool(False) is True
    assert is_bool(1) is False
    assert is_bool("true") is False
