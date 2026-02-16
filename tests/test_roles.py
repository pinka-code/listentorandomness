import pytest # type: ignore
import types
import random

from roles import (
    RoleComportement,
    RoleMelodie,
    RoleBasse,
    RolePad,
    RoleContrechant,
    creer_role
)

class FakeMesure:
    """Mesure factice pour tests de rôle"""
    def __init__(self, motif=[0,1,2], rng=None):
        self.motif = motif
        self.rng = rng or random.Random()

@pytest.fixture
def rng():
    return random.Random(42)

@pytest.fixture
def mesure_factice(rng):
    return FakeMesure(rng=rng)

def test_creer_role_instancie_le_bon_role():
    r1 = creer_role("melodie")
    r2 = creer_role("basse")
    r3 = creer_role("pad")
    r4 = creer_role("contrechant")
    r_default = creer_role("inconnu")

    assert isinstance(r1, RoleMelodie)
    assert isinstance(r2, RoleBasse)
    assert isinstance(r3, RolePad)
    assert isinstance(r4, RoleContrechant)
    assert isinstance(r_default, RoleComportement)

def test_choisir_degre_rol_comportement(mesure_factice):
    role = RoleComportement()
    motif_idx = 0
    degre = role.choisir_degre(mesure_factice, motif_idx)
    assert degre in mesure_factice.motif

def test_choisir_octave_range(mesure_factice):
    roles = [RoleComportement(), RoleMelodie(), RoleBasse(), RolePad(), RoleContrechant()]
    for role in roles:
        octave = role.choisir_octave(mesure_factice)
        assert 0 <= octave <= 5  # plage réaliste pour tests

def test_ajuster_velocity(mesure_factice):
    roles = [RoleComportement(), RoleMelodie(), RoleBasse(), RolePad(), RoleContrechant()]
    for role in roles:
        v = 64
        v2 = role.ajuster_velocity(v)
        assert 0 <= v2 <= 127
        # tests spécifiques aux rôles
        if isinstance(role, RoleMelodie):
            assert v2 == min(127, v + 10)
        elif isinstance(role, RoleBasse):
            assert v2 == min(127, v + 5)
        elif isinstance(role, RolePad):
            assert v2 == max(20, v - 10)
        elif isinstance(role, RoleContrechant):
            assert v2 == min(127, v + 5)
        else:
            assert v2 == v

def test_choisir_note_finale(mesure_factice, rng):
    roles = [RoleMelodie(), RoleBasse(), RolePad(), RoleContrechant(), RoleComportement()]
    for role in roles:
        degre, octave, fraction_duree = role.choisir_note_finale(mesure_factice, config=types.SimpleNamespace(notes_gamme=list(range(12))), rng=rng)
        assert degre in range(12)
        assert 0 <= octave <= 5
        assert 0.0 < fraction_duree <= 1.0
