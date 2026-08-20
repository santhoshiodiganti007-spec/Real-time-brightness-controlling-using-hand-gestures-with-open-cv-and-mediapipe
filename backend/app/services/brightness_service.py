"""
OS Display Brightness Hardware Controller Abstraction.
Supports Windows (screen_brightness_control), Linux, macOS, and DEMO mode fallback.
"""
import sys
import platform
from typing import Tuple
from app.core.config import settings
from app.core.logging_config import logger
from app.utils.normalization import clamp_brightness

# Attempt to import screen_brightness_control safely
SBC_AVAILABLE = False
try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except Exception as e:
    logger.warning(f"screen_brightness_control module loading warning: {e}")
    SBC_AVAILABLE = False


class BrightnessService:
    def __init__(self):
        self.os_type = platform.system()
        self._current_brightness = 50.0
        self._demo_mode = settings.DEMO_MODE or not SBC_AVAILABLE
        self._min_b = settings.MIN_BRIGHTNESS
        self._max_b = settings.MAX_BRIGHTNESS
        self._update_threshold = settings.UPDATE_THRESHOLD
        
        # Test initial hardware brightness query
        self._init_brightness()

    def _init_brightness(self):
        if not self._demo_mode and SBC_AVAILABLE:
            try:
                b_list = sbc.get_brightness()
                if b_list and len(b_list) > 0:
                    self._current_brightness = float(b_list[0])
                    logger.info(f"Initialized physical monitor brightness at {self._current_brightness}% ({self.os_type})")
                else:
                    logger.warning("No physical monitor brightness returned. Falling back to DEMO mode.")
                    self._demo_mode = True
            except Exception as ex:
                logger.warning(f"Could not read physical display brightness ({ex}). Enabling DEMO mode.")
                self._demo_mode = True
        else:
            logger.info("Brightness Service initialized in DEMO mode.")

    def is_demo_mode(self) -> bool:
        return self._demo_mode

    def set_demo_mode(self, enabled: bool):
        self._demo_mode = enabled
        logger.info(f"Brightness service DEMO mode set to: {enabled}")

    def get_brightness(self) -> float:
        if not self._demo_mode and SBC_AVAILABLE:
            try:
                b_list = sbc.get_brightness()
                if b_list and len(b_list) > 0:
                    self._current_brightness = float(b_list[0])
            except Exception as e:
                logger.error(f"Error querying physical display brightness: {e}")
        return self._current_brightness

    def set_brightness(self, target_brightness: float, force: bool = False) -> Tuple[float, bool]:
        """
        Sets screen brightness after safety clamping and threshold checking.
        Returns: (actual_brightness, was_hardware_updated)
        """
        clamped = clamp_brightness(target_brightness, self._min_b, self._max_b)

        # Check threshold to prevent rapid flickering
        diff = abs(clamped - self._current_brightness)
        if not force and diff < self._update_threshold:
            return self._current_brightness, False

        previous = self._current_brightness
        self._current_brightness = clamped
        hardware_updated = False

        if not self._demo_mode and SBC_AVAILABLE:
            try:
                sbc.set_brightness(int(clamped))
                hardware_updated = True
                logger.info(f"Updated physical monitor brightness: {int(clamped)}% (Prev: {int(previous)}%)")
            except Exception as ex:
                logger.error(f"Failed to set physical screen brightness: {ex}. Falling back to DEMO mode.")
                self._demo_mode = True

        return self._current_brightness, hardware_updated

    def update_bounds(self, min_b: float, max_b: float, threshold: float):
        self._min_b = min_b
        self._max_b = max_b
        self._update_threshold = threshold
        logger.info(f"Updated brightness bounds: Min={min_b}%, Max={max_b}%, Threshold={threshold}%")

brightness_service = BrightnessService()
