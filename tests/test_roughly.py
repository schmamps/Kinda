"""Comparison Functions"""
from sys import version_info

from pytest import mark

import roughly

# pylint: disable=unused-import
if version_info >= (3, 5, 0):
    from typing import Any   # noqa
    # pylint: enable=unused-import

LT = 'lt'
EQ = 'eq'
GT = 'gt'


def param_test(a_val, b_val, actual_comp, rel_tol, abs_tol):
    # type: (float, float, str, Any, Any) -> tuple
    """Generate test fixture

    Returns:
        tuple -- (kwargs for function, is_lt, is_eq, accept_approximate)
    """
    arg_dict = {'a': a_val, 'b': b_val, 'rel_tol': rel_tol, 'abs_tol': abs_tol}
    kwargs = {key: val for key, val in arg_dict.items() if val is not None}
    approx = rel_tol is not None or abs_tol is not None

    return (kwargs, actual_comp == LT, actual_comp == EQ, approx)


def format_pair(key, val):
    # type: (str, str) -> str
    """Generate key/value pair

    Returns:
        str -- key=val
    """
    return '='.join([key, val])


def format_num(num, places, if_none='default'):
    # type: (Any, int, str) -> str
    """Format `num` to decimal `places` if not None, else `if_none`

    Returns:
        str -- formatted string
    """
    if num is None:
        return if_none

    return '{{:.{}f}}'.format(places).format(num)


def id_test(actual_comp, rel_tol, abs_tol, places):
    # type: (str, Any, Any, int) -> str
    """Generate test ID

    Returns:
        str -- test ID
    """
    crumbs = [
        format_pair('actual', actual_comp),
        format_pair('places', str(places)),
        format_pair('rel', format_num(rel_tol, places, '')),
        format_pair('abs', format_num(abs_tol, places, '')), ]

    return ','.join([crumb for crumb in crumbs if len(crumb) > 4])


def run_test(compare, kwargs, expected):
    # type: (Any, dict, bool) -> None
    """Assert `compare(**kwargs) == expected`"""
    received = compare(**kwargs)

    if received != expected:
        breakpoint()
        pass  # pylint: disable=unnecessary-pass

    assert received == expected


def permute_tests(start, stop, step):
    # type: (int, int, int) -> tuple
    """Generate list of tests and IDs

    Returns:
        tuple[list[tuple], list[str]] -- (test_params, test_ids)
    """
    values = []
    ids = []

    for places in range(start, stop, step):
        inc = 1.0 / pow(10, places)
        val_b = float('1.' + '0' * max(1, places))
        lt_b = val_b - inc
        gt_b = val_b + inc

        for abs_tol in [None, inc * 1.01]:
            for val_a, nom_comp in [(lt_b, LT), (val_b, EQ), (gt_b, GT), ]:
                # avoid defaults for longer numbers
                if places < 9 or abs_tol is not None:
                    actual_comp = nom_comp if abs_tol is None else EQ

                    values.append(
                        param_test(val_a, val_b, actual_comp, None, abs_tol))
                    ids.append(
                        id_test(actual_comp, None, abs_tol, places))

    return values, ids


def parametrize(test_func, test_data):
    # type: (Any, tuple) -> Any
    """Wrap `pytest.mark.parametrize` with test permutations

    Arguments:
        test_func {callable} -- function to test
    """
    argnames = 'func,kwargs,is_lt,is_eq,approx'
    argvalues = [(test_func, *test) for test in test_data[0]]

    return mark.parametrize(argnames, argvalues, ids=test_data[1])


TEST_DATA = permute_tests(1, 14, 1)


@parametrize(roughly.eq, TEST_DATA)
# pylint: disable=unused-argument
def test_eq(func, kwargs, is_lt, is_eq, approx):
    # type: (Any, dict, bool, bool, bool) -> None
    """Test equality"""
    run_test(func, kwargs, is_eq or approx)


@parametrize(roughly.ne, TEST_DATA)
# pylint: disable=unused-argument
def test_ne(func, kwargs, is_lt, is_eq, approx):
    # type: (Any, dict, bool, bool, bool) -> None
    """Test inequality"""
    run_test(func, kwargs, not is_eq and not approx)


@parametrize(roughly.lt, TEST_DATA)
# pylint: disable=unused-argument
def test_lt(func, kwargs, is_lt, is_eq, approx):
    # type: (Any, dict, bool, bool, bool) -> None
    """Test less than"""
    run_test(func, kwargs, is_lt and not approx)


@parametrize(roughly.gt, TEST_DATA)
# pylint: disable=unused-argument
def test_gt(func, kwargs, is_lt, is_eq, approx):
    # type: (Any, dict, bool, bool, bool) -> None
    """Test greater than"""
    run_test(func, kwargs, not is_lt and not is_eq and not approx)


@parametrize(roughly.le, TEST_DATA)
# pylint: disable=unused-argument
def test_le(func, kwargs, is_lt, is_eq, approx):
    # type: (Any, dict, bool, bool, bool) -> None
    """Test less than/equality"""
    run_test(func, kwargs, is_lt or is_eq or approx)


@parametrize(roughly.ge, TEST_DATA)
def test_ge(func, kwargs, is_lt, is_eq, approx):
    # type: (Any, dict, bool, bool, bool) -> None
    """Test greater than/equality"""
    run_test(func, kwargs, not is_lt or is_eq or approx)
