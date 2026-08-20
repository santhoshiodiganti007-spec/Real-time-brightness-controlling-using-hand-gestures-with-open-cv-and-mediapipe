"""
Unit tests for distance normalization and brightness mapping functions.
"""
import pytest
from app.utils.normalization import normalize_distance, map_distance_to_brightness, clamp_brightness

def test_normalize_distance_bounds():
    # Below minimum distance -> 0.0
    assert normalize_distance(0.01, min_dist=0.03, max_dist=0.25) == 0.0
    # Above maximum distance -> 1.0
    assert normalize_distance(0.30, min_dist=0.03, max_dist=0.25) == 1.0
    # Midpoint distance -> 0.5
    mid = 0.03 + (0.25 - 0.03) / 2
    assert pytest.approx(normalize_distance(mid, min_dist=0.03, max_dist=0.25), 0.01) == 0.5

def test_map_distance_to_brightness():
    # Min gesture distance -> Min brightness (10%)
    assert map_distance_to_brightness(0.01, min_dist=0.03, max_dist=0.25, min_brightness=10.0, max_brightness=100.0) == 10.0
    # Max gesture distance -> Max brightness (100%)
    assert map_distance_to_brightness(0.30, min_dist=0.03, max_dist=0.25, min_brightness=10.0, max_brightness=100.0) == 100.0

def test_clamp_brightness_safety():
    # Values outside range should be safely clamped
    assert clamp_brightness(-15.0, min_b=10.0, max_b=100.0) == 10.0
    assert clamp_brightness(150.0, min_b=10.0, max_b=100.0) == 100.0
    assert clamp_brightness(55.5, min_b=10.0, max_b=100.0) == 55.5
