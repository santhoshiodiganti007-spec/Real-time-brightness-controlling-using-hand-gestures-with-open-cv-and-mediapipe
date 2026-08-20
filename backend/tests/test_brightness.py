"""
Unit tests for Brightness Service.
"""
from app.services.brightness_service import BrightnessService

def test_brightness_service_demo_mode():
    service = BrightnessService()
    service.set_demo_mode(True)
    assert service.is_demo_mode() is True

    val, updated = service.set_brightness(75.0, force=True)
    assert val == 75.0
    assert service.get_brightness() == 75.0

def test_brightness_clamping_limits():
    service = BrightnessService()
    service.set_demo_mode(True)
    service.update_bounds(min_b=15.0, max_b=90.0, threshold=1.0)
    
    val, _ = service.set_brightness(5.0, force=True)
    assert val == 15.0  # Clamped to min 15

    val, _ = service.set_brightness(99.0, force=True)
    assert val == 90.0  # Clamped to max 90
