import pytest
from listener_to_randomness.core.phrase import Phrase
from listener_to_randomness.midi.note import Note


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
    def choose_pitch(self, degree):
        return 60 + degree

    def adjust_velocity(self, velocity):
        return velocity
    
    def generate_rhythm(self, measure_duration):
        pattern = []
        remaining = measure_duration
        while remaining > 0:
            dur = 1.0 if remaining >= 1.0 else remaining
            pattern.append((dur, False))  # False = no silence
            remaining -= dur
        return pattern

    def choose_final_note(self):
        degree = 0
        duration_ratio = 0.5
        pitch = self.choose_pitch(degree)
        return pitch, duration_ratio


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
    return DummyConfig()


def test_phrase_adds_final_note(config):
    role = DummyRole()
    rnd = DummyRandom()

    phrase = Phrase(
        config=config,
        melodic_pattern=[0],
        measure_count=1,
        role=role,
        velocity=80,
        measure_class=DummyMeasure,
        rng=rnd,
    )

    notes = phrase.play(start_time=0)

    assert len(notes) == 2
    assert notes[-1].pitch == 60


def test_phrase_applies_variation(config):
    role = DummyRole()
    rnd = DummyRandom()
    rnd._random_value = 0.1  # less than 0.5 → apply variation

    phrase = Phrase(
        config=config,
        melodic_pattern=[0],
        measure_count=2,
        role=role,
        velocity=80,
        measure_class=DummyMeasure,
        rng=rnd,
    )

    notes = phrase.play(start_time=0)

    assert len(notes) == 3  # 2 measures + final note