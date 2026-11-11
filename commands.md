# Commands

Every command run for this project, in order, copy-pasteable. Machine: Linux, RTX 3060 12 GB,
conda env `lerobot` (LeRobot 0.6.0).

## Phase 0: repo (2026-11-08)

```bash
mkdir -p ~/so101-project/{scripts,results/figures,media} && cd ~/so101-project && git init -b main
```

## Phase 1: camera settings (run at the start of every session)

Keeps both C270 webcams at a steady 30 fps in dim light and sets their flicker filter to 50 Hz mains. Run again after a
replug or reboot. The two webcams report the same serial number, so they are named by USB port: keep each in its port.

Top camera (USB port 9):

```bash
v4l2-ctl -d /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0 -c exposure_dynamic_framerate=0,power_line_frequency=1
```

Side camera (USB port 10):

```bash
v4l2-ctl -d /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0 -c exposure_dynamic_framerate=0,power_line_frequency=1
```

## Phase 3: record the demos (2026-11-09)

Round 1: 9 demos, dots 1 to 9, aligned. LeRobot adds the date and time to the dataset name.

```bash
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 \
  --robot.id=my_awesome_follower_arm \
  --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" \
  --teleop.type=so101_leader \
  --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B009251-if00 \
  --teleop.id=my_awesome_leader_arm \
  --dataset.repo_id=jaaaa000/so101_blue_sponge \
  --dataset.single_task="Pick up the blue sponge and put it in the white tray." \
  --dataset.num_episodes=9 \
  --dataset.episode_time_s=30 \
  --dataset.reset_time_s=20 \
  --dataset.fps=30 \
  --dataset.push_to_hub=false \
  --display_data=false
```

Rounds 2 to 6: adds 9 demos to the same dataset each time. Round 2 is 45°, then aligned, 45°, aligned, 45°.

```bash
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 \
  --robot.id=my_awesome_follower_arm \
  --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" \
  --teleop.type=so101_leader \
  --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B009251-if00 \
  --teleop.id=my_awesome_leader_arm \
  --dataset.repo_id=jaaaa000/so101_blue_sponge_20261109_161302 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_blue_sponge_20261109_161302 \
  --dataset.single_task="Pick up the blue sponge and put it in the white tray." \
  --dataset.num_episodes=9 \
  --dataset.episode_time_s=30 \
  --dataset.reset_time_s=20 \
  --dataset.fps=30 \
  --dataset.push_to_hub=false \
  --display_data=false \
  --resume=true
```

The first recording (54 demos, daylight) became the pilot. Its ACT model scored 2 of 6 in uncounted tries under the lamp.

## Phase 3b: second recording, under the lamp (2026-11-09 evening)

Same rig, one fixed lamp light, slower demos, each demo ends right after the release. Going home happens in
the unrecorded reset, so the reset time is 30 s.

Round 1: 9 demos, dots 1 to 9, aligned.

```bash
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 \
  --robot.id=my_awesome_follower_arm \
  --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" \
  --teleop.type=so101_leader \
  --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B009251-if00 \
  --teleop.id=my_awesome_leader_arm \
  --dataset.repo_id=jaaaa000/so101_blue_sponge_v2 \
  --dataset.single_task="Pick up the blue sponge and put it in the white tray." \
  --dataset.num_episodes=9 \
  --dataset.episode_time_s=30 \
  --dataset.reset_time_s=30 \
  --dataset.fps=30 \
  --dataset.push_to_hub=false \
  --display_data=false
```

Rounds 2 to 6: adds 9 demos each time. Round 2 is 45°, then aligned, 45°, aligned, 45°.

```bash
lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 \
  --robot.id=my_awesome_follower_arm \
  --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" \
  --teleop.type=so101_leader \
  --teleop.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B009251-if00 \
  --teleop.id=my_awesome_leader_arm \
  --dataset.repo_id=jaaaa000/so101_blue_sponge_v2_20261109_212801 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_blue_sponge_v2_20261109_212801 \
  --dataset.single_task="Pick up the blue sponge and put it in the white tray." \
  --dataset.num_episodes=9 \
  --dataset.episode_time_s=30 \
  --dataset.reset_time_s=30 \
  --dataset.fps=30 \
  --dataset.push_to_hub=false \
  --display_data=false \
  --resume=true
```

