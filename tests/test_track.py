import pytest
from listener_to_randomness.core.track import Track
from listener_to_randomness.midi.note import Note
from listener_to_randomness.core.rhythm import RhythmicPattern


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


def test_track_does_not_exceed_section_duration(config):
    instrument = DummyInstrument()
    rng = DummyRandom()
    role = DummyRole()

    track = Track(
        config=config,
        rng=rng,
        role=role,
        instrument=instrument,
        instrument_name="piano",
        measure_class=DummyMeasure,
    )

    class DummySection:
        name = "A"
        bars = 2
        tempo_name = "ANDANTE"
        tempo_bpm = 90

        def bar_duration(self, config):
            beat_duration = 60.0 / self.tempo_bpm
            beat_unit = 4 / config.time_signature_den
            return config.time_signature_num * beat_unit * beat_duration

    section = DummySection()
    start_bar = 0

    track.generate_section(section, start_bar)

    section_duration = section.bars * section.bar_duration(config)

    assert all(
        note.start + note.duration <= section_duration
        for note in instrument.notes
    )
