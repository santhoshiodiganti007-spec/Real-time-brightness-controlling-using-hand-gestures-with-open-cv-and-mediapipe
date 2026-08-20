"""
User Settings Management Endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.settings import SettingsSchema
from app.models.database import get_db
from app.models.settings import UserSettingsModel
from app.services.gesture_service import gesture_service
from app.services.brightness_service import brightness_service
from app.services.hand_tracking_service import hand_tracking_service

router = APIRouter(prefix="/api/settings", tags=["Settings"])

@router.get("", response_model=SettingsSchema)
def get_settings(db: Session = Depends(get_db)):
    db_setting = db.query(UserSettingsModel).filter(UserSettingsModel.id == 1).first()
    if not db_setting:
        db_setting = UserSettingsModel(id=1)
        db.add(db_setting)
        db.commit()
        db.refresh(db_setting)
        
    return SettingsSchema(
        smoothing_factor=gesture_service.ema_brightness.alpha,
        sensitivity=gesture_service.sensitivity,
        min_brightness=gesture_service.min_brightness,
        max_brightness=gesture_service.max_brightness,
        min_distance=gesture_service.min_distance,
        max_distance=gesture_service.max_distance,
        camera_index=db_setting.camera_index,
        update_threshold=db_setting.update_threshold,
        gesture_control_enabled=gesture_service.control_enabled,
        demo_mode=brightness_service.is_demo_mode()
    )

@router.put("", response_model=SettingsSchema)
def update_settings(new_settings: SettingsSchema, db: Session = Depends(get_db)):
    gesture_service.update_settings(
        min_dist=new_settings.min_distance,
        max_dist=new_settings.max_distance,
        min_b=new_settings.min_brightness,
        max_b=new_settings.max_brightness,
        alpha=new_settings.smoothing_factor,
        sensitivity=new_settings.sensitivity
    )
    brightness_service.update_bounds(
        min_b=new_settings.min_brightness,
        max_b=new_settings.max_brightness,
        threshold=new_settings.update_threshold
    )
    brightness_service.set_demo_mode(new_settings.demo_mode)
    gesture_service.set_control_enabled(new_settings.gesture_control_enabled)

    # Persist in DB
    db_setting = db.query(UserSettingsModel).filter(UserSettingsModel.id == 1).first()
    if not db_setting:
        db_setting = UserSettingsModel(id=1)
        db.add(db_setting)

    db_setting.smoothing_factor = new_settings.smoothing_factor
    db_setting.sensitivity = new_settings.sensitivity
    db_setting.min_brightness = new_settings.min_brightness
    db_setting.max_brightness = new_settings.max_brightness
    db_setting.min_distance = new_settings.min_distance
    db_setting.max_distance = new_settings.max_distance
    db_setting.camera_index = new_settings.camera_index
    db_setting.update_threshold = new_settings.update_threshold
    db_setting.gesture_control_enabled = new_settings.gesture_control_enabled
    db_setting.demo_mode = new_settings.demo_mode
    db.commit()

    return new_settings
