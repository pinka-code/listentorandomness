from listener_to_randomness.core.rhythm import RhythmicPattern
from tests.utils.dummies import DummyRole
from tests.utils.builders import RhythmicPatternBuilder

def test_rhythmicpattern_total_duration_and_iter():
    pattern = [(1.0, False), (0.5, True), (0.25, False)]
    rp = RhythmicPattern(pattern)
    assert rp.total_duration() == 1.0 + 0.5 + 0.25
    assert len(rp) == 3
    assert list(rp) == pattern


def test_generate_creates_non_empty_pattern():
    ctx = RhythmicPatternBuilder().build_context()
    role = DummyRole()
    rp = RhythmicPattern.generate(ctx, role)
    assert isinstance(rp, RhythmicPattern)
    assert len(rp) > 0
    total = rp.total_duration()
    assert total <= ctx.measure_duration
    assert any(not rest for _, rest in rp)


def test_generate_with_high_rest_probability():
    ctx = RhythmicPatternBuilder().with_rest_probability(1.0).build_context()
    role = DummyRole()
    rp = RhythmicPattern.generate(ctx, role)
    # should still contain at least one note
    assert any(not rest for _, rest in rp)


def test_generate_respects_measure_duration():
    ctx = RhythmicPatternBuilder().with_measure_duration(3.0).build_context()
    rp = RhythmicPattern.generate(ctx)
    assert sum(d for d, _ in rp) <= 3.0


def test_generate_syncopation_applied():
    ctx = RhythmicPatternBuilder().with_syncopation(1.0).build_context()
    rp = RhythmicPattern.generate(ctx)
    # if syncopation applied, expect some short durations <= 0.5
    assert any(d <= 0.5 for d, _ in rp)


def test_generate_with_ternary_signature():
    ctx = RhythmicPatternBuilder().with_time_signature("ternary").build_context()
    rp = RhythmicPattern.generate(ctx)
    assert sum(d for d, _ in rp) <= ctx.measure_duration
    assert any(not rest for _, rest in rp)