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

    first_term = sympify(preprocess(parts[0]), locals=local_symbols)
    second_term = sympify(preprocess(parts[1]), locals=local_symbols)
    rhs = sympify(preprocess(rhs), locals=local_symbols)

    difference = simplify(second_term - first_term)

    return {
        "first_term": first_term,
        "difference": difference,
        "rhs": rhs
    }


def mark(ok):
    return "OK" if ok else "FAIL"


def base_case(statement, base=1, explain=False):
    proposition = parse(statement)
    
    lhs = proposition["first_term"]
    rhs_1 = proposition["rhs"].subs(n, base)
    ok = lhs == rhs_1

    if explain:
        print(f"Base (n = 1):  {lhs} = {rhs_1}  {mark(ok)}")

    return ok


def inductive_step(statement, explain=False):
    proposition = parse(statement)

    Pk = proposition["rhs"].subs(n, k)
    next_term = proposition["first_term"] + k * proposition["difference"]
    lhs = Pk + next_term
    rhs_k1 = proposition["rhs"].subs(n, k + 1)
    ok = simplify(lhs - rhs_k1) == 0

    if explain:
        print(f"Hypothesis:  assume P(k) = {Pk}")
        print(f"Step:  add the next term, {next_term} ->")
        print(f"    {Pk} + ({next_term}) = {rhs_k1}  {mark(ok)}")

    return ok


def explain(statement):
    print(f"proposition  {statement}")
    print()

    base_ok = base_case(statement, explain=True)
    step_ok = inductive_step(statement, explain=True)

    if base_ok and step_ok:
        print("So, P(k+1) holds. By induction, true for all n >= 1.")
    else:
        print("Induction fails: " + ("base case" if not base_ok else "inductive step") + " does not hold.")
