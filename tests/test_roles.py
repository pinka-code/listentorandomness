import pytest  # type: ignore
import random

from roles import RoleMelody, RoleBass, RolePad, RoleCountermelody


class FakeConfig:
    # scale notes modulo 12
    scale_notes = [0, 2, 4, 5, 7, 9, 11]
    tempo_bpm = 120
    time_signature_num = 4
    time_signature_den = 4
    total_duration = 16.0
    phrase_length_min = 1
    phrase_length_max = 2
    phrase_variation_prob = 0.5
    tonic_resolution_prob = 0.5
    tonic_midi = 60


@pytest.fixture
def rng():
    return random.Random(42)


@pytest.fixture
def config():
    return FakeConfig()


@pytest.mark.parametrize("RoleClass", [RoleMelody, RoleBass, RolePad, RoleCountermelody])
def test_role_generate_pitch_octave_and_velocity(config, rng, RoleClass):
    role = RoleClass(config=config, rng=rng)

    for _ in range(20):
        degree = rng.randint(0, len(config.scale_notes) - 1)
        octave = role.choose_octave()
        pitch = role.choose_pitch(degree, octave)
        velocity = role.adjust_velocity(80)

        # pitch must be within scale modulo 12
        interval = (pitch - config.tonic_midi) % 12
        assert interval in config.scale_notes, f"Interval {interval} not in scale {config.scale_notes}"

        # valid MIDI pitch
        assert 0 <= pitch <= 127

        # valid velocity
        assert 0 <= velocity <= 127


def test_role_final_note(config, rng):
    role = RoleMelody(config=config, rng=rng)

    for _ in range(20):
        pitch, fraction = role.choose_final_note()

        interval = (pitch - config.tonic_midi) % 12
        assert interval in config.scale_notes

        # fraction must be positive and <=1
        assert 0 < fraction <= 1


def test_role_octave_variation(config, rng):
    role = RoleBass(config=config, rng=rng)
    octaves = set(role.choose_octave() for _ in range(50))
    # expect multiple octaves for this role
    assert octaves <= {1, 2}


def test_role_velocity_adjustment(config, rng):
    role = RolePad(config=config, rng=rng)

    # base velocity 80 → must decrease by 10 for pad
    v = role.adjust_velocity(80)
    assert v == 70


def test_role_pitch_deterministic(config):
    # with fixed rng, pitch must be deterministic
    rng1 = random.Random(123)
    rng2 = random.Random(123)
    role1 = RoleMelody(config=config, rng=rng1)
    role2 = RoleMelody(config=config, rng=rng2)

    degree = 2
    octave = role1.choose_octave()
    pitch1 = role1.choose_pitch(degree, octave)
    pitch2 = role2.choose_pitch(degree, octave)

    assert pitch1 == pitch2