import pytest

from axiomata.induction import (
    preprocess,
    parse,
    base_case,
    inductive_step,
    explain,
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
    assert data["first_term"] == 1
    assert data["difference"] == 1
    assert data["rhs"] == n * (n + 1) / 2


def test_parse_odd_numbers():
    data = parse("1 + 3 + 5 + ... + (2n-1) = n^2")
    assert data["first_term"] == 1
    assert data["difference"] == 2
    assert data["rhs"] == n ** 2


def test_parse_starting_at_two():
    data = parse("2 + 4 + 6 + ... + 2n = n(n+1)")
    assert data["first_term"] == 2
    assert data["difference"] == 2
    assert data["rhs"] == n * (n + 1)


# base_case

@pytest.mark.parametrize("statement", [
    "1 + 2 + 3 + ... + n = n(n+1)/2",
    "1 + 3 + 5 + ... + (2n-1) = n^2",
    "2 + 4 + 6 + ... + 2n = n(n+1)",
])
def test_base_case_true(statement):
    assert base_case(statement, explain=False) is True


def test_base_case_false_for_incorrect_identity():
    assert base_case("1 + 2 + 3 + ... + n = n^2 + 1", explain=False) is False


# inductive_step

@pytest.mark.parametrize("statement", [
    "1 + 2 + 3 + ... + n = n(n+1)/2",
    "1 + 3 + 5 + ... + (2n-1) = n^2",
    "2 + 4 + 6 + ... + 2n = n(n+1)",
])
def test_inductive_step_true(statement):
    assert inductive_step(statement, explain=False) is True


def test_inductive_step_false_for_incorrect_identity():
    assert inductive_step("1 + 2 + 3 + ... + n = n^2", explain=False) is False


def test_verified_statement_passes_both_induction_conditions():
    statement = "1 + 2 + 3 + ... + n = n(n+1)/2"
    assert base_case(statement, explain=False) is True
    assert inductive_step(statement, explain=False) is True


# base_case / inductive_step explain output

def test_base_case_explain_false_prints_nothing(capsys):
    base_case("1 + 2 + 3 + ... + n = n(n+1)/2", explain=False)
    assert capsys.readouterr().out == ""


def test_base_case_explain_true_prints_line(capsys):
    ok = base_case("1 + 3 + 5 + ... + (2n-1) = n^2", explain=True)
    out = capsys.readouterr().out

    assert ok is True
    assert "Base (n = 1):  1 = 1  OK" in out


def test_inductive_step_explain_false_prints_nothing(capsys):
    inductive_step("1 + 2 + 3 + ... + n = n(n+1)/2", explain=False)
    assert capsys.readouterr().out == ""


def test_inductive_step_explain_true_prints_lines(capsys):
    ok = inductive_step("1 + 3 + 5 + ... + (2n-1) = n^2", explain=True)
    out = capsys.readouterr().out

    assert ok is True
    assert "Hypothesis:  assume P(k) = k**2" in out
    assert "k**2 + (2*k + 1) = (k + 1)**2  OK" in out


# explain

def test_explain_reports_success_for_correct_identity(capsys):
    explain("1 + 3 + 5 + ... + (2n-1) = n^2")
    out = capsys.readouterr().out

    assert "Base (n = 1):  1 = 1  OK" in out
    assert "k**2 + (2*k + 1) = (k + 1)**2  OK" in out
    assert "By induction, true for all n >= 1." in out


def test_explain_reports_failure_for_incorrect_identity(capsys):
    explain("1 + 2 + 3 + ... + n = n^2")
    out = capsys.readouterr().out

    assert "FAIL" in out
    assert "Induction fails: inductive step does not hold." in out
