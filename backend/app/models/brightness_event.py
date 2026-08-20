"""
SQLAlchemy brightness event model.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from app.models.database import Base

class BrightnessEventModel(Base):
    __tablename__ = "brightness_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    brightness = Column(Float, nullable=False)
    gesture_distance = Column(Float, nullable=True)
    raw_distance = Column(Float, nullable=True)
