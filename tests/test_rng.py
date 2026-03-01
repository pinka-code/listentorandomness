import pytest
import math
from listener_to_randomness.randomness.base import (
    DeterministicRandom,
    TimeSeedRandom,
    SecureRandom,
    FractalRandom,
)


@pytest.mark.parametrize("cls", [DeterministicRandom])
def test_prng_repeatable(cls):
    """PRNG with fixed seed should produce the same sequence."""
    rng1 = cls(seed=42) if cls is DeterministicRandom else cls()
    rng2 = cls(seed=42) if cls is DeterministicRandom else cls()
    
    for _ in range(10):
        assert rng1.randint(0, 100) == rng2.randint(0, 100)
        assert math.isclose(rng1.random(), rng2.random(), rel_tol=1e-9)


def test_secure_random_unpredictable():
    """SecureRandom should not produce the same sequence twice."""
    rng = SecureRandom()
    results = [rng.randint(0, 100) for _ in range(100)]
    # Should contain some variation
    assert len(set(results)) > 1


@pytest.mark.parametrize("cls", [DeterministicRandom, TimeSeedRandom, SecureRandom, FractalRandom])
def test_choice_methods(cls):
    """Test choice and choice_weighted produce elements from the sequence."""
    rng = cls(seed=123) if cls in [DeterministicRandom, FractalRandom] else cls()
    seq = [10, 20, 30, 40, 50]
    weights = [1, 1, 1, 1, 1]
    
    for _ in range(20):
        val1 = rng.choice(seq)
        val2 = rng.choice_weighted(seq, weights)
        assert val1 in seq
        assert val2 in seq


@pytest.mark.parametrize("cls", [DeterministicRandom, TimeSeedRandom, SecureRandom, FractalRandom])
def test_randint_range(cls):
    """randint should always be within bounds."""
    rng = cls(seed=123) if cls in [DeterministicRandom, FractalRandom] else cls()
    
    for _ in range(50):
        val = rng.randint(10, 20)
        assert 10 <= val <= 20


@pytest.mark.parametrize("cls", [DeterministicRandom, TimeSeedRandom, SecureRandom, FractalRandom])
def test_random_range(cls):
    """random() should return float in [0,1)."""
    rng = cls(seed=123) if cls in [DeterministicRandom, FractalRandom] else cls()
    
    for _ in range(50):
        val = rng.random()
        assert 0.0 <= val < 1.0