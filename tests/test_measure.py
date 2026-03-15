import pytest
from tests.utils.dummies import DummyNote, DummyRole
from tests.utils.builders import MeasureBuilder

def test_measure_generates_notes():

    notes = (
        MeasureBuilder()
        .with_pattern([(1.0, False), (1.0, False), (1.0, False)])
        .play()
    )

    assert len(notes) == 3


def test_measure_skips_rests():

    notes = (
        MeasureBuilder()
        .with_pattern([
            (1.0, False),
            (1.0, True),
            (1.0, False),
        ])
        .play()
    )

    assert len(notes) == 2


def test_measure_time_progression():

    notes = (
        MeasureBuilder()
        .with_pattern([
            (1.0, False),
            (2.0, False),
        ])
        .with_start_time(10)
        .play()
    )

    assert notes[0].start == 10
    assert notes[1].start == 11


def test_melodic_pattern_loops():

    notes = (
        MeasureBuilder()
        .with_degrees([0, 1])
        .with_pattern([
            (1, False),
            (1, False),
            (1, False),
            (1, False),
        ])
        .play()
    )

    pitches = [n.pitch for n in notes]

    assert pitches == [60, 62, 60, 62]


def test_velocity_pipeline():

    class VelocityDynamics:
        def choose(self, pos):
            return 50

    class VelocityRole(DummyRole):
        def adjust_velocity(self, v):
            return v + 5

    notes = (
        MeasureBuilder()
        .with_dynamic(VelocityDynamics())
        .with_role(VelocityRole())
        .play()
    )

    assert notes[0].velocity >= 55


def test_articulation_splits_note():

    class SplitArticulation:
        def apply(self, pitch, start, duration, velocity):
            return [
                DummyNote(pitch, start, duration / 2, velocity),
                DummyNote(pitch, start + duration / 2, duration / 2, velocity),
            ]

    notes = (
        MeasureBuilder()
        .with_articulation(SplitArticulation())
        .with_pattern([(2.0, False)])
        .play()
    )

    assert len(notes) == 2


def test_sound_design_layers_notes():

    class LayerSoundDesign:
        def apply(self, pitch, start, duration, velocity):
            return [
                DummyNote(pitch, start, duration, velocity),
                DummyNote(pitch + 12, start, duration, velocity),
            ]

    notes = (
        MeasureBuilder()
        .with_sound_design(LayerSoundDesign())
        .play()
    )

    assert len(notes) == 2
    assert notes[1].pitch == notes[0].pitch + 12


def test_measure_handles_empty_pattern():

    notes = (
        MeasureBuilder()
        .with_pattern([])
        .play()
    )

    assert notes == []


def test_measure_respects_bar_duration_for_position():

    class PosDynamics:
        def __init__(self):
            self.positions = []

        def choose(self, pos):
            self.positions.append(pos)
            return 60

    dyn = PosDynamics()

    MeasureBuilder() \
        .with_dynamic(dyn) \
        .with_pattern([(1, False), (1, False)]) \
        .play()

    assert dyn.positions[0] == pytest.approx(0.0)
    assert dyn.positions[1] == pytest.approx(0.25)