from typing import Optional, Callable, Dict

from .interface import RandomInterface
from .base import TinyRandom, DeterministicRandom, TimeSeedRandom, SecureRandom, FractalRandom
from .strategies import (
    BiasedRandom,
    GaussianRandom,
    MarkovRandom,
    RhythmicRandom,
)

def create_random(
    seed: Optional[int] = None,
    mode: str = "default",
    **kwargs
) -> RandomInterface:

    if seed is not None:
        base = DeterministicRandom(seed)
    else:
        base = TimeSeedRandom()

    registry: Dict[str, Callable[[], RandomInterface]] = {
        "default": lambda: base,
        "secure": lambda: SecureRandom(),
        "biased": lambda: BiasedRandom(base, kwargs.get("bias_factor", 1.5)),
        "gaussian": lambda: GaussianRandom(
            base,
            kwargs.get("mean", 0.5),
            kwargs.get("std", 0.15),
        ),
        "markov": lambda: MarkovRandom(
            base,
            kwargs["transition_matrix"],
        ),
        "rhythmic": lambda: RhythmicRandom(
            base,
            kwargs.get("period", 4),
        ),
        "fractal": lambda: FractalRandom(
            kwargs.get("fractal_seed", 0.5),
            kwargs.get("r", 3.99),
        ),
        "tiny": lambda: TinyRandom(seed if seed is not None else 1),
}

    try:
        return registry[mode]()
    except KeyError:
        raise ValueError(f"Unknown random mode: {mode}")