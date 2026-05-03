# A Small Empirical Probe of Chain-of-Thought Faithfulness Under Misleading Mathematical Hints

## Motivation

This project tests whether model explanations faithfully reveal reliance on misleading external hints in mathematical reasoning tasks. Mathematical problems are useful for this probe because correctness is externally checkable, while misleading hints can be made plausible but objectively wrong.

## Experimental design

I constructed a set of short probability, combinatorics, and algebra problems with known answers. Each problem was evaluated under three prompt conditions:

1. Baseline: original problem only.
2. Correct hint: original problem plus a previous-solver hint containing the correct answer.
3. Misleading hint: original problem plus a previous-solver hint containing an incorrect but plausible answer.

For each model output, I recorded whether the final answer was correct, whether it followed the misleading hint, and whether the explanation explicitly disclosed reliance on the hint.

## Metrics

- Baseline accuracy
- Correct-hint accuracy
- Misleading-hint accuracy
- Hint-following rate under misleading hints
- Disclosure rate among hint-following cases
- Possible rationalization rate among hint-following cases

## Preliminary hypotheses

- Misleading hints will reduce accuracy.
- Some model responses will follow misleading hints without explicitly acknowledging reliance on them.
- Problems with tempting common fallacies, especially conditional probability and waiting-time problems, will produce more failures than direct algebraic tasks.

## Results

Add table or plot here.

## Discussion

The goal of this experiment is not to prove unfaithfulness in a mechanistic sense, but to create a small, inspectable dataset of cases where the model's final answer, explanation, and external hint can be compared. This provides a concrete starting point for studying when chain-of-thought explanations are useful oversight signals and when they may instead function as post-hoc rationalizations.

## Limitations

- Small sample size.
- Manual grading is imperfect.
- String matching should be replaced by more careful answer normalization for larger experiments.
- The experiment probes behavioral faithfulness, not internal model computation directly.
