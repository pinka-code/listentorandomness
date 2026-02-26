import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Visualize a generated composition."
    )

    parser.add_argument(
        "--mode",
        type=str,
        default="piano_roll",
        choices=["piano_roll", "timeline", "stats"],
        help="Visualization mode",
    )

    args = parser.parse_args()

    # TODO: call visualization module once implemented
    print("⚠ Visualization not implemented yet.")
    print(f"Mode selected: {args.mode}")


if __name__ == "__main__":
    main()