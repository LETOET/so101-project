# Asks for the outcome of each test trial and saves it to <results file>.
# Run it from the project root: python scripts/eval_log_part2.py <order file> <results file>

import csv
import os
import sys
from datetime import datetime

# 1. Read the fixed trial order.
with open(sys.argv[1], newline="") as f:
    trials = list(csv.DictReader(f))

path = sys.argv[2]
columns = ["trial", "block", "system", "sentence_nr", "blue_dot", "red_dot", "placement", "sponge", "tray", "code", "timestamp"]

# 2. Find the trials already saved: after a crash it carries on from there.
done = set()
if os.path.exists(path):
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            done.add(row["trial"])
print(len(done), "trials already done")

# 3. Go through the trials in order and skip the saved ones.
print(len(trials), "trials")
for trial in trials:
    
    if trial["trial"] in done:
        continue
        
    print("Trial", trial["trial"], "of", len(trials), ": ", trial["system"], "|", trial["sentence"], "| blue", trial["blue_dot"], "red", trial["red_dot"], trial.get("placement", ""))

    # 4. Keep asking until the answer is one of the outcome codes from protocol.md.
    allowed = ["Y", "O", "N"]

    while True:
        sponge = input("Sponge it went to (Y = named, O = other, N = none): ").strip().upper()
        if sponge in allowed:
            break
        print("Not valid, try again.")

    print("You chose", sponge)

    while True:
        tray = input("Tray it went to (Y = named, O = other, N = none): ").strip().upper()
        if tray in allowed:
            break
        print("Not valid, try again.")

    print("You chose", tray)

    allowed = ["S", "A", "G", "D", "M", "T", "F", "W", "X"]

    while True:
        code = input("Code (S/A/G/D/M/T/F/W/X): ").strip().upper()
        if code in allowed:
            break
        print("Not valid, try again.")

    print("You chose", code)

    # 5. Save it straight away: a crash can't lose a result that is already typed in.
    is_new = not os.path.exists(path)

    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)

        if is_new:
            writer.writeheader()
        writer.writerow({
            "trial": trial["trial"],
            "block": trial.get("block", ""),
            "system": trial["system"],
            "sentence_nr": trial["sentence_nr"],
            "blue_dot": trial["blue_dot"],
            "red_dot": trial["red_dot"],
            "placement": trial.get("placement", ""),
            "sponge": sponge,
            "tray": tray,
            "code": code,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        })


    print("saved")

