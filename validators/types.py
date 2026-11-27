"""types.py — bool-safe type guards for camera specs.

Python treats True as 1 (True == 1, isinstance(True, int) is True),
so a naive `isinstance(x, int)` check lets `lanes: true` pass as
"1 lane". Every numeric field in a spec must go through these guards.
A bool where a number is expected is a clean ERROR, never a pass.
"""
import math


def is_int(value):
    """True only for a real int — never a bool, never a float."""
    return isinstance(value, int) and not isinstance(value, bool)


def is_number(value):
    """True only for a finite real int/float — never a bool, never NaN/inf."""
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    return False


def is_nonempty_str(value):
    return isinstance(value, str) and value.strip() != ""


def is_unverified(value):
    """True when a value is the literal UNVERIFIED marker (any case)."""
    return isinstance(value, str) and value.strip().upper() == "UNVERIFIED"


def is_bool(value):
    return isinstance(value, bool)
