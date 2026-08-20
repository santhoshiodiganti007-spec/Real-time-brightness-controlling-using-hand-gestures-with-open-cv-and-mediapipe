"""
Unit tests for Gesture State Machine and Exponential Moving Average.
"""
from app.services.gesture_service import GestureService
from app.utils.smoothing import ExponentialMovingAverage
from app.core.constants import GestureState

def test_exponential_moving_average():
    ema = ExponentialMovingAverage(alpha=0.5, initial_value=10.0)
    # First update with 20.0 -> 0.5 * 20 + 0.5 * 10 = 15.0
    val1 = ema.update(20.0)
    assert val1 == 15.0
    # Second update with 30.0 -> 0.5 * 30 + 0.5 * 15 = 22.5
    val2 = ema.update(30.0)
    assert val2 == 22.5

def test_gesture_service_states():
    gs = GestureService()
    
    # Test NO_HAND
    res_no_hand = gs.process_gesture({"hand_detected": False})
    assert res_no_hand["state"] == GestureState.NO_HAND

    # Test PAUSED gesture (open hand)
    res_paused = gs.process_gesture({"hand_detected": True, "distance": 0.1, "is_open_hand": True})
    assert res_paused["state"] == GestureState.PAUSED

    # Test GESTURE_ACTIVE
    res_active = gs.process_gesture({"hand_detected": True, "distance": 0.14, "is_open_hand": False})
    assert res_active["state"] == GestureState.GESTURE_ACTIVE
    assert res_active["smoothed_brightness"] is not None
