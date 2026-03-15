from listener_to_randomness.core.dynamics import Dynamics, DYNAMICS
from listener_to_randomness.randomness.base import DeterministicRandom

def make_rng():
    return DeterministicRandom(seed=42)


# ------------------------------------------------------------
# Initialization
# ------------------------------------------------------------

def test_init_with_explicit_velocities():
    rng = make_rng()

    dyn = Dynamics(
        rng,
        start_velocity=40,
        end_velocity=80
    )

    assert dyn.start_velocity == 40
    assert dyn.end_velocity == 80


def test_init_random_start_velocity():
    rng = make_rng()

    dyn = Dynamics(rng)

    assert dyn.start_velocity in DYNAMICS.values()


def test_end_velocity_no_change_when_prob_zero():
    rng = make_rng()

    dyn = Dynamics(
        rng,
        start_velocity=60,
        change_prob=0
    )

    assert dyn.end_velocity == dyn.start_velocity


# ------------------------------------------------------------
# choose()
# ------------------------------------------------------------

def test_choose_linear_curve():
    rng = make_rng()

    dyn = Dynamics(
        rng,
        start_velocity=40,
        end_velocity=80,
        curve="linear",
        noise_range=0
    )

    v_start = dyn.choose(position=0.0)
    v_mid = dyn.choose(position=0.5)
    v_end = dyn.choose(position=1.0)

    assert v_start == 40
    assert v_mid == 60
    assert v_end == 80


def test_choose_random_curve_range():
    rng = make_rng()

    dyn = Dynamics(
        rng,
        start_velocity=40,
        end_velocity=60,
        curve="random",
        noise_range=0
    )

    for _ in range(50):
        v = dyn.choose(position=0.5)
        assert 40 <= v <= 60


def test_choose_constant_curve():
    rng = make_rng()

    dyn = Dynamics(
        rng,
        start_velocity=50,
        end_velocity=100,
        curve="constant",
        noise_range=0
    )

    for _ in range(10):
        assert dyn.choose(position=0.5) == 50


# ------------------------------------------------------------
# Noise
# ------------------------------------------------------------

def test_noise_affects_velocity():
    rng = make_rng()

    dyn = Dynamics(
        rng,
        start_velocity=60,
        end_velocity=60,
        noise_range=5
    )

    values = [dyn.choose(position=0.5) for _ in range(30)]

    assert min(values) >= 55
    assert max(values) <= 65
    assert len(set(values)) > 1


def test_velocity_clamped_midi_range():
    rng = make_rng()

    dyn = Dynamics(
        rng,
        start_velocity=1,
        end_velocity=1,
        noise_range=20
    )

    for _ in range(50):
        v = dyn.choose(position=0.5)
        assert 0 <= v <= 127


# ------------------------------------------------------------
# Accent boost
# ------------------------------------------------------------

def test_accent_downbeat():
    assert Dynamics.accent_boost(0.0) == 12


def test_accent_half_bar():
    assert Dynamics.accent_boost(0.5) == 8


def test_accent_quarter_positions():
    assert Dynamics.accent_boost(0.25) == 4
    assert Dynamics.accent_boost(0.75) == 4


def test_accent_no_accent():
    assert Dynamics.accent_boost(0.33) == 0


# ------------------------------------------------------------
# Deterministic behavior
# ------------------------------------------------------------

def test_dynamics_repeatable_with_deterministic_rng():
    rng1 = DeterministicRandom(seed=123)
    rng2 = DeterministicRandom(seed=123)

    dyn1 = Dynamics(rng1, start_velocity=40, end_velocity=80)
    dyn2 = Dynamics(rng2, start_velocity=40, end_velocity=80)

    seq1 = [dyn1.choose(0.5) for _ in range(20)]
    seq2 = [dyn2.choose(0.5) for _ in range(20)]

    assert seq1 == seq2