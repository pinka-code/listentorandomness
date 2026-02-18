import pytest
from morceau import Morceau
from roles import RoleComportement


class DummyInstrument:
    def __init__(self):
        self.notes = []


class DummyRandom:
    def __init__(self):
        self.values = [0.0, 0.0]  # force ajout contrechant et pad
        self.index = 0

    def choice(self, seq):
        return seq[0]

    def randint(self, a, b):
        return a

    def random(self):
        val = self.values[self.index % len(self.values)]
        self.index += 1
        return val



class DummyRole(RoleComportement):
    def __init__(self, config=None, tonique_midi=60, rng=None):
        self.config = config
        self.tonique_midi = tonique_midi
        self.rng = rng

    def choisir_degre(self, mesure, motif_idx):
        return 0

    def choisir_octave(self):
        return 4

    def ajuster_velocity(self, velocity, idx):
        return velocity

    def choisir_pitch(self, degre, index):
        """Pour les tests, retourne juste tonique + octave*12 + degre modulo gamme"""
        note_base = self.tonique_midi
        return note_base + 12 * 4 + degre  # octave fixe 4 pour le test


@pytest.fixture
def config():
    class DummyConfig:
        tempo_bpm = 120
        duree_totale = 4.0
        longueur_phrase_min = 1
        longueur_phrase_max = 1
        notes_gamme = [0, 2, 4, 5, 7]
        variation_phrase_prob = 0.0
        tonique_midi = 60
    return DummyConfig()


def dummy_choisir_instrument_pour_role(rng, role):
    return DummyInstrument(), f"dummy_{role}"


def test_morceau_genere_des_pistes(monkeypatch, config):
    monkeypatch.setattr(
        "morceau.creer_role",
        lambda **kwargs: DummyRole()
    )

    rng = DummyRandom()
    morceau = Morceau(config, rng)

    midi = morceau.generer()

    times, tempos = midi.get_tempo_changes()

    assert len(tempos) == 1
    assert tempos[0] == config.tempo_bpm
    assert times[0] == 0.0

    # 3 rôles fixes + 2 optionnels forcés par DummyRandom
    assert len(midi.instruments) == 5
    assert len(morceau.pistes) == 5
