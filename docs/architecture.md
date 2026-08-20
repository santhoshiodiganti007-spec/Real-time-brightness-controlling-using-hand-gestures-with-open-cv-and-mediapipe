# System Architecture & Design Specification

## Overview

The **Touchless Brightness Control** system is designed using a decoupled modular architecture that separates computer vision frame processing, gesture signal math, OS hardware control, REST API endpoints, WebSocket broadcasting, data persistence, and UI presentation.

```text
               ┌─────────────────────────────────────────┐
               │              OpenCV Feed                │
               └────────────────────┬────────────────────┘
                                    │ BGR Frame
               ┌────────────────────▼────────────────────┐
               │    MediaPipe Hand Tasks Landmarker     │
               └────────────────────┬────────────────────┘
                                    │ 21 3D Landmarks
               ┌────────────────────▼────────────────────┐
               │        Gesture Distance Engine          │
               │  d = sqrt((x1-x2)^2 + (y1-y2)^2)        │
               └────────────────────┬────────────────────┘
                                    │ Normalized d in [0, 1]
               ┌────────────────────▼────────────────────┐
               │     Exponential Moving Average (EMA)    │
               │   S_t = alpha*Y_t + (1-alpha)*S_prev    │
               └────────────────────┬────────────────────┘
                                    │ Smoothed Brightness %
               ┌────────────────────▼────────────────────┐
               │  Brightness Hardware Controller (SBC)   │
               └────────────────────┬────────────────────┘
                                    │
               ┌────────────────────┼────────────────────┐
               │                    │                    │
     FastAPI WebSocket     SQLite Event Log     Physical Monitor
      (/ws/brightness)      (SQLAlchemy)         Hardware Display
               │                    │
               ▼                    ▼
        React Dashboard      Historical Charts
```

## Component Breakdowns

### 1. Camera Service (`camera_service.py`)
Thread-safe OpenCV video reader. Operates at ~30 FPS, generates MJPEG video streams for browser clients (`/api/camera/stream`), and incorporates synthetic frame generation for headless container environments.

### 2. Hand Tracking Service (`hand_tracking_service.py`)
MediaPipe Hand Landmarker integration. Extracts 21 normalized 3D keypoints per hand, locates landmark 4 (Thumb Tip) and landmark 8 (Index Tip), and renders visual overlays.

### 3. Gesture Processing Engine (`gesture_service.py`)
Calculates 2D Euclidean distance in normalized coordinate space, applies distance normalization $[0.03, 0.25] \rightarrow [0.0, 1.0]$, applies Exponential Moving Average ($\alpha = 0.2$) signal filtering, and manages state machine (`NO_HAND`, `HAND_DETECTED`, `GESTURE_ACTIVE`, `GESTURE_INVALID`, `CALIBRATING`, `PAUSED`).

### 4. Brightness Controller (`brightness_service.py`)
Encapsulates platform-specific OS display hardware APIs using `screen_brightness_control`. Applies strict safety clamping $[10\%, 100\%]$ and update thresholding ($\Delta \ge 2\%$). Falls back to simulated DEMO mode on unsupported platforms or cloud containers.

### 5. WebSocket Telemetry Broadcaster (`main.py`)
Pushes low-latency JSON telemetry payloads over `/ws/brightness` at 20 Hz to eliminate HTTP polling in the dashboard.

### 6. React Vite UI (`/frontend`)
Glassmorphic dashboard displaying annotated video stream, circular brightness meter, status cards, settings sliders, calibration wizard, and historical charts.
