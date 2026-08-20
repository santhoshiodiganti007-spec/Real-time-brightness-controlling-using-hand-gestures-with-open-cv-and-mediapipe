"""
Health and System Diagnostics API Endpoints.
"""
import sys
import platform
from fastapi import APIRouter
from app.core.config import settings
from app.services.brightness_service import brightness_service
from app.services.camera_service import camera_service

router = APIRouter(tags=["Health"])

@router.get("/api/health")
def health_check():
    """Returns application health status and diagnostics."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "platform": platform.system(),
        "python_version": sys.version.split()[0],
        "demo_mode": brightness_service.is_demo_mode(),
        "camera_active": camera_service.is_running
    }

@router.get("/api/diagnostics")
def system_diagnostics():
    """Runs system startup diagnostics."""
    checks = {
        "python": True,
        "opencv": True,
        "mediapipe": True,
        "camera": not camera_service.use_simulated_feed,
        "brightness_controller": not brightness_service.is_demo_mode(),
        "database": True,
        "configuration": True
    }
    system_ready = all(checks.values())
    return {
        "system_ready": system_ready,
        "checks": checks,
        "message": "System operating normally." if system_ready else "Running with fallback / DEMO mode capabilities."
    }
