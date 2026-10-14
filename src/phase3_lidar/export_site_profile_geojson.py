"""
GeoSense Agent 2.0 - Phase 3
Export unified site profile to GeoJSON for QGIS.
"""

import os
import json

PROFILE_PATH = "outputs/reports/enhanced_site_profile_32.77_-117.15.json"
OUTPUT_PATH = "outputs/reports/enhanced_site_profile_32.77_-117.15.geojson"


def main():
    with open(PROFILE_PATH, "r") as file:
        profile = json.load(file)

    lat = profile["latitude"]
    lon = profile["longitude"]
    composition = profile.get("scene_composition", {})

    feature = {
        "type": "Feature",
        "properties": {
            "site_name": "GeoSense Site Profile",
            "walkability_score": profile.get("walkability_score", 0.0),
            "avg_building_height_m": profile.get(
                "avg_building_height_m", 0.0
            ),
            "canopy_cover_pct": profile.get("canopy_cover_pct", 0.0),
            "impervious_surface_pct": profile.get(
                "impervious_surface_pct", 0.0
            ),
            "slope_risk_score": profile.get("slope_risk_score", 0.0),
            "road_pct": composition.get("road", 0.0),
            "sidewalk_pct": composition.get("sidewalk", 0.0),
            "building_pct": composition.get("building", 0.0),
            "vegetation_pct": composition.get("vegetation", 0.0),
            "sky_pct": composition.get("sky", 0.0),
            "car_pct": composition.get("car", 0.0),
        },
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat],
        },
    }

    geojson = {
        "type": "FeatureCollection",
        "features": [feature],
    }

    os.makedirs("outputs/reports", exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(geojson, file, indent=2)

    print("GeoJSON created successfully.")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Coordinates: longitude={lon}, latitude={lat}")


if __name__ == "__main__":
    main()