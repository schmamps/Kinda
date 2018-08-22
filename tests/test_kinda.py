"""Comparison Functions"""
from sys import version_info

from pytest import mark

import kinda

# pylint: disable=unused-import
if version_info >= (3, 5, 0):
    from typing import Any   # noqa
    # pylint: enable=unused-import

LT = 'lt'
EQ = 'eq'
GT = 'gt'


def get_place_values(places):
    # type: (int) -> tuple
    """Get values of `a`, `b`, and tolerance for decimal `places`

    Returns:
        tuple[float, float, float, float] --
            (`b - tol`, `b`, `b + tol`, tolerance)
    """
    diff = 1.0 / pow(10, places)
    eq_val = float('1.' + '0' * max(1, places))
    lt_val = eq_val - diff
    gt_val = eq_val + diff

    return lt_val, eq_val, gt_val


def get_tol_values(places):
    # type: (float) -> list
    """List of tolerances to test

    Returns:
        list[tuple[float, float]] -- [(abs_tol, rel_tol)]
    """
    abs_tol = 1.1 / pow(10, places)
    return [(None, None), (abs_tol, None)]


def get_comp_values(place_vals, places, abs_tol, rel_tol):
    # type: (tuple, int, Any, Any) -> list
    """List comparisons to test

    Returns:
        list[tuple[float, float, str]] -- [(a, b, comparison)]
    """
    lt_val, eq_val, gt_val = place_vals
    eq_comp = (eq_val, eq_val, EQ)
    eq_tol_only = places > 8 and abs_tol is None and rel_tol is None

    if eq_tol_only:
        return [eq_comp]

    return [(lt_val, eq_val, LT), eq_comp, (gt_val, eq_val, GT)]


def get_test_args(val_a, val_b, abs_tol, rel_tol):
    # type: (float, float, Any, Any) -> dict
    """Get essential arguments for test function call as dict (for splatting)

    Removes values of `None`

    Returns:
        dict[str, Any] -- {a, b, rel_tol, abs_tol}
    """

    arg_dict = {'a': val_a, 'b': val_b, 'rel_tol': rel_tol, 'abs_tol': abs_tol}

    return {key: val for key, val in arg_dict.items() if val is not None}


def get_test_params(val_a, val_b, actual_comp, abs_tol, rel_tol):
    # type: (float, float, str, Any, Any) -> tuple
    """Generate test params

    Returns:
        tuple[dict, bool, bool, bool] -- (kwargs, is_lt, is_eq, approx)
    """
    kwargs = get_test_args(val_a, val_b, abs_tol, rel_tol)
    is_lt = (actual_comp == LT)
    is_eq = (actual_comp == EQ)
    approx = rel_tol is not None or abs_tol is not None

    return (kwargs, is_lt, is_eq, approx)


def format_tol(tol):
    # type: (Any) -> Any
    """Format `tol` if is not `None` else `None`

    Returns:
        str -- formatted value
    """
    return tol if tol is None else 'to_places'


def format_pair(kv_tuple):
    # type: (tuple) -> str
    """Generate key/value pair

    Returns:
        str -- 'key=val'
    """
    return '{}={}'.format(*kv_tuple)


def get_test_id(actual_comp, abs_tol, rel_tol, places):
    # type: (str, float, float, int) -> str
    """Generate test ID with salient information

    Returns:
        str -- test ID
    """
    crumbs = [
        ('actual', actual_comp),
        ('places', places),
        ('abs_tol', format_tol(abs_tol)),
        ('rel_tol', format_tol(rel_tol)), ]

    return ','.join([
        format_pair(crumb)
        for crumb in crumbs
        if crumb[1] is not None])


def permute_tests(start, stop, step):
    """Generate test params and IDs

    Returns:
        tuple[list[tuple], list[str]] -- (test_params, test_ids)
    """
    params = []
    ids = []
    for places in range(start, stop, step):
        place_vals = get_place_values(places)

        for abs_tol, rel_tol in get_tol_values(places):
            comparisons = get_comp_values(
                place_vals, places, abs_tol, rel_tol)

            for val_a, val_b, actual_comp in comparisons:
                params.append(get_test_params(
                    val_a, val_b, actual_comp, abs_tol, rel_tol))
                ids.append(get_test_id(
                    actual_comp, abs_tol, rel_tol, places))

    return params, ids


def parametrize(test_func, test_data):
    # type: (Any, tuple) -> Any
    """Wrap `pytest.mark.parametrize` with test permutations

    Arguments:
        test_func {callable} -- function to test
    """
    argnames = 'func,kwargs,is_lt,is_eq,approx'
    argvalues = [(test_func, *test) for test in test_data[0]]

    return mark.parametrize(argnames, argvalues, ids=test_data[1])


TEST_DATA = permute_tests(0, 97, 12)


def run_test(compare, kwargs, expected):
    # type: (Any, dict, bool) -> None
    """Wrap around `assert compare(**kwargs) == expected`"""
    received = compare(**kwargs)

    if received != expected:
        breakpoint()
        pass  # pylint: disable=unnecessary-pass

    assert received == expected


@parametrize(kinda.eq, TEST_DATA)
# pylint: disable=unused-argument
def test_eq(func, kwargs, is_lt, is_eq, approx):
    # type: (Any, dict, bool, bool, bool) -> None
    """Test equality"""
    run_test(func, kwargs, is_eq or approx)


@parametrize(kinda.ne, TEST_DATA)
# pylint: disable=unused-argument
def test_ne(func, kwargs, is_lt, is_eq, approx):
    # type: (Any, dict, bool, bool, bool) -> None
    """Test inequality"""
    run_test(func, kwargs, not is_eq and not approx)


@parametrize(kinda.lt, TEST_DATA)
# pylint: disable=unused-argument
def test_lt(func, kwargs, is_lt, is_eq, approx):
    # type: (Any, dict, bool, bool, bool) -> None
    """Test less than"""
    run_test(func, kwargs, is_lt and not approx)


@parametrize(kinda.gt, TEST_DATA)
# pylint: disable=unused-argument
def test_gt(func, kwargs, is_lt, is_eq, approx):
    # type: (Any, dict, bool, bool, bool) -> None
    """Test greater than"""
    run_test(func, kwargs, not is_lt and not is_eq and not approx)


@parametrize(kinda.le, TEST_DATA)
# pylint: disable=unused-argument
def test_le(func, kwargs, is_lt, is_eq, approx):
    # type: (Any, dict, bool, bool, bool) -> None
    """Test less than/equality"""
    run_test(func, kwargs, is_lt or is_eq or approx)


@parametrize(kinda.ge, TEST_DATA)
def test_ge(func, kwargs, is_lt, is_eq, approx):
    # type: (Any, dict, bool, bool, bool) -> None
    """Test greater than/equality"""
    run_test(func, kwargs, not is_lt or is_eq or approx)
