"""
Gesture Processing Service.
Handles state machine, distance normalization, smoothing, thresholding, and brightness mapping.
"""
from typing import Dict, Any, Tuple
from app.core.constants import GestureState, DEFAULT_MIN_DISTANCE, DEFAULT_MAX_DISTANCE, DEFAULT_SMOOTHING_ALPHA
from app.core.config import settings
from app.core.logging_config import logger
from app.utils.smoothing import ExponentialMovingAverage
from app.utils.normalization import normalize_distance, map_distance_to_brightness
from app.services.brightness_service import brightness_service

class GestureService:
    def __init__(self):
        self.min_distance = settings.MIN_GESTURE_DISTANCE
        self.max_distance = settings.MAX_GESTURE_DISTANCE
        self.min_brightness = settings.MIN_BRIGHTNESS
        self.max_brightness = settings.MAX_BRIGHTNESS
        self.sensitivity = 1.0

        self.control_enabled = True
        self.is_calibrating = False
        self.is_paused = False

        self.ema_brightness = ExponentialMovingAverage(alpha=settings.SMOOTHING_ALPHA)
        self.current_state = GestureState.NO_HAND

        self._last_raw_distance = None
        self._last_calculated_brightness = None
        self._last_smoothed_brightness = None

    def set_control_enabled(self, enabled: bool):
        self.control_enabled = enabled
        logger.info(f"Gesture control enabled set to: {enabled}")

    def update_settings(self, min_dist: float, max_dist: float, min_b: float, max_b: float, alpha: float, sensitivity: float):
        self.min_distance = min_dist
        self.max_distance = max_dist
        self.min_brightness = min_b
        self.max_brightness = max_b
        self.sensitivity = sensitivity
        self.ema_brightness.set_alpha(alpha)
        logger.info(f"Updated Gesture Service settings: dist=[{min_dist}, {max_dist}], b=[{min_b}, {max_b}], alpha={alpha}")

    def process_gesture(self, tracking_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes MediaPipe tracking outputs and processes gesture distance, state, and smoothed target brightness.
        """
        hand_detected = tracking_result.get("hand_detected", False)
        raw_distance = tracking_result.get("distance", None)
        is_open_hand = tracking_result.get("is_open_hand", False)

        if not hand_detected or raw_distance is None:
            self.current_state = GestureState.NO_HAND
            return {
                "state": self.current_state,
                "distance": None,
                "normalized_distance": None,
                "target_brightness": None,
                "smoothed_brightness": self._last_smoothed_brightness,
                "hardware_updated": False
            }

        # Check pause gesture (optional open hand feature)
        if is_open_hand and not self.is_calibrating:
            self.current_state = GestureState.PAUSED
            return {
                "state": self.current_state,
                "distance": raw_distance,
                "normalized_distance": None,
                "target_brightness": None,
                "smoothed_brightness": self._last_smoothed_brightness,
                "hardware_updated": False
            }

        if self.is_calibrating:
            self.current_state = GestureState.CALIBRATING
            return {
                "state": self.current_state,
                "distance": raw_distance,
                "normalized_distance": normalize_distance(raw_distance, self.min_distance, self.max_distance),
                "target_brightness": None,
                "smoothed_brightness": self._last_smoothed_brightness,
                "hardware_updated": False
            }

        # Hand detected & active gesture processing
        self.current_state = GestureState.GESTURE_ACTIVE
        self._last_raw_distance = raw_distance

        # Normalize & map to target brightness
        norm_dist = normalize_distance(raw_distance, self.min_distance, self.max_distance)
        
        # Apply sensitivity scaling
        if self.sensitivity != 1.0:
            norm_dist = max(0.0, min(1.0, norm_dist * self.sensitivity))

        raw_target_b = self.min_brightness + norm_dist * (self.max_brightness - self.min_brightness)
        self._last_calculated_brightness = raw_target_b

        # Apply Exponential Moving Average (EMA) smoothing to eliminate noise/jitter
        smoothed_b = self.ema_brightness.update(raw_target_b)
        self._last_smoothed_brightness = smoothed_b

        hardware_updated = False
        # Update system screen brightness if gesture control is active
        if self.control_enabled:
            actual_b, hardware_updated = brightness_service.set_brightness(smoothed_b)

        return {
            "state": self.current_state,
            "distance": raw_distance,
            "normalized_distance": norm_dist,
            "target_brightness": raw_target_b,
            "smoothed_brightness": smoothed_b,
            "hardware_updated": hardware_updated
        }

gesture_service = GestureService()
