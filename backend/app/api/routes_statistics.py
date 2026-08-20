"""
Statistics and Historical Timeline API Endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.statistics import StatisticsSummaryResponse, HistoryResponse
from app.schemas.brightness import BrightnessEventSchema
from app.services.statistics_service import statistics_service
from app.services.camera_service import camera_service
from app.services.brightness_service import brightness_service
from app.models.database import get_db
from app.models.brightness_event import BrightnessEventModel

router = APIRouter(tags=["Statistics & History"])

@router.get("/api/statistics", response_model=StatisticsSummaryResponse)
def get_statistics():
    summary = statistics_service.get_summary()
    summary["hand_detected"] = camera_service.latest_state.get("hand_detected", False)
    summary["gesture_state"] = str(camera_service.latest_state.get("gesture_state", "NO_HAND"))
    summary["is_demo_mode"] = brightness_service.is_demo_mode()
    return StatisticsSummaryResponse(**summary)

@router.get("/api/history", response_model=HistoryResponse)
def get_history(limit: int = 50, db: Session = Depends(get_db)):
    events = (
        db.query(BrightnessEventModel)
        .order_by(BrightnessEventModel.timestamp.desc())
        .limit(limit)
        .all()
    )
    events.reverse()  # Chronological order for chart plotting
    
    event_schemas = [
        BrightnessEventSchema(
            id=ev.id,
            timestamp=ev.timestamp,
            brightness=ev.brightness,
            gesture_distance=ev.gesture_distance
        )
        for ev in events
    ]
    return HistoryResponse(events=event_schemas)
