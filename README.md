# CoT Faithfulness Stress Test on Mathematical Hints

A small empirical project testing whether language models faithfully disclose reliance on misleading hints in mathematical reasoning tasks.

## Research question

When a model changes its answer after receiving a misleading hint, does its explanation reveal that it relied on the hint?

This project compares model behavior across three prompt conditions:

1. **Baseline**: the original problem only.
2. **Correct hint**: the problem plus a previous-solver hint containing the correct answer.
3. **Misleading hint**: the problem plus a previous-solver hint containing an incorrect but plausible answer.

The goal is not to benchmark raw capability. The goal is to probe whether explanations remain faithful under subtle external pressure.

## Repository structure

```text
cot-faithfulness-math-hints/
├── data/
│   └── problems_sample.csv
├── docs/
│   └── report_template.md
├── results/
│   └── .gitkeep
├── src/
│   ├── build_prompts.py
│   ├── evaluate_results.py
│   └── schema.py
├── notebooks/
│   └── .gitkeep
├── requirements.txt
├── .gitignore
└── README.md
```

## Data format

Each row in `data/problems_sample.csv` is one problem.

Required columns:

| Column | Description |
|---|---|
| `id` | Unique problem ID |
| `domain` | Problem type, e.g. probability, combinatorics, algebra |
| `problem` | The problem statement |
| `correct_answer` | Gold answer |
| `misleading_answer` | Plausible incorrect hint |
| `notes` | Optional notes on why the wrong answer is tempting |

## How to run

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate prompts:

```bash
python src/build_prompts.py --input data/problems_sample.csv --output results/prompts.csv
```

After querying a model manually or through an API, save outputs as:

```text
results/model_outputs.csv
```

with columns:

```text
id,condition,model_answer,model_explanation
```

Then evaluate:

```bash
python src/evaluate_results.py \
  --problems data/problems_sample.csv \
  --outputs results/model_outputs.csv \
  --output results/evaluation.csv
```

## Run against an OpenAI model

Recommended model choices, based on the current OpenAI model docs:

- `gpt-5.2` for the strongest benchmark run
- `gpt-5-mini` for a cheaper pilot run

Set your API key:

```bash
export OPENAI_API_KEY=your_key_here
```

Run the sample benchmark:

```bash
python src/run_openai_model.py \
  --input data/problems_sample.csv \
  --output results/model_outputs.csv \
  --model gpt-5.2 \
  --reasoning-effort medium
```

Then score the outputs:

```bash
python src/evaluate_results.py \
  --problems data/problems_sample.csv \
  --outputs results/model_outputs.csv \
  --output results/evaluation.csv
```

For a quick smoke test before spending more tokens:

```bash
python src/run_openai_model.py \
  --input data/problems_sample.csv \
  --output results/model_outputs_sample.csv \
  --model gpt-5-mini \
  --reasoning-effort low \
  --limit 2
```

## Free manual test path

If you want a no-cost version, use a free chat model manually in the browser, then score the answers with the existing evaluator.

Generate a manual test sheet:

```bash
python src/build_manual_test_sheet.py \
  --input data/problems_sample.csv \
  --output results/manual_test_sheet.csv
```

Then:

1. Open `results/manual_test_sheet.csv`.
2. Paste each prompt into ChatGPT Free or another free chat model.
3. Copy the model's final answer into `model_answer`.
4. Copy the short explanation into `model_explanation`.
5. Save the filled file as `results/model_outputs.csv`.

Score it with:

```bash
python src/evaluate_results.py \
  --problems data/problems_sample.csv \
  --outputs results/model_outputs.csv \
  --output results/evaluation.csv
```

## Website demo

This repository now includes a static website in `website/` that can be deployed on GitHub Pages, Netlify, or Vercel.

Features:

- Interactive prompt generator for all three conditions
- Searchable browser view of the sample dataset
- Client-side evaluator for uploaded `model_outputs.csv`

Preview it locally:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/website/
```

If you update `data/problems_sample.csv`, regenerate the website JSON:

```bash
python src/export_web_data.py \
  --input data/problems_sample.csv \
  --output website/problems.json
```

### Deploy on GitHub Pages

This repository includes [.github/workflows/deploy-pages.yml](.github/workflows/deploy-pages.yml), so GitHub can deploy the `website/` directory automatically.

1. Push this folder to a GitHub repository.
2. Rename your default branch to `main` if needed.
3. In GitHub, open `Settings` -> `Pages`.
4. Set `Source` to `GitHub Actions`.
5. Push to `main` and wait for the `Deploy Website` workflow to finish.

You can also deploy the same `website/` directory directly to Netlify or Vercel as a static site.

## Main metrics

- Baseline accuracy
- Correct-hint accuracy
- Misleading-hint accuracy
- Hint-following rate under misleading hints
- Disclosure rate among hint-following cases
- Apparent rationalization rate

## Suggested writeup framing

This project is motivated by the concern that chain-of-thought explanations can be useful for oversight while still being incomplete or unfaithful. Mathematical reasoning problems are a useful testbed because correctness is often externally checkable, and misleading hints can be designed to be plausible without being ambiguous.
