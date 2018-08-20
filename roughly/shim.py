"""Shim for Python < 3.5"""


# pylint: disable=invalid-name
def isclose(a, b, rel_tol, abs_tol):
    # type: (float, float, float, float) -> bool
    """Implement math.isclose where not builtin"""
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
