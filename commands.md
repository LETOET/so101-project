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
