# calculate

Tools for computing asymptotic bounds.

## `master_theorem.py`

Classifies a divide-and-conquer recurrence `T(n) = a*T(n/b) + f(n)` into Case 1, 2, or 3 of the Master Theorem and returns the resulting `Θ(...)` bound.

```python
from calculate.master_theorem import master_theorem

master_theorem(2, 2, "n")
# {'a': 2, 'b': 2, 'f_n': n, 'critical_exponent': 1, 'case': 2, 'theta': n*log(n)}

master_theorem(2, 2, "n", explain=True)
# T(n) = 2*T(n/2) + n
# Critical exponent:  c = log_2(2) = 1
# Compare f(n) to n^c:  n  vs  n**1
# -> Case 2: f(n) = Theta(n^c * log(n)^0) (lim ratio/log(n)^0 is a nonzero finite constant)
# Conclusion:  T(n) = Theta(n*log(n))
```

- `a` — number of subproblems (`a >= 1`)
- `b` — factor the problem size shrinks by (`b > 1`)
- `f_n` — non-recursive work per call; a sympy expression or a string (parsed via `checks.equal.preprocess`, so natural notation like `"n log(n)"` or `"n²"` works)
- `explain=True` — print the derivation (critical exponent, comparison, case, conclusion)

Case 3 results also include `regularity_holds` in the returned dict — whether the regularity condition (`a*f(n/b) <= r*f(n)` for some `r<1`) is satisfied, which the Master Theorem requires for Case 3 to actually apply.

### Scope

Only covers recurrences that fit the `aT(n/b) + f(n)` shape — a *constant-factor* shrink each call. Recurrences that shrink by a constant *amount* instead (`T(n-1) + f(n)`, e.g. bubble sort, linear search) aren't divide-and-conquer and fall outside what this function can solve; those resolve by direct summation instead.
