"""
GeoSense Agent 2.0 - Phase 3
PDAL LiDAR preprocessing pipeline.

Input:
data/lidar/raw/study_area.laz

Output:
data/lidar/processed/study_area_classified.laz

Pipeline:
1. Decimation to reduce memory usage
2. Statistical outlier removal
3. SMRF ground classification
4. Height Above Ground
5. Write classified LAZ
"""

import json
from pathlib import Path

import pdal


INPUT_LAZ = Path("data/lidar/raw_small/split_1_1.laz")
OUTPUT_LAZ = Path("data/lidar/processed/study_area_classified.laz")

OUTPUT_LAZ.parent.mkdir(parents=True, exist_ok=True)


def build_pipeline(input_laz, output_laz):
    """
    Build the PDAL preprocessing pipeline.

    Parameters:
    input_laz: raw LiDAR point cloud
    output_laz: cleaned and classified output point cloud
    """

    pipeline = {
        "pipeline": [
            str(input_laz),

            # Reduce memory usage by keeping every 2nd point.
            {
                "type": "filters.decimation",
                "step": 8,
            },

            # Remove statistical outliers / noise points.
            {
                "type": "filters.outlier",
                "method": "statistical",
                "mean_k": 8,
                "multiplier": 2.5,
            },

            # Classify ground points using SMRF.
            {
                "type": "filters.smrf",
            },

            # Calculate Height Above Ground.
            {
                "type": "filters.hag_nn",
            },

            # Write the processed and classified LAZ file.
            {
                "type": "writers.las",
                "filename": str(output_laz),
                "extra_dims": "all",
            },
        ]
    }

    return pipeline


def run_pipeline():
    """
    Build, serialise, and execute the PDAL pipeline.
    """

    print("=" * 60)
    print("GeoSense Agent 2.0 - LiDAR Preprocessing Pipeline")
    print("=" * 60)

    print(f"Input file: {INPUT_LAZ}")
    print(f"Output file: {OUTPUT_LAZ}")

    if not INPUT_LAZ.exists():
        raise FileNotFoundError(
            f"Input LiDAR file not found: {INPUT_LAZ}"
        )

    pipeline_dict = build_pipeline(INPUT_LAZ, OUTPUT_LAZ)

    pipeline_json = json.dumps(pipeline_dict, indent=2)

    pipeline_json_path = Path(
        "data/lidar/processed/pdal_pipeline.json"
    )

    with open(pipeline_json_path, "w", encoding="utf-8") as f:
        f.write(pipeline_json)

    print(f"Pipeline JSON saved: {pipeline_json_path}")

    pipeline = pdal.Pipeline(pipeline_json)

    print("Running PDAL pipeline...")

    processed_points = pipeline.execute()

    print()
    print("=" * 60)
    print(f"Processed {processed_points} points")
    print(f"Output file created: {OUTPUT_LAZ}")
    print("=" * 60)

    return processed_points


if __name__ == "__main__":
    run_pipeline()