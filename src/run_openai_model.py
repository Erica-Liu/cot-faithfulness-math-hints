import argparse
import csv
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import List, Tuple

import pandas as pd

from build_prompts import make_prompt


FORMAT_INSTRUCTION = """

Return your response in exactly this format:
FINAL ANSWER: <your answer>
EXPLANATION: <a short explanation>
""".strip()


def extract_fields(text: str) -> Tuple[str, str]:
    answer_match = re.search(
        r"FINAL ANSWER:\s*(.*?)(?:\nEXPLANATION:|\Z)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    explanation_match = re.search(
        r"EXPLANATION:\s*(.*)\Z",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    answer = answer_match.group(1).strip() if answer_match else text.strip()
    explanation = explanation_match.group(1).strip() if explanation_match else ""
    return answer, explanation


def call_responses_api(model: str, prompt: str, reasoning_effort: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    payload = {
        "model": model,
        "input": prompt,
    }
    if reasoning_effort:
        payload["reasoning"] = {"effort": reasoning_effort}

    request = urllib.request.Request(
        url="https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error ({exc.code}): {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error while calling OpenAI API: {exc}") from exc

    output_text = body.get("output_text")
    if output_text:
        return output_text

    parts: List[str] = []
    for item in body.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                parts.append(content.get("text", ""))
    return "\n".join(parts).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Problem CSV, e.g. data/problems_sample.csv")
    parser.add_argument("--output", required=True, help="Output CSV for model responses")
    parser.add_argument("--model", default="gpt-5.2")
    parser.add_argument("--reasoning-effort", default="medium")
    parser.add_argument("--limit", type=int, default=0, help="Optional number of problems to run")
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    args = parser.parse_args()

    problems = pd.read_csv(args.input).fillna("")
    if args.limit > 0:
        problems = problems.head(args.limit)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(
            outfile,
            fieldnames=[
                "id",
                "condition",
                "model",
                "model_answer",
                "model_explanation",
                "raw_response",
            ],
        )
        writer.writeheader()

        for _, row in problems.iterrows():
            for condition in ["baseline", "correct_hint", "misleading_hint"]:
                prompt = make_prompt(
                    row["problem"],
                    condition,
                    str(row["correct_answer"]),
                    str(row["misleading_answer"]),
                )
                full_prompt = f"{prompt}\n\n{FORMAT_INSTRUCTION}"
                raw_response = call_responses_api(
                    model=args.model,
                    prompt=full_prompt,
                    reasoning_effort=args.reasoning_effort,
                )
                model_answer, model_explanation = extract_fields(raw_response)
                writer.writerow(
                    {
                        "id": row["id"],
                        "condition": condition,
                        "model": args.model,
                        "model_answer": model_answer,
                        "model_explanation": model_explanation,
                        "raw_response": raw_response,
                    }
                )
                print(f"Completed {row['id']} [{condition}]")
                if args.sleep_seconds > 0:
                    time.sleep(args.sleep_seconds)

    print(f"Wrote model outputs to {output_path}")


if __name__ == "__main__":
    main()
