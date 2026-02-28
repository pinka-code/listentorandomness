import pytest  # type: ignore
import random
from listener_to_randomness.core import dynamics
from listener_to_randomness.randomness.rng import DefaultRandom

@pytest.fixture
def rng():
    return DefaultRandom(seed=42)

def test_choose_dynamic_returns_int(rng):
    velocity = dynamics.choose_dynamic(rng)
    assert isinstance(velocity, int)

def test_choose_dynamic_in_range(rng):
    for _ in range(100):
        velocity = dynamics.choose_dynamic(rng)
        assert 10 <= velocity <= 110

def test_choose_dynamic_deterministic_with_seed():
    rng1 = random.Random(123)
    rng2 = random.Random(123)
    values1 = [dynamics.choose_dynamic(rng1) for _ in range(10)]
    values2 = [dynamics.choose_dynamic(rng2) for _ in range(10)]
    assert values1 == values2

def test_choose_dynamic_variation(rng):
    # Ensure multiple calls produce different values
    values = {dynamics.choose_dynamic(rng) for _ in range(50)}
    assert len(values) > 1