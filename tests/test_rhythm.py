import pytest
from listener_to_randomness.core.rhythm import RhythmicPattern, DURATIONS
from listener_to_randomness.randomness import DeterministicRandom


@pytest.fixture
def rng():
    return DeterministicRandom(seed=42)


@pytest.mark.parametrize("total_beats", [0.5, 1.0, 2.0, 4.0])
@pytest.mark.parametrize("rest_probability", [0.0, 0.2, 0.5])
def test_generate_rhythmic_pattern_structure(rng, total_beats, rest_probability):

    pattern = RhythmicPattern.generate(total_beats, rng, rest_probability)

    assert isinstance(pattern, RhythmicPattern)

    for dur, is_rest in pattern:
        assert dur in DURATIONS.values()
        assert isinstance(is_rest, bool)

    assert abs(pattern.total_duration() - total_beats) < 1e-6


def test_generate_rhythmic_pattern_rest_distribution(rng):

    total_beats = 4.0
    rest_probability = 0.3
    trials = 500

    rests = []

    for _ in range(trials):
        pattern = RhythmicPattern.generate(total_beats, rng, rest_probability)
        rests.extend(is_rest for _, is_rest in pattern)

    proportion = sum(rests) / len(rests)

    assert abs(proportion - rest_probability) < 0.05


def test_total_duration():

    pattern = RhythmicPattern([
        (1.0, False),
        (0.5, True),
        (0.5, False),
        (2.0, False)
    ])

    assert pattern.total_duration() == 4.0


def test_rhythmic_pattern_iterable():

    pattern = RhythmicPattern([
        (1.0, False),
        (1.0, True)
    ])

    values = list(pattern)

    assert values == [(1.0, False), (1.0, True)]


def test_rhythmic_pattern_len():

    pattern = RhythmicPattern([
        (1.0, False),
        (0.5, False),
        (0.5, True)
    ])

    assert len(pattern) == 3