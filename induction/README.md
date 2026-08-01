# induction

Tools for checking mathematical induction proofs of arithmetic-series identities.

## `arithmetic_series.py`

Given a statement like `"1 + 3 + 5 + ... + (2n-1) = n^2"`, checks whether it holds by verifying the two standard induction steps: the base case (`n = 1`) and the inductive step (assume true for `k`, show true for `k+1`).

```python
from induction.arithmetic_series import base_case, inductive_step, explain

base_case("1 + 3 + 5 + ... + (2n-1) = n^2")        # True
inductive_step("1 + 3 + 5 + ... + (2n-1) = n^2")    # True

explain("1 + 3 + 5 + ... + (2n-1) = n^2")
# Claim  1 + 3 + 5 + ... + (2n-1) = n^2
#
# Base (n = 1):  1 = 1  OK
# Hypothesis:  assume P(k) = k**2
# Step:  add the next term, 2*k + 1 ->
#     k**2 + (2*k + 1) = (k + 1)**2  OK
# So, P(k+1) holds. By induction, true for all n >= 1.
```

`base_case` and `inductive_step` each accept an `explain=True` flag to print their own derivation without going through `explain()`. `base_case` also accepts `base=` (default `1`) if the induction should start at a different index.

### Statement syntax

Statements are parsed with `preprocess()`: `^` for exponents, implicit multiplication (`n(n+1)`), and standard `+`/`-` are all supported.
