# Evaluation protocol
Written on 9 November 2026, before any training.

## Task
Exact task sentence: "Pick up the blue sponge and put it in the white tray."
Object: blue sponge. Target: white tray at its taped position.
Cameras: top and side, fixed. No wrist camera.

## Test positions
9 dots × 2 angles (aligned, 45°) = 18 trials per model.

## Order
Fixed before training by scripts/make_trial_order.py, seed 42.
Blocks of 3 trials, alternating models in the pattern A B B A.

## One trial
Start: arm in the folded pose, sponge centred on the dot.
Time limit: 30 s. No restarts: the first attempt counts.
Every trial is filmed.

## Outcome codes
S success: sponge in the tray and released within the time limit
A missed approach, G failed grasp, D dropped on the way,
M missed the tray, T timeout
If the sponge is only partly in the tray: Counts as a miss (M); success means the whole sponge rests inside the rim

## Verdict
Margin per model: √(n·p·(1−p)). Margin of the gap: √(m_A² + m_B²).
I believe a gap of at least 2 gap-margins (about 6 of 18).
If the difference is smaller than 6: I call it a tie, or I run all 18 trials again.

## Extra tests (reported separately, never mixed into the 18)
Replace the blue sponge with the yellow sponge. 4 trials per model on dots 1, 3, 7 and 9, aligned. Task sentence unchanged.