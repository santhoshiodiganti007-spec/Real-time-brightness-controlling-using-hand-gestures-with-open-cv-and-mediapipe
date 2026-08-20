"""
SQLAlchemy user settings model.
"""
from sqlalchemy import Column, Integer, Float, Boolean
from app.models.database import Base

class UserSettingsModel(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True, default=1)
    smoothing_factor = Column(Float, default=0.2)
    sensitivity = Column(Float, default=1.0)
    min_brightness = Column(Float, default=10.0)
    max_brightness = Column(Float, default=100.0)
    min_distance = Column(Float, default=0.03)
    max_distance = Column(Float, default=0.25)
    camera_index = Column(Integer, default=0)
    update_threshold = Column(Float, default=2.0)
    gesture_control_enabled = Column(Boolean, default=True)
    demo_mode = Column(Boolean, default=False)
