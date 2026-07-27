import pytest
from sympy import Rational, sympify

from induction.induction import (
    preprocess,
    parse,
    verify,
    base_case,
    inductive_step,
    n,
)


# preprocess

@pytest.mark.parametrize("expr, expected", [
    ("2n", "2*n"),
    ("n(n+1)", "n*(n+1)"),
    ("(n+1)n", "(n+1)*n"),
    ("n^2", "n**2"),
    ("2n^2", "2*n**2"),
])
def test_preprocess(expr, expected):
    assert preprocess(expr) == expected


# parse

def test_parse_consecutive_integers():
    data = parse("1 + 2 + 3 + ... + n = n(n+1)/2")
    assert data["a"] == 1
    assert data["d"] == 1
    assert data["last"] == n
    assert data["terms"] == n
    assert data["lhs_sum"] == n * (n + 1) / 2
    assert data["rhs"] == n * (n + 1) / 2


def test_parse_odd_numbers():
    data = parse("1 + 3 + 5 + ... + (2n-1) = n^2")
    assert data["a"] == 1
    assert data["d"] == 2
    assert data["rhs"] == n ** 2


# verify

@pytest.mark.parametrize("statement", [
    "1 + 2 + 3 + ... + n = n(n+1)/2",
    "1 + 3 + 5 + ... + (2n-1) = n^2",
    "2 + 4 + 6 + ... + 2n = n(n+1)",
])
def test_verify_true_for_correct_identities(statement):
    assert verify(statement) is True


def test_verify_false_for_incorrect_identity():
    assert verify("1 + 2 + 3 + ... + n = n^2") is False


# base_case

@pytest.mark.parametrize("statement", [
    "1 + 2 + 3 + ... + n = n(n+1)/2",
    "1 + 3 + 5 + ... + (2n-1) = n^2",
])
def test_base_case_true(statement):
    assert base_case(statement) is True


def test_base_case_false_for_incorrect_identity():
    assert base_case("1 + 2 + 3 + ... + n = n^2 + 1") is False


# inductive_step

@pytest.mark.parametrize("statement", [
    "1 + 2 + 3 + ... + n = n(n+1)/2",
    "1 + 3 + 5 + ... + (2n-1) = n^2",
    "2 + 4 + 6 + ... + 2n = n(n+1)",
])
def test_inductive_step_true(statement):
    assert inductive_step(statement) is True


def test_inductive_step_false_for_incorrect_identity():
    assert inductive_step("1 + 2 + 3 + ... + n = n^2") is False


def test_verified_statement_passes_both_induction_conditions():
    statement = "1 + 2 + 3 + ... + n = n(n+1)/2"
    assert base_case(statement) is True
    assert inductive_step(statement) is True
