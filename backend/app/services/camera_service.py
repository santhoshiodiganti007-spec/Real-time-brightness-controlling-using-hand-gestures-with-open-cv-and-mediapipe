"""
OpenCV Camera Service & Video Stream Generator.
Handles camera initialization, frame processing thread, MJPEG streaming, and simulated synthetic feed fallback.
"""
import cv2
import time
import math
import asyncio
import threading
import numpy as np
from typing import Generator, Optional, Dict, Any, Tuple
from app.core.config import settings
from app.core.logging_config import logger
from app.services.hand_tracking_service import hand_tracking_service
from app.services.gesture_service import gesture_service
from app.services.statistics_service import statistics_service
from app.services.brightness_service import brightness_service

class CameraService:
    def __init__(self):
        self.camera_index = settings.CAMERA_INDEX
        self.width = settings.CAMERA_WIDTH
        self.height = settings.CAMERA_HEIGHT
        
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.use_simulated_feed = False

        self.latest_frame: Optional[np.ndarray] = None
        self.latest_state: Dict[str, Any] = {
            "hand_detected": False,
            "num_hands": 0,
            "gesture_state": "NO_HAND",
            "distance": None,
            "normalized_distance": None,
            "calculated_brightness": 50.0,
            "smoothed_brightness": 50.0,
            "fps": 0.0
        }

        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        # Callbacks for WebSocket broadcasting
        self.websocket_callbacks = []

    def register_ws_callback(self, callback):
        if callback not in self.websocket_callbacks:
            self.websocket_callbacks.append(callback)

    def unregister_ws_callback(self, callback):
        if callback in self.websocket_callbacks:
            self.websocket_callbacks.remove(callback)

    def start_camera(self, camera_index: int = None) -> bool:
        if camera_index is not None:
            self.camera_index = camera_index

        with self._lock:
            if self.is_running:
                return True

            logger.info(f"Attempting to start camera (Index: {self.camera_index})...")
            try:
                self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW if cv2.os.name == 'nt' else cv2.CAP_ANY)
                if not self.cap.isOpened():
                    # Fallback to standard index 0
                    self.cap = cv2.VideoCapture(0)

                if self.cap.isOpened():
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                    self.use_simulated_feed = False
                    logger.info("Webcam hardware initialized successfully.")
                else:
                    logger.warning("No physical webcam hardware detected. Enabling synthetic video feed.")
                    self.use_simulated_feed = True
            except Exception as e:
                logger.error(f"Camera open error ({e}). Enabling synthetic video feed.")
                self.use_simulated_feed = True

            self.is_running = True
            self._thread = threading.Thread(target=self._capture_loop, daemon=True)
            self._thread.start()
            return True

    def stop_camera(self):
        with self._lock:
            self.is_running = False
            if self.cap is not None:
                try:
                    self.cap.release()
                except Exception as e:
                    logger.error(f"Error releasing camera: {e}")
                self.cap = None
            logger.info("Camera service stopped.")

    def _generate_synthetic_frame(self, frame_count: int) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Generates a synthetic camera frame with animated gesture visualization
        for headless/Docker/demo mode when physical webcam is not attached.
        """
        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Dark tech background grid
        img[:] = (20, 24, 33)
        cv2.putText(img, "DEMO / SYNTHETIC CAMERA FEED", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 200), 2)

        # Sine wave animated finger distance simulation
        t = frame_count * 0.05
        sim_dist = 0.03 + 0.22 * (0.5 + 0.5 * math.sin(t))

        # Coordinates
        center_x, center_y = self.width // 2, self.height // 2
        pixel_span = int(sim_dist * 800)

        t_x, t_y = center_x - pixel_span // 2, center_y
        i_x, i_y = center_x + pixel_span // 2, center_y

        # Draw hand visualization
        cv2.circle(img, (t_x, t_y), 12, (255, 0, 128), -1)  # Thumb
        cv2.circle(img, (t_x, t_y), 15, (255, 255, 255), 2)
        cv2.putText(img, "Thumb", (t_x - 30, t_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.circle(img, (i_x, i_y), 12, (0, 255, 255), -1)  # Index
        cv2.circle(img, (i_x, i_y), 15, (255, 255, 255), 2)
        cv2.putText(img, "Index", (i_x - 15, i_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.line(img, (t_x, t_y), (i_x, i_y), (0, 255, 0), 3)

        tracking_data = {
            "hand_detected": True,
            "num_hands": 1,
            "thumb_tip": (t_x, t_y),
            "index_tip": (i_x, i_y),
            "wrist": (center_x, center_y + 120),
            "distance": sim_dist,
            "is_open_hand": False
        }
        return img, tracking_data

    def _capture_loop(self):
        synthetic_frame_count = 0
        while self.is_running:
            start_t = time.time()

            if not self.use_simulated_feed and self.cap is not None and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    logger.warning("Failed to read frame from webcam. Switching to synthetic feed.")
                    self.use_simulated_feed = True
                    continue
                # Horizontal flip for intuitive mirror interaction
                frame = cv2.flip(frame, 1)
                processed_frame, tracking_result = hand_tracking_service.process_frame(frame)
            else:
                synthetic_frame_count += 1
                processed_frame, tracking_result = self._generate_synthetic_frame(synthetic_frame_count)

            # Process gesture & calculate brightness
            gesture_output = gesture_service.process_gesture(tracking_result)

            # Calculate FPS
            current_fps = statistics_service.update_fps()
            
            # Log metrics
            statistics_service.log_gesture_frame(
                hand_detected=tracking_result.get("hand_detected", False),
                brightness=gesture_output.get("smoothed_brightness"),
                gesture_distance=gesture_output.get("distance")
            )

            if gesture_output.get("hardware_updated", False):
                statistics_service.log_brightness_event(
                    brightness=gesture_output.get("smoothed_brightness"),
                    distance=gesture_output.get("distance")
                )

            # Draw HUD overlays on frame
            h, w, _ = processed_frame.shape
            b_val = gesture_output.get("smoothed_brightness") or brightness_service.get_brightness()
            state_val = gesture_output.get("state", "NO_HAND")

            # Status banner
            cv2.rectangle(processed_frame, (0, 0), (w, 50), (15, 18, 26), -1)
            cv2.putText(
                processed_frame,
                f"State: {state_val} | Dist: {gesture_output.get('distance', 0.0) or 0.0:.3f} | Brightness: {int(b_val)}% | FPS: {current_fps:.1f}",
                (15, 32),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 200) if state_val == "GESTURE_ACTIVE" else (200, 200, 200),
                2
            )

            # Visual Brightness Bar gauge on right edge of video
            bar_top, bar_bottom = 70, h - 30
            bar_height = bar_bottom - bar_top
            fill_height = int((b_val / 100.0) * bar_height)
            
            cv2.rectangle(processed_frame, (w - 35, bar_top), (w - 15, bar_bottom), (50, 50, 50), -1)
            cv2.rectangle(processed_frame, (w - 35, bar_bottom - fill_height), (w - 15, bar_bottom), (0, 255, 128), -1)
            cv2.rectangle(processed_frame, (w - 35, bar_top), (w - 15, bar_bottom), (255, 255, 255), 2)

            self.latest_frame = processed_frame
            self.latest_state = {
                "hand_detected": tracking_result.get("hand_detected", False),
                "num_hands": tracking_result.get("num_hands", 0),
                "gesture_state": state_val,
                "distance": gesture_output.get("distance"),
                "normalized_distance": gesture_output.get("normalized_distance"),
                "calculated_brightness": gesture_output.get("target_brightness"),
                "smoothed_brightness": b_val,
                "control_enabled": gesture_service.control_enabled,
                "is_demo_mode": brightness_service.is_demo_mode() or self.use_simulated_feed,
                "fps": round(current_fps, 1)
            }

            # Sleep to maintain ~30 FPS loop
            elapsed = time.time() - start_t
            delay = max(0.001, (1.0 / settings.CAMERA_FPS) - elapsed)
            time.sleep(delay)

    def get_mjpeg_stream(self) -> Generator[bytes, None, None]:
        """Yields multipart/x-mixed-replace MJPEG frame stream for HTTP endpoints."""
        while True:
            if self.latest_frame is not None:
                ret, jpeg = cv2.imencode('.jpg', self.latest_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            time.sleep(0.03)

camera_service = CameraService()
