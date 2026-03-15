import pytest
import math

from listener_to_randomness.randomness.base import (
    DeterministicRandom,
    TimeSeedRandom,
    SecureRandom,
    FractalRandom,
)

# All RNG implementations to test
RNG_CLASSES = [
    DeterministicRandom,
    TimeSeedRandom,
    SecureRandom,
    FractalRandom,
]


def make_rng(cls):
    """Factory to create RNG instances with proper seeding."""
    if cls in (DeterministicRandom, FractalRandom):
        return cls(seed=123)
    return cls()


# ------------------------------------------------------------
# Deterministic behaviour
# ------------------------------------------------------------

def test_deterministic_repeatability():
    """DeterministicRandom should produce identical sequences."""
    rng1 = DeterministicRandom(seed=42)
    rng2 = DeterministicRandom(seed=42)

    for _ in range(20):
        assert rng1.randint(0, 100) == rng2.randint(0, 100)
        assert math.isclose(rng1.random(), rng2.random(), rel_tol=1e-9)


def test_secure_random_not_constant():
    """SecureRandom should not produce constant values."""
    rng = SecureRandom()
    results = [rng.randint(0, 100) for _ in range(100)]

    assert len(set(results)) > 1


# ------------------------------------------------------------
# Basic value ranges
# ------------------------------------------------------------

@pytest.mark.parametrize("cls", RNG_CLASSES)
def test_random_range(cls):
    """random() should return float in [0,1)."""
    rng = make_rng(cls)

    for _ in range(100):
        val = rng.random()
        assert 0.0 <= val < 1.0


@pytest.mark.parametrize("cls", RNG_CLASSES)
def test_randint_range(cls):
    """randint should always stay in bounds."""
    rng = make_rng(cls)

    for _ in range(100):
        val = rng.randint(10, 20)
        assert 10 <= val <= 20


@pytest.mark.parametrize("cls", RNG_CLASSES)
def test_uniform_range(cls):
    """uniform should return values within range."""
    rng = make_rng(cls)

    for _ in range(100):
        val = rng.uniform(-5, 5)
        assert -5 <= val <= 5


# ------------------------------------------------------------
# Choice methods
# ------------------------------------------------------------

@pytest.mark.parametrize("cls", RNG_CLASSES)
def test_choice(cls):
    """choice should always pick an element from sequence."""
    rng = make_rng(cls)

    seq = [10, 20, 30, 40]

    for _ in range(50):
        assert rng.choice(seq) in seq


@pytest.mark.parametrize("cls", RNG_CLASSES)
def test_choice_weighted(cls):
    """choice_weighted should pick valid elements."""
    rng = make_rng(cls)

    seq = ["a", "b", "c"]
    weights = [1, 2, 3]

    for _ in range(50):
        val = rng.choice_weighted(seq, weights)
        assert val in seq


# ------------------------------------------------------------
# Shuffle
# ------------------------------------------------------------

@pytest.mark.parametrize("cls", RNG_CLASSES)
def test_shuffle_preserves_elements(cls):
    """shuffle should keep same elements."""
    rng = make_rng(cls)

    seq = [1, 2, 3, 4, 5]
    shuffled = rng.shuffle(seq.copy())

    assert sorted(shuffled) == sorted(seq)
    assert len(shuffled) == len(seq)


# ------------------------------------------------------------
# Fork behaviour
# ------------------------------------------------------------

@pytest.mark.parametrize("cls", RNG_CLASSES)
def test_fork_returns_same_type(cls):
    """fork() should return the same RNG class."""
    rng = make_rng(cls)
    child = rng.fork()

    assert isinstance(child, cls)


@pytest.mark.parametrize("cls", RNG_CLASSES)
def test_fork_independent_instance(cls):
    """fork() should create a distinct RNG instance."""
    rng = make_rng(cls)
    child = rng.fork(seed_offset=1)

    assert child is not rng
    assert isinstance(child, cls)

@pytest.mark.parametrize("cls", RNG_CLASSES)
def test_fork_changes_state_when_possible(cls):
    rng = make_rng(cls)
    child = rng.fork(seed_offset=1)

    if hasattr(rng, "x") and hasattr(child, "x"):
        assert rng.x != child.x

# ------------------------------------------------------------
# FractalRandom specific tests
# ------------------------------------------------------------

def test_fractal_random_stays_in_bounds():
    """Fractal map should never escape [0,1)."""
    rng = FractalRandom(seed=0.5)

    for _ in range(1000):
        val = rng.random()
        assert 0 <= val < 1


def test_fractal_random_repeatable():
    """Same seed should give same chaotic sequence."""
    rng1 = FractalRandom(seed=0.123)
    rng2 = FractalRandom(seed=0.123)

    for _ in range(50):
        assert math.isclose(rng1.random(), rng2.random(), rel_tol=1e-9)

def test_fractal_fork_changes_seed():
    rng = FractalRandom(seed=0.5)
    child = rng.fork(seed_offset=0.1)

    assert rng.x != child.x