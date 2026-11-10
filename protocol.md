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

## Additions on 10 November 2026, after the 36 counted trials
Written after seeing the results and before watching the video. Not pre-registered.

### Which code when one problem leads to another
The code is the first thing that went wrong.
T only when nothing went wrong but the robot was too slow.
A missed approach: the gripper closes beside the sponge, not around it.
G failed grasp: the gripper closes around the sponge, but the sponge slips out.
Why: trials 25 and 27 had the same problem (gripper beside the sponge, closing pushed it away)
but I coded them A and G during the test. results/trials.csv keeps the codes as typed;
the codes checked against these rules go in results/video_review.csv.

### Grasp quality (a second measure, for all 36 trials)
Scored by me from the phone video. Not blind: I knew which model ran each trial.
clean: the gripper closes around the sponge's sides on the first try.
marginal: it held the sponge in the end, but the first grasp was at the edge or on top,
pushed or flipped the sponge, or it needed a second try.
failed: it never held the sponge.

## Extra tests, 10 November 2026, written before the first extra trial
Codes and the coding rule as in the additions after the 36 counted trials.
Orders in results/yellow_order.csv and results/smolvla_v1_order.csv.

### Yellow sponge (8 trials)
ACT v2 and SmolVLA v2, 4 trials each on dots 1, 3, 7 and 9, all aligned.
Task sentence unchanged ("blue sponge"). Order in blocks of 2: ACT, SmolVLA, SmolVLA, ACT.
My bets: ACT 1 of 4, SmolVLA 4 of 4.
Why: ACT has only ever seen a blue sponge, so it may not find a yellow one.
SmolVLA can generalise: it reads the sentence and can work out that the sponge is now yellow.
Note: yellow stands out less from the light table than blue, so a failure can also come from contrast.

### SmolVLA trained on the first recording (18 trials)
Blue sponge. The 18 SmolVLA placements of the test, in the same order.
Same command as SmolVLA in the test, with outputs/smolvla_blue_sponge. My bet: 5 of 18.

### Yellow sponge, sentence changed (decided after the 8 yellow trials, before running these)
All 8 yellow trials failed (ACT 0 of 4, SmolVLA 0 of 4). ACT came close to the sponge; SmolVLA did not.
4 SmolVLA v2 trials, yellow sponge, dots 1, 3, 7 and 9 aligned, in that order,
task sentence "Pick up the yellow sponge and put it in the white tray."
Question: can the word "yellow" make SmolVLA find the sponge?
My bet: SmolVLA 4 of 4.


## Follow-up: 18 demos (written 10 November 2026, before training)

Question: does SmolVLA's pretraining help when demos are scarce? With 53 demos both models were at the ceiling (16/18 and 18/18).

- Data: the second recording, episodes 18–35 only (rounds 3 and 4: every dot once aligned and once at 45°), 18 demos.
  I chose these rounds before training, because they are the middle of the recording session: by then I had practised
  (rounds 1–2) and I was not yet tired (rounds 5–6).
- Training: same settings as the test models (30,000 steps, batch 8). Only the number of demos changes.
- Test: the same 36 trials in the same order (results/trial_order.csv), same lamp light, same codes, 30 s limit and inference settings. Results go to results/demos18_trials.csv.
- Verdict: same rule, a gap of at least 2 gap-margins. If the gap is 4 or 5, I run 18 more trials per model in the same order.
- Bets: ACT 10 of 18, SmolVLA 15 of 18.
  Both models will perform worse because they have less varied data to train on. They will overfit on a few
  demonstrations, and a small difference at test time can already be out of distribution.
  I suspect ACT will have more trouble, because with 53 demos it already had more trouble picking the sponge up and
  often barely made it. SmolVLA will also drop for the same reason, but less, because it was a little more robust with
  53 demos. On top of that, I think the pretrained action head will help keep its performance high.