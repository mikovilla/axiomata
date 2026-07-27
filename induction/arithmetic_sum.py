import re
from sympy import symbols, sympify, simplify

n, k = symbols("n k", integer=True, positive=True)

def preprocess(expr):
    """Convert implicit multiplication to explicit multiplication."""
    expr = expr.replace("^", "**")
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'([a-zA-Z])\(', r'\1*(', expr)
    expr = re.sub(r'\)([a-zA-Z0-9])', r')*\1', expr)
    return expr


def parse(statement):
    lhs, rhs = statement.split("=")

    parts = [p.strip() for p in lhs.split("+")]
    local_symbols = {"n": n, "k": k}

    a = sympify(preprocess(parts[0]), locals=local_symbols)
    second = sympify(preprocess(parts[1]), locals=local_symbols)
    last = sympify(preprocess(parts[-1]), locals=local_symbols)
    rhs = sympify(preprocess(rhs), locals=local_symbols)

    d = simplify(second - a)
    terms = simplify((last - a) / d + 1)
    lhs_sum = simplify(terms * (a + last) / 2)

    return {
        "a": a,
        "d": d,
        "last": last,
        "terms": terms,
        "lhs_sum": lhs_sum,
        "rhs": rhs
    }


def verify(statement):
    data = parse(statement)
    return simplify(data["lhs_sum"] - data["rhs"]) == 0


def base_case(statement):
    data = parse(statement)

    lhs = data["lhs_sum"].subs(n, 1)
    rhs = data["rhs"].subs(n, 1)

    return simplify(lhs - rhs) == 0


def inductive_step(statement):
    data = parse(statement)

    a = data["a"]
    d = data["d"]
    rhs = data["rhs"]
    
    Pk = rhs.subs(n, k)
    
    next_term = simplify(a + k * d)
    lhs = simplify(Pk + next_term)
    rhs_k1 = simplify(rhs.subs(n, k + 1))

    return simplify(lhs - rhs_k1) == 0