from tests.utils.dummies import (
    DummyNote,
    DummyDynamics,
    DummyArticulation,
    DummySoundDesign,
    DummyRole,
    DummyContext,
    DummyMelodicPattern,
    DummyRhythmicPattern,
)
from listener_to_randomness.core.measure import Measure
from listener_to_randomness.core.rhythm import DURATIONS
from listener_to_randomness.randomness.base import DeterministicRandom

class RhythmicPatternBuilder:
    def __init__(self):
        self.measure_duration = 4.0
        self.time_signature = "binary"
        self.duration_weights = {d: 1.0 for d in DURATIONS.values()}
        self.rest_probability = 0.0
        self.syncopation_prob = 0.0
        self.role = None
        self.rng = DeterministicRandom(seed=42)

    def with_measure_duration(self, duration):
        self.measure_duration = duration
        return self

    def with_time_signature(self, ts_type):
        self.time_signature = ts_type
        return self

    def with_rest_probability(self, p):
        self.rest_probability = p
        return self

    def with_syncopation(self, p):
        self.syncopation_prob = p
        return self

    def with_role(self, role):
        self.role = role
        return self

    def build_context(self):
        class Ctx(DummyContext):
            measure_duration = self.measure_duration
            rng = self.rng
            time_signature = type("TS", (), {"type": self.time_signature})
            style = type(
                "Style",
                (),
                {"rhythmic_profile": {
                    "duration_weights": self.duration_weights,
                    "rest_probability": self.rest_probability,
                    "syncopation_prob": self.syncopation_prob,
                }}
            )
        return Ctx()


class MeasureBuilder:

    def __init__(self):

        self.context = DummyContext()
        self.degrees = [0, 1, 2]
        self.pattern = [(1.0, False)]
        self.role = DummyRole()

        self.dynamic = DummyDynamics()
        self.articulation = DummyArticulation()
        self.sound_design = DummySoundDesign()

        self.start_time = 0
        self.config = None

    def with_pattern(self, pattern):
        self.pattern = pattern
        return self

    def with_degrees(self, degrees):
        self.degrees = degrees
        return self

    def with_role(self, role):
        self.role = role
        return self

    def with_dynamic(self, dynamic):
        self.dynamic = dynamic
        return self

    def with_articulation(self, articulation):
        self.articulation = articulation
        return self

    def with_sound_design(self, sound_design):
        self.sound_design = sound_design
        return self

    def with_start_time(self, start):
        self.start_time = start
        return self

    def build(self):

        melodic_pattern = DummyMelodicPattern(self.degrees)
        rhythmic_pattern = DummyRhythmicPattern(self.pattern)

        return Measure(
            config=self.config,
            context=self.context,
            melodic_pattern=melodic_pattern,
            rhythmic_pattern=rhythmic_pattern,
            role=self.role
        )

    def play(self):

        measure = self.build()

        return measure.play(
            start_time=self.start_time,
            dynamic=self.dynamic,
            articulation=self.articulation,
            sound_design=self.sound_design
        )
