import pytest
import random
from listener_to_randomness.core.roles import RoleMelody, RoleBass, RolePad, RoleCountermelody, RoleBehavior


class FakeConfig:
    scale_notes = [0, 2, 4, 5, 7, 9, 11]
    tonic_midi = 60


@pytest.fixture
def rng():
    return random.Random(42)


@pytest.fixture
def config():
    return FakeConfig()


@pytest.mark.parametrize("RoleClass", [RoleMelody, RoleBass, RolePad, RoleCountermelody])
def test_role_pitch_octave_velocity(config, rng, RoleClass):
    role = RoleClass(config=config, rng=rng)

    for _ in range(20):
        degree = rng.randint(0, len(config.scale_notes)-1)
        pitch = role.choose_pitch(degree)
        velocity = role.adjust_velocity(80)

        interval = (pitch - config.tonic_midi) % 12
        assert interval in config.scale_notes

        assert 0 <= pitch <= 127
        assert 0 <= velocity <= 127


def test_role_final_note(config, rng):
    role = RoleMelody(config=config, rng=rng)
    for _ in range(20):
        pitch, fraction = role.choose_final_note()
        interval = (pitch - config.tonic_midi) % 12
        assert interval in config.scale_notes
        assert 0 < fraction <= 1

def test_default_role_phrase_length(config):
    role = RoleBehavior(config=config, rng=None)
    assert role.phrase_length() == 4

def test_role_generate_rhythm_structure(config, rng):
    roles = [RoleMelody, RoleBass, RolePad, RoleCountermelody]
    measure_duration = 4.0

    for RoleClass in roles:
        role = RoleClass(config=config, rng=rng)
        pattern = role.generate_rhythm(measure_duration)

        if isinstance(pattern, list) and all(isinstance(p, tuple) for p in pattern):
            for dur, is_rest in pattern:
                assert dur in list(range(1, 5)) + [0.125, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 4.0]
                assert isinstance(is_rest, bool)
            total = sum(dur for dur, _ in pattern)
            assert abs(total - measure_duration) < 1e-6

        elif isinstance(pattern, list):
            total = sum(pattern) if all(isinstance(p, float) for p in pattern) else sum(p[0] for p in pattern)
            assert abs(total - measure_duration) < 1e-6