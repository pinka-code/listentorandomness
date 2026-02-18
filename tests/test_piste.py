import pytest
from piste import Piste
from note import Note

class DummyInstrument:
    def __init__(self):
        self.notes = []

class DummyRole:
    def choisir_pitch(self, degre, index_note):
        return 60

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


class DummyRandom:
    def choice(self, seq):
        return seq[0]

    def randint(self, a, b):
        return a

    def random(self):
        return 1.0


@pytest.fixture
def config():
    class DummyConfig:
        duree_totale = 4.0
        longueur_phrase_min = 1
        longueur_phrase_max = 1
        notes_gamme = [0, 2, 4, 5, 7]
        variation_phrase_prob = 0.0
    return DummyConfig()


def test_piste_ne_depasse_pas_duree_totale(config):
    instrument = DummyInstrument()
    piste = Piste(
        config=config,
        rng=DummyRandom(),
        role=DummyRole(),
        instrument=instrument,
        nom_instrument="piano",
        mesure_class=DummyMesure,
    )

    piste.generer()

    assert all(note.end <= config.duree_totale for note in instrument.notes)
