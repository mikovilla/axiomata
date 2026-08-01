from sympy import symbols, log, limit, oo, simplify, sympify

from checks.equal import preprocess

n = symbols("n", positive=True)


def _to_expr(f_n):
    if isinstance(f_n, str):
        expr = sympify(preprocess(f_n), locals={"n": n})
    else:
        expr = sympify(f_n)
        for symbol in expr.free_symbols:
            if symbol.name == "n" and symbol != n:
                expr = expr.subs(symbol, n)
    return expr


def critical_exponent(a, b):
    return simplify(log(a) / log(b))


def _match_log_power(ratio, max_k=6):
    """Try ratio ~ C * log(n)**k for k = 0..max_k. Return (k, constant) or None."""
    for k in range(max_k + 1):
        candidate = ratio if k == 0 else simplify(ratio / log(n) ** k)
        L = limit(candidate, n, oo)
        if L.is_finite and L != 0:
            return k, L
    return None


def master_theorem(a, b, f_n, explain=False):
    """Classify T(n) = a*T(n/b) + f(n) using the Master Theorem.

    Returns a dict with the critical exponent, which case applies (1, 2, or 3),
    and the resulting Theta bound. Case 3 also includes whether the regularity
    condition (a*f(n/b) <= r*f(n) for some r<1) holds.
    """
    a = sympify(a)
    b = sympify(b)
    f_expr = _to_expr(f_n)

    c = critical_exponent(a, b)
    ratio = simplify(f_expr / n ** c)
    L = limit(ratio, n, oo)

    regularity_holds = None

    if L == 0:
        case = 1
        theta = n ** c
        reason = "f(n) is polynomially smaller than n^c (lim f(n)/n^c = 0)"

    else:
        match = _match_log_power(ratio)

        if match is not None:
            k, _ = match
            case = 2
            theta = n ** c * log(n) ** (k + 1)
            reason = f"f(n) = Theta(n^c * log(n)^{k}) (lim ratio/log(n)^{k} is a nonzero finite constant)"

        else:
            case = 3
            regularity_ratio = simplify(a * f_expr.subs(n, n / b) / f_expr)
            regularity_limit = limit(regularity_ratio, n, oo)
            regularity_holds = regularity_limit < 1
            theta = f_expr
            reason = "f(n) is polynomially larger than n^c (lim f(n)/n^c = oo)"

    result = {
        "a": a,
        "b": b,
        "f_n": f_expr,
        "critical_exponent": c,
        "case": case,
        "theta": theta,
    }
    if case == 3:
        result["regularity_holds"] = regularity_holds

    if explain:
        print(f"T(n) = {a}*T(n/{b}) + {f_expr}")
        print(f"Critical exponent:  c = log_{b}({a}) = {c}")
        print(f"Compare f(n) to n^c:  {f_expr}  vs  n**{c}")
        print(f"-> Case {case}: {reason}")
        if case == 3:
            status = "holds" if regularity_holds else "FAILS -- Master Theorem does not apply"
            print(f"Regularity condition (a*f(n/b) <= r*f(n) for some r<1):  {status}")
        print(f"Conclusion:  T(n) = Theta({theta})")

    return result
