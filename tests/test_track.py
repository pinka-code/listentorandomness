import pytest

from listener_to_randomness.core.track import Track
from tests.utils.dummies import (
    DummySection,
    DummyInstrument,
    DummyRole,
)

@pytest.fixture
def track():
    role = DummyRole()
    instrument = DummyInstrument("piano")
    config = {}
    return Track(config=config, role=role, instrument=instrument)


def test_generate_section_returns_last_note_end(track):
    section = DummySection(name="A", bars=2)
    start_bar = 0
    last_note_end = track.generate_section(section, start_bar)

    assert isinstance(last_note_end, float)
    assert last_note_end >= 0

def test_generate_section_creates_notes(track):
    section = DummySection(name="B", bars=2)
    start_bar = 0
    track.generate_section(section, start_bar)

    assert len(track.instrument.midi.notes) > 0
    for note in track.instrument.midi.notes:
        assert isinstance(note.start, (int, float))
        assert isinstance(note.duration, (int, float))
        assert isinstance(note.velocity, int)