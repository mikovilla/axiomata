import pytest
from sympy import symbols

from axiomata.checks import equal, preprocess

k = symbols("k")


def test_equal_true_for_matching_expansion():
    assert equal((k + 1) ** 3 - (k + 1), (k ** 3 - k) + 3 * k * (k + 1)) is True


def test_equal_false_for_mismatched_expressions():
    assert equal((k + 1) ** 2, k ** 2 + 1) is False


def test_equal_true_for_trivially_identical_expressions():
    assert equal(k + 1, k + 1) is True


def test_equal_true_for_numeric_expressions():
    assert equal(2 + 2, 4) is True


def test_equal_accepts_string_expressions():
    assert equal("k**2 - 1", "(k-1)*(k+1)") is True

# preprocess

@pytest.mark.parametrize("expr, expected", [
    ("k³", "k**3"),
    ("k² + 1", "k**2 + 1"),
    ("(k+1)³ − (k+1)", "(k+1)**3 - (k+1)"),
    ("3k(k+1)", "3*k*(k+1)"),
    ("(k+1)(k-1)", "(k+1)*(k-1)"),
])
def test_preprocess(expr, expected):
    assert preprocess(expr) == expected


# natural math notation

def test_equal_true_with_superscripts_and_unicode_minus():
    assert equal("(k+1)³ − (k+1)", "(k³ − k) + 3k(k+1)") is True


def test_equal_false_with_superscripts_and_unicode_minus():
    assert equal("(k+1)²", "k² + 1") is False
