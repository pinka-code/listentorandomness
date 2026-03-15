import pytest

from listener_to_randomness.core.phrase import Phrase
from tests.utils.dummies import (
    DummyNote,
    DummyDynamics,
    DummySoundDesign,
    DummyRole,
    DummyContext,
    DummyMelodicPattern,
)

@pytest.fixture
def phrase():
    context = DummyContext()
    role = DummyRole()
    dynamics = DummyDynamics()
    sound_design = DummySoundDesign()
    melodic_pattern = DummyMelodicPattern(degrees=[0, 1, 2])
    measure_count = 2
    config = {}

    return Phrase(
        config=config,
        context=context,
        melodic_pattern=melodic_pattern,
        measure_count=measure_count,
        role=role,
        dynamics=dynamics,
        sound_design=sound_design
    )


def test_phrase_returns_notes(phrase):
    notes = phrase.play(start_time=0.0)
    assert isinstance(notes, list)
    assert all(isinstance(n, DummyNote) for n in notes)
    assert len(notes) > 0


def test_notes_start_time_increment(phrase):
    notes = phrase.play(start_time=0.0)
    times = [note.start for note in notes]
    assert times == sorted(times)


def test_pitch_choices_from_role(phrase):
    notes = phrase.play(start_time=0.0)
    scale = phrase.context.scale_notes
    for note in notes:
        assert note.pitch in scale


def test_velocity_with_accents(phrase):
    notes = phrase.play(start_time=0.0)
    valid_velocities = {60, 64, 68, 72}  # 60 + accent_boost
    for note in notes:
        assert isinstance(note.velocity, int)
        assert note.velocity in valid_velocities


def test_phrase_variation_disabled():
    context = DummyContext()
    context.style.phrase_variation_prob = 0.0
    role = DummyRole()
    dynamics = DummyDynamics()
    sound_design = DummySoundDesign()
    melodic_pattern = DummyMelodicPattern(degrees=[0, 1, 2])
    phrase = Phrase(
        config={},
        context=context,
        melodic_pattern=melodic_pattern,
        measure_count=2,
        role=role,
        dynamics=dynamics,
        sound_design=sound_design
    )

    notes = phrase.play(start_time=0.0)
    degrees_played = [(note.pitch - 60) % 12 for note in notes]
    assert all(d in [0, 2, 4] for d in degrees_played)