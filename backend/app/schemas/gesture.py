"""
Pydantic schemas for Gesture processing and Calibration.
"""
from pydantic import BaseModel, Field
from typing import Optional
from app.core.constants import GestureState

class GestureStatusResponse(BaseModel):
    hand_detected: bool
    num_hands: int
    gesture_state: GestureState
    distance: Optional[float] = None
    normalized_distance: Optional[float] = None
    calculated_brightness: Optional[float] = None
    smoothed_brightness: Optional[float] = None
    control_enabled: bool
    fps: float

class CalibrationStartRequest(BaseModel):
    step: str = Field(..., description="'min' or 'max'")

class CalibrationSaveRequest(BaseModel):
    min_distance: float = Field(..., gt=0.0)
    max_distance: float = Field(..., gt=0.0)
