import sys
import csv
import math

with open(sys.argv[1], newline="") as f:
    results = list(csv.DictReader(f))

counts_trials = {}
counts_successes = {}
for row in results:
    model = row["model"]
    counts_trials[model] = counts_trials.get(model, 0) + 1
    if row["code"] == "S":
        counts_successes[model] = counts_successes.get(model, 0) + 1
    # print(row["trial"], model, row["code"], counts_successes)

margins = {}
for model in counts_trials:
    n = counts_trials[model]
    successes = counts_successes.get(model, 0)
    p = successes / n
    margin = math.sqrt(n * p * (1-p))
    margins[model] = margin
    print(model, successes, n, f"{p:.2f}", f"{margin:.2f}")

    if successes == 0 or successes == n:
        print(" note: at 0% or 100% the margin formula gives 0, which is too small")

models = list(counts_trials)
if len(models) == 2:
    a = models[0]
    b = models[1]
    gap = abs(counts_successes.get(a, 0) - counts_successes.get(b, 0))
    gap_margin = math.sqrt(margins[a]**2 + margins[b] ** 2)
    print("gap:", gap, "| gap margin:", f"{gap_margin:.2f}", "| believe at:", f"{2 * gap_margin:.2f}")
    if gap >= 2 * gap_margin and gap != 0:
        print("verdict: believable difference")
    else: 
        print("verdict: no believable difference")
