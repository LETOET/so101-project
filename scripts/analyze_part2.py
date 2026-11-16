# Prints the numbers of the part 2 results table from one results file:
# trials and successes per system, how often it went for the named sponge and to the named tray,
# and trials and successes per sentence and per placement (seen in the demos, or new).
# A success follows protocol_part2.md: code S, the named sponge (Y) and the named tray (Y).
# Run it from the project root: python scripts/analyze_part2.py <results file>

import sys
import csv

# 1. Read the results file: one row per trial, with the system and the outcome code.
with open(sys.argv[1], newline="") as f:
    results = list(csv.DictReader(f))

# 2. Count. Each dict is a small table: label -> count.
counts_trials = {}         # per system
counts_successes = {}
counts_named_sponge = {}
counts_named_tray = {}
trials_per_sentence = {}   # per system and sentence
counts_per_sentence = {}
trials_per_placement = {}  # per system and placement (seen or new)
counts_per_placement = {}
for row in results:
    system = row["system"]  # the system name in this row, for example "SmolVLA"
    sentence_label = system + " sentence: " + row["sentence_nr"]
    placement_label = system + " placement: " + row["placement"]

    # Every row is one more trial.
    counts_trials[system] = counts_trials.get(system, 0) + 1  # (starts from 0)
    trials_per_sentence[sentence_label] = trials_per_sentence.get(sentence_label, 0) + 1
    if row["placement"] != "":  # only the main test has seen and new placements
        trials_per_placement[placement_label] = trials_per_placement.get(placement_label, 0) + 1

    # A success: code S, the named sponge (Y) and the named tray (Y).
    if row["code"] == "S" and row["sponge"] == "Y" and row["tray"] == "Y":
        counts_successes[system] = counts_successes.get(system, 0) + 1
        counts_per_sentence[sentence_label] = counts_per_sentence.get(sentence_label, 0) + 1
        if row["placement"] != "":
            counts_per_placement[placement_label] = counts_per_placement.get(placement_label, 0) + 1

    # Which sponge it went for and which tray it went to, whatever happened after that.
    if row["sponge"] == "Y":
        counts_named_sponge[system] = counts_named_sponge.get(system, 0) + 1
    if row["tray"] == "Y":
        counts_named_tray[system] = counts_named_tray.get(system, 0) + 1

# 3. Print per system.
for system in counts_trials:
    n = counts_trials[system]
    successes = counts_successes.get(system, 0)  # 0 if this system never succeeded
    sponge = counts_named_sponge.get(system, 0)
    tray = counts_named_tray.get(system, 0)
    print(system, "trials:", n, "successes:", successes, "named sponge:", sponge, "named tray:", tray)

# 4. Print per system and sentence, in alphabetical order.
for label in sorted(trials_per_sentence):
    n = trials_per_sentence[label]
    successes = counts_per_sentence.get(label, 0)  # 0 if this sentence never succeeded
    print(label, "trials:", n, "successes:", successes)

# 5. Print per system and placement. Nothing is printed for a file without placements.
for label in sorted(trials_per_placement):
    n = trials_per_placement[label]
    successes = counts_per_placement.get(label, 0)
    print(label, "trials:", n, "successes:", successes)