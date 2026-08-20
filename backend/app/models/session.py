"""
SQLAlchemy session model.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime
from app.models.database import Base

class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, default=0.0)
    average_brightness = Column(Float, default=0.0)
    min_brightness = Column(Float, default=100.0)
    max_brightness = Column(Float, default=0.0)
    total_gesture_events = Column(Integer, default=0)
