import argparse

from listener_to_randomness.randomness import create_random
from listener_to_randomness.core.rng_demo import generate_rng_demo


def main():
    parser = argparse.ArgumentParser(
        description="Generate a simple MIDI demonstrating random generator sequences."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed",
    )

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
        "--notes",
        type=int,
        default=120,
        help="Number of notes to generate",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="rng_demo.mid",
        help="Output MIDI file",
    )

    args = parser.parse_args()

    rng = create_random(
        seed=args.seed,
        mode=args.generator,
    )

    midi = generate_rng_demo(
        rng=rng,
        note_count=args.notes,
        cycle_length=getattr(rng, "period", None),
    )

    midi.write(args.output)

    print("RNG demo MIDI generated 🎶")


if __name__ == "__main__":
    main()