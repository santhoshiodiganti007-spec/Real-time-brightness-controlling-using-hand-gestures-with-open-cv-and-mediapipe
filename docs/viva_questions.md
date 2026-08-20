# Comprehensive Viva Project Examination Guide

30+ Viva Questions & Detailed Technical Answers for Academic Defense & Presentations.

---

## 1. Computer Vision & MediaPipe

### Q1. What is MediaPipe and how does hand tracking work?
**Answer:** MediaPipe is a cross-platform open-source ML framework developed by Google. Hand tracking uses a 2-stage pipeline: (1) a Palm Detection model that locates hand bounding boxes in the full image frame, and (2) a Hand Landmark model that predicts 21 3D keypoints per hand within the cropped region.

### Q2. Which hand landmarks are used for brightness control?
**Answer:** Landmark #4 (Thumb Tip) and Landmark #8 (Index Finger Tip).

### Q3. How is the gesture distance calculated?
**Answer:** Using the 2D Euclidean distance formula:
$$d = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$$
where $(x_1, y_1)$ and $(x_2, y_2)$ are normalized coordinate pairs in image plane space $[0.0, 1.0]$.

### Q4. Why do we normalize gesture distance instead of using raw pixel distance?
**Answer:** Pixel distance varies depending on camera resolution and distance of the user's hand from the camera lens. Normalized coordinates ($x \in [0,1], y \in [0,1]$) provide scale-invariant distance representation.

### Q5. How does MediaPipe perform landmark inference in real time?
**Answer:** It employs lightweight MobileNet/SqueezeNet-style convolutional neural networks optimized for CPU/GPU inference with TFLite.

---

## 2. Signal Processing & Noise Reduction

### Q6. Why is smoothing necessary for hand gesture control?
**Answer:** Natural physiological hand tremor, micro-jitter, and camera sensor noise cause rapid fluctuations in raw distance metrics. Without smoothing, display brightness would flicker rapidly.

### Q7. What mathematical formula is used for smoothing?
**Answer:** Exponential Moving Average (EMA):
$$S_t = \alpha \cdot Y_t + (1 - \alpha) \cdot S_{t-1}$$
where $\alpha = 0.2$ is the smoothing weight factor, $Y_t$ is current calculated target brightness, and $S_{t-1}$ is previous smoothed output.

### Q8. What is the update threshold?
**Answer:** A safety deadband threshold ($\Delta \ge 2\%$). System screen brightness is only updated when the difference between new target brightness and current brightness exceeds $2\%$, reducing unnecessary OS hardware calls.

---

## 3. System Architecture & Backend

### Q9. Why separate the local Python service from the UI dashboard?
**Answer:** Separation of concerns. The computer vision engine and OS hardware controller run as a local background process, ensuring physical brightness control continues reliably even if the web dashboard is closed or reloaded.

### Q10. Why use FastAPI instead of Flask or Django?
**Answer:** FastAPI offers high asynchronous performance with Starlette/Pydantic, automatic OpenAPI specification generation (`/docs`), type validation, and built-in WebSocket support.

### Q11. Why use WebSockets instead of REST API polling?
**Answer:** REST polling introduces HTTP overhead and latency. WebSockets establish a single persistent full-duplex TCP connection streaming 20 Hz telemetry updates with sub-10ms latency.

### Q12. What database is used and what is stored?
**Answer:** SQLite with SQLAlchemy ORM storing session statistics (`sessions`), historical brightness events (`brightness_events`), and user settings (`user_settings`).

---

## 4. Hardware & Operating System Integration

### Q13. How does Python modify physical monitor brightness?
**Answer:** Via `screen-brightness-control`, which communicates with Windows WMI/VCP (Virtual Control Panel) / DDC/CI monitor protocols, Linux `/sys/class/backlight`, or macOS IOKit APIs.

### Q14. What happens if physical brightness control fails or is unsupported?
**Answer:** The system catches the hardware exception and gracefully transitions into DEMO MODE, simulating brightness adjustments without crashing the application.

---

## 5. Additional Viva Questions (15-30)

### Q15. Is MediaPipe supervised learning?
**Answer:** Yes, MediaPipe's underlying deep networks were trained on thousands of annotated hand images using supervised learning.

### Q16. How does the open-hand pause gesture work?
**Answer:** It checks if the Y coordinates of all four finger tips (index, middle, ring, pinky) are above their respective PIP joints, indicating extended fingers, which pauses gesture brightness adjustment.

### Q17. How is personal hand calibration implemented?
**Answer:** The user records minimum pinch distance $d_{\min}$ and maximum spread distance $d_{\max}$. Normalized distance is computed as $\frac{d - d_{\min}}{d_{\max} - d_{\min}}$.

### Q18. How is screen blackout prevented?
**Answer:** Strict brightness safety bounds ($10\%$ floor, $100\%$ ceiling) clamp values before calling OS hardware APIs.

### Q19. Why can't cloud server Docker containers modify local screen brightness directly?
**Answer:** Cloud servers do not have physical bus access (WMI/DDC/CI) to the remote user's display monitor.

### Q20. How is multi-hand detection handled?
**Answer:** The system isolates the primary (first detected) hand, while displaying total count of hands detected.

### Q21. How is thread safety maintained between OpenCV capture and FastAPI?
**Answer:** Python `threading.Lock` protects shared memory state (`latest_frame` and `latest_state`).

### Q22. How is FPS computed?
**Answer:** Moving frame accumulator: $FPS = \frac{\text{Frames Processed}}{\Delta t}$ calculated over 1.0 second intervals.

### Q23. What is PyInstaller used for?
**Answer:** Freezes Python application code, MediaPipe models, and dependencies into a standalone Windows executable (`.exe`).

### Q24. How are CORS errors handled?
**Answer:** FastAPI `CORSMiddleware` allows cross-origin requests from the React Vite frontend.

### Q25. What is the role of Pydantic schemas?
**Answer:** Enforces strict data type validation and JSON serialization for API request and response bodies.

### Q26. How is webcam privacy protected?
**Answer:** All image frames are processed in-memory locally and are never stored or transmitted externally.

### Q27. What is the purpose of GitHub Actions CI?
**Answer:** Automatically executes unit tests (`pytest`) and frontend Vite builds on every push to verify codebase health.

### Q28. How does the system handle poor lighting?
**Answer:** MediaPipe hand detection operates across varied contrast conditions, but confidence settings can be adjusted in Settings.

### Q29. What happens if the camera disconnects?
**Answer:** The capture loop catches frame read failures and automatically transitions to a synthetic animated video feed fallback.

### Q30. What are future extensions of this project?
**Answer:** Multi-monitor support, volume control pinching, smart home IoT integration, and edge AI deployment.
