import pytest
from phrase import Phrase
from note import Note

class DummyRandom:
    def __init__(self):
        self._random_value = 0.0
        self._choice_value = 0

    def choice(self, seq):
        return self._choice_value

    def randint(self, a, b):
        return a

    def random(self):
        return self._random_value


class DummyRole:
    def choisir_pitch(self, degre, index_note):
        return 60 + degre

    def ajuster_velocity(self, velocity, index_note):
        return velocity

    def choisir_note_finale(self):
        degre = 0
        octave = 3
        fraction_duree = 0.5
        pitch = self.choisir_pitch(degre, octave)
        return pitch, fraction_duree


class DummyMesure:
    def __init__(self, config, motif, rythme, role):
        self.rythme = rythme

    def jouer(self, time_depart, nuance):
        return [
            Note(
                pitch=60,
                start=time_depart,
                duration=1.0,
                velocity=nuance,
            )
        ]


@pytest.fixture
def config():
    class DummyConfig:
        variation_phrase_prob = 0.5
    return DummyConfig()


def test_phrase_ajoute_note_finale(config):
    role = DummyRole()
    rnd = DummyRandom()

    phrase = Phrase(
        config=config,
        motif_melodique=[0],
        motif_rythmique=[1],
        nb_mesures=1,
        role=role,
        mesure_class=DummyMesure,
        rng=rnd,
    )

    notes = phrase.jouer(time_depart=0, nuance=80)

    assert len(notes) == 2
    assert notes[-1].pitch == 60


def test_phrase_applique_variation(config):
    role = DummyRole()
    rnd = DummyRandom()
    rnd._random_value = 0.1  # inférieur à 0.5 → variation

    phrase = Phrase(
        config=config,
        motif_melodique=[0],
        motif_rythmique=[1],
        nb_mesures=2,
        role=role,
        mesure_class=DummyMesure,
        rng=rnd,
    )

    notes = phrase.jouer(time_depart=0, nuance=80)

    assert len(notes) == 3  # 2 mesures + note finale
