import argparse
from pathlib import Path

from listener_to_randomness.visualisation.midi_visualizer import (
    plot_midi_pitch_time_velocity,
    plot_global_complexity_map,
    analyze_midi_tracks,
    plot_phrase_clustering
)

def main():
    parser = argparse.ArgumentParser(
        description="Visualize a generated MIDI composition or RNG distributions."
    )

    parser.add_argument(
        "--midi_file",
        type=str,
        default=None,
        help="Path to the MIDI file (.mid). Not needed for RNG mode."
    )

    parser.add_argument(
        "output_dir",
        type=str,
        help="Path to the output directory"
    )

    parser.add_argument(
        "--mode",
        type=str,
        default="timeline",
        choices=["timeline", "analysis", "todo"],
        help="Visualization mode"
    )

    args = parser.parse_args()

    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if args.mode == "timeline":
        if not args.midi_file:
            raise ValueError("timeline mode requires --midi_file")
        plot_midi_pitch_time_velocity(args.midi_file, str(output_path))

    elif args.mode == "analysis":
        if not args.midi_file:
            raise ValueError("analysis mode requires --midi_file")
        analyze_midi_tracks(args.midi_file, str(output_path))
        plot_global_complexity_map(args.midi_file, str(output_path))
        plot_phrase_clustering(
            args.midi_file,
            str(output_path / "phrase_clustering.png"),
            n_clusters=4,
            pause_threshold=0.5
        )

    elif args.mode == "todo":
        print("Not implemented yet.")


if __name__ == "__main__":
    main()