import inspect

import pytest

from axiomata.sort import Sort, Type, Animation, bubble, selection, insertion

TYPES = [Type.BUBBLE, Type.SELECTION, Type.INSERTION]


@pytest.mark.parametrize("sort_type", TYPES)
def test_sorts_random_default_count(sort_type):
    result = Sort(sort_type).animate()
    assert result == sorted(result)
    assert len(result) == 10
    assert len(set(result)) == 10


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_with_int_generates_random_count(sort_type):
    result = Sort(sort_type).array(6).animate()
    assert result == sorted(result)
    assert len(result) == 6
    assert len(set(result)) == 6


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_with_explicit_values_sorts_them(sort_type):
    result = Sort(sort_type).array([5, 3, 8, 1, 9, 2]).animate()
    assert result == [1, 2, 3, 5, 8, 9]


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_called_without_arguments_resets_to_default_ten(sort_type):
    result = Sort(sort_type).array(3).array().animate()
    assert len(result) == 10


@pytest.mark.parametrize("sort_type", TYPES)
def test_does_not_mutate_input_array(sort_type):
    original = [5, 3, 8, 1]
    Sort(sort_type).array(original).animate()
    assert original == [5, 3, 8, 1]


@pytest.mark.parametrize("sort_type", TYPES)
def test_count_over_max_raises(sort_type):
    with pytest.raises(ValueError):
        Sort(sort_type).array(11).animate()


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_over_max_raises(sort_type):
    with pytest.raises(ValueError):
        Sort(sort_type).array(list(range(11))).animate()


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_with_duplicates_raises(sort_type):
    with pytest.raises(ValueError):
        Sort(sort_type).array([1, 2, 2, 3]).animate()


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_with_non_numbers_raises(sort_type):
    with pytest.raises(ValueError):
        Sort(sort_type).array([1, 2, "3"]).animate()


@pytest.mark.parametrize("sort_type", TYPES)
def test_array_with_booleans_raises(sort_type):
    with pytest.raises(ValueError):
        Sort(sort_type).array([1, 2, True]).animate()


@pytest.mark.parametrize("sort_type", TYPES)
def test_matplotlib_animation_not_implemented(sort_type):
    with pytest.raises(NotImplementedError):
        Sort(sort_type).animate(Animation.MATPLOTLIB)


@pytest.mark.parametrize("sort_type", TYPES)
def test_ansi_animation_returns_sorted_values(sort_type):
    result = Sort(sort_type).array([5, 3, 8, 1, 9]).delay(0).animate(Animation.ANSI)
    assert result == [1, 3, 5, 8, 9]


@pytest.mark.parametrize("sort_type", TYPES)
def test_ansi_animation_prints_frames(sort_type, capsys):
    Sort(sort_type).array([5, 3, 8, 1]).delay(0).animate(Animation.ANSI)
    out = capsys.readouterr().out
    assert "#" in out


def test_repeated_animate_calls_reuse_same_starting_values():
    run = Sort(Type.BUBBLE).array([5, 3, 8, 1])
    assert run.animate() == [1, 3, 5, 8]
    assert run.animate() == [1, 3, 5, 8]


@pytest.mark.parametrize("convenience_fn", [bubble, selection, insertion])
def test_module_level_convenience_functions(convenience_fn):
    result = convenience_fn()
    assert result == sorted(result)
    assert len(result) == 10


@pytest.mark.parametrize("convenience_fn", [bubble, selection, insertion])
def test_shorthand_delay_defaults_to_one(convenience_fn):
    assert inspect.signature(convenience_fn).parameters["delay"].default == 1


@pytest.mark.parametrize("convenience_fn", [bubble, selection, insertion])
def test_shorthand_can_animate(convenience_fn, capsys):
    result = convenience_fn(animate=Animation.ANSI, delay=0)
    assert result == sorted(result)
    out = capsys.readouterr().out
    assert "#" in out
    assert len(set(result)) == 10
