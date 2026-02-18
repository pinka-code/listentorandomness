import pytest # type: ignore
import random

from roles import RoleMelodie, RoleBasse, RolePad, RoleContrechant

class FakeConfig:
    # notes_gamme modulo 12
    notes_gamme = [0, 2, 4, 5, 7, 9, 11]
    tempo_bpm = 120
    signature_num = 4
    signature_den = 4
    duree_totale = 16.0
    longueur_phrase_min = 1
    longueur_phrase_max = 2
    variation_phrase_prob = 0.5
    prob_resolution_tonique = 0.5
    tonique_midi = 60

@pytest.fixture
def rng():
    return random.Random(42)

@pytest.fixture
def config():
    return FakeConfig()

@pytest.mark.parametrize("RoleClass", [RoleMelodie, RoleBasse, RolePad, RoleContrechant])
def test_role_generer_pitch_octave_et_velocity(config, rng, RoleClass):
    role = RoleClass(config=config, rng=rng)

    for _ in range(20):
        degre = rng.randint(0, len(config.notes_gamme)-1)
        octave = role.choisir_octave()
        pitch = role.choisir_pitch(degre, octave)
        velocity = role.ajuster_velocity(80)

        # pitch doit être dans la gamme relative modulo 12
        intervalle = (pitch - config.tonique_midi) % 12
        assert intervalle in config.notes_gamme, f"Intervalle {intervalle} pas dans la gamme {config.notes_gamme}"

        # pitch MIDI valide
        assert 0 <= pitch <= 127

        # velocity valide
        assert 0 <= velocity <= 127

def test_role_note_finale(config, rng):
    role = RoleMelodie(config=config, rng=rng)

    for _ in range(20):
        pitch, fraction = role.choisir_note_finale()

        intervalle = (pitch - config.tonique_midi) % 12
        assert intervalle in config.notes_gamme

        # fraction doit être positive et <=1
        assert 0 < fraction <= 1

def test_role_octave_variation(config, rng):
    role = RoleBasse(config=config, rng=rng)
    octaves = set(role.choisir_octave() for _ in range(50))
    # on attend plusieurs octaves possibles pour ce rôle
    assert octaves <= {1, 2}

def test_role_velocity_adjustment(config, rng):
    role = RolePad(config=config, rng=rng)

    # velocity de base 80 → doit diminuer de 10 pour pad
    v = role.ajuster_velocity(80)
    assert v == 70

def test_role_pitch_deterministe(config):
    # Avec un rng fixé, le pitch doit être déterministe
    rng1 = random.Random(123)
    rng2 = random.Random(123)
    role1 = RoleMelodie(config=config, rng=rng1)
    role2 = RoleMelodie(config=config, rng=rng2)

    degre = 2
    octave = role1.choisir_octave()
    pitch1 = role1.choisir_pitch(degre, octave)
    pitch2 = role2.choisir_pitch(degre, octave)

    assert pitch1 == pitch2
