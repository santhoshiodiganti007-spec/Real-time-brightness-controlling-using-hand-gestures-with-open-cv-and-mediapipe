"""
Adaptive Guided Calibration Service.
Allows user to pinch fingers close to capture MIN distance, spread fingers apart to capture MAX distance.
"""
from typing import Dict, Any, Optional
from app.core.logging_config import logger
from app.services.gesture_service import gesture_service

class CalibrationService:
    def __init__(self):
        self.step = "idle"
        self.temp_min_distance: Optional[float] = None
        self.temp_max_distance: Optional[float] = None

    def start_calibration(self):
        self.step = "min_step"
        self.temp_min_distance = None
        self.temp_max_distance = None
        gesture_service.is_calibrating = True
        logger.info("Calibration started: awaiting MIN distance capture.")

    def record_min_distance(self, current_distance: float) -> float:
        if current_distance is None or current_distance <= 0:
            raise ValueError("Invalid distance captured for minimum pinch.")
        self.temp_min_distance = float(current_distance)
        self.step = "max_step"
        logger.info(f"Captured MIN distance: {self.temp_min_distance:.4f}. Awaiting MAX distance capture.")
        return self.temp_min_distance

    def record_max_distance(self, current_distance: float) -> float:
        if current_distance is None or current_distance <= 0:
            raise ValueError("Invalid distance captured for maximum spread.")
        if self.temp_min_distance is not None and current_distance <= self.temp_min_distance:
            # Enforce reasonable min < max delta
            self.temp_max_distance = self.temp_min_distance + 0.15
        else:
            self.temp_max_distance = float(current_distance)
        self.step = "ready_to_save"
        logger.info(f"Captured MAX distance: {self.temp_max_distance:.4f}.")
        return self.temp_max_distance

    def save_calibration(self) -> Dict[str, float]:
        if self.temp_min_distance is None or self.temp_max_distance is None:
            raise ValueError("Calibration incomplete. Both MIN and MAX distances must be recorded.")

        min_d = self.temp_min_distance
        max_d = self.temp_max_distance
        
        # Update gesture service parameters
        gesture_service.min_distance = min_d
        gesture_service.max_distance = max_d
        gesture_service.is_calibrating = False
        self.step = "idle"

        logger.info(f"Calibration saved successfully: Min={min_d:.4f}, Max={max_d:.4f}")
        return {"min_distance": min_d, "max_distance": max_d}

    def cancel_calibration(self):
        self.step = "idle"
        gesture_service.is_calibrating = False
        logger.info("Calibration cancelled.")

calibration_service = CalibrationService()
