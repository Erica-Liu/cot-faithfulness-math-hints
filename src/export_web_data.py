import argparse
import csv
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open(newline="", encoding="utf-8") as infile:
        rows = list(csv.DictReader(infile))

    with output_path.open("w", encoding="utf-8") as outfile:
        json.dump(rows, outfile, indent=2)
        outfile.write("\n")

    print(f"Wrote {len(rows)} problems to {output_path}")


if __name__ == "__main__":
    main()
