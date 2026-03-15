import argparse
import json
from typing import Dict, Any
from listener_to_randomness.randomness import create_random
from listener_to_randomness.core import generate_structure, Composition
from listener_to_randomness.core.rng_demo import generate_rng_demo

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

def generate_demo_midi(rng, output_file, note_count):
    midi = generate_rng_demo(
        rng=rng,
        note_count=note_count,
        cycle_length=getattr(rng, "period", None),
    )
    midi.write(output_file)

def generate_composition_midi(rng, output_file):
    cfg = generate_structure(rng)

    print("===== COMPOSITION CONFIGURATION =====")
    print(f"Orchestration density: {cfg.orchestration_density}")
    print("=====================================")

    composition = Composition(cfg, rng)
    midi = composition.generate()
    midi.write(output_file)