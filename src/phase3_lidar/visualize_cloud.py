"""
GeoSense Agent 2.0 - Phase 3
Colour-coded LiDAR point cloud visualisation.

Input:
data/lidar/processed/study_area_classified.laz

Output:
outputs/point_clouds/study_area_colored.ply

Colours:
Ground = brown
Vegetation = green
Building = grey
"""

import os
import numpy as np
import laspy
import open3d as o3d


INPUT_LAZ = "data/lidar/processed/study_area_classified.laz"

OUTPUT_PLY = "outputs/point_clouds/study_area_colored.ply"

os.makedirs(os.path.dirname(OUTPUT_PLY), exist_ok=True)


def load_cloud(filepath):
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
    labels = np.zeros(len(hag), dtype=int)

    labels[hag < 0.5] = 0

    low_veg = (hag >= 0.5) & (hag < 2.5)
    labels[low_veg] = 1

    high_veg = (hag >= 2.5) & (num_returns > 1)
    labels[high_veg] = 1

    building = (hag >= 2.5) & (num_returns == 1)
    labels[building] = 2

    return labels


def create_colored_ply(x, y, z, labels, output_ply):
    xyz = np.column_stack((x, y, z))

    colors = np.zeros((len(labels), 3))

    # Ground = brown
    colors[labels == 0] = [0.55, 0.35, 0.20]

    # Vegetation = green
    colors[labels == 1] = [0.20, 0.70, 0.30]

    # Building = grey
    colors[labels == 2] = [0.70, 0.70, 0.70]

    pcd = o3d.geometry.PointCloud()

    pcd.points = o3d.utility.Vector3dVector(xyz)

    pcd.colors = o3d.utility.Vector3dVector(colors)

    o3d.io.write_point_cloud(output_ply, pcd)

    print(f"Saved coloured point cloud: {output_ply}")


def main():
    print("=" * 60)
    print("GeoSense Agent 2.0 - LiDAR Visualisation")
    print("=" * 60)

    print(f"Loading classified cloud: {INPUT_LAZ}")

    x, y, z, hag, num_returns, return_num = load_cloud(INPUT_LAZ)

    print(f"Total LiDAR points loaded: {len(x)}")

    labels = classify_points(hag, num_returns, return_num)

    print("Classifying points completed.")

    create_colored_ply(x, y, z, labels, OUTPUT_PLY)

    print()
    print("=" * 60)
    print("LiDAR visualisation completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()