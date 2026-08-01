import re
from sympy import sympify, expand, simplify

_SUPERSCRIPT_DIGITS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")

_FUNCTION_NAMES = {
    "log", "ln", "exp", "sqrt",
    "sin", "cos", "tan", "asin", "acos", "atan",
    "Abs", "floor", "ceiling",
}


def preprocess(expr):
    expr = expr.replace("−", "-")
    expr = expr.replace("^", "**")

    expr = re.sub(
        r'([a-zA-Z0-9\)])([⁰¹²³⁴⁵⁶⁷⁸⁹]+)',
        lambda m: f"{m.group(1)}**{m.group(2).translate(_SUPERSCRIPT_DIGITS)}",
        expr,
    )

    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)

    def _insert_mult_before_call(match):
        identifier = match.group(1)
        if identifier in _FUNCTION_NAMES:
            return match.group(0)
        return f"{identifier}*("

    expr = re.sub(r'([a-zA-Z]+)\(', _insert_mult_before_call, expr)
    expr = re.sub(r'\)([a-zA-Z0-9\(])', r')*\1', expr)
    return expr


def _to_sympy(value):
    if isinstance(value, str):
        return sympify(preprocess(value))
    return sympify(value)


def equal(lhs, rhs):
    lhs = _to_sympy(lhs)
    rhs = _to_sympy(rhs)

    difference = lhs - rhs
    expanded = expand(difference)
    simplified = simplify(expanded)
    result = simplified == 0

    return result
