import pytest
from listener_to_randomness.core.phrase import Phrase
from listener_to_randomness.midi.note import Note
from listener_to_randomness.core.rhythm import RhythmicPattern
from listener_to_randomness.core.melodic_pattern import MelodicPattern

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
    def choose_pitch(self, degree, note_index):
        return 60

    def adjust_velocity(self, velocity, note_index):
        return velocity
    
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


class DummyMeasure:
    def __init__(self, config, melodic_pattern, rhythmic_pattern, role):
        self.rhythm = rhythmic_pattern

    def play(self, start_time, dynamic):
        return [
            Note(
                pitch=60,
                start=start_time,
                duration=1.0,
                velocity=dynamic,
            )
        ]


@pytest.fixture
def config():
    class DummyConfig:
        phrase_variation_prob = 0.5
        time_signature_num = 4
        time_signature_den = 4

        def measure_duration_quarters(self) -> float:
            return self.time_signature_num * (4 / self.time_signature_den)
    return DummyConfig()


def test_phrase_applies_variation(config):
    role = DummyRole()
    rnd = DummyRandom()
    rnd._random_value = 0.1  # less than 0.5 → apply variation

    phrase = Phrase(
        config=config,
        melodic_pattern=MelodicPattern([0]),
        measure_count=2,
        role=role,
        dynamics=80,
        measure_class=DummyMeasure,
        rng=rnd,
    )

    notes = phrase.play(start_time=0)

    for note in notes:
        assert note.start >= 0
        assert note.start + note.duration <= config.measure_duration_quarters() * phrase.measure_count + 1.0  # marge pour la note finale