import matplotlib
matplotlib.use("Agg")

import pytest

from axiomata.sort import Sort, Type, Animation

TYPES = [Type.BUBBLE, Type.SELECTION, Type.INSERTION]


@pytest.mark.parametrize("sort_type", TYPES)
def test_sorts_random_default_count(sort_type):
    result = Sort(sort_type).run()
    assert result == sorted(result)
    assert len(result) == 20
    assert len(set(result)) == 20


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_with_int_generates_random_count(sort_type):
    result = Sort(sort_type).array(6).run()
    assert result == sorted(result)
    assert len(result) == 6
    assert len(set(result)) == 6


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_with_explicit_values_sorts_them(sort_type):
    result = Sort(sort_type).array([5, 3, 8, 1, 9, 2]).run()
    assert result == [1, 2, 3, 5, 8, 9]


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_called_without_arguments_resets_to_default_count(sort_type):
    result = Sort(sort_type).array(3).array().run()
    assert len(result) == 20


@pytest.mark.parametrize("sort_type", TYPES)
def test_does_not_mutate_input_array(sort_type):
    original = [5, 3, 8, 1]
    Sort(sort_type).array(original).run()
    assert original == [5, 3, 8, 1]


@pytest.mark.parametrize("sort_type", TYPES)
def test_count_over_max_raises(sort_type):
    with pytest.raises(ValueError):
        Sort(sort_type).array(21).run()


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_over_max_raises(sort_type):
    with pytest.raises(ValueError):
        Sort(sort_type).array(list(range(21))).run()


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_with_duplicates_raises(sort_type):
    with pytest.raises(ValueError):
        Sort(sort_type).array([1, 2, 2, 3]).run()


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_with_non_numbers_raises(sort_type):
    with pytest.raises(ValueError):
        Sort(sort_type).array([1, 2, "3"]).run()


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_with_booleans_raises(sort_type):
    with pytest.raises(ValueError):
        Sort(sort_type).array([1, 2, True]).run()


@pytest.mark.parametrize("sort_type", TYPES)
def test_animate_defaults_to_ansi(sort_type, capsys):
    result = Sort(sort_type).array([5, 3, 8, 1]).delay(0).animate()
    assert result == sorted(result)
    out = capsys.readouterr().out
    assert "#" in out


@pytest.mark.parametrize("sort_type", TYPES)
def test_ansi_animation_returns_sorted_values(sort_type):
    result = Sort(sort_type).array([5, 3, 8, 1, 9]).delay(0).animate(Animation.ANSI)
    assert result == [1, 3, 5, 8, 9]


@pytest.mark.parametrize("sort_type", TYPES)
def test_ansi_animation_shows_before_and_after_labels(sort_type, capsys):
    Sort(sort_type).array([5, 3, 8, 1]).delay(0).animate(Animation.ANSI)
    out = capsys.readouterr().out
    assert "Before" in out
    assert "After" in out


@pytest.mark.parametrize("sort_type", TYPES)
def test_matplotlib_animation_returns_sorted_values(sort_type):
    result = Sort(sort_type).array([5, 3, 8, 1, 9]).delay(0).animate(Animation.MATPLOTLIB)
    assert result == [1, 3, 5, 8, 9]


@pytest.mark.parametrize("sort_type", TYPES)
def test_invalid_animation_raises(sort_type):
    with pytest.raises(ValueError):
        Sort(sort_type).animate("not-an-animation")


def test_run_prints_before_and_after(capsys):
    result = Sort(Type.BUBBLE).array([5, 3, 8, 1]).run()
    out = capsys.readouterr().out
    assert "Before" in out
    assert "After" in out
    assert result == [1, 3, 5, 8]


def test_run_prints_steps_summary(capsys):
    Sort(Type.BUBBLE).array([5, 3, 8, 1]).run()
    out = capsys.readouterr().out
    assert "Before: [5, 3, 8, 1]" in out
    assert "After:  [1, 3, 5, 8]" in out
    assert "Steps:" in out


def test_run_does_not_print_intermediate_step_frames(capsys):
    Sort(Type.BUBBLE).array([5, 3, 8, 1]).run()
    out = capsys.readouterr().out
    assert "Step 1/" not in out


@pytest.mark.parametrize("sort_type", TYPES)
def test_animate_prints_steps_summary(sort_type, capsys):
    Sort(sort_type).array([5, 3, 8, 1]).delay(0).animate()
    out = capsys.readouterr().out
    assert "Before: [5, 3, 8, 1]" in out
    assert "After:  [1, 3, 5, 8]" in out
    assert "Steps:" in out


def test_repeated_animate_calls_reuse_same_starting_values():
    run = Sort(Type.BUBBLE).array([5, 3, 8, 1]).delay(0)
    assert run.animate() == [1, 3, 5, 8]
    assert run.animate() == [1, 3, 5, 8]
