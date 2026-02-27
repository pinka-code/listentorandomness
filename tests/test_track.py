import pytest
from listener_to_randomness.core.track import Track
from listener_to_randomness.midi.note import Note


class DummyInstrument:
    def __init__(self):
        self.notes = []


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
            pattern.append((dur, False))  # False = no silence
            remaining -= dur
        return pattern
    
    def phrase_length(self):
        return 4

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


class DummyRandom:
    def choice(self, seq):
        return seq[0]

    def randint(self, a, b):
        return a

    def random(self):
        return 1.0
    
    def choice_weighted(self, seq, weights):
        return seq[0]


@pytest.fixture
def config():
    class DummyConfig:
        total_duration = 4.0
        pattern_length_min = 1
        pattern_length_max = 1
        scale_notes = [0, 2, 4, 5, 7]
        phrase_variation_prob = 0.0
        time_signature_num = 4
        time_signature_den = 4
    return DummyConfig()


def test_track_does_not_exceed_total_duration(config):
    instrument = DummyInstrument()
    track = Track(
        config=config,
        rng=DummyRandom(),
        role=DummyRole(),
        instrument=instrument,
        instrument_name="piano",
        measure_class=DummyMeasure,
    )

    track.generate()

    assert all(note.end <= config.total_duration for note in instrument.notes)