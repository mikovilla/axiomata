import pytest
from sympy import log, symbols

from calculate.master_theorem import critical_exponent, master_theorem

n = symbols("n", positive=True)


# critical_exponent

def test_critical_exponent_merge_sort():
    assert critical_exponent(2, 2) == 1


def test_critical_exponent_binary_search():
    assert critical_exponent(1, 2) == 0


def test_critical_exponent_perfect_square():
    assert critical_exponent(9, 3) == 2


# master_theorem: case 1

def test_case_1_returns_expected_theta():
    result = master_theorem(9, 3, "n")
    assert result["case"] == 1
    assert result["critical_exponent"] == 2
    assert result["theta"] == n ** 2


# master_theorem: case 2

def test_case_2_merge_sort():
    result = master_theorem(2, 2, "n")
    assert result["case"] == 2
    assert result["theta"] == n * log(n)


def test_case_2_binary_search():
    result = master_theorem(1, 2, "1")
    assert result["case"] == 2
    assert result["theta"] == log(n)


def test_case_2_with_log_factor_already_present():
    # T(n) = 4T(n/2) + n^2 -> c=2, f(n)=n^2=Theta(n^c), so Theta(n^2 log n)
    result = master_theorem(4, 2, "n^2")
    assert result["case"] == 2
    assert result["theta"] == n ** 2 * log(n)


# master_theorem: case 3

def test_case_3_with_regularity_holding():
    result = master_theorem(3, 4, "n*log(n)")
    assert result["case"] == 3
    assert result["theta"] == n * log(n)
    assert bool(result["regularity_holds"]) is True


# accepts sympy expressions, not just strings

def test_accepts_sympy_expression_for_f_n():
    result = master_theorem(2, 2, n)
    assert result["case"] == 2
    assert result["theta"] == n * log(n)


# explain output

def test_explain_false_prints_nothing(capsys):
    master_theorem(2, 2, "n", explain=False)
    assert capsys.readouterr().out == ""


def test_explain_true_prints_case_and_conclusion(capsys):
    master_theorem(2, 2, "n", explain=True)
    out = capsys.readouterr().out

    assert "Critical exponent" in out
    assert "Case 2" in out
    assert "Conclusion:  T(n) = Theta(n*log(n))" in out


def test_explain_true_prints_regularity_for_case_3(capsys):
    master_theorem(3, 4, "n*log(n)", explain=True)
    out = capsys.readouterr().out

    assert "Regularity condition" in out
    assert "holds" in out
