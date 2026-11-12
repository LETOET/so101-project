import csv
import itertools
import random

SEED = 42
BLOCK_SIZE = 3
LEFT = ["L1", "L2", "L3"]      # row 1 is the row nearest me, row 3 is nearest the arm
RIGHT = ["R1", "R2", "R3"]
SENTENCES = {
    1: "Put the blue sponge in the left tray.",
    2: "Put the blue sponge in the right tray.",
    3: "Put the red sponge in the left tray.",
    4: "Put the red sponge in the right tray.",
}
REWORDED = {
    1: "Place the blue sponge into the tray on the left.",
    2: "Place the blue sponge into the tray on the right.",
    3: "Place the red sponge into the tray on the left.",
    4: "Place the red sponge into the tray on the right.",
}
SYSTEMS = ["ACT x4", "SmolVLA"]
rng = random.Random(SEED)


def save(name, header, rows):
    with open(f"results/{name}", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def dots(place):
    """place = (left dot, right dot, colour on the left dot) -> (dot of blue, dot of red)"""
    left, right, colour_left = place
    return (left, right) if colour_left == "blue" else (right, left)


# 1. Dot pairs kept out of the demos: every left dot and every right dot once.
shuffled_right = RIGHT[:]
rng.shuffle(shuffled_right)
kept_out_pairs = list(zip(LEFT, shuffled_right))
demo_pairs = [(l, r) for l in LEFT for r in RIGHT if (l, r) not in kept_out_pairs]

# 2. A placement is a dot pair plus which colour lies left.
demo_places = [(l, r, c) for (l, r) in demo_pairs for c in ("blue", "red")]      # 12
new_places = [(l, r, c) for (l, r) in kept_out_pairs for c in ("blue", "red")]   # 6

# 3. The 24-demo set uses 3 of the 6 demo dot pairs (both colour orders),
#    again with every left dot and every right dot once.
choices = [list(zip(LEFT, p)) for p in itertools.permutations(RIGHT)
           if all((l, r) in demo_pairs for l, r in zip(LEFT, p))]
small_pairs = rng.choice(choices)

# 4. Demo order: 8 rounds of 12. One round = one sentence on all 12 demo placements.
rows = []
for round_nr, sentence_nr in enumerate([1, 2, 3, 4, 1, 2, 3, 4], start=1):
    order = demo_places[:]
    rng.shuffle(order)
    for place in order:
        blue, red = dots(place)
        in_48 = 3 <= round_nr <= 6
        in_24 = in_48 and (place[0], place[1]) in small_pairs
        rows.append([len(rows) + 1, round_nr, sentence_nr, SENTENCES[sentence_nr], blue, red, int(in_48), int(in_24)])
save("part2_demo_order.csv", ["demo", "round", "sentence_nr", "sentence", "blue_dot", "red_dot", "in_48", "in_24"], rows)

# 5. Main test: 36 trials. Every placement is used twice, with two different sentences.
#    The six sentence pairs, dealt over the shuffled placements, give every sentence
#    6 trials on demo placements and 3 on kept-out placements.
sentence_pairs = [(1, 2), (3, 4), (1, 3), (2, 4), (1, 4), (2, 3)]
trials = []
for kind, places in (("seen", demo_places), ("new", new_places)):
    order = places[:]
    rng.shuffle(order)
    for i, place in enumerate(order):
        for sentence_nr in sentence_pairs[i % 6]:
            trials.append((kind, place, sentence_nr))
rng.shuffle(trials)

# 6. Cut into blocks of 3. Both systems do each block; who goes first alternates.
rows = []
blocks = [trials[i:i + BLOCK_SIZE] for i in range(0, len(trials), BLOCK_SIZE)]
for block_nr, block in enumerate(blocks, start=1):
    order = SYSTEMS if block_nr % 2 == 1 else SYSTEMS[::-1]
    for system in order:
        for kind, place, sentence_nr in block:
            blue, red = dots(place)
            rows.append([len(rows) + 1, block_nr, system, sentence_nr, SENTENCES[sentence_nr], blue, red, kind])
save("part2_trial_order.csv", ["trial", "block", "system", "sentence_nr", "sentence", "blue_dot", "red_dot", "placement"], rows)

# 7. Reworded sentences: 4 trials per sentence, on demo placements, SmolVLA only.
rows = []
reworded = [(sentence_nr, place) for sentence_nr in SENTENCES for place in rng.sample(demo_places, 4)]
rng.shuffle(reworded)
for sentence_nr, place in reworded:
    blue, red = dots(place)
    rows.append([len(rows) + 1, "SmolVLA", sentence_nr, REWORDED[sentence_nr], blue, red])
save("part2_reworded_order.csv", ["trial", "system", "sentence_nr", "sentence", "blue_dot", "red_dot"], rows)

# 8. Fewer demos: the 24 "seen" trials of the main test, for SmolVLA trained on 24 and on 48 demos.
#    In every second block the 96-demo model runs the block again, as a same-day check (12 trials).
seen = [t for t in trials if t[0] == "seen"]
rows = []
blocks = [seen[i:i + BLOCK_SIZE] for i in range(0, len(seen), BLOCK_SIZE)]
for block_nr, block in enumerate(blocks, start=1):
    order = ["SmolVLA 24", "SmolVLA 48"] if block_nr % 2 == 1 else ["SmolVLA 48", "SmolVLA 24"]
    if block_nr % 2 == 1:
        order = order + ["SmolVLA 96"]
    for system in order:
        for kind, place, sentence_nr in block:
            blue, red = dots(place)
            rows.append([len(rows) + 1, block_nr, system, sentence_nr, SENTENCES[sentence_nr], blue, red])
save("part2_fewer_demos_order.csv", ["trial", "block", "system", "sentence_nr", "sentence", "blue_dot", "red_dot"], rows)

print("kept-out dot pairs:", kept_out_pairs)
print("dot pairs of the 24-demo set:", small_pairs)