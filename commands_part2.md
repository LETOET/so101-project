# Commands, part 2

Every command run for part 2, in order, copy-pasteable. Same machine and environment as part 1
([commands.md](commands.md)): Linux, RTX 3060 12 GB, conda env `lerobot` (LeRobot 0.6.0). Run from `~/so101-project`.

At the start of every session I run the two camera-setting lines from [commands.md](commands.md), Phase 1.

## Lists (2026-11-12)

The placements kept out of the demos, the order of the demos and the trial lists, all from seed 42. Committed
together with [protocol_part2.md](protocol_part2.md) before any demo was recorded.

```bash
python scripts/make_part2_lists.py
```

It writes `results/part2_demo_order.csv`, `results/part2_trial_order.csv`, `results/part2_reworded_order.csv` and
`results/part2_fewer_demos_order.csv`.

## Practice demos (2026-11-12, not used for training)

Eight demos, two per sentence, to check the time limit, the layout and that four sentences fit in one dataset.
LeRobot adds the date and time to the dataset name.

```bash
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 \
  --robot.id=my_awesome_follower_arm \
  --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" \
  --teleop.type=so101_leader \
  --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B009251-if00 \
  --teleop.id=my_awesome_leader_arm \
  --dataset.repo_id=jaaaa000/so101_part2_practice_s1 \
  --dataset.single_task="Put the blue sponge in the left tray." \
  --dataset.num_episodes=2 \
  --dataset.episode_time_s=40 \
  --dataset.reset_time_s=30 \
  --dataset.fps=30 \
  --dataset.push_to_hub=false \
  --display_data=false
```

The other three recordings use the same command with `_s2`, `_s3`, `_s4` and the sentences 2, 3 and 4 below.

## Recording the demos (2026-11-13, 09:02 to 11:30)

Lamp light, curtains closed. One recording per round: one sentence, 12 demos, the placements of that round in
`results/part2_demo_order.csv`. Each demo ends when the gripper is fully open; going home happens in the
unrecorded reset. Round 1:

```bash
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 \
  --robot.id=my_awesome_follower_arm \
  --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" \
  --teleop.type=so101_leader \
  --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B009251-if00 \
  --teleop.id=my_awesome_leader_arm \
  --dataset.repo_id=jaaaa000/so101_part2_r1 \
  --dataset.single_task="Put the blue sponge in the left tray." \
  --dataset.num_episodes=12 \
  --dataset.episode_time_s=40 \
  --dataset.reset_time_s=30 \
  --dataset.fps=30 \
  --dataset.push_to_hub=false \
  --display_data=false
```

The other recordings use the same command with another `--dataset.repo_id`, `--dataset.single_task` and
`--dataset.num_episodes`:

| Recording | `--dataset.repo_id=jaaaa000/…` | Sentence | Demos | Dataset it made |
|---|---|---|---|---|
| Round 1 | `so101_part2_r1` | 1 | 12 | `so101_part2_r1_20261113_090209` (not used) |
| Round 2 | `so101_part2_r2` | 2 | 12 | `so101_part2_r2_20261113_092030` |
| Round 3 | `so101_part2_r3` | 3 | 12 | `so101_part2_r3_20261113_093402` |
| Round 4 | `so101_part2_r4` | 4 | 12 | `so101_part2_r4_20261113_095319` |
| Round 5 | `so101_part2_r5` | 1 | 12 | `so101_part2_r5_20261113_100620` |
| Round 6 | `so101_part2_r6` | 2 | 12 | `so101_part2_r6_20261113_102009` |
| Round 7 | `so101_part2_r7` | 3 | 12 | `so101_part2_r7_20261113_103832` |
| Round 8 | `so101_part2_r8` | 4 | 12 | `so101_part2_r8_20261113_105144` |
| Round 1 again | `so101_part2_redo_r1` | 1 | 12 | `so101_part2_redo_r1_20261113_111327` |
| Two demos again | `so101_part2_redo_s2` | 2 | 2 | `so101_part2_redo_s2_20261113_112653` |
| One demo again | `so101_part2_redo_s3` | 3 | 1 | `so101_part2_redo_s3_20261113_112924` |

The sentences:

1. `Put the blue sponge in the left tray.`
2. `Put the blue sponge in the right tray.`
3. `Put the red sponge in the left tray.`
4. `Put the red sponge in the right tray.`

