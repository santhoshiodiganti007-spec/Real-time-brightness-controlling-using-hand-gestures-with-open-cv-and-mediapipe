"""
FastAPI Main Application Entry Point.
Initializes database, CORS, routes, system diagnostics, and WebSocket broadcaster.
"""
import os
import sys
import asyncio

# Ensure backend root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging_config import logger
from app.models.database import init_db
from app.services.camera_service import camera_service
from app.services.brightness_service import brightness_service
from app.api import (
    routes_health,
    routes_brightness,
    routes_gesture,
    routes_settings,
    routes_statistics,
    routes_camera
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # System Diagnostics on Startup
    logger.info("=" * 60)
    logger.info("  SYSTEM DIAGNOSTICS & INITIALIZATION")
    logger.info("=" * 60)
    logger.info(f"✓ Python Version: {sys.version.split()[0]}")
    logger.info(f"✓ Environment: {settings.APP_ENV}")

    # Initialize SQLite Database
    init_db()
    logger.info("✓ SQLite Database Initialized.")

    # Check Brightness Hardware
    demo_status = " (DEMO MODE)" if brightness_service.is_demo_mode() else ""
    logger.info(f"✓ Brightness Controller Initialized{demo_status}")

    # Auto-start Camera Background Service
    camera_service.start_camera(settings.CAMERA_INDEX)
    logger.info(f"✓ Camera Service Started (Index: {settings.CAMERA_INDEX})")
    logger.info("=" * 60)
    logger.info("SYSTEM READY - TOUCHLESS BRIGHTNESS CONTROL ACTIVE")
    logger.info("=" * 60)

    yield

    # Shutdown logic
    logger.info("Shutting down Camera Service...")
    camera_service.stop_camera()
    logger.info("Application shutdown complete.")

app = FastAPI(
    title=settings.APP_NAME,
    description="Production-grade AI/ML hand gesture-controlled screen brightness application.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for React UI integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(routes_health.router)
app.include_router(routes_brightness.router)
app.include_router(routes_gesture.router)
app.include_router(routes_settings.router)
app.include_router(routes_statistics.router)
app.include_router(routes_camera.router)

# Real-time WebSocket Endpoint
@app.websocket("/ws/brightness")
async def websocket_brightness_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info(f"WebSocket client connected: {websocket.client}")
    try:
        while True:
            st = camera_service.latest_state
            payload = {
                "brightness": round(st.get("smoothed_brightness") or 50.0, 1),
                "distance": round(st.get("distance") or 0.0, 4),
                "normalized_distance": round(st.get("normalized_distance") or 0.0, 2),
                "hand_detected": st.get("hand_detected", False),
                "gesture_active": st.get("gesture_state") == "GESTURE_ACTIVE",
                "gesture_state": str(st.get("gesture_state", "NO_HAND")),
                "fps": round(st.get("fps", 0.0), 1),
                "is_demo_mode": st.get("is_demo_mode", False),
                "control_enabled": st.get("control_enabled", True)
            }
            await websocket.send_json(payload)
            await asyncio.sleep(0.05)  # 20 Hz update rate
    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected: {websocket.client}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
