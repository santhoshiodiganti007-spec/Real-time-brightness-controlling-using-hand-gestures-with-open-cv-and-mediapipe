"""
Input validation utilities.
"""
def validate_brightness_settings(min_b: float, max_b: float):
    if min_b < 0 or min_b > 100:
        raise ValueError("Min brightness must be between 0 and 100.")
    if max_b < 0 or max_b > 100:
        raise ValueError("Max brightness must be between 0 and 100.")
    if min_b >= max_b:
        raise ValueError("Min brightness must be strictly less than max brightness.")

def validate_gesture_settings(min_d: float, max_d: float):
    if min_d < 0.001 or min_d > 1.0:
        raise ValueError("Min distance must be between 0.001 and 1.0.")
    if max_d < 0.001 or max_d > 1.0:
        raise ValueError("Max distance must be between 0.001 and 1.0.")
    if min_d >= max_d:
        raise ValueError("Min distance must be strictly less than max distance.")
