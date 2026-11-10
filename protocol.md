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
Start: arm in the folded pose. The sponge's corner nearest me on the left goes on the dot; at 45° that corner stays on the dot and the sponge turns clockwise.
Dots are numbered from the row nearest me, left to right (1–3), then moving away from me (4–6, 7–9).
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

## Additions on 10 November 2026, before the first counted trial
Written after training and 16 pilot tries, before trial 1 of the 36.

### Models
Both trained on the new recording jaaaa000/so101_blue_sponge_v2_20261109_212801:
53 of 54 demos (demo 5 left out: the gripper closed again at the end).
ACT: trained from scratch, outputs/act_blue_sponge_v2.
SmolVLA: fine-tuned from lerobot/smolvla_base, outputs/smolvla_blue_sponge_v2.
Both: 30,000 steps, batch size 8, no image augmentation, last checkpoint (030000).

### How each model runs
ACT: temporal ensembling (--policy.n_action_steps=1 --policy.temporal_ensemble_coeff=0.01).
SmolVLA: real-time chunking (--inference.type=rtc, LeRobot defaults).
Why: each method's own real-robot setting. In the pilots, SmolVLA's default mode
stood still for about 5 of every 30 s while computing.
One trial = one lerobot-rollout run with --duration=30. Exact commands: commands.md, section "Test".

### Scene
Light: Using only artificial light (indoor lamps) as during the new recording, curtains closed, no daylight.
Cameras: the side camera moved about 3 px after the recording (measured against the demos)
and was not put back. The top camera did not move.
Before every trial: arm folded, gripper closed, tray on its tape marks.
If the robot moves the tray, it goes back on the marks before the next trial.

### Pilot tries (not counted)
9 November: 12 tries with the first ACT model on dots 2, 5 and 8, 6 without and 6 with ensembling.
10 November: 4 tries with the test models on dot 5 aligned: SmolVLA default mode 30 s (timeout)
and 45 s (finished, but after 30s limit), SmolVLA rtc (success), ACT with ensembling (success).

### My bets (made before these models ever moved the robot)
ACT 9 of 18, SmolVLA 10 of 18.

### More extra tests (reported separately, never mixed into the 18)
SmolVLA trained on the first recording (my bet: 5 of 18).
Both models retrained with image augmentation, as a follow-up.
New demonstrations in daylight. Then do augmented training on both sets.