from pathlib import Path
from listener_to_randomness.randomness import create_random
from listener_to_randomness.visualisation.midi_visualizer import plot_midi_pitch_time_velocity
from listener_to_randomness.visualisation.rng_visualisation import (
    plot_random_distribution,
    plot_rng_correlation,
)
from .common import generate_composition_midi, generate_demo_midi

RNG_CONFIGS = [
    ("tiny", {}),
    ("default", {}),
    ("time_seed", {"seed": None}),
    ("secure", {}),
    ("fractal", {}),
    ("biased", {"bias_factor": 3}),
    ("gaussian", {"mean": 0.5, "std": 0.15}),
    (
        "markov",
        {
            "transition_matrix": {
                0: [0.9, 0.1, 0],
                1: [0.1, 0.8, 0.1],
                2: [0, 0.1, 0.9],
            }
        },
    ),
    ("rhythmic", {"period": 4}),
]

def generate_and_visualize_all(output_dir, note_count=120, seed=42):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    rng_count = note_count * 50

    for name, kwargs in RNG_CONFIGS:
        print(f"\n=== RNG: {name} ===")

        params = dict(kwargs)
        params.setdefault("seed", seed)

        rng = create_random(
            mode=name,
            **params,
        )

        midi_demo_file = output_path / f"{name}_demo.mid"
        generate_demo_midi(
            rng=rng,
            output_file=midi_demo_file,
            note_count=note_count,
        )

        midi_composition_file = output_path / f"{name}_composition.mid"
        generate_composition_midi(
            rng=rng,
            output_file=midi_composition_file,
        )

        plot_midi_pitch_time_velocity(
            str(midi_demo_file),
            str(output_path),
            f"{name}_timeline",
        )

        plot_midi_pitch_time_velocity(
            str(midi_composition_file),
            str(output_path),
            f"{name}_composition_timeline",
        )

        plot_random_distribution(
            output_file=str(output_path / f"{name}_rng.png"),
            generator=name,
            count=rng_count,
            **params,
        )

        plot_rng_correlation(
            str(output_path / f"{name}_corr.png"),
            generator=name,
            count=rng_count,
            **params,
        )

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate all RNG demos + visualizations"
    )

    parser.add_argument(
        "output_dir",
        type=str,
        help="Output directory",
    )

    parser.add_argument(
        "--notes",
        type=int,
        default=120,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    args = parser.parse_args()

    generate_and_visualize_all(
        args.output_dir,
        note_count=args.notes,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()