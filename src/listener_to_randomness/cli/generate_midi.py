from listener_to_randomness.cli.common import parse_common_args, create_rng_from_args
from .common import generate_composition_midi

def main():
    args = parse_common_args(description="Generate a structured random MIDI composition.")
    rng = create_rng_from_args(args)
    generate_composition_midi(rng, output_file=args.output)
    print(f"Structured MIDI generated 🎶 -> {args.output}")


if __name__ == "__main__":
    main()