import pytest # type: ignore
import random
import nuances

@pytest.fixture
def rng():
    return random.Random(42)

def test_choisir_nuance_retourne_int(rng):
    velocity = nuances.choisir_nuance(rng)
    assert isinstance(velocity, int)

def test_choisir_nuance_dans_intervalle(rng):
    for _ in range(100):
        velocity = nuances.choisir_nuance(rng)
        assert 10 <= velocity <= 110

def test_choisir_nuance_deterministe_avec_seed():
    rng1 = random.Random(123)
    rng2 = random.Random(123)
    valeurs1 = [nuances.choisir_nuance(rng1) for _ in range(10)]
    valeurs2 = [nuances.choisir_nuance(rng2) for _ in range(10)]
    assert valeurs1 == valeurs2

def test_choisir_nuance_variation(rng):
    # On s'assure que plusieurs appels produisent différentes valeurs
    valeurs = {nuances.choisir_nuance(rng) for _ in range(50)}
    assert len(valeurs) > 1
