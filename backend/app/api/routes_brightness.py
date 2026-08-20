"""
Brightness Control API Endpoints.
"""
from fastapi import APIRouter, HTTPException
from app.schemas.brightness import BrightnessRequest, BrightnessResponse
from app.services.brightness_service import brightness_service
from app.services.statistics_service import statistics_service

router = APIRouter(prefix="/api/brightness", tags=["Brightness"])

@router.get("", response_model=BrightnessResponse)
def get_brightness():
    current_b = brightness_service.get_brightness()
    return BrightnessResponse(
        brightness=current_b,
        previous_brightness=current_b,
        is_demo_mode=brightness_service.is_demo_mode(),
        status="active"
    )

@router.post("", response_model=BrightnessResponse)
def set_brightness(req: BrightnessRequest):
    prev_b = brightness_service.get_brightness()
    actual_b, hardware_updated = brightness_service.set_brightness(req.brightness, force=True)
    statistics_service.log_brightness_event(actual_b)
    
    return BrightnessResponse(
        brightness=actual_b,
        previous_brightness=prev_b,
        is_demo_mode=brightness_service.is_demo_mode(),
        status="updated"
    )
