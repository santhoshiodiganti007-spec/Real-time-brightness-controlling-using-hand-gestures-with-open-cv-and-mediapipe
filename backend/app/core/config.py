"""
Configuration management using pydantic-settings.
"""
import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "Touchless Brightness Control"
    APP_ENV: str = Field("development", env="APP_ENV")
    API_HOST: str = Field("127.0.0.1", env="API_HOST")
    API_PORT: int = Field(8000, env="API_PORT")

    CAMERA_INDEX: int = Field(0, env="CAMERA_INDEX")
    CAMERA_WIDTH: int = Field(640, env="CAMERA_WIDTH")
    CAMERA_HEIGHT: int = Field(480, env="CAMERA_HEIGHT")
    CAMERA_FPS: int = Field(30, env="CAMERA_FPS")

    MIN_BRIGHTNESS: float = Field(10.0, env="MIN_BRIGHTNESS")
    MAX_BRIGHTNESS: float = Field(100.0, env="MAX_BRIGHTNESS")
    SMOOTHING_ALPHA: float = Field(0.2, env="SMOOTHING_ALPHA")
    MIN_GESTURE_DISTANCE: float = Field(0.03, env="MIN_GESTURE_DISTANCE")
    MAX_GESTURE_DISTANCE: float = Field(0.25, env="MAX_GESTURE_DISTANCE")
    UPDATE_THRESHOLD: float = Field(2.0, env="UPDATE_THRESHOLD")
    DEMO_MODE: bool = Field(False, env="DEMO_MODE")

    DETECTION_CONFIDENCE: float = Field(0.7, env="DETECTION_CONFIDENCE")
    TRACKING_CONFIDENCE: float = Field(0.7, env="TRACKING_CONFIDENCE")
    MAX_NUM_HANDS: int = Field(2, env="MAX_NUM_HANDS")

    DATABASE_URL: str = Field("sqlite:///./touchless_brightness.db", env="DATABASE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
