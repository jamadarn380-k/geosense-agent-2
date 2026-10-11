"""
GeoSense Agent 2.0 - Phase 3
Unit tests for lidar_analyzer and unified_site_profile.
"""

import pytest

from lidar_analyzer import analyze_bbox, _compute_slope_risk
from unified_site_profile import build_profile
from streetview_semantic import compute_walkability_score


def test_analyze_bbox_returns_dict():
    result = analyze_bbox(32.7666, -117.1484, 32.7766, -117.1384)
    assert isinstance(result, dict)


def test_analyze_bbox_has_required_keys():
    result = analyze_bbox(32.7666, -117.1484, 32.7766, 32.7766)
    required_keys = [
        "bbox",
        "avg_building_height_m",
        "canopy_cover_pct",
        "impervious_surface_pct",
        "slope_risk_score",
        "total_points_analyzed",
    ]
    for key in required_keys:
        assert key in result


def test_canopy_cover_between_0_and_100():
    result = analyze_bbox(32.7666, -117.1484, 32.7766, 32.7766)
    assert 0 <= result["canopy_cover_pct"] <= 100


def test_slope_risk_zero_for_few_points():
    assert _compute_slope_risk([10.0]) == 0.0
    assert _compute_slope_risk([]) == 0.0


def test_walkability_score_between_0_and_10():
    composition = {
        "sidewalk": 50.0,
        "vegetation": 50.0,
        "car": 50.0,
    }
    score = compute_walkability_score(composition)
    assert 0 <= score <= 10


def test_unified_profile_has_required_fields():
    profile = build_profile(32.7666, -117.1484)
    required_fields = [
        "latitude",
        "longitude",
        "avg_building_height_m",
        "canopy_cover_pct",
        "impervious_surface_pct",
        "slope_risk_score",
        "scene_composition",
        "walkability_score",
    ]
    for field in required_fields:
        assert field in profile