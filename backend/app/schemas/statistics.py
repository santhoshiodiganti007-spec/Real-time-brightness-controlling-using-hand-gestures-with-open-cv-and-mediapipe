"""
Pydantic schemas for Statistics and Session Summary.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.brightness import BrightnessEventSchema

class StatisticsSummaryResponse(BaseModel):
    session_duration_seconds: float
    total_brightness_changes: int
    average_brightness: float
    min_brightness: float
    max_brightness: float
    gesture_detection_count: int
    detection_failures: int
    average_fps: float
    hand_detected: bool
    gesture_state: str
    is_demo_mode: bool

class HistoryResponse(BaseModel):
    events: List[BrightnessEventSchema]
