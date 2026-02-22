import pytest  # type: ignore
import random
import rhythm


@pytest.fixture
def rng():
    return random.Random(42)


def test_choose_duration_returns_valid_value(rng):
    duration = rhythm.choose_duration(rng)
    assert duration in rhythm.DURATIONS.values()


@pytest.mark.parametrize("probability", [0.0, 0.2, 0.5, 1.0])
def test_generate_rest_value_and_probability(rng, probability):
    trials = 1000
    results = [rhythm.generate_rest(rng, probability) for _ in range(trials)]
    # all results must be boolean
    assert all(isinstance(r, bool) for r in results)
    # check proportion matches probability
    proportion = sum(results) / trials
    assert abs(proportion - probability) < 0.05  # 5% tolerance


@pytest.mark.parametrize("length_beats", [1.0, 2.0, 4.0])
def test_generate_rhythmic_pattern_sum_correct(rng, length_beats):
    pattern = rhythm.generate_rhythmic_pattern(length_beats, rng)
    total = sum(pattern)
    assert abs(total - length_beats) < 1e-6
    assert all(d in rhythm.DURATIONS.values() for d in pattern)


@pytest.mark.parametrize("role", ["pad", "bass", "harmony", "counterpoint", "melody"])
def test_generate_rhythmic_pattern_for_role_sum_correct(rng, role):
    measure_length = 4.0
    pattern = rhythm.generate_rhythmic_pattern_for_role(measure_length, rng, role)
    total = sum(pattern)
    assert abs(total - measure_length) < 1e-6

    # role-specific checks
    if role == "pad":
        assert len(pattern) == 1
        assert pattern[0] == measure_length
    elif role == "bass":
        assert all(d == 1.0 for d in pattern)
        assert len(pattern) == int(measure_length)
    elif role == "harmony":
        assert all(d > 0 for d in pattern)
        assert total == pytest.approx(measure_length, abs=1e-6)
    elif role == "melody":
        assert all(d <= 1.0 for d in pattern)
    elif role == "counterpoint":
        assert all(d > 0 for d in pattern)
        assert total == pytest.approx(measure_length, abs=1e-6)