Recorded again, as written in [protocol_part2.md](protocol_part2.md):
- Round 1, because I was slower there than in the other rounds. The first round 1 is not used.
- Round 2 demo 1 and round 3 demo 2, because the sponges were on swapped sides.
- Round 2 demo 4, because the arm stood still for about 10 s.

## Merging into one dataset (2026-11-13)

Ten recordings into `jaaaa000/so101_part2`: round 1 again, rounds 2 to 8, then the three single demos. The first
round 1 is left out. Nothing is uploaded.

```bash
lerobot-edit-dataset \
  --new_repo_id jaaaa000/so101_part2 \
  --new_root /home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2 \
  --operation.type merge \
  --operation.repo_ids "['jaaaa000/so101_part2_redo_r1_20261113_111327', 'jaaaa000/so101_part2_r2_20261113_092030', 'jaaaa000/so101_part2_r3_20261113_093402', 'jaaaa000/so101_part2_r4_20261113_095319', 'jaaaa000/so101_part2_r5_20261113_100620', 'jaaaa000/so101_part2_r6_20261113_102009', 'jaaaa000/so101_part2_r7_20261113_103832', 'jaaaa000/so101_part2_r8_20261113_105144', 'jaaaa000/so101_part2_redo_s2_20261113_112653', 'jaaaa000/so101_part2_redo_s3_20261113_112924']" \
  --operation.roots "['/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2_redo_r1_20261113_111327', '/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2_r2_20261113_092030', '/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2_r3_20261113_093402', '/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2_r4_20261113_095319', '/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2_r5_20261113_100620', '/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2_r6_20261113_102009', '/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2_r7_20261113_103832', '/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2_r8_20261113_105144', '/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2_redo_s2_20261113_112653', '/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2_redo_s3_20261113_112924']" \
  --push_to_hub false
```

The merged dataset has 99 demos and 63,299 frames, numbered 0 to 98:

- The episode number is the demo number in `results/part2_demo_order.csv` minus 1.
- Three exceptions: demos 13, 16 and 26 are episodes 96, 97 and 98 (the three recorded again).
- Episodes 12, 15 and 25 are their first versions. They are left out of every training below.

That leaves 96 demos and 61,358 frames, 24 demos per sentence.

## Training (2026-11-13, started 12:25)

Five trainings ran one after the other on the RTX 3060, typed as one line joined with ` ; `. They are split up
here. All five use 46,000 steps (6 passes over the 96 demos at batch 8), batch 8 and a checkpoint at 23,000 and
46,000 steps.
- Training curves go to Weights & Biases. `--wandb.disable_artifact=true` keeps the checkpoints local.
- Nothing is pushed to the Hub.
- `--dataset.video_backend=pyav` is needed because the default video reader can't load FFmpeg on this machine.
- `--dataset.episodes` lists the demos each model trains on.

SmolVLA, fine-tuned from `lerobot/smolvla_base`, on all 96 demos.
- As in part 1: the vision-language backbone stays frozen, only the action expert is trained, and the rename map
  gives my two cameras the names the base model was pretrained with.
- New: `--policy.scheduler_decay_steps=46000`. By default the learning rate reaches its lowest value at step
  30,000, so without this the last 16,000 steps would teach almost nothing.

It took 5 h 04 min.

```bash
lerobot-train \
  --policy.path=lerobot/smolvla_base \
  --policy.push_to_hub=false \
  --policy.device=cuda \
  --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.side": "observation.images.camera3"}' \
  --dataset.repo_id=jaaaa000/so101_part2 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2 \
  --dataset.video_backend=pyav \
  --dataset.episodes="[0,1,2,3,4,5,6,7,8,9,10,11,13,14,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98]" \
  --steps=46000 \
  --policy.scheduler_decay_steps=46000 \
  --batch_size=8 \
  --save_freq=23000 \
  --output_dir=outputs/smolvla_part2 \
  --job_name=smolvla_part2 \
  --wandb.enable=true \
  --wandb.project=so101-project \
  --wandb.disable_artifact=true
```

ACT, from scratch, four models. Each one trains only on the 24 demos of its own sentence.

They took 3 h 50 min, 3 h 52 min, 3 h 47 min and 3 h 47 min, in the order of the sentences. The queue of five
ran from 12:25 on 13 November to 08:45 on 14 November.

