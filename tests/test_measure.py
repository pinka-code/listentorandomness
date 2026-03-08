import pytest
from listener_to_randomness.core.measure import Measure
from listener_to_randomness.core.rhythm import RhythmicPattern
from listener_to_randomness.core.melodic_pattern import MelodicPattern

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
        signature_num = 4
        signature_den = 4
    return DummyConfig()


def test_measure_generates_notes_from_pattern(config):
    pattern = MelodicPattern([0, 2, 4])
    rhythm = RhythmicPattern([(1, False), (1, False), (1, False)])

    role = DummyRole()
    measure = Measure(config, pattern, rhythm, role)

    notes = measure.play(start_time=0, dynamic=80)

    assert len(notes) == 3
    assert notes[0].pitch == 60
    assert notes[1].pitch == 62
    assert notes[2].pitch == 64


def test_measure_applies_role_velocity(config):
    pattern = MelodicPattern([0])
    rhythm = RhythmicPattern([(1, False)])

    role = DummyRole()
    measure = Measure(config, pattern, rhythm, role)

    notes = measure.play(start_time=0, dynamic=70)

    assert notes[0].velocity == 75


def test_measure_respects_timing(config):
    pattern = MelodicPattern([0, 1])
    rhythm = RhythmicPattern([(1, False), (2, False)])

    role = DummyRole()
    measure = Measure(config, pattern, rhythm, role)

    notes = measure.play(start_time=10, dynamic=80)

    assert notes[0].start == 10
    assert notes[1].start == 11