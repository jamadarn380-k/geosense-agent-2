"""
Convert processed LAZ point cloud to LAS format for QGIS.
"""

import os
import laspy

INPUT_PATH = "data/lidar/processed/study_area_classified.laz"
OUTPUT_PATH = "outputs/point_clouds/study_area_classified.las"


def main():
    print("Reading LAZ file...")

    las = laspy.read(INPUT_PATH)

    os.makedirs("outputs/point_clouds", exist_ok=True)

    print("Writing LAS file...")

    las.write(OUTPUT_PATH)

    print("Conversion completed.")
    print(f"Output file: {OUTPUT_PATH}")
    print(f"Total points: {len(las.points)}")


if __name__ == "__main__":
    main()