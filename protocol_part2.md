# Evaluation protocol, part 2
Written on 12 November 2026, before recording any part 2 demo.

## Question
With two sponges and two trays on the table, does the arm do what the sentence says,
and do I need a model that reads for that?

## What is compared
- SmolVLA: one model, fine-tuned from lerobot/smolvla_base on all 96 demos. It gets the sentence.
- ACT x4: four ACT models trained from scratch, one per sentence, each on the 24 demos of
  its sentence. The sentence picks which model runs.
- Same 96 demos for both systems. Every model trains for the same number of steps N:
  6 passes over the 96 demos at batch size 8 (N = 6 x frames / 8, rounded to the nearest 1,000).
  N is fixed after the recording and before training. SmolVLA's learning-rate decay is set to N steps.
- As in part 1: no image augmentation, last checkpoint, ACT with temporal ensembling, SmolVLA with RTC.

## Scene
- One blue and one red sponge, always both on the table. Two white trays, left and right of the arm,
  on tape marks.
- Six dots in front of the arm: L1-L3 and R1-R3, columns 12 cm apart, rows 6 cm apart. Row 1 is nearest me.
- One sponge on a left dot, one on a right dot, aligned, the corner nearest me on the left on the dot.
- Cameras top and side, lamp light, curtains closed.

## Sentences
1. "Put the blue sponge in the left tray."
2. "Put the blue sponge in the right tray."
3. "Put the red sponge in the left tray."
4. "Put the red sponge in the right tray."

## Lists (scripts/make_part2_lists.py, seed 42)
- 18 placements. 6 are kept out of the demos: dot pairs L1-R2, L2-R1, L3-R3, both colour orders.
- Demos: results/part2_demo_order.csv. 8 rounds of 12; one round is one sentence on the 12 demo placements.
- Main test: results/part2_trial_order.csv. 36 trials per system (9 per sentence: 6 on demo placements,
  3 on kept-out ones), blocks of 3, the system that goes first alternates.
- Reworded sentences: results/part2_reworded_order.csv. 16 trials, SmolVLA only, same session as the main test.
- Fewer demos: results/part2_fewer_demos_order.csv. SmolVLA trained on 48 demos (rounds 3-6) and on 24 demos
  (rounds 3-6, three dot pairs), each on the 24 seen trials of the main test. The 96-demo model repeats
  12 of them the same day.

## One trial
Start: arm folded, gripper closed, trays empty and on their marks, sponges placed as the list says.
Time limit 30 s. First attempt counts. Every trial is filmed.
I note which sponge it went for (named, other, none), which tray it went to (named, other, none),
and the outcome code.
Success: the named sponge rests fully inside the named tray, released, within the time limit.

## Outcome codes
As in part 1 (S, A, G, D, M, T, F), plus W wrong sponge and X wrong tray.
The code is the first thing that went wrong.

## Verdict
- Between the systems: my rule from part 1, a gap of at least 2 gap-margins (about 9 of 36). Smaller is a tie.
- Against luck: a system that ignores the sentence gets about 9 of 36. 16 or more rules luck out.
- Seen against new placements (24 and 12 trials): reported, no verdict.
- Reworded sentences: 9 or more of 16 rules luck out.
- Fewer demos: 24 against 96 demos, a gap of about 7 of 24. If the 96-demo model scores 4 or more below
  its main-test score on its 12 repeat trials, I stop and check the setup first.

## My bets
Main test: SmolVLA 30 of 36, ACT x4 9 of 36.
Reworded sentences: SmolVLA 8 of 16.
Fewer demos: SmolVLA on 24 demos 6 of 24, on 48 demos 12 of 24.
Why: I think SmolVLA is able to generalize pretty well. Occasional failed grasps and choosing the wrong sponge can happen. ACT cannot understand language and doesn't know which sponge to pick up and doesn't know which tray to put it in. Therefore i expect that there is a 25% chance that ACT will take the right sponge and the right tray. With reworded sentence i expect that the SmolVLA will still be able to perform, but will make more mistakes as it has new language inputs and then needs to know how to react to that. In the first part of this experiment the performance of SmolVLA dropped when trained on fewer data, similarly I expect the SmolVLA models to perform worse when trained on fewer demo data.

## Additions on 13 November 2026, after recording and before training
- Dataset: jaaaa000/so101_part2. I recorded 111 demos on 13 November; 96 are used.
- Round 1 was recorded again at the end of the session, and the first round 1 is not used.
  Its pace differed from the other rounds: I let go of the sponge after 23 s on average,
  against 17 to 19 s in rounds 2 to 8.
- Three single demos were recorded again and their first versions are left out of training:
  round 2 demo 1 and round 3 demo 2 (the sponges were on swapped sides), and round 2 demo 4
  (the arm stood still for about 10 s).
- N = 46,000 steps for every model: the 96 demos hold 61,358 frames, 6 passes at batch size 8.
- Before the real recording I made 8 practice demos on 12 November. They are not used for training.