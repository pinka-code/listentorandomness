import argparse
import json

from listener_to_randomness.core import generate_structure, Composition
from listener_to_randomness.utils import debug_notes
from listener_to_randomness.randomness import create_random

def main():
    parser = argparse.ArgumentParser(
        description="Generate a structured random MIDI composition."
    )

    parser.add_argument("--seed", type=int, default=42, help="Random seed")

    parser.add_argument(
        "--generator",
        type=str,
        default="default",
        choices=[
            "default",
            "biased",
            "secure",
            "gaussian",
            "markov",
            "rhythmic",
            "fractal",
            "tiny",
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
        "--output",
        type=str,
        default="generative_structured.mid",
        help="Output MIDI file",
    )

    args = parser.parse_args()

    transition_matrix = None
    if args.transition_matrix:
        transition_matrix = json.loads(args.transition_matrix)

    random_generator = create_random(
        seed=args.seed,
        mode=args.generator,
        bias_factor=args.bias_factor,
        transition_matrix=transition_matrix,
    )

    cfg = generate_structure(random_generator)

    print("===== COMPOSITION CONFIGURATION =====")
    print(f"Orchestration density: {cfg.orchestration_density}")
    print("=====================================")

    part = Composition(cfg, random_generator)
    midi = part.generate()

    # debug_notes(midi)

    midi.write(args.output)

    print("MIDI generated ! 🎶")


if __name__ == "__main__":
    main()