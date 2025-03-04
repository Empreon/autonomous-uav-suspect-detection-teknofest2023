# Autonomous UAV Suspect Detection - Teknofest 2023
Autonomous UAV suspect detection code for Teknofest 2023 - International Unmanned Aerial Vehicle Competition.

Multi-process system combining:
- YOLOv4 human detection (Python 3)
- Face recognition with Haar Cascades (Python 3)
- HSV color-space target identification (Python 3)
- MAVLink-based UAV control (Python 2)

**Core Innovation**: Cross-Python-version IPC using serialized pickle queues

## Technical Highlights
- Dual Python runtime coordination (2.7 ↔ 3.6+)
- Real-time object detection (YOLOv4 @ 8 FPS on RPi 4)
- Priority-based target confirmation system
- MAVLink command translation layer

## Dependency Matrix
| Component | Python Version | Key Packages |
|-----------|----------------|--------------|
| Flight Control | 2.7 | `dronekit==2.4.0`, `pymavlink==2.4.37` |
| Detection Stack | 3.8+ | `opencv-python==4.7.0.72`, `numpy>=1.24.3` |

## Setup Instructions
Python 2 Flight Environment
```
virtualenv -p python2 flight-env
source flight-env/bin/activate
pip install -r requirements/flight.txt
```

Python 3 Detection Environment
```
virtualenv -p python3.9 detection-env
source detection-env/bin/activate
pip install -r requirements/detection.txt
```

## Operational Workflow
1. Initialize flight controller with Python 2
2. Start detection pipeline with Python 3
