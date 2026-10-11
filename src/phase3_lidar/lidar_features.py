"""
GeoSense Agent 2.0 - Phase 3
LiDAR feature extraction and grid metrics.

Input:
data/lidar/processed/study_area_classified.laz

Output:
Prints grid cell count and first three grid results.
"""

import numpy as np
import laspy


INPUT_LAZ = "data/lidar/processed/study_area_classified.laz"

CELL_SIZE_M = 50


def load_classified_cloud(filepath):
    """
    Load classified LAZ file and return required arrays.
    """

    las = laspy.read(filepath)

    x = np.asarray(las.x)
    y = np.asarray(las.y)
    z = np.asarray(las.z)

    try:
        hag = np.asarray(las.HeightAboveGround)
    except Exception:
        hag = np.asarray(las.user_data)

    num_returns = np.asarray(las.number_of_returns)
    return_num = np.asarray(las.return_number)

    return x, y, z, hag, num_returns, return_num


def classify_points(hag, num_returns, return_num):
    """
    Classify LiDAR points.

    0 = ground
    1 = vegetation
    2 = building
    """

    labels = np.zeros(len(hag), dtype=int)

    # Ground: below 0.5 m
    labels[hag < 0.5] = 0

    # Low vegetation: 0.5 m to 2.5 m
    low_veg = (hag >= 0.5) & (hag < 2.5)
    labels[low_veg] = 1

    # Vegetation: 2.5 m or more with multiple returns
    high_veg = (hag >= 2.5) & (num_returns > 1)
    labels[high_veg] = 1

    # Building: 2.5 m or more with single return
    building = (hag >= 2.5) & (num_returns == 1)
    labels[building] = 2

    return labels


def compute_grid_metrics(x, y, hag, labels, cell_size_m=50):
    """
    Compute average building height and canopy cover per grid cell.
    """

    min_x = np.min(x)
    min_y = np.min(y)

    grid_x = ((x - min_x) / cell_size_m).astype(int)
    grid_y = ((y - min_y) / cell_size_m).astype(int)

    unique_cells = np.unique(
        np.vstack((grid_x, grid_y)).T,
        axis=0,
    )

    grid_results = []

    for cell in unique_cells:

        cx = cell[0]
        cy = cell[1]

        mask = (grid_x == cx) & (grid_y == cy)

        cell_hag = hag[mask]
        cell_labels = labels[mask]

        building_heights = cell_hag[cell_labels == 2]

        if len(building_heights) > 0:
            avg_building_height = np.mean(building_heights)
        else:
            avg_building_height = 0.0

        canopy_points = np.sum(cell_labels == 1)
        total_points = len(cell_labels)

        if total_points > 0:
            canopy_cover_pct = (canopy_points / total_points) * 100
        else:
            canopy_cover_pct = 0.0

        grid_results.append({
            "grid_x": int(cx),
            "grid_y": int(cy),
            "avg_building_height_m": float(avg_building_height),
            "canopy_cover_pct": float(canopy_cover_pct),
        })

    return grid_results


def main():
    print("=" * 60)
    print("GeoSense Agent 2.0 - LiDAR Feature Extraction")
    print("=" * 60)

    print(f"Loading classified cloud: {INPUT_LAZ}")

    x, y, z, hag, num_returns, return_num = load_classified_cloud(INPUT_LAZ)

    print(f"Total LiDAR points loaded: {len(x)}")

    labels = classify_points(hag, num_returns, return_num)

    print("Classifying points completed.")

    grid_results = compute_grid_metrics(
        x,
        y,
        hag,
        labels,
        cell_size_m=CELL_SIZE_M,
    )

    print()
    print(f"Computed metrics for {len(grid_results)} grid cells")

    print()
    print("First three grid cells:")

    for i, cell in enumerate(grid_results[:3], start=1):
        print(f"Cell {i}: {cell}")

    print()
    print("=" * 60)
    print("LiDAR feature extraction completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()