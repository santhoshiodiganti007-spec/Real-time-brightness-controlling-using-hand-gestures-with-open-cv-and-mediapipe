"""
Gesture Control and Guided Calibration Endpoints.
"""
from fastapi import APIRouter, HTTPException
from app.schemas.gesture import GestureStatusResponse, CalibrationStartRequest, CalibrationSaveRequest
from app.services.gesture_service import gesture_service
from app.services.calibration_service import calibration_service
from app.services.camera_service import camera_service

router = APIRouter(tags=["Gesture & Calibration"])

@router.get("/api/gesture/status", response_model=GestureStatusResponse)
def get_gesture_status():
    st = camera_service.latest_state
    return GestureStatusResponse(
        hand_detected=st.get("hand_detected", False),
        num_hands=st.get("num_hands", 0),
        gesture_state=st.get("gesture_state", "NO_HAND"),
        distance=st.get("distance"),
        normalized_distance=st.get("normalized_distance"),
        calculated_brightness=st.get("calculated_brightness"),
        smoothed_brightness=st.get("smoothed_brightness"),
        control_enabled=gesture_service.control_enabled,
        fps=st.get("fps", 0.0)
    )

@router.post("/api/gesture/start")
def start_gesture_control():
    gesture_service.set_control_enabled(True)
    return {"message": "Gesture brightness control enabled", "control_enabled": True}

@router.post("/api/gesture/stop")
def stop_gesture_control():
    gesture_service.set_control_enabled(False)
    return {"message": "Gesture brightness control disabled", "control_enabled": False}

@router.post("/api/calibration/start")
def start_calibration():
    calibration_service.start_calibration()
    return {"message": "Calibration started. Pinch fingers close together.", "step": calibration_service.step}

@router.post("/api/calibration/record")
def record_calibration_step(req: CalibrationStartRequest):
    curr_dist = camera_service.latest_state.get("distance")
    if curr_dist is None:
        raise HTTPException(status_code=400, detail="No hand detected in webcam feed. Hold hand in front of camera.")
    
    if req.step == "min":
        val = calibration_service.record_min_distance(curr_dist)
        return {"message": f"Captured MIN distance: {val:.4f}. Now spread fingers wide apart.", "step": calibration_service.step, "min_distance": val}
    elif req.step == "max":
        val = calibration_service.record_max_distance(curr_dist)
        return {"message": f"Captured MAX distance: {val:.4f}. Click save to complete.", "step": calibration_service.step, "max_distance": val}
    else:
        raise HTTPException(status_code=400, detail="Invalid calibration step.")

@router.post("/api/calibration/save")
def save_calibration():
    try:
        res = calibration_service.save_calibration()
        return {"message": "Calibration parameters saved successfully.", "calibration": res}
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
