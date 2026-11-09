import csv
import random

SEED = 42
BLOCK_SIZE = 3
dots = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
angles = ["aligned", "45"]
models = ["ACT", "SmolVLA"]

# 1. Make every combination.
samples = []
for dot in dots:
    for angle in angles:
        samples.append((dot, angle))

# 2. Shuffle with a fixed seed: the same order every time you run it.
rng = random.Random(SEED)
rng.shuffle(samples)

# 3. Cut the shuffled list into blocks.
blocks = []
for start in range(0, len(samples), BLOCK_SIZE):
    blocks.append(samples[start:start + BLOCK_SIZE])

# 4. Both models do each block; who goes first alternates.
rows = []
for block_nr, block in enumerate(blocks, start=1):
    if block_nr % 2 == 1:
        order = models
    else:
        order = [models[1], models[0]]
    for model in order:
        for dot, angle in block:
            rows.append([len(rows) + 1, block_nr, dot, angle, model])

# 5. Save it.
with open("results/trial_order.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["trial", "block", "dot", "angle", "model"])
    writer.writerows(rows)

print(len(rows), "trials saved")