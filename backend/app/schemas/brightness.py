"""
Pydantic schemas for Brightness control endpoints.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BrightnessRequest(BaseModel):
    brightness: float = Field(..., ge=0.0, le=100.0, description="Target brightness percentage")

class BrightnessResponse(BaseModel):
    brightness: float
    previous_brightness: float
    is_demo_mode: bool
    status: str
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class BrightnessEventSchema(BaseModel):
    id: int
    timestamp: datetime
    brightness: float
    gesture_distance: Optional[float] = None

    class Config:
        from_attributes = True
