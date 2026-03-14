from pathlib import Path
from listener_to_randomness.randomness import create_random
from listener_to_randomness.core.rng_demo import generate_rng_demo
from listener_to_randomness.visualisation.midi_visualizer import plot_midi_pitch_time_velocity


def generate_and_visualize_all(output_dir: str, note_count: int = 120, seed: int = 42):
    """
    Generate MIDI files for each RNG type and visualize them in timeline mode.
    """
    rng_configs = [
        {"name": "default", "kwargs": {}},
        {"name": "time_seed", "kwargs": {}},
        {"name": "secure", "kwargs": {}},
        {"name": "fractal", "kwargs": {}},
        {"name": "biased", "kwargs": {"bias_factor": 3}},
        {"name": "gaussian", "kwargs": {"mean": 0.5, "std": 0.15}},
        {"name": "markov", "kwargs": {
            "transition_matrix": {
                0: [0.9,0.1,0],
                1: [0.1,0.8,0.1],
                2: [0,0.1,0.9],
            }
        }},
        {"name": "rhythmic", "kwargs": {"period": 4}},
    ]

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for cfg in rng_configs:
        rng_name = cfg["name"]
        rng_kwargs = cfg["kwargs"]

        rng = create_random(seed=seed, mode=rng_name, **rng_kwargs)
        midi_file = output_path / f"{rng_name}.mid"
        midi = generate_rng_demo(rng=rng, note_count=note_count, cycle_length=getattr(rng, "period", None))
        midi.write(str(midi_file))
        print(f"[{rng_name}] MIDI saved: {midi_file}")

        plot_midi_pitch_time_velocity(str(midi_file), str(output_path), rng_name)
        print(f"[{rng_name}] Timeline visualization done\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate and visualize MIDI for all RNG types.")
    parser.add_argument("output_dir", type=str, help="Directory to save MIDI and plots")
    parser.add_argument("--notes", type=int, default=120, help="Number of notes per MIDI")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")

    args = parser.parse_args()

    generate_and_visualize_all(
        output_dir=args.output_dir,
        note_count=args.notes,
        seed=args.seed
    )


if __name__ == "__main__":
    main()