"""
GeoSense Agent 2.0 - Phase 3
Unified enhanced site profile combining LiDAR and street-level analysis.
"""

import os
import json
from dataclasses import dataclass, asdict

from lidar_analyzer import analyze_bbox
from streetview_semantic import analyze_location


@dataclass
class EnhancedSiteProfile:
    latitude: float
    longitude: float
    avg_building_height_m: float
    canopy_cover_pct: float
    impervious_surface_pct: float
    slope_risk_score: float
    scene_composition: dict
    walkability_score: float


def build_profile(lat, lon, bbox_radius_deg=0.005):
    lidar_result = analyze_bbox(
        lat - bbox_radius_deg,
        lon - bbox_radius_deg,
        lat + bbox_radius_deg,
        lon + bbox_radius_deg,
    )

    street_result = analyze_location(lat, lon)

    profile = EnhancedSiteProfile(
        latitude=lat,
        longitude=lon,
        avg_building_height_m=lidar_result["avg_building_height_m"],
        canopy_cover_pct=lidar_result["canopy_cover_pct"],
        impervious_surface_pct=lidar_result["impervious_surface_pct"],
        slope_risk_score=lidar_result["slope_risk_score"],
        scene_composition=street_result.get("scene_composition", {}),
        walkability_score=street_result.get("walkability_score", 0.0),
    )

    return asdict(profile)


def main():
    print("=" * 60)
    print("GeoSense Agent 2.0 - Unified Enhanced Site Profile")
    print("=" * 60)

    lat, lon = 32.7666, -117.1484

    profile = build_profile(lat, lon)

    os.makedirs("outputs/reports", exist_ok=True)

    filename = f"outputs/reports/enhanced_site_profile_{lat:.2f}_{lon:.2f}.json"

    with open(filename, "w") as f:
        json.dump(profile, f, indent=2)

    print()
    print("Profile saved to:")
    print(filename)

    print()
    print(json.dumps(profile, indent=2))

    print()
    print("=" * 60)
    print("Unified site profile completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()