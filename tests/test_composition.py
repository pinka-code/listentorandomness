import pytest
from composition import Composition
from roles import RoleBehavior


class DummyInstrument:
    def __init__(self):
        self.notes = []


class DummyRandom:
    def __init__(self):
        self.values = [0.0, 0.0]  # force adding countermelody and pad
        self.index = 0

    def choice(self, seq):
        return seq[0]

    def randint(self, a, b):
        return a

    def random(self):
        val = self.values[self.index % len(self.values)]
        self.index += 1
        return val


class DummyRole(RoleBehavior):
    def __init__(self, config=None, tonic_midi=60, rng=None):
        self.config = config
        self.tonic_midi = tonic_midi
        self.rng = rng

    def choose_degree(self, measure, motif_idx):
        return 0

    def choose_octave(self):
        return 4

    def adjust_velocity(self, velocity, idx):
        return velocity

    def choose_pitch(self, degree, index):
        """For tests, just return tonic + octave*12 + degree modulo scale"""
        base_note = self.tonic_midi
        return base_note + 12 * 4 + degree  # fixed octave 4 for the test


@pytest.fixture
def config():
    class DummyConfig:
        tempo_bpm = 120
        total_duration = 4.0
        phrase_length_min = 1
        phrase_length_max = 1
        scale_notes = [0, 2, 4, 5, 7]
        phrase_variation_prob = 0.0
        tonic_midi = 60
    return DummyConfig()


def dummy_choose_instrument_for_role(rng, role):
    return DummyInstrument(), f"dummy_{role}"


def test_composition_generates_tracks(monkeypatch, config):
    monkeypatch.setattr(
        "composition.create_role",
        lambda **kwargs: DummyRole()
    )

    rng = DummyRandom()
    composition = Composition(config, rng)

    midi = composition.generate()

    times, tempos = midi.get_tempo_changes()

    assert len(tempos) == 1
    assert tempos[0] == config.tempo_bpm
    assert times[0] == 0.0

    # 3 fixed roles + 2 optional forced by DummyRandom
    assert len(midi.instruments) == 5
    assert len(composition.tracks) == 5