"""
Camera Control and MJPEG Video Stream Endpoints.
"""
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.camera_service import camera_service

router = APIRouter(prefix="/api/camera", tags=["Camera"])

@router.get("/stream")
def video_stream():
    """Returns real-time annotated MJPEG video stream with MediaPipe gesture overlay."""
    return StreamingResponse(
        camera_service.get_mjpeg_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@router.post("/start")
def start_camera(camera_index: int = 0):
    success = camera_service.start_camera(camera_index=camera_index)
    return {"message": "Camera started", "active": success}

@router.post("/stop")
def stop_camera():
    camera_service.stop_camera()
    return {"message": "Camera stopped", "active": False}
