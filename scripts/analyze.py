import os
import sys
import csv
import math

with open(sys.argv[1], newline="") as f:
    results = list(csv.DictReader(f))


columns = ["model", "successes", "n", "rate", "margin"]


counts_trials = {}
counts_successes = {}
for row in results:
    model = row["model"]
    counts_trials[model] = counts_trials.get(model, 0) + 1
    if row["code"] == "S":
        counts_successes[model] = counts_successes.get(model, 0) + 1
    # print(row["trial"], model, row["code"], counts_successes)

for model in counts_trials:
    n = counts_trials[model]
    successes = counts_successes.get(model, 0)
    p = successes / n
    margin = math.sqrt(n * p * (1-p))
    print(model, successes, n, f"{p:.2f}", f"{margin:.2f}")


