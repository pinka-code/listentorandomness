import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Generate a musical score from a random composition."
    )

    parser.add_argument(
        "--output",
        type=str,
        default="score.pdf",
        help="Output score file name",
    )

    parser.add_argument(
        "--format",
        type=str,
        default="standard",
        choices=["standard", "neumatique"],
        help="Notation format",
    )

    args = parser.parse_args()

    # TODO: call notation module once implemented
    print("⚠ Score generation not implemented yet.")
    print(f"Requested format: {args.format}")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()