Episode 5 closes the gripper again after the release and hit the 30 s limit, so it is left out of training:
53 demos.

## Phase 4: trial order and training (2026-11-09 evening and night)

Fixed trial order for the test (seed 42, blocks of 3), committed before training:

```bash
python scripts/make_trial_order.py
```

The three trainings ran one after the other on the RTX 3060, typed as one line joined with ` ; `. They are split
up here. All three use 30,000 steps, batch 8 and a checkpoint every 10,000 steps.
- Training curves go to Weights & Biases. `--wandb.disable_artifact=true` keeps the checkpoints local.
- Nothing is pushed to the Hub.
- `--dataset.video_backend=pyav` is needed because the default video reader can't load FFmpeg on this machine.

ACT, from scratch, second recording (2 h 27 min):

```bash
lerobot-train \
  --policy.type=act \
  --dataset.repo_id=jaaaa000/so101_blue_sponge_v2_20261109_212801 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_blue_sponge_v2_20261109_212801 \
  --dataset.video_backend=pyav \
  --dataset.episodes="[0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53]" \
  --policy.device=cuda \
  --steps=30000 \
  --batch_size=8 \
  --save_freq=10000 \
  --output_dir=outputs/act_blue_sponge_v2 \
  --job_name=act_blue_sponge_v2 \
  --policy.push_to_hub=false \
  --wandb.enable=true \
  --wandb.project=so101-project \
  --wandb.disable_artifact=true
```

SmolVLA, fine-tuned from `lerobot/smolvla_base`, second recording (3 h 04 min).
- The vision-language backbone stays frozen, and only the action expert is trained. These are the base model's
  defaults.
- The rename map gives my two cameras the names the base model was pretrained with.

```bash
lerobot-train \
  --policy.path=lerobot/smolvla_base \
  --policy.push_to_hub=false \
  --policy.device=cuda \
  --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.side": "observation.images.camera3"}' \
  --dataset.repo_id=jaaaa000/so101_blue_sponge_v2_20261109_212801 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_blue_sponge_v2_20261109_212801 \
  --dataset.video_backend=pyav \
  --dataset.episodes="[0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53]" \
  --steps=30000 \
  --batch_size=8 \
  --save_freq=10000 \
  --output_dir=outputs/smolvla_blue_sponge_v2 \
  --job_name=smolvla_blue_sponge_v2 \
  --wandb.enable=true \
  --wandb.project=so101-project \
  --wandb.disable_artifact=true
```

SmolVLA on the first recording, for the extra test only (3 h 04 min). Episodes 9 and 12 are left out because
their wrist turned the other way from the other demos at the same dot.

```bash
lerobot-train \
  --policy.path=lerobot/smolvla_base \
  --policy.push_to_hub=false \
  --policy.device=cuda \
  --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.side": "observation.images.camera3"}' \
  --dataset.repo_id=jaaaa000/so101_blue_sponge_20261109_161302 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_blue_sponge_20261109_161302 \
  --dataset.video_backend=pyav \
  --dataset.episodes="[0,1,2,3,4,5,6,7,8,10,11,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53]" \
  --steps=30000 \
  --batch_size=8 \
  --save_freq=10000 \
  --output_dir=outputs/smolvla_blue_sponge \
  --job_name=smolvla_blue_sponge \
  --wandb.enable=true \
  --wandb.project=so101-project \
  --wandb.disable_artifact=true
```

## Test (2026-11-10)

Run from ~/so101-project. One run per trial; type the outcome into scripts/eval_log.py in a second terminal.

ACT:

```bash
lerobot-rollout --strategy.type=base --policy.path=outputs/act_blue_sponge_v2/checkpoints/last/pretrained_model --policy.n_action_steps=1 --policy.temporal_ensemble_coeff=0.01 --robot.type=so101_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 --robot.id=my_awesome_follower_arm --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" --task="Pick up the blue sponge and put it in the white tray." --duration=30
```

SmolVLA:

```bash
lerobot-rollout --strategy.type=base --inference.type=rtc --policy.path=outputs/smolvla_blue_sponge_v2/checkpoints/last/pretrained_model --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.side": "observation.images.camera3"}' --robot.type=so101_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 --robot.id=my_awesome_follower_arm --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" --task="Pick up the blue sponge and put it in the white tray." --duration=30
```

Logging the test results, in the second terminal:

```bash
python scripts/eval_log.py results/trial_order.csv results/trials.csv
```

## Extra tests (2026-11-10 afternoon)

Same rollout commands as the test above, same lamp light.

**Yellow sponge, 8 trials:** the yellow sponge replaces the blue one. The ACT and SmolVLA commands and the task
sentence are unchanged. The order is in `results/yellow_order.csv`.

```bash
python scripts/eval_log.py results/yellow_order.csv results/yellow_trials.csv
```

**Yellow sponge with "yellow" in the sentence, 4 SmolVLA trials:**

```bash
lerobot-rollout --strategy.type=base --inference.type=rtc --policy.path=outputs/smolvla_blue_sponge_v2/checkpoints/last/pretrained_model --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.side": "observation.images.camera3"}' --robot.type=so101_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 --robot.id=my_awesome_follower_arm --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" --task="Pick up the yellow sponge and put it in the white tray." --duration=30
```

```bash
python scripts/eval_log.py results/yellow_sentence_order.csv results/yellow_sentence_trials.csv
```

**SmolVLA trained on the first recording, 18 trials** (blue sponge, the test's placements):

```bash
lerobot-rollout --strategy.type=base --inference.type=rtc --policy.path=outputs/smolvla_blue_sponge/checkpoints/last/pretrained_model --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.side": "observation.images.camera3"}' --robot.type=so101_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 --robot.id=my_awesome_follower_arm --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" --task="Pick up the blue sponge and put it in the white tray." --duration=30
```

```bash
python scripts/eval_log.py results/smolvla_v1_order.csv results/smolvla_v1_trials.csv
```

## Analysis

This prints the success rate and margin per model. When the file has two models, it also prints the gap and the
verdict.

```bash
python scripts/analyze.py results/trials.csv
python scripts/analyze.py results/yellow_trials.csv
python scripts/analyze.py results/yellow_sentence_trials.csv
python scripts/analyze.py results/smolvla_v1_trials.csv
```

## Follow-up: 18 demos (training 2026-11-10 night, test 2026-11-11)

Both models are trained again on episodes 18–35 of the second recording only: rounds 3 (aligned) and 4 (45°), 18 demos
and 13,811 frames. Everything else is the same as the test models. The protocol section "Follow-up: 18 demos" was
committed before training.

The two trainings ran one after the other, typed as one line joined with ` ; `. These are the exact arguments, taken
from each run's wandb metadata.

ACT, from scratch (2 h 28 min):

```bash
lerobot-train \
  --policy.type=act \
  --dataset.repo_id=jaaaa000/so101_blue_sponge_v2_20261109_212801 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_blue_sponge_v2_20261109_212801 \
  --dataset.video_backend=pyav \
  --dataset.episodes="[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]" \
  --policy.device=cuda \
  --steps=30000 \
  --batch_size=8 \
  --save_freq=10000 \
  --output_dir=outputs/act_18demos \
  --job_name=act_18demos \
  --policy.push_to_hub=false \
  --wandb.enable=true \
  --wandb.project=so101-project \
  --wandb.disable_artifact=true
```

SmolVLA, fine-tuned from `lerobot/smolvla_base` (3 h 05 min):

```bash
lerobot-train \
  --policy.path=lerobot/smolvla_base \
  --policy.push_to_hub=false \
  --policy.device=cuda \
  --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.side": "observation.images.camera3"}' \
  --dataset.repo_id=jaaaa000/so101_blue_sponge_v2_20261109_212801 \
  --dataset.root=/home/user/.cache/huggingface/lerobot/jaaaa000/so101_blue_sponge_v2_20261109_212801 \
  --dataset.video_backend=pyav \
  --dataset.episodes="[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]" \
  --steps=30000 \
  --batch_size=8 \
  --save_freq=10000 \
  --output_dir=outputs/smolvla_18demos \
  --job_name=smolvla_18demos \
  --wandb.enable=true \
  --wandb.project=so101-project \
  --wandb.disable_artifact=true
```

Setup control (2026-11-11 morning, before the 18-demo test): the two 53-demo models of the main test on trials 1–18 of
the main order, 9 per model, because the cameras had moved a few pixels and the GPU driver was updated. Written in
`protocol.md` before the first control trial.

The order file, the header plus the first 18 trials:

```bash
head -19 results/trial_order.csv > results/control53_order.csv
```

Logging, in the second terminal:

```bash
python scripts/eval_log.py results/control53_order.csv results/control53_trials.csv
```

ACT, 53 demos (the same command as in the main test):

```bash
lerobot-rollout --strategy.type=base --policy.path=outputs/act_blue_sponge_v2/checkpoints/last/pretrained_model --policy.n_action_steps=1 --policy.temporal_ensemble_coeff=0.01 --robot.type=so101_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 --robot.id=my_awesome_follower_arm --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" --task="Pick up the blue sponge and put it in the white tray." --duration=30
```

SmolVLA, 53 demos (the same command as in the main test):

```bash
lerobot-rollout --strategy.type=base --inference.type=rtc --policy.path=outputs/smolvla_blue_sponge_v2/checkpoints/last/pretrained_model --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.side": "observation.images.camera3"}' --robot.type=so101_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 --robot.id=my_awesome_follower_arm --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" --task="Pick up the blue sponge and put it in the white tray." --duration=30
```

Analysis:

```bash
python scripts/analyze.py results/control53_trials.csv
```

Test: the same 36 trials in the same order, light and settings as the main test. Only the checkpoint path changes.

ACT:

```bash
lerobot-rollout --strategy.type=base --policy.path=outputs/act_18demos/checkpoints/last/pretrained_model --policy.n_action_steps=1 --policy.temporal_ensemble_coeff=0.01 --robot.type=so101_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 --robot.id=my_awesome_follower_arm --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" --task="Pick up the blue sponge and put it in the white tray." --duration=30
```

SmolVLA:

```bash
lerobot-rollout --strategy.type=base --inference.type=rtc --policy.path=outputs/smolvla_18demos/checkpoints/last/pretrained_model --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.side": "observation.images.camera3"}' --robot.type=so101_follower --robot.port=/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B7B015577-if00 --robot.id=my_awesome_follower_arm --robot.cameras="{top: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:9:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}, side: {type: opencv, index_or_path: /dev/v4l/by-path/pci-0000:00:14.0-usb-0:10:1.0-video-index0, width: 640, height: 480, fps: 30, fourcc: MJPG}}" --task="Pick up the blue sponge and put it in the white tray." --duration=30
```

Logging and analysis:

```bash
python scripts/eval_log.py results/trial_order.csv results/demos18_trials.csv
```

```bash
python scripts/analyze.py results/demos18_trials.csv
```

Only if the gap is 4 or 5 (the protocol's rule): 18 more trials per model in the same order. Then join both files,
keeping one header, and give the verdict on all 36 trials per model.

```bash
python scripts/eval_log.py results/trial_order.csv results/demos18_more_trials.csv
```

```bash
{ cat results/demos18_trials.csv; tail -n +2 results/demos18_more_trials.csv; } > results/demos18_all_trials.csv
```

```bash
python scripts/analyze.py results/demos18_all_trials.csv
```
