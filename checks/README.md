# checks

Symbolic equality checks for algebraic expressions.

## `equal.py`

Checks whether two expressions are algebraically equal (expands and simplifies their difference to see if it collapses to `0`). Accepts sympy expressions or strings written in natural math notation.

```python
from checks.equal import equal

equal((k + 1) ** 3 - (k + 1), (k ** 3 - k) + 3 * k * (k + 1))  # True

equal("(k+1)³ − (k+1)", "(k³ − k) + 3k(k+1)")  # True, same check via natural notation
equal("(k+1)²", "k² + 1")                       # False
```

### Statement syntax

String inputs go through `preprocess()`, which supports:

- `^` or unicode superscripts (`k³`) for exponents
- unicode minus (`−`) alongside `-`
- implicit multiplication: `3k(k+1)` -> `3*k*(k+1)`
- common function calls left untouched: `log`, `ln`, `exp`, `sqrt`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `Abs`, `floor`, `ceiling`
