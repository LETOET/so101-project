# Prints the success rate and margin per model from a results file; with two models, also the gap and the verdict.
# The margin formula and the verdict rule are the ones written in protocol.md before the test.
# Run it from the project root: python scripts/analyze.py <results file>

import sys
import csv
import math

# 1. Read the results file: one row per trial, with the model and the outcome code.
with open(sys.argv[1], newline="") as f:
    results = list(csv.DictReader(f))

# 2. Count trials and successes per model. Each dict is a small table: model name -> count.
counts_trials = {}
counts_successes = {}
for row in results:
    model = row["model"]  # the model name in this row, for example "ACT"
    counts_trials[model] = counts_trials.get(model, 0) + 1  # one more trial for this model (starts from 0)
    if row["code"] == "S":  # S = success, every other code is a failure
        counts_successes[model] = counts_successes.get(model, 0) + 1
    # print(row["trial"], model, row["code"], counts_successes)

# 3. Success rate and margin per model. The margin is √(n·p·(1−p)), counted in trials.
margins = {}  # model name -> margin, used again in step 4
for model in counts_trials:
    n = counts_trials[model]
    successes = counts_successes.get(model, 0)  # 0 if this model never succeeded
    p = successes / n  # success rate
    margin = math.sqrt(n * p * (1-p))
    margins[model] = margin  # store the margin under the model's name
    print(model, successes, n, f"{p:.2f}", f"{margin:.2f}")

    # At 0 % or 100 % the formula gives 0, but a few trials can't make the result certain.
    if successes == 0 or successes == n:
        print(" note: at 0% or 100% the margin formula gives 0, which is too small")

# 4. Two models in the file: the gap, its margin and the verdict.
#    protocol.md: believe a gap of at least 2 gap-margins.
models = list(counts_trials)  # the model names, in the order they first appear in the file
if len(models) == 2:
    a = models[0]  # a and b hold names; margins[a] is the number stored under that name
    b = models[1]
    gap = abs(counts_successes.get(a, 0) - counts_successes.get(b, 0))  # difference in successes, never negative
    gap_margin = math.sqrt(margins[a]**2 + margins[b] ** 2)  # the two models' margins combined
    print("gap:", gap, "| gap margin:", f"{gap_margin:.2f}", "| believe at:", f"{2 * gap_margin:.2f}")
    if gap >= 2 * gap_margin and gap != 0:  # equal scores are never a difference, even when both margins are 0
        print("verdict: believable difference")
    else:
        print("verdict: no believable difference")
