import pytest
from mesure import Mesure


class DummyRole:
    def choisir_pitch(self, degre, index_note):
        return 60 + degre

    def ajuster_velocity(self, velocity, index_note):
        return velocity + 5


@pytest.fixture
def config():
    class DummyConfig:
        signature_num = 4
        signature_den = 4
    return DummyConfig()


def test_mesure_genere_notes_selon_motif(config):
    motif = [0, 2, 4]
    rythme = [1, 1, 1]

    role = DummyRole()
    mesure = Mesure(config, motif, rythme, role)

    notes = mesure.jouer(time_depart=0, nuance=80)

    assert len(notes) == 3
    assert notes[0].pitch == 60
    assert notes[1].pitch == 62
    assert notes[2].pitch == 64


def test_mesure_applique_velocity_role(config):
    motif = [0]
    rythme = [1]

    role = DummyRole()
    mesure = Mesure(config, motif, rythme, role)

    notes = mesure.jouer(time_depart=0, nuance=70)

    assert notes[0].velocity == 75


def test_mesure_respecte_timing(config):
    motif = [0, 1]
    rythme = [1, 2]

    role = DummyRole()
    mesure = Mesure(config, motif, rythme, role)

    notes = mesure.jouer(time_depart=10, nuance=80)

    assert notes[0].start == 10
    assert notes[1].start == 11
