import argparse
from listener_to_randomness.visualisation.midi_visualizer import plot_midi_pitch_time_velocity


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
        "--mode",
        type=str,
        default="timeline",
        choices=["timeline", "piano_roll", "stats"],
        help="Visualization mode"
    )

    args = parser.parse_args()

    if args.mode == "timeline":
        plot_midi_pitch_time_velocity(args.midi_file)

    elif args.mode == "piano_roll":
        print("⚠ Piano roll mode not implemented yet.")

    elif args.mode == "stats":
        print("⚠ Stats mode not implemented yet.")


if __name__ == "__main__":
    main()