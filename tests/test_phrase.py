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
    def choose_pitch(self, degree, note_index):
        return 60 + degree

    def adjust_velocity(self, velocity, note_index):
        return velocity

    def choose_final_note(self):
        degree = 0
        octave = 3
        duration_ratio = 0.5
        pitch = self.choose_pitch(degree, octave)
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
    return DummyConfig()


def test_phrase_adds_final_note(config):
    role = DummyRole()
    rnd = DummyRandom()

    phrase = Phrase(
        config=config,
        melodic_pattern=[0],
        rhythmic_pattern=[1],
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
        rhythmic_pattern=[1],
        measure_count=2,
        role=role,
        velocity=80,
        measure_class=DummyMeasure,
        rng=rnd,
    )

    notes = phrase.play(start_time=0)

    assert len(notes) == 3  # 2 measures + final note