from listener_to_randomness.midi.instruments import InstrumentType
import pretty_midi

class DummyNote:
    def __init__(self, pitch, start, duration, velocity):
        self.pitch = pitch
        self.start = start
        self.duration = duration
        self.velocity = velocity

    def to_midi(self):
        return pretty_midi.Note(
            velocity=self.velocity,
            pitch=self.pitch,
            start=self.start,
            end=self.start + self.duration
        )

class DummyDynamics:
    def choose(self, pos):
        return 60

class DummyArticulation:
    def apply(self, pitch, start, duration, velocity):
        return [DummyNote(pitch, start, duration, velocity)]

class DummySoundDesign:
    def apply(self, pitch, start, duration, velocity):
        return [DummyNote(pitch, start, duration, velocity)]

class DummyRhythm:
    def __init__(self):
        self.pattern = [(1.0, False), (1.0, False), (1.0, False)]
    
    def total_duration(self):
        return sum(duration for duration, _ in self.pattern)

class DummyConfig:
    def __init__(self, density_factor=0.7):
        self.density_factor = density_factor

class DummyRole:
    """
    Minimal implementation of RoleBehavior for testing purposes.
    Methods return deterministic or simple values suitable for tests.
    """

    name = "dummy"
    rhythm_profile = {}
    melodic_profile = {}

    def choose_pitch(self, scale_notes, degree):
        # Simply return the scale note at the given degree (modulo length)
        return scale_notes[degree % len(scale_notes)]

    def adjust_velocity(self, v):
        # Identity mapping, no modification
        return v

    def choose_octave(self):
        # Always return octave 4 for simplicity
        return 4

    def generate_rhythm(self, context):
        return DummyRhythm()

    def phrase_length(self):
        # Fixed phrase length
        return 4

class DummyRNG:
    """Simple deterministic RNG for testing."""
    def __init__(self):
        self.counter = 0

    def random(self):
        val = (self.counter % 100) / 100.0
        self.counter += 1
        return val

    def randint(self, a, b):
        return a + (self.counter % (b - a + 1))

    def choice(self, seq):
        return seq[self.counter % len(seq)]

    def choice_weighted(self, seq, weights):
        return seq[self.counter % len(seq)]

    def uniform(self, a, b):
        return a + (b - a) * self.random()

    def shuffle(self, seq):
        return list(seq)

    def fork(self, seed_offset=0):
        return DummyRNG()

class DummySection:
    def __init__(self, name="A", bars=2):
        self.name = name
        self.bars = bars
        self.context = DummyContext()

class DummyForm:
    def __init__(self):
        self.style = DummyStyle()
        self.sections = [DummySection() for _ in range(2)]

class DummyRoleSpec:
    def __init__(self, instruments=None):
        self.instruments = instruments or ["piano"]

class DummyMidi:
    def __init__(self):
        self.notes = []

class DummyInstrumentType:
    def __init__(self, name="piano"):
        self.name = name

    def create_pretty_midi(self):
        return DummyMidi()

class DummyStyle:
    def __init__(self):
        self.name = "dummy_style"
        self.pattern_length_min = 1
        self.pattern_length_max = 4
        self.phrase_variation_prob = 0.0
        self.melodic_profile = {
            "intervals": [-2, -1, 0, 1, 2, 3, -3],
            "weights":   [1, 4, 3, 4, 2, 1, 1],
            "start_degree_weight": {0:6, 2:1, 4:2}
        }
        self.rhythmic_profile = {
            "duration_weights": {
                0.125: 1.0,
                0.25: 1.0,
                0.5: 1.0,
                0.75: 1.0,
                1.0: 1.0,
                1.5: 1.0,
                2.0: 1.0,
                4.0: 1.0
            },
            "rest_probability": 0.0
        }
        self.roles = {"dummy_role": DummyRoleSpec(instruments=[InstrumentType.ACOUSTIC_GRAND_PIANO])}
        self.core_roles = list(self.roles.keys())
        self.optional_roles = {}
        self.forms = [ [("A",2), ("B",3)] ]
        self.tempo_choices = [120]

    def choose_roles(self, rng, density=1.0):
        return list(self.core_roles)

    def choose_tempo(self, rng):
        return 120

    def choose_time_signature(self, rng):
        return DummyTimeSignature()

class DummyTimeSignature:
    def __init__(self):
        self.name = "4/4"
        self.numerator = 4
        self.denominator = 4
        self.type = "binary"

    def measure_duration_quarters(self):
        return 4.0
    
class DummyKeySignature:
    def __init__(self, tonic="C", mode="major"):
        self._tonic = tonic
        self._mode = mode

    def tonic(self):
        return self._tonic

    def mode(self):
        return self._mode

    def generate_scale(self):
        return [60, 62, 64, 65, 67, 69, 71]

    def choose_neighbour_key(self, rng, same_prob=0.7):
        return self

class DummyContext:
    def __init__(self):
        self.rng = DummyRNG()

        self.scale_notes = [60, 62, 64, 65, 67, 69, 71]

        self.measure_duration_value = 4.0
        self.bar_duration_value = 4.0
        self.tempo_bpm = 120

        self.style = DummyStyle()

        self.time_signature = DummyTimeSignature()
        self.key_signature = DummyKeySignature()

    @property
    def measure_duration(self):
        return self.measure_duration_value

    @property
    def bar_duration(self):
        return self.bar_duration_value


class DummyMelodicPattern:
    def __init__(self, degrees):
        self.degrees = degrees

    def transform(self, rng):
        return self

class DummyRhythmicPattern:
    def __init__(self, pattern):
        self.pattern = pattern

class DummyInstrument:
    def __init__(self, name):
        self.name = name
        self.midi = DummyMidi()
        self.sound = DummySoundDesign()

class DummyTrack:
    def __init__(self, config, role, instrument):
        self.config = config
        self.role = role
        self.instrument = instrument
    def generate_section(self, section, start_bar, last_note_end):
        return last_note_end + section.bars
