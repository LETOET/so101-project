# Asks for the outcome of each test trial and saves it to <results file>.
# Run it from the project root: python scripts/eval_log.py <order file> <results file>

import csv
import os
import sys
from datetime import datetime

# 1. Read the fixed trial order.
with open(sys.argv[1], newline="") as f:
    trials = list(csv.DictReader(f))

path = sys.argv[2]
columns = ["trial", "dot", "angle", "model", "code", "timestamp"]

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
        
    print("Trial", trial["trial"], "of", len(trials), ": dot ", trial["dot"], trial["angle"], "model", trial["model"])

    # 4. Keep asking until the answer is one of the outcome codes from protocol.md.
    allowed = ["S", "A", "G", "D", "M", "T", "F"]

    while True:
        code = input("Code (S/A/G/D/M/F/T): ").strip().upper()
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
            "dot": trial["dot"],
            "angle": trial["angle"],
            "model": trial["model"],
            "code": code,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        })


    print("saved")

