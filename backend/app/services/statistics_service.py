"""
Statistics & Metrics Tracking Service.
Maintains session timers, FPS calculation, min/max/average brightness records, and database persistence.
"""
import time
from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.core.logging_config import logger
from app.models.database import SessionLocal, init_db
from app.models.session import SessionModel
from app.models.brightness_event import BrightnessEventModel

class StatisticsService:
    def __init__(self):
        self.session_start_time = time.time()
        self.total_brightness_changes = 0
        self.brightness_history: List[float] = []
        self.detection_success_count = 0
        self.detection_failure_count = 0
        
        # FPS calculation
        self._fps_frame_count = 0
        self._fps_start_time = time.time()
        self.current_fps = 0.0

        # Active DB session id
        self.db_session_id = None
        self._init_db_session()

    def _init_db_session(self):
        try:
            init_db()  # Ensure database tables exist
            db = SessionLocal()
            session_entry = SessionModel(
                start_time=datetime.utcnow(),
                average_brightness=50.0,
                min_brightness=10.0,
                max_brightness=100.0,
                total_gesture_events=0
            )
            db.add(session_entry)
            db.commit()
            db.refresh(session_entry)
            self.db_session_id = session_entry.id
            db.close()
            logger.info(f"Database statistics session initialized (ID: {self.db_session_id}).")
        except Exception as e:
            logger.error(f"Failed to initialize DB session: {e}")

    def update_fps(self) -> float:
        self._fps_frame_count += 1
        elapsed = time.time() - self._fps_start_time
        if elapsed >= 1.0:
            self.current_fps = self._fps_frame_count / elapsed
            self._fps_frame_count = 0
            self._fps_start_time = time.time()
        return self.current_fps

    def log_gesture_frame(self, hand_detected: bool, brightness: float = None, gesture_distance: float = None):
        if hand_detected:
            self.detection_success_count += 1
        else:
            self.detection_failure_count += 1

        if brightness is not None:
            self.brightness_history.append(brightness)
            if len(self.brightness_history) > 1000:
                self.brightness_history = self.brightness_history[-1000:]

    def log_brightness_event(self, brightness: float, distance: float = None):
        self.total_brightness_changes += 1
        self.brightness_history.append(brightness)
        
        # Record into database
        try:
            db = SessionLocal()
            event = BrightnessEventModel(
                session_id=self.db_session_id,
                timestamp=datetime.utcnow(),
                brightness=brightness,
                gesture_distance=distance
            )
            db.add(event)
            db.commit()
            db.close()
        except Exception as e:
            logger.error(f"Failed to log brightness event to database: {e}")

    def get_summary(self) -> Dict[str, Any]:
        duration = time.time() - self.session_start_time
        avg_b = sum(self.brightness_history) / len(self.brightness_history) if self.brightness_history else 50.0
        min_b = min(self.brightness_history) if self.brightness_history else 10.0
        max_b = max(self.brightness_history) if self.brightness_history else 100.0

        return {
            "session_duration_seconds": round(duration, 1),
            "total_brightness_changes": self.total_brightness_changes,
            "average_brightness": round(avg_b, 1),
            "min_brightness": round(min_b, 1),
            "max_brightness": round(max_b, 1),
            "gesture_detection_count": self.detection_success_count,
            "detection_failures": self.detection_failure_count,
            "average_fps": round(self.current_fps, 1)
        }

statistics_service = StatisticsService()
