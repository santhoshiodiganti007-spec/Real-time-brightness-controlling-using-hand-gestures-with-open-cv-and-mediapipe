"""
Normalization algorithms mapping Euclidean gesture distance to percentage and brightness.
"""
def normalize_distance(
    distance: float,
    min_dist: float = 0.03,
    max_dist: float = 0.25
) -> float:
    """
    Normalizes gesture distance into a 0.0 -> 1.0 range based on min_dist and max_dist thresholds.
    """
    if max_dist <= min_dist:
        return 0.0

    raw_norm = (distance - min_dist) / (max_dist - min_dist)
    return max(0.0, min(1.0, float(raw_norm)))


def map_distance_to_brightness(
    distance: float,
    min_dist: float = 0.03,
    max_dist: float = 0.25,
    min_brightness: float = 10.0,
    max_brightness: float = 100.0
) -> float:
    """
    Maps gesture distance directly to target brightness percentage with strict safety clamping.
    """
    norm = normalize_distance(distance, min_dist, max_dist)
    target_b = min_brightness + norm * (max_brightness - min_brightness)
    # Strict clamping between safety limits
    return clamp_brightness(target_b, min_brightness, max_brightness)


def clamp_brightness(
    val: float,
    min_b: float = 10.0,
    max_b: float = 100.0
) -> float:
    """
    Clamps brightness value to specified range (default 10% to 100%).
    """
    safe_min = max(0.0, min(100.0, min_b))
    safe_max = max(safe_min, min(100.0, max_b))
    return max(safe_min, min(safe_max, float(val)))
