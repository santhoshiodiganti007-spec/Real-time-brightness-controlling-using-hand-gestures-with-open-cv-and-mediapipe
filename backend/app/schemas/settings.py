"""
Pydantic schemas for User Settings.
"""
from pydantic import BaseModel, Field

class SettingsSchema(BaseModel):
    smoothing_factor: float = Field(0.2, ge=0.01, le=1.0)
    sensitivity: float = Field(1.0, ge=0.1, le=3.0)
    min_brightness: float = Field(10.0, ge=0.0, le=100.0)
    max_brightness: float = Field(100.0, ge=0.0, le=100.0)
    min_distance: float = Field(0.03, ge=0.001, le=1.0)
    max_distance: float = Field(0.25, ge=0.001, le=1.0)
    camera_index: int = Field(0, ge=0)
    update_threshold: float = Field(2.0, ge=0.1, le=20.0)
    gesture_control_enabled: bool = True
    demo_mode: bool = False

    class Config:
        from_attributes = True