Sentence 1, "Put the blue sponge in the left tray." (round 1 again and round 5):

```bash
lerobot-train \
  --policy.type=act \
  --dataset.repo_id=jaaaa000/so101_part2 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2 \
  --dataset.video_backend=pyav \
  --dataset.episodes="[0,1,2,3,4,5,6,7,8,9,10,11,48,49,50,51,52,53,54,55,56,57,58,59]" \
  --policy.device=cuda \
  --steps=46000 \
  --batch_size=8 \
  --save_freq=23000 \
  --output_dir=outputs/act_part2_s1 \
  --job_name=act_part2_s1 \
  --policy.push_to_hub=false \
  --wandb.enable=true \
  --wandb.project=so101-project \
  --wandb.disable_artifact=true
```

Sentence 2, "Put the blue sponge in the right tray." (rounds 2 and 6, with the two demos recorded again):

```bash
lerobot-train \
  --policy.type=act \
  --dataset.repo_id=jaaaa000/so101_part2 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2 \
  --dataset.video_backend=pyav \
  --dataset.episodes="[13,14,16,17,18,19,20,21,22,23,60,61,62,63,64,65,66,67,68,69,70,71,96,97]" \
  --policy.device=cuda \
  --steps=46000 \
  --batch_size=8 \
  --save_freq=23000 \
  --output_dir=outputs/act_part2_s2 \
  --job_name=act_part2_s2 \
  --policy.push_to_hub=false \
  --wandb.enable=true \
  --wandb.project=so101-project \
  --wandb.disable_artifact=true
```

Sentence 3, "Put the red sponge in the left tray." (rounds 3 and 7, with the one demo recorded again):

```bash
lerobot-train \
  --policy.type=act \
  --dataset.repo_id=jaaaa000/so101_part2 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2 \
  --dataset.video_backend=pyav \
  --dataset.episodes="[24,26,27,28,29,30,31,32,33,34,35,72,73,74,75,76,77,78,79,80,81,82,83,98]" \
  --policy.device=cuda \
  --steps=46000 \
  --batch_size=8 \
  --save_freq=23000 \
  --output_dir=outputs/act_part2_s3 \
  --job_name=act_part2_s3 \
  --policy.push_to_hub=false \
  --wandb.enable=true \
  --wandb.project=so101-project \
  --wandb.disable_artifact=true
```

Sentence 4, "Put the red sponge in the right tray." (rounds 4 and 8):

```bash
lerobot-train \
  --policy.type=act \
  --dataset.repo_id=jaaaa000/so101_part2 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2 \
  --dataset.video_backend=pyav \
  --dataset.episodes="[36,37,38,39,40,41,42,43,44,45,46,47,84,85,86,87,88,89,90,91,92,93,94,95]" \
  --policy.device=cuda \
  --steps=46000 \
  --batch_size=8 \
  --save_freq=23000 \
  --output_dir=outputs/act_part2_s4 \
  --job_name=act_part2_s4 \
  --policy.push_to_hub=false \
  --wandb.enable=true \
  --wandb.project=so101-project \
  --wandb.disable_artifact=true
```

## Training on fewer demos (2026-11-14, started 12:42)

Two more SmolVLA models for the fewer-demos test, typed as one line joined with ` ; `. Same command and the
same 46,000 steps as the SmolVLA model above. Only the demos, the output folder and the job name differ. The
demos are the `in_48` and `in_24` columns of `results/part2_demo_order.csv`, and the 24 are part of the 48.

48 demos (rounds 3 to 6). It took 4 h 43 min.

```bash
lerobot-train \
  --policy.path=lerobot/smolvla_base \
  --policy.push_to_hub=false \
  --policy.device=cuda \
  --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.side": "observation.images.camera3"}' \
  --dataset.repo_id=jaaaa000/so101_part2 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2 \
  --dataset.video_backend=pyav \
  --dataset.episodes="[24,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,98]" \
  --steps=46000 \
  --policy.scheduler_decay_steps=46000 \
  --batch_size=8 \
  --save_freq=23000 \
  --output_dir=outputs/smolvla_part2_48 \
  --job_name=smolvla_part2_48 \
  --wandb.enable=true \
  --wandb.project=so101-project \
  --wandb.disable_artifact=true
```

24 demos (rounds 3 to 6, three dot pairs). It took 4 h 43 min.

