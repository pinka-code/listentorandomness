import pytest
from listener_to_randomness.core.composition import Composition
from listener_to_randomness.core.rhythm import RhythmicPattern

class DummyInstrument:
    def __init__(self):
        self.notes = []


class DummyRandom:
    def __init__(self):
        self.values = [0.0, 0.0]  # force adding countermelody and pad
        self.index = 0

    def choice(self, seq):
        return seq[0]
    
    def choice_weighted(self, seq, weights):
        return seq[0]

    def randint(self, a, b):
        return a

    def random(self):
        val = self.values[self.index % len(self.values)]
        self.index += 1
        return val


class DummyRole:
    def choose_pitch(self, degree):
        return 60 + degree

    def adjust_velocity(self, velocity):
        return velocity + 5
    
    def generate_rhythm(self, measure_duration):
        pattern = []
        remaining = measure_duration
        while remaining > 0:
            dur = 1.0 if remaining >= 1.0 else remaining
            pattern.append((dur, False))
            remaining -= dur

        return RhythmicPattern(pattern)

    def phrase_length(self):
            return 4

@pytest.fixture
def config():
    class DummyConfig:
        pattern_length_min = 1
        pattern_length_max = 1
        scale_notes = [0, 2, 4, 5, 7]
        phrase_variation_prob = 0.0
        tonic_midi = 60
        time_signature_num = 4
        time_signature_den = 4

        def measure_duration_quarters(self) -> float:
            return self.time_signature_num * (4 / self.time_signature_den)

    return DummyConfig()


def dummy_choose_instrument_for_role(rng, role):
    return DummyInstrument(), f"dummy_{role}"


def test_composition_generates_tracks(monkeypatch, config):
    monkeypatch.setattr(
        "listener_to_randomness.core.composition.create_role",
        lambda **kwargs: DummyRole()
    )

    rng = DummyRandom()
    composition = Composition(config, rng)

    midi = composition.generate()

    times, tempos = midi.get_tempo_changes()

    assert len(tempos) == 1
    assert times[0] == 0.0

    # 3 fixed roles + 2 optional forced by DummyRandom
    assert len(midi.instruments) == 5
    assert len(composition.tracks) == 5