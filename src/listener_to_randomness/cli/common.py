import argparse
import json
from typing import Dict, Any
from listener_to_randomness.randomness import create_random

def parse_common_args(description: str) -> argparse.Namespace:
    """
    Parse common arguments for RNG/MIDI CLI tools.
    """
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("--seed", type=int, default=42, help="Random seed")

    parser.add_argument(
        "--generator",
        type=str,
        default="default",
        choices=[
            "default", "time_seed", "biased", "secure", "gaussian",
            "markov", "rhythmic", "fractal", "tiny",
        ],
        help="Random generator type",
    )

    parser.add_argument(
        "--bias-factor",
        type=float,
        default=1.5,
        help="Bias factor (used by biased RNG)",
    )

    parser.add_argument(
        "--transition-matrix",
        type=str,
        help="Transition matrix for Markov RNG (JSON)",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="output.mid",
        help="Output MIDI file",
    )

    parser.add_argument(
        "--notes",
        type=int,
        default=120,
        help="Number of notes to generate (used by simple RNG demo)"
    )

    return parser.parse_args()


def create_rng_from_args(args: argparse.Namespace) -> Any:
    """
    Create a RNG based on parsed CLI arguments.
    """
    transition_matrix = None
    if getattr(args, "transition_matrix", None):
        transition_matrix = json.loads(args.transition_matrix)

    rng_kwargs: Dict[str, Any] = {
        "bias_factor": getattr(args, "bias_factor", 1.5),
        "transition_matrix": transition_matrix,
    }

    return create_random(
        seed=getattr(args, "seed", None),
        mode=getattr(args, "generator", "default"),
        **rng_kwargs
    )