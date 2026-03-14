from listener_to_randomness.cli.common import parse_common_args, create_rng_from_args
from listener_to_randomness.core import generate_structure, Composition

def main():
    args = parse_common_args(description="Generate a structured random MIDI composition.")
    rng = create_rng_from_args(args)

    cfg = generate_structure(rng)

    print("===== COMPOSITION CONFIGURATION =====")
    print(f"Orchestration density: {cfg.orchestration_density}")
    print("=====================================")

    part = Composition(cfg, rng)
    midi = part.generate()

    midi.write(args.output)
    print(f"Structured MIDI generated 🎶 -> {args.output}")


if __name__ == "__main__":
    main()