```bash
lerobot-train \
  --policy.path=lerobot/smolvla_base \
  --policy.push_to_hub=false \
  --policy.device=cuda \
  --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.side": "observation.images.camera3"}' \
  --dataset.repo_id=jaaaa000/so101_part2 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_part2 \
  --dataset.video_backend=pyav \
  --dataset.episodes="[28,29,30,31,34,36,38,40,42,43,45,48,49,52,56,57,58,60,64,65,69,70,71,98]" \
  --steps=46000 \
  --policy.scheduler_decay_steps=46000 \
  --batch_size=8 \
  --save_freq=23000 \
  --output_dir=outputs/smolvla_part2_24 \
  --job_name=smolvla_part2_24 \
  --wandb.enable=true \
  --wandb.project=so101-project \
  --wandb.disable_artifact=true
```

## Pilot tries (2026-11-14, not counted)

To see that every model runs on the robot and to choose SmolVLA's `execution_horizon`. Same rollout commands
as in the test below.
- ACT: one try per model.
- SmolVLA: one try each with `--inference.rtc.execution_horizon=` 10, 14, 15, 16, 17, 18, 19 and 20. I chose 15,
  for the reason in [protocol_part2.md](protocol_part2.md).

## Test (2026-11-15 and 2026-11-16)

Lamp light, curtains closed. One run per trial, 30 seconds (`--duration=30`). I type the outcome into
`scripts/eval_log_part2.py` in a second terminal, which shows each trial of the list.

ACT, one model per sentence. This is the command for sentence 1:

```bash
lerobot-rollout --strategy.type=base --policy.path=outputs/act_part2_s1/checkpoints/last/pretrained_model --policy.n_action_steps=1 --policy.temporal_ensemble_coeff=0.01 --robot.type=so101_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 --robot.id=my_awesome_follower_arm --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" --task="Put the blue sponge in the left tray." --duration=30
```

For the other sentences the folder in `--policy.path` and the sentence in `--task` change together:

| Sentence | Model |
|---|---|
| 1. `Put the blue sponge in the left tray.` | `outputs/act_part2_s1` |
| 2. `Put the blue sponge in the right tray.` | `outputs/act_part2_s2` |
| 3. `Put the red sponge in the left tray.` | `outputs/act_part2_s3` |
| 4. `Put the red sponge in the right tray.` | `outputs/act_part2_s4` |

SmolVLA, one model for all four sentences. Only `--task` changes:

```bash
lerobot-rollout --strategy.type=base --inference.type=rtc --inference.rtc.execution_horizon=15 --policy.path=outputs/smolvla_part2/checkpoints/last/pretrained_model --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.side": "observation.images.camera3"}' --robot.type=so101_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 --robot.id=my_awesome_follower_arm --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" --task="Put the blue sponge in the left tray." --duration=30
```

**Main test, 72 trials (2026-11-15):** the order is in `results/part2_trial_order.csv`.

```bash
python scripts/eval_log_part2.py results/part2_trial_order.csv results/part2_trials.csv
```

**Reworded sentences, 16 SmolVLA trials (2026-11-15):** the SmolVLA command above with one of these four
sentences in `--task`. The order is in `results/part2_reworded_order.csv`.

1. `Place the blue sponge into the tray on the left.`
2. `Place the blue sponge into the tray on the right.`
3. `Place the red sponge into the tray on the left.`
4. `Place the red sponge into the tray on the right.`

```bash
python scripts/eval_log_part2.py results/part2_reworded_order.csv results/part2_reworded_trials.csv
```

**Fewer demos, 60 SmolVLA trials (2026-11-16):** the SmolVLA command above with the model of that trial in
`--policy.path`: `outputs/smolvla_part2_24`, `outputs/smolvla_part2_48` or `outputs/smolvla_part2`. The order
is in `results/part2_fewer_demos_order.csv`.

```bash
python scripts/eval_log_part2.py results/part2_fewer_demos_order.csv results/part2_fewer_demos_trials.csv
```

## Analysis

This prints, per system, the trials, the successes, how often it went for the named sponge and to the named
tray, and the trials and successes per sentence and per placement.

```bash
python scripts/analyze_part2.py results/part2_trials.csv
python scripts/analyze_part2.py results/part2_reworded_trials.csv
python scripts/analyze_part2.py results/part2_fewer_demos_trials.csv
```
