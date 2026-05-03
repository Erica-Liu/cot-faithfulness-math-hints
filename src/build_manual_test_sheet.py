import argparse
import pandas as pd

from build_prompts import make_prompt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    problems = pd.read_csv(args.input).fillna("")
    rows = []

    for _, row in problems.iterrows():
        for condition in ["baseline", "correct_hint", "misleading_hint"]:
            rows.append(
                {
                    "id": row["id"],
                    "domain": row["domain"],
                    "condition": condition,
                    "prompt": make_prompt(
                        row["problem"],
                        condition,
                        str(row["correct_answer"]),
                        str(row["misleading_answer"]),
                    ),
                    "model_answer": "",
                    "model_explanation": "",
                }
            )

    pd.DataFrame(rows).to_csv(args.output, index=False)
    print(f"Wrote {len(rows)} manual test rows to {args.output}")


if __name__ == "__main__":
    main()
