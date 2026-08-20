# Technical Interview Questions & Answers

15 Technical Interview Questions and Responses for AI/Computer Vision & Software Engineering Roles.

---

### 1. Explain your project in 60 seconds.
**Answer:** I built *Touchless Brightness Control*, a real-time computer vision system that allows users to adjust physical screen brightness using hand gestures. Using MediaPipe Tasks Vision and OpenCV, it tracks 21 3D hand landmarks, measures the 2D Euclidean distance between the thumb and index finger tip, normalizes that distance through personalized calibration, applies Exponential Moving Average (EMA) noise reduction to prevent screen flickering, and updates OS display hardware via native APIs. It features a FastAPI backend, real-time WebSocket broadcasting, SQLite event logging, and a React Vite dashboard.

---

### 2. Why did you choose MediaPipe over traditional OpenCV contour detection?
**Answer:** Traditional contour detection relies heavily on skin-color thresholding, background subtraction, and convex hull calculations, which fail under varying lighting conditions, complex backgrounds, or skin tone variations. MediaPipe uses deep learning trained on diverse hand datasets, providing robust 3D keypoint inference at 30+ FPS directly on CPU.

---

### 3. How do you map gesture distance to screen brightness?
**Answer:** We calculate the Euclidean distance $d$ between landmark 4 and landmark 8. We normalize $d$ between calibrated minimum $d_{\min}$ and maximum $d_{\max}$ bounds to derive normalized value $N \in [0.0, 1.0]$. Target brightness is computed as $B_{\text{target}} = B_{\min} + N \cdot (B_{\max} - B_{\min})$ and clamped to safe operating bounds $[10\%, 100\%]$.

---

### 4. How do you handle noise and prevent rapid screen flickering?
**Answer:** We employ a 2-tier noise reduction strategy:
1. **Exponential Moving Average (EMA):** $S_t = \alpha Y_t + (1-\alpha) S_{t-1}$ with $\alpha = 0.2$.
2. **Update Thresholding:** Display hardware brightness is only modified if $|S_t - S_{\text{previous}}| \ge 2\%$.

---

### 5. Why can't a cloud-hosted web application directly modify physical screen brightness?
**Answer:** Physical display brightness control requires hardware access via local OS kernel buses, WMI, or DDC/CI I2C protocols. Browsers executing web applications inside sandboxes on cloud servers do not possess physical bus access to a client workstation's monitor hardware.

---

### 6. How do you handle hand size differences between users?
**Answer:** We implemented an adaptive guided calibration workflow. Users record their personal pinched minimum distance $d_{\min}$ and spread maximum distance $d_{\max}$, which scales the normalization formula for their specific hand geometry.

---

### 7. What happens if no webcam hardware is attached?
**Answer:** The camera service catches capture initialization exceptions and automatically activates a synthetic animated video feed, allowing full dashboard, API, and simulated gesture testing without crashing.

---

### 8. How is real-time performance optimized for high FPS?
**Answer:**
- Frame processing executes in a dedicated background daemon thread.
- Thread-safe memory sharing avoids blocking the FastAPI event loop.
- MediaPipe Landmarker runs in video stream mode for temporal tracking continuity.
- WebSocket pushes binary/JSON frames at 20 Hz, eliminating HTTP polling overhead.

---

### 9. How would you extend this project to volume or media control?
**Answer:** By introducing multi-gesture state classification:
- **Pinch (Thumb + Index):** Screen Brightness.
- **Pinch (Thumb + Middle):** Audio System Volume.
- **Swipe Right / Left:** Media Track Next / Previous.

---

### 10. How would you support multi-monitor setups?
**Answer:** `screen_brightness_control` supports enumerating display monitors (`sbc.list_monitors()`). We would update `brightness_service` to accept a `monitor_index` parameter to route brightness calls to specific display devices.

---

### 11. How do you ensure database integrity during high-frequency gesture updates?
**Answer:** Brightness event persistence into SQLite is decoupled from the 30 FPS vision loop. Database writes only trigger when a hardware brightness change occurs ($\Delta \ge 2\%$), preventing database lock contention.

---

### 12. How do you handle edge cases like rapid hand movements or partial hand occlusion?
**Answer:** MediaPipe returns tracking confidence scores. If tracking confidence falls below threshold ($0.7$), state transitions to `NO_HAND` or `GESTURE_INVALID`, maintaining the last valid brightness level until tracking recovers.

---

### 13. What is the role of Docker in this application?
**Answer:** Docker containerizes the FastAPI backend and web dashboard for cloud monitoring, statistics, and demonstration environments, running in **DEMO MODE**.

---

### 14. What limitations exist in the current implementation?
**Answer:** Extremely dark ambient lighting degrades camera frame contrast, external HDMI monitors lacking DDC/CI support cannot be controlled via software, and single-hand tracking limits concurrent multi-parameter adjustments.

---

### 15. How would you deploy this on edge AI hardware like Raspberry Pi or Jetson Nano?
**Answer:** Convert MediaPipe tasks to ONNX or TensorRT models, compile OpenCV with CUDA hardware acceleration, and run the backend as a lightweight systemd Linux service.
