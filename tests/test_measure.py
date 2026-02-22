import pytest
from measure import Measure


class DummyRole:
    def choose_pitch(self, degree, note_index):
        return 60 + degree

    def adjust_velocity(self, velocity, note_index):
        return velocity + 5


@pytest.fixture
def config():
    class DummyConfig:
        signature_num = 4
        signature_den = 4
    return DummyConfig()


def test_measure_generates_notes_from_pattern(config):
    pattern = [0, 2, 4]
    rhythm = [1, 1, 1]

    role = DummyRole()
    measure = Measure(config, pattern, rhythm, role)

    notes = measure.play(start_time=0, dynamic=80)

    assert len(notes) == 3
    assert notes[0].pitch == 60
    assert notes[1].pitch == 62
    assert notes[2].pitch == 64


def test_measure_applies_role_velocity(config):
    pattern = [0]
    rhythm = [1]

    role = DummyRole()
    measure = Measure(config, pattern, rhythm, role)

    notes = measure.play(start_time=0, dynamic=70)

    assert notes[0].velocity == 75


def test_measure_respects_timing(config):
    pattern = [0, 1]
    rhythm = [1, 2]

    role = DummyRole()
    measure = Measure(config, pattern, rhythm, role)

    notes = measure.play(start_time=10, dynamic=80)

    assert notes[0].start == 10
    assert notes[1].start == 11