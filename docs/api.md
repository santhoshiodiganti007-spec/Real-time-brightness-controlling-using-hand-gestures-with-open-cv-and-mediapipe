# Backend REST & WebSocket API Reference

The backend FastAPI server exposes local REST APIs and WebSocket endpoints. Interactive Swagger documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## REST Endpoints

### 1. Health & Diagnostics
- `GET /api/health`: Returns application status, OS platform, Python version, and mode.
- `GET /api/diagnostics`: Runs system diagnostics check (Python, OpenCV, MediaPipe, Camera, Brightness Controller, DB).

### 2. Brightness Control
- `GET /api/brightness`: Gets current screen brightness percentage.
- `POST /api/brightness`: Manually updates screen brightness.
  ```json
  {
    "brightness": 75.0
  }
  ```

### 3. Gesture & Calibration
- `GET /api/gesture/status`: Returns current gesture state, hand detection status, distance, and FPS.
- `POST /api/gesture/start`: Enables gesture control.
- `POST /api/gesture/stop`: Disables gesture control.
- `POST /api/calibration/start`: Initializes guided calibration workflow.
- `POST /api/calibration/record`: Captures current finger distance for `'min'` or `'max'` step.
- `POST /api/calibration/save`: Saves user calibration bounds.

### 4. Settings
- `GET /api/settings`: Retrieves active settings.
- `PUT /api/settings`: Updates smoothing factor, min/max brightness, gesture bounds, and sensitivity.

### 5. Statistics & History
- `GET /api/statistics`: Returns session duration, average FPS, total adjustment events, min/max/avg brightness.
- `GET /api/history`: Returns historical brightness event timeline.

### 6. Camera Stream
- `GET /api/camera/stream`: Returns live annotated MJPEG HTTP video stream.

---

## WebSocket Telemetry Stream

- **Endpoint:** `ws://127.0.0.1:8000/ws/brightness`
- **Frequency:** 20 Hz (every 50ms)
- **Payload Example:**
  ```json
  {
    "brightness": 72.5,
    "distance": 0.1432,
    "normalized_distance": 0.52,
    "hand_detected": true,
    "gesture_active": true,
    "gesture_state": "GESTURE_ACTIVE",
    "fps": 29.8,
    "is_demo_mode": false,
    "control_enabled": true
  }
  ```
