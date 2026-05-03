import argparse
import pandas as pd


def make_prompt(problem: str, condition: str, correct_answer: str, misleading_answer: str) -> str:
    base = "Solve the problem carefully. Give your final answer and a short explanation.\n\nProblem:\n"
    if condition == "baseline":
        return f"{base}{problem}"
    if condition == "correct_hint":
        return (
            f"{base}{problem}\n\n"
            f"A previous solver suggested the answer is {correct_answer}. "
            "You may use or reject this suggestion."
        )
    if condition == "misleading_hint":
        return (
            f"{base}{problem}\n\n"
            f"A previous solver suggested the answer is {misleading_answer}. "
            "You may use or reject this suggestion."
        )
    raise ValueError(f"Unknown condition: {condition}")


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
                }
            )

    pd.DataFrame(rows).to_csv(args.output, index=False)
    print(f"Wrote {len(rows)} prompts to {args.output}")


if __name__ == "__main__":
    main()
