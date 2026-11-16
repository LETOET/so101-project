# Prints trials and successes per system from a part 2 results file, and successes per system and sentence.
# A success follows protocol_part2.md: code S, the named sponge (Y) and the named tray (Y).
# Run it from the project root: python scripts/analyze_part2.py <results file> 
import sys
import csv

# 1. Read the results file: one row per trial, with the system and the outcome code.
with open(sys.argv[1], newline="") as f:
    results = list(csv.DictReader(f))

# 2. Count trials and successes per system, and successes per system and sentence.
counts_trials = {}
counts_successes = {}
counts_per_system = {}
counts_per_sentence = {}
for row in results:
    system = row["system"]  # the system name in this row, for example "SmolVLA"
    sentence_nr = row["system"] + " sentence: " + row["sentence_nr"]
    counts_trials[system] = counts_trials.get(system, 0) + 1  # one more trial for this system (starts from 0)
    if row["code"] == "S" and row["sponge"] == "Y" and row["tray"] == "Y": # a success: code S, the named sponge (Y) and the named tray (Y)
        counts_successes[system] = counts_successes.get(system, 0) + 1
        counts_per_sentence[sentence_nr] = counts_per_sentence.get(sentence_nr, 0) + 1

# 3. Print trials and successes per system.
for system in counts_trials:
    n = counts_trials[system]
    successes = counts_successes.get(system, 0)
    print(system, "trials:", n, "successes:", successes)

# 4. Print successes per system and sentence (a sentence without any success is not listed yet).
for sentence in counts_per_sentence:
    print(sentence, "successes:", counts_per_sentence[sentence])