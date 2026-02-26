import argparse

from listener_to_randomness.randomness import DefaultRandom, BiasedRandom
from listener_to_randomness.core import generate_structure, Composition
from listener_to_randomness.utils import debug_notes


def main():
    parser = argparse.ArgumentParser(
        description="Generate a structured random MIDI composition."
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
        choices=["default", "biased"],
        help="Random generator type",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="generative_structured.mid",
        help="Output MIDI file",
    )

    args = parser.parse_args()

    # Generator choice
    if args.generator == "biased":
        random_generator = BiasedRandom(seed=args.seed)
    else:
        random_generator = DefaultRandom(seed=args.seed)

    cfg = generate_structure(random_generator)

    print("===== COMPOSITION CONFIGURATION =====")
    print(f"Key signature: {cfg.key_name}")
    print(f"Tempo: {cfg.tempo_name} → {cfg.tempo_bpm} BPM")
    print(f"Time signature: {cfg.time_signature_name}")
    print(f"Number of tracks: {cfg.num_tracks}")
    print(f"Target total duration: {cfg.total_duration} sec")
    print("=====================================")

    part = Composition(cfg, random_generator)
    midi = part.generate()

    debug_notes(midi)

    midi.write(args.output)

    print("MIDI generated ! 🎶")


if __name__ == "__main__":
    main()