# Kinda

## About

Kinda is a pythonic library for comparing floating point values with
[Python operator functions](https://docs.python.org/2/library/operator.html#mapping-operators-to-functions).

## Installation

Kinda is available as a package.

```sh
pip install kinda
```

## Comparison

### Equality

```py
>>> import kinda
>>> # a == b
>>> kinda.eq(1.0000, 1.0000)
True
>>> # a != b
>>> kinda.eq(0.9999, 1.0001)
False
```

### Tolerances

All functions take the same arguments and defaults of
[`math.isclose()`](https://docs.python.org/3/library/math.html)
and make use the native function when available.

For complete details, refer to that function's documentation,
but as an overview, those keyword arguments are:

* `abs_tol`: absolute difference (`bigger - smaller)`)
* `rel_tol`: difference coefficient (`bigger * rel_tol`)

```py
>>> import kinda
>>> # reduce absolute precision
>>> kinda.eq(0.9999, 1.0001, abs_tol=0.0002)
True
>>> # reduce relative precision to 5%
>>> kinda.eq(1.0000, 1.0500, rel_tol=0.05)
True
>>> # reduce relative precision to 1%
>>> kinda.eq(1.0000, 1.0500, rel_tol=0.01)
False
```

### Inequality

```py
>>> import kinda
>>> [kinda.ne(0.9999, 1.0001), kinda.ne(1.0000, 1.0000)]
[True, False]
```

### Less/Greater Than

```py
>>> import kinda
>>> # [a < b, a > b]
>>> [kinda.lt(1.0000, 1.0001), kinda.gt(1.0001, 1.0000)]
[True, True]
```

### Less/Greater Than or Equal To

```py
>>> import kinda
>>> kinda.le(1.0000, 1.0001) and kinda.ge(1.0000, 1.0001)
[True, False]
>>> kinda.le(1.0000, 1.0000) and kinda.ge(1.0000, 1.0000)
[True, True]
>>> kinda.le(1.0000, 0.9999) and kinda.ge(1.0000, 0.9999)
[False, True]
```