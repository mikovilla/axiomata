# axiomata

## `induction`

Tools for checking mathematical induction proofs of arithmetic-series identities.

Given a statement like `"1 + 3 + 5 + ... + (2n-1) = n^2"`, checks whether it holds by verifying the two standard induction steps: the base case (`n = 1`) and the inductive step (assume true for `k`, show true for `k+1`).

```python
from axiomata import induction

induction.base_case("1 + 3 + 5 + ... + (2n-1) = n^2")        # True
induction.inductive_step("1 + 3 + 5 + ... + (2n-1) = n^2")    # True

induction.explain("1 + 3 + 5 + ... + (2n-1) = n^2")
# proposition  1 + 3 + 5 + ... + (2n-1) = n^2
#
# Base (n = 1):  1 = 1  OK
# Hypothesis:  assume P(k) = k**2
# Step:  add the next term, 2*k + 1 ->
#     k**2 + (2*k + 1) = (k + 1)**2  OK
# So, P(k+1) holds. By induction, true for all n >= 1.
```

`base_case` and `inductive_step` each accept an `explain=True` flag to print their own derivation without going through `explain()`. `base_case` also accepts `start=` (default `1`) if the induction should start at a different index.

Statements are parsed with `induction.preprocess()`: `^` for exponents, implicit multiplication (`n(n+1)`), and standard `+`/`-` are all supported.

## `checks`

Symbolic equality checks for algebraic expressions.

Checks whether two expressions are algebraically equal (expands and simplifies their difference to see if it collapses to `0`). Accepts sympy expressions or strings written in natural math notation.

```python
from axiomata import checks

checks.equal((k + 1) ** 3 - (k + 1), (k ** 3 - k) + 3 * k * (k + 1))  # True

checks.equal("(k+1)³ − (k+1)", "(k³ − k) + 3k(k+1)")  # True, same check via natural notation
checks.equal("(k+1)²", "k² + 1")                       # False
```

String inputs go through `checks.preprocess()`, which supports:

- `^` or unicode superscripts (`k³`) for exponents
- unicode minus (`−`) alongside `-`
- implicit multiplication: `3k(k+1)` -> `3*k*(k+1)`
- common function calls left untouched: `log`, `ln`, `exp`, `sqrt`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `Abs`, `floor`, `ceiling`

## `master_theorem`

Classifies a divide-and-conquer recurrence `T(n) = a*T(n/b) + f(n)` into Case 1, 2, or 3 of the Master Theorem and returns the resulting `Θ(...)` bound.

```python
from axiomata import master_theorem

master_theorem.calculate(2, 2, "n")
# {'a': 2, 'b': 2, 'f_n': n, 'critical_exponent': 1, 'case': 2, 'theta': n*log(n)}

master_theorem.calculate(2, 2, "n", explain=True)
# T(n) = 2*T(n/2) + n
# Critical exponent:  c = log_2(2) = 1
# Compare f(n) to n^c:  n  vs  n**1
# -> Case 2: f(n) = Theta(n^c * log(n)^0) (lim ratio/log(n)^0 is a nonzero finite constant)
# Conclusion:  T(n) = Theta(n*log(n))
```

- `a` — number of subproblems (`a >= 1`)
- `b` — factor the problem size shrinks by (`b > 1`)
- `f_n` — non-recursive work per call; a sympy expression or a string (parsed via `axiomata.checks.preprocess`, so natural notation like `"n log(n)"` or `"n²"` works)
- `explain=True` — print the derivation (critical exponent, comparison, case, conclusion)

Case 3 results also include `regularity_holds` in the returned dict — whether the regularity condition (`a*f(n/b) <= r*f(n)` for some `r<1`) is satisfied, which the Master Theorem requires for Case 3 to actually apply.

Only covers recurrences that fit the `aT(n/b) + f(n)` shape — a *constant-factor* shrink each call. Recurrences that shrink by a constant *amount* instead (`T(n-1) + f(n)`, e.g. bubble sort, linear search) aren't divide-and-conquer and fall outside what this function can solve; those resolve by direct summation instead.

## `sort`

Elementary O(n²) sorting algorithms: `bubble`, `selection`, `insertion`.

```python
from axiomata.sort import Sort, Type, Animation

Sort(Type.BUBBLE).run()                                # sorts 10 random distinct numbers, prints Before/After only
Sort(Type.SELECTION).array(5).run()                     # sorts 5 random distinct numbers, prints Before/After only
Sort(Type.INSERTION).array([5, 3, 8, 1, 9]).run()       # sorts the given array, prints Before/After only

# animated: defaults to Animation.ANSI, a live terminal bar chart redrawn
# in place every `delay` seconds, labeled "Before" / "Step n" / "After"
Sort(Type.BUBBLE).array([5, 3, 8, 1, 9]).delay(0.5).animate()

# in a Jupyter notebook, use matplotlib instead — ANSI's in-place
# redraw doesn't render correctly in notebook output cells
Sort(Type.SELECTION).array([5, 3, 8, 1, 9]).delay(0.5).animate(Animation.MATPLOTLIB)
```

`Sort(algorithm)` fixes which algorithm the instance runs — `Type.BUBBLE`, `Type.SELECTION`, or `Type.INSERTION`. `.array(...)` and `.delay(seconds)` are chainable configuration methods. `.run()` and `.animate(...)` are the two terminal calls — pick one:

- `.run()` — sorts without a step-by-step animation, but still prints a `Before` and `After` bar chart (no delay between them) so the starting and ending arrangement are visible, then returns the result.
- `.animate(animation=Animation.ANSI)` — sorts with a full step-by-step visualization and returns the result. Every frame is labeled `Before`, `Step n/total`, or `After`, so the starting and ending arrangement are always shown, not just the last step.
  - `Animation.ANSI` (default) — redraws a bar chart in place in the terminal on every comparison/swap, using plain ASCII bars (portable across terminal codepages) and inverse-video highlighting for the indices currently being compared. Needs a real terminal — doesn't redraw correctly in a Jupyter output cell.
  - `Animation.MATPLOTLIB` — redraws a matplotlib bar chart each frame. Inside a Jupyter notebook it updates the same output cell in place (via `IPython.display`); outside a notebook it opens a live-updating figure window (falls back to a plain redraw if no GUI backend is available).

Calling `.run()` or `.animate()` more than once on the same instance reuses the same starting values.

- `.array(values=None)` — `array()` (no arguments) generates `10` random distinct numbers; `array(n)` generates `n` random distinct numbers (max `10` for now); `array([...])` sorts that explicit list instead (must be distinct numbers, max `10` elements for now)
- `.delay(seconds)` — seconds between animation frames (default `1`), only meaningful when `.animate(...)` is used
