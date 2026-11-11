# Appendix

Details behind the [README](README.md): setup, data, models, every result table, and the full list of limitations.

- [Why this experiment](#why-this-experiment)
- [Setup](#setup)
- [Demonstrations](#demonstrations)
- [Models and training](#models-and-training)
- [Protocol](#protocol)
- [Results](#results)
- [Other findings](#other-findings)
- [Limitations](#limitations)
- [Reproduce](#reproduce)

## Why this experiment

Every robot-learning task in industry starts with the same questions: how many demonstrations does it need, and which
model? Large pretrained models promise to need fewer demos, because they bring prior knowledge. SmolVLA was
pretrained on community data from SO-100 arms, which are nearly the same body as the SO-101. If its pretraining pays
off anywhere, it should be here.

In an earlier simulation exercise on a different arm (ALOHA), SmolVLA's robot pretraining made no difference after
5,000 fine-tuning steps (20/50 against 19/50 with a randomly initialised action expert). This project tests the
matching-body case on real hardware.

## Setup

| | |
|---|---|
| Arm | SO-101 follower, teleoperated with an SO-101 leader arm |
| Cameras | 2 × Logitech C270, 640×480 at 30 fps (MJPG): one top-down, one from the side. No wrist camera |
| Object | a blue kitchen sponge; target: a white tray at a taped position |
| Scene | 9 taped dots 5 cm apart; the sponge starts on a dot, aligned or turned 45° |
| Light | indoor lamp light, curtains closed (the same light for demos and tests) |
| Computer | one PC for teleoperation, training and testing: NVIDIA RTX 3060 12 GB, Intel i5-6500 (4 cores), Ubuntu 22.04 |
| Software | [LeRobot](https://github.com/huggingface/lerobot) 0.6.0 |

<table>
<tr>
<td><img src="media/task_start.jpg" alt="Start: sponge on a dot"></td>
<td><img src="media/task_end.jpg" alt="End: sponge in the tray"></td>
</tr>
<tr>
<td align="center">Start: sponge on a dot</td>
<td align="center">End: sponge in the tray</td>
</tr>
</table>

## Demonstrations

| | First recording ("rushed") | Second recording ("careful") |
|---|---|---|
| Demos recorded / used | 54 / 52 | 54 / 53 |
| Coverage | each dot 3× aligned, 3× at 45° | each dot 3× aligned, 3× at 45° |
| Length | 27 s at the start, 18 s by the end (I sped up) | 22 s on average to the release, steady |
| Grasp | quick | short wait above the sponge, then a careful grasp |
| Release | gripper opened about two thirds as wide as before the grasp | gripper opened fully |
| End of a demo | after driving back to the home pose | right after the release |
| Light | daylight, then dusk | the lamp |

Two demos of the first recording turned the wrist the other way at 45° and were left out. One demo of the second
recording closed the gripper again after the release and was left out.

In the first recording, 24 % of all frames come after the release, while the arm drives back home. 15 % of those
frames lie on the carry path to the tray, running the other way, so the same arm position is followed by opposite
moves. The second recording has no frames after the release.

## Models and training

| | ACT | SmolVLA |
|---|---|---|
| Start | from scratch | fine-tuned from `lerobot/smolvla_base` |
| Size | 52 M parameters | 450 M parameters, of which 100 M trained (the action expert; vision-language backbone frozen) |
| Training | 30,000 steps, batch 8 | 30,000 steps, batch 8 |
| Time on the RTX 3060 | about 2.5 h | about 3 h |
| Running on the robot | temporal ensembling: a new prediction every step, averaged | real-time chunking: chunks of 50 steps, the next one computed in the background |

Each model runs in its authors' real-robot setting. Without real-time chunking, SmolVLA stood still for about 5 of
every 30 seconds while it computed its next chunk (325 ms each).

## Protocol

The full protocol is in [protocol.md](protocol.md). It was committed before the first training run. Every later
addition is dated in the file and was committed before the trials it covers, except three coding rules that were
written after a test and before reviewing it; those are marked as such.

- **18 trials per model:** 9 dots × 2 angles (aligned, 45°), in a seeded order
  ([trial_order.csv](results/trial_order.csv)).
- **Interleaved:** blocks of 3 trials in an A B B A pattern, so slow drift (warm servos, light) hits both models
  equally.
- **One attempt per trial, 30 s limit.** Success means the whole sponge in the tray and released.
- **Failure codes,** the first thing that went wrong: `A` missed approach, `G` failed grasp, `D` dropped on the way,
  `M` missed the tray, `T` timeout, and `F` frozen on the way (holds the sponge but stops in mid-air; added after the
  test of ACT on the rushed recording).
- **Verdict rule:** a model's margin is √(n·p·(1−p)) trials; I believe a gap between the models only if it is at least
  2 × √(m_ACT² + m_SmolVLA²), about 6 of 18.
- **Bets** for each test were written in the protocol before it ran.

## Results

### Main test: 53 careful demos

| Model | Success | Margin | Grasp: clean / marginal / failed | Failures |
|---|---|---|---|---|
| ACT | 16/18 | ±1.3 | 13 / 3 / 2 | 2 × A |
| SmolVLA | 18/18 | ±0 by the formula* | 13 / 5 / 0 | none |

Gap 2; my margin rule needs a gap of at least 2.7. No significant difference: both models are at the ceiling of this
test (see [Is the difference significant?](#is-the-difference-significant)).

\* At 100 % the formula gives 0. The exact 95 % lower bound for 18 of 18 is about 81 %.

Grasp quality was scored from the video ([video_review.csv](results/video_review.csv)): *clean* means the gripper
closes around the sponge's sides on the first try; *marginal* means it held the sponge in the end, but came down on
top or at the edge, pushed or flipped it, or needed a second try. Both ACT failures had the same cause: the gripper
came down beside or on top of the sponge, and closing pushed it away.

### Follow-up: 18 demos

Does SmolVLA's pretraining help when demos are scarce? I retrained both models on 18 of the 53 careful demos (every
dot once aligned and once at 45°), with the same settings, and ran the same 36 trials.

| Model | 53 demos | 18 demos | Margin (18 demos) | Grasp (18 demos): clean / marginal / failed | Failures (18 demos) |
|---|---|---|---|---|---|
| ACT | 16/18 | 13/18 | ±1.9 | 10 / 5 / 3 | 3 × A, 1 × G, 1 × T |
| SmolVLA | 18/18 | 11/18 | ±2.1 | 8 / 3 / 7 | 5 × A, 2 × G |

- **ACT against SmolVLA with 18 demos:** gap 2; my margin rule needs a gap of at least 5.6. No significant difference.
- **Both did worse with fewer demos,** SmolVLA the most (18 → 11). This comparison runs across two days and wasn't part
  of the pre-registered verdict, so I report it as an observation.
- **A new failure:** the gripper standing in place above the sponge without closing or opening (SmolVLA twice, ACT
  once). It didn't happen in any counted trial with 53 demos.
- **Noticed afterwards (not pre-registered):** all 5 ACT failures were on aligned placements (4/9 aligned, 9/9 at 45°).

### Is the difference significant?

I checked it two ways, and they agree: no.

| Test | ACT | SmolVLA | Gap | Gap my rule needs | Fisher's exact test |
|---|---|---|---|---|---|
| Main test, 53 demos | 16/18 | 18/18 | 2 | 2.7 | p = 0.49 |
| 18 demos | 13/18 | 11/18 | 2 | 5.6 | p = 0.72 |

**My margin rule** (fixed before testing): a model's margin is $m = \sqrt{n\,p\,(1-p)}$ trials, with $n$ trials and
success rate $p$. I only believe a gap between the models if it is at least $2\sqrt{m_\text{ACT}^2 + m_\text{SmolVLA}^2}$.

**Fisher's exact test** asks: if both models were equally good, how likely is a split at least this uneven? With
$n = 18$ trials per model, $x$ successes for ACT and $s$ successes in total, the chance of one particular split is

$$P(x) = \frac{\binom{n}{x}\binom{n}{s-x}}{\binom{2n}{s}}$$

The p-value adds up $P$ over every split that is as unlikely as the one I saw, or more. A difference counts as
significant when $p < 0.05$. Here $p$ is 0.49 and 0.72: a gap of 2 out of 18 easily happens by chance.

The two tests on the rushed recording (ACT 0/18, SmolVLA 7/18) ran on different days, so I don't test that pair.

Codes and grasp quality for this test come from my notes during the trials
([demos18_video_review.csv](results/demos18_video_review.csv)).

### Setup control

The cameras had shifted a few pixels and the GPU driver had been updated since the main test. So before the 18-demo
trials I ran the two 53-demo models again on the first 18 trials of the order
([control53_trials.csv](results/control53_trials.csv)): 8/9 each, against 9/9 each in the main test. On the same
trials the 18-demo models scored 6/9 each. So the setup change alone doesn't explain the drop.

### Extra tests (reported separately from the 18)

| Test | ACT | SmolVLA | For comparison |
|---|---|---|---|
| Yellow sponge, same 4 corner placements, sentence unchanged | 0/4 | 0/4 | blue sponge on the same placements: 4/4 and 4/4 |
| Yellow sponge, sentence says "yellow" (decided after the 0/8) | not run | 0/4 | |
| Trained on the rushed first recording | 0/18 | 7/18 | careful recording: 16/18 and 18/18 |

- With the yellow sponge, ACT came close and just missed it; SmolVLA did not even come close. With "yellow" in the
  sentence, SmolVLA often didn't go down to the sponge at all. ACT has no language input, so the sentence test was
  SmolVLA only.
- During fine-tuning, SmolVLA's vision-language backbone was frozen; only the action expert was trained, and it only
  ever saw one blue sponge and one sentence. The backbone still "knows" yellow, but the part that turns what it sees
  into movement never learned to use it.
- Yellow also stands out less against the light table than blue, so contrast may play a part.
- On the rushed recording the two models failed in different ways. SmolVLA failed at the approach (4 × A) and the
  grasp (6 × G), exactly the manoeuvres I rushed, and missed the tray once (1 × M). ACT held the sponge in 11 of 18
  trials, then froze in mid-air and never reached the tray (10 × F; 8 × A). Most likely cause: the way home in those
  demos passes the same arm positions as the way to the tray, in the opposite direction (see
  [Demonstrations](#demonstrations)). Why SmolVLA didn't freeze I haven't tested.
- The two rushed-recording tests ran on different days (SmolVLA on 10 November, ACT on 11 November), not
  interleaved, so I don't compare the two models there. Before this, ACT on the rushed recording only had 12
  uncounted pilot tries (3 of 12).

### All counted outcomes

| Test | Model | S | A | G | D | M | T | F |
|---|---|---|---|---|---|---|---|---|
| Main, 53 demos | ACT | 16 | 2 | | | | | |
| Main, 53 demos | SmolVLA | 18 | | | | | | |
| 18 demos | ACT | 13 | 3 | 1 | | | 1 | |
| 18 demos | SmolVLA | 11 | 5 | 2 | | | | |
| Rushed recording | ACT | 0 | 8 | | | | | 10 |
| Rushed recording | SmolVLA | 7 | 4 | 6 | | 1 | | |
| Yellow sponge | ACT | 0 | 2 | 1 | 1 | | | |
| Yellow sponge | SmolVLA | 0 | 3 | 1 | | | | |
| Yellow sponge, "yellow" sentence | SmolVLA | 0 | 4 | | | | | |

The main test, the 18-demo test and ACT on the rushed recording use the codes after the coding rule
([video_review.csv](results/video_review.csv), [demos18_video_review.csv](results/demos18_video_review.csv),
[act_v1_video_review.csv](results/act_v1_video_review.csv)); the other rows are the codes as typed during the test.

### My bets against the results

| Test | Bet | Result |
|---|---|---|
| ACT, main test | 9/18 | 16/18 |
| SmolVLA, main test | 10/18 | 18/18 |
| ACT, yellow sponge | 1/4 | 0/4 |
| SmolVLA, yellow sponge | 4/4 | 0/4 |
| SmolVLA, "yellow" sentence | 4/4 | 0/4 |
| SmolVLA, rushed recording | 5/18 | 7/18 |
| ACT, rushed recording | 5/18 | 0/18 |
| ACT, 18 demos | 10/18 | 13/18 |
| SmolVLA, 18 demos | 15/18 | 11/18 |

I underestimated both models on careful data, and overestimated SmolVLA's ability to generalise and ACT on the rushed
data.

## Other findings

- **Small hardware details matter.** The C270 webcams only gave 15 fps in dim light until I switched off one camera
  setting (`exposure_dynamic_framerate`). A side-camera shift of 3 pixels made ACT close its gripper about 10 frames
  later in an offline test.
- **Fixing the rule before the data keeps me honest.** My bets were far off, and a 2-trial gap is a tie by my own rule.
  Writing that rule down first is what stops me from calling 18 against 16 a win.

## Limitations

- **Small samples.** 18 trials per model can only show gaps of about 6 or more.
- **Not blind.** I placed the sponge, judged every trial, and knew which model was running.
- **Rushed against careful demos:** the light changed too (daylight against the lamp), so this comparison can't fully
  separate demo quality from light. The two tests on the rushed recording also ran on different days (SmolVLA on 10
  November, ACT on 11 November), not interleaved with each other or with the careful-demo tests.
- **Cameras:** the side camera sat a few pixels off its demo position during all tests. Both cameras had moved a few
  pixels more by the 18-demo test, and the top camera moved about 5 pixels during it. The setup control checks the
  effect on the 53-demo models; the two models within each test were always interleaved.
- **Compute:** with temporal ensembling, ACT's control loop ran at 9–30 Hz on the 4-core CPU, below the 30 Hz of the
  demos. The GPU driver was updated between the main test and the 18-demo test; the measured inference times didn't
  change.
- **Training budget:** the 18-demo models used the same 30,000 steps as the 53-demo models, so they saw each demo about
  3× as often. I did not tune anything for the smaller set.
- **Rules added after a test:** the rule for which code to use when one problem leads to another, and the grasp-quality
  scale, were written after the main test but before watching its video. The codes for "never closes" (G) and "frozen
  on the way" (F) were added after the tests where they first appeared, before reviewing them. The yellow-sentence
  test was decided after the yellow results. All are marked as such in the protocol.
- **Pilot tries:** 16 uncounted tries before the main test fixed the inference settings (listed in the protocol).
- **No image augmentation** during training, so absolute pixel positions were a reliable cue for both models.
- **One object, one tray position, one light.** Nothing here says how the models generalise beyond that.

## Reproduce

- Every command I ran, in order, is in [commands.md](commands.md): camera settings, recording, training, the test
  rollouts and the analysis.
- [scripts/make_trial_order.py](scripts/make_trial_order.py) makes the seeded trial order,
  [scripts/eval_log.py](scripts/eval_log.py) records each trial's outcome, and
  [scripts/analyze.py](scripts/analyze.py) computes success rates, margins and the verdict:

  ```bash
  python scripts/analyze.py results/trials.csv
  ```
