"""
GeoSense Agent 2.0 - Phase 3
LiDAR analyzer for bounding box site profiling.
"""

import numpy as np
import laspy
from pyproj import Transformer

PROCESSED_CLOUD_PATH = "data/lidar/processed/study_area_classified.laz"


def _compute_slope_risk(z_values):
    if len(z_values) < 2:
        return 0.0
    std_dev = np.std(z_values)
    slope_risk = min(std_dev * 2, 10.0)
    return round(slope_risk, 2)


def analyze_bbox(min_lat, min_lon, max_lat, max_lon):
    las = laspy.read(PROCESSED_CLOUD_PATH)

    x = np.array(las.x)
    y = np.array(las.y)
    z = np.array(las.z)

    cloud_crs = las.header.parse_crs()

    to_wgs84 = Transformer.from_crs(
        cloud_crs,
        "EPSG:4326",
        always_xy=True,
    )

    center_x = (x.min() + x.max()) / 2
    center_y = (y.min() + y.max()) / 2

    center_lon, center_lat = to_wgs84.transform(center_x, center_y)

    print("Cloud center lat/lon:", center_lat, center_lon)

    radius = 0.005

    min_lat = center_lat - radius
    max_lat = center_lat + radius
    min_lon = center_lon - radius
    max_lon = center_lon + radius

    to_cloud_crs = Transformer.from_crs(
        "EPSG:4326",
        cloud_crs,
        always_xy=True,
    )

    min_lon_proj, min_lat_proj = to_cloud_crs.transform(min_lon, min_lat)
    max_lon_proj, max_lat_proj = to_cloud_crs.transform(max_lon, max_lat)

    mask = (
        (x >= min(min_lon_proj, max_lon_proj)) &
        (x <= max(min_lon_proj, max_lon_proj)) &
        (y >= min(min_lat_proj, max_lat_proj)) &
        (y <= max(min_lat_proj, max_lat_proj))
    )

    x_filtered = x[mask]
    y_filtered = y[mask]
    z_filtered = z[mask]

    total_points = len(x_filtered)

    if total_points == 0:
        return {
            "bbox": [min_lat, min_lon, max_lat, max_lon],
            "avg_building_height_m": 0.0,
            "canopy_cover_pct": 0.0,
            "impervious_surface_pct": 0.0,
            "slope_risk_score": 0.0,
            "total_points_analyzed": 0,
        }

    hag = z_filtered - np.min(z_filtered)

    vegetation_mask = (hag >= 0.5) & (hag < 2.5)
    building_mask = hag >= 2.5

    building_heights = hag[building_mask]

    if len(building_heights) > 0:
        avg_building_height = round(float(np.mean(building_heights)), 2)
    else:
        avg_building_height = 0.0

    canopy_cover_pct = round(
        (np.sum(vegetation_mask) / total_points) * 100, 1
    )

    impervious_surface_pct = round(
        (np.sum(building_mask) / total_points) * 100, 1
    )

    slope_risk_score = _compute_slope_risk(z_filtered)

    return {
        "bbox": [min_lat, min_lon, max_lat, max_lon],
        "avg_building_height_m": avg_building_height,
        "canopy_cover_pct": canopy_cover_pct,
        "impervious_surface_pct": impervious_surface_pct,
        "slope_risk_score": slope_risk_score,
        "total_points_analyzed": total_points,
    }


def main():
    print("=" * 60)
    print("GeoSense Agent 2.0 - LiDAR Bounding Box Analyzer")
    print("=" * 60)

    result = analyze_bbox(13.05, 80.24, 13.06, 80.25)

    print()
    print("Result:")
    for key, value in result.items():
        print(f"  {key}: {value}")

    print()
    print("=" * 60)
    print("LiDAR bounding box analysis completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()