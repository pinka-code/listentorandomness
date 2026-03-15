import pytest
from listener_to_randomness.core.roles import (
    Role,
    RoleBehavior,
    RoleMelody,
    RoleHarmony,
    RoleBass,
    RolePad,
    RoleCountermelody,
    create_role
)
from listener_to_randomness.randomness.base import DeterministicRandom
from tests.utils.dummies import DummyContext


@pytest.fixture
def rng():
    return DeterministicRandom(seed=42)


@pytest.fixture
def context(rng):
    class Ctx(DummyContext):
        measure_duration = 4.0
        rng = rng
    return Ctx()


@pytest.mark.parametrize(
    "RoleClass, expected_octaves, velocity_adjust",
    [
        (RoleMelody, [4, 5], 10),
        (RoleHarmony, [3, 4], 0),
        (RoleBass, [1, 2], 5),
        (RolePad, [3, 4], -10),
        (RoleCountermelody, [3, 4], 5),
    ]
)
def test_role_pitch_velocity_octave(RoleClass, expected_octaves, velocity_adjust, rng):
    role = RoleClass(config=None, rng=rng)
    scale = [60, 62, 64, 65, 67]  # C major scale degrees
    degree = 2

    pitch = role.choose_pitch(scale, degree)
    assert pitch in [n + 12*o for o in expected_octaves for n in scale]
    
    base_velocity = 50
    v = role.adjust_velocity(base_velocity)
    if velocity_adjust >= 0:
        assert v == min(127, base_velocity + velocity_adjust)
    else:
        assert v == max(20, base_velocity + velocity_adjust)

    oct_val = role.choose_octave()
    assert oct_val in expected_octaves


@pytest.mark.parametrize(
    "RoleClass, expected_len",
    [
        (RoleBehavior, 4),
        (RoleMelody, 4),
        (RoleHarmony, 2),
        (RoleBass, 8),
        (RolePad, 8),
        (RoleCountermelody, 4),
    ]
)
def test_role_phrase_length(RoleClass, expected_len, rng):
    role = RoleClass(config=None, rng=rng)
    assert role.phrase_length() == expected_len


@pytest.mark.parametrize(
    "RoleClass",
    [RoleBehavior, RoleMelody, RoleHarmony, RoleBass, RolePad, RoleCountermelody]
)
def test_role_generate_rhythm_type(RoleClass, context):
    role = RoleClass(config=None, rng=context.rng)
    rhythm = role.generate_rhythm(context)
    # Should return a list-like object or RhythmicPattern
    # For simplicity, check that the returned object has __iter__ and non-zero length
    assert hasattr(rhythm, "__iter__")
    assert len(rhythm) > 0


@pytest.mark.parametrize(
    "role_name, expected_class",
    [
        (Role.MELODY, RoleMelody),
        (Role.HARMONY, RoleHarmony),
        (Role.BASS, RoleBass),
        (Role.PAD, RolePad),
        (Role.COUNTERMELODY, RoleCountermelody),
        ("unknown_role", RoleBehavior)
    ]
)
def test_create_role_returns_correct_instance(role_name, expected_class, rng):
    role = create_role(role_name, config=None, rng=rng)
    assert isinstance(role, expected_class)