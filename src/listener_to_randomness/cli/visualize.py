import argparse
from listener_to_randomness.visualisation.midi_visualizer import plot_midi_pitch_time_velocity, analyze_midi_tracks


def main():
    parser = argparse.ArgumentParser(
        description="Visualize a generated MIDI composition."
    )

    parser.add_argument(
        "midi_file",
        type=str,
        help="Path to the MIDI file (.mid)"
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

    if args.mode == "timeline":
        plot_midi_pitch_time_velocity(args.midi_file, args.output_dir)

    elif args.mode == "analysis":
        analyze_midi_tracks(args.midi_file, args.output_dir)

    elif args.mode == "todo":
        print("not implemented yet.")


if __name__ == "__main__":
    main()