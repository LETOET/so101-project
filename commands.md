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