# Roughly

## About

Roughly is a pythonic library for comparing floating point values with
[Python operator functions](https://docs.python.org/2/library/operator.html#mapping-operators-to-functions).

## Arguments

The implementation and documentation are identical to
[math.isclose](https://docs.python.org/3/library/math.html#number-theoretic-and-representation-functions).

## Comparisons

### Equality

```py
>>> import roughly
>>> # a == b
>>> roughly.eq(1.0000, 1.0000)
True
>>> # a != b (default precision)
>>> roughly.eq(0.9999, 1.0001)
False
```

### Precision

All `math.isclose()` arguments are accepted in all functions.

* `abs_tol`: absolute tolerance (`abs(a - b)`)
* `rel_tol`: percentage tolerance (1% = .01)

```py
>>> # reduce absolute precision
>>> roughly.eq(0.9999, 1.0001, abs_tol=0.0002)
True
>>> # precision: 1%
>>> roughly.eq(1.0000, 1.0500, rel_tol=0.01)
False
>>> # precision: 5%
>>> roughly.eq(1.0000, 1.0500, rel_tol=0.05)
True
```

### Inequality

```py
>>> import roughly
>>> [roughly.ne(0.9999, 1.0001), roughly.ne(1.0000, 1.0000)]
[True, False]
```

### Less/Greater Than

```py
>>> import roughly
>>> # [a < b, a > b]
>>> [roughly.lt(1.0000, 1.0001), roughly.gt(1.0001, 1.0000)]
[True, True]
```

### Less/Greater Than or Equal To

```py
>>> import roughly
>>> roughly.le(1.0000, 1.0001) and roughly.ge(1.0000, 1.0001)
[True, False]
>>> roughly.le(1.0000, 1.0000) and roughly.ge(1.0000, 1.0000)
[True, True]
>>> roughly.le(1.0000, 0.9999) and roughly.ge(1.0000, 0.9999)
[False, True]
```