"""
GeoSense Agent 2.0 - Phase 3
SAM rooftop/object detection demo using a Mapillary street image.

Input:
One Mapillary image from data/streetview/images/

Output:
Prints number of candidate segments and estimates volume.
Saves SAM overlay image.
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator

load_dotenv()

SAM_CHECKPOINT = os.getenv(
    "SAM_CHECKPOINT_PATH",
    "models/saved/sam/sam_vit_b_01ec64.pth",
)

IMAGE_PATH = "data/streetview/images/mapillary_1021272693364148.jpg"

OUTPUT_IMAGE = "outputs/reports/sam_segmentation_result.png"

AVG_BUILDING_HEIGHT_M = 8.4

PIXEL_AREA_M2 = 0.25

MIN_MASK_AREA = 40
MAX_MASK_AREA = 4000

os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)

generator = None


def load_sam_generator():
    sam = sam_model_registry["vit_b"](
        checkpoint=SAM_CHECKPOINT
    )

    generator = SamAutomaticMaskGenerator(sam)

    return generator


def detect_rooftops(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    print(f"Running SAM on image: {image_path}")

    masks = generator.generate(image)

    plt.figure(figsize=(12, 8))

    plt.imshow(image)

    for mask in masks:

        m = mask["segmentation"]

        plt.imshow(
            m,
            alpha=0.35,
        )

    plt.axis("off")

    plt.savefig(
        OUTPUT_IMAGE,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Saved SAM output image: {OUTPUT_IMAGE}")

    candidates = []

    for mask in masks:

        area = int(mask["area"])

        if MIN_MASK_AREA <= area <= MAX_MASK_AREA:
            candidates.append(mask)

    print(f"Detected {len(candidates)} candidate rooftop segments")

    return candidates


def estimate_building_volume(rooftop_mask, avg_height_m, pixel_area_m2=0.25):
    area = int(rooftop_mask["area"])

    footprint_area_m2 = area * pixel_area_m2

    height_m = avg_height_m

    volume_m3 = footprint_area_m2 * height_m

    return {
        "footprint_area_m2": footprint_area_m2,
        "height_m": height_m,
        "volume_m3": volume_m3,
    }


def main():
    print("=" * 60)
    print("GeoSense Agent 2.0 - SAM Rooftop Detection Demo")
    print("=" * 60)

    global generator

    print(f"Loading SAM checkpoint: {SAM_CHECKPOINT}")

    generator = load_sam_generator()

    candidates = detect_rooftops(IMAGE_PATH)

    if len(candidates) == 0:
        print("No candidate segments found.")
        return

    first_rooftop = candidates[0]

    result = estimate_building_volume(
        first_rooftop,
        AVG_BUILDING_HEIGHT_M,
        PIXEL_AREA_M2,
    )

    print()
    print("First rooftop estimate:")
    print(result)

    print()
    print("=" * 60)
    print("SAM rooftop detection demo completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()