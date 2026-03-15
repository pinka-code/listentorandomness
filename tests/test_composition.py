import pytest
from tests.utils.dummies import DummyRNG, DummySection, DummyStyle, DummyTrack, DummyConfig
from listener_to_randomness.core.composition import Composition

@pytest.fixture
def composition():
    config = DummyConfig(density_factor=0.7)
    rng = DummyRNG()
    comp = Composition(config=config, rng=rng)
    comp.style = DummyStyle()
    comp.form.sections = [DummySection("A", 2), DummySection("B", 3)]
    comp.Track = DummyTrack
    return comp


def test_composition_generate_returns_midi(composition):
    midi = composition.generate()
    assert len(composition.tracks) > 0
    for track in composition.tracks:
        assert hasattr(track.instrument, "midi")
        assert len(midi.instruments) > 0