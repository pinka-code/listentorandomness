import pytest
import random
from listener_to_randomness.core import rhythm
from listener_to_randomness.randomness.rng import DefaultRandom

@pytest.fixture
def rng():
    return DefaultRandom(seed=42)


def test_generate_rest_returns_boolean(rng):
    for _ in range(100):
        result = rhythm.generate_rest(rng, probability=0.5)
        assert isinstance(result, bool)


@pytest.mark.parametrize("probability", [0.0, 0.1, 0.5, 1.0])
def test_generate_rest_probability(rng, probability):
    trials = 1000
    results = [rhythm.generate_rest(rng, probability) for _ in range(trials)]
    proportion = sum(results) / trials
    assert abs(proportion - probability) < 0.05


@pytest.mark.parametrize("total_beats", [0.5, 1.0, 2.0, 4.0])
@pytest.mark.parametrize("rest_probability", [0.0, 0.2, 0.5])
def test_generate_rhythmic_pattern_structure(rng, total_beats, rest_probability):
    pattern = rhythm.generate_rhythmic_pattern(total_beats, rng, rest_probability)

    assert all(isinstance(p, tuple) and len(p) == 2 for p in pattern)

    for dur, is_rest in pattern:
        assert dur in rhythm.DURATIONS.values()
        assert isinstance(is_rest, bool)

    total = sum(dur for dur, _ in pattern)
    assert abs(total - total_beats) < 1e-6


def test_generate_rhythmic_pattern_rest_distribution(rng):
    total_beats = 4.0
    rest_probability = 0.3
    trials = 500

    rests = []
    for _ in range(trials):
        pattern = rhythm.generate_rhythmic_pattern(total_beats, rng, rest_probability)
        rests.extend(is_rest for _, is_rest in pattern)

    proportion = sum(rests) / len(rests)
    assert abs(proportion - rest_probability) < 0.05