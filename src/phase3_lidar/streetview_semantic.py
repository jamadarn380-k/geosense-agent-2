"""
GeoSense Agent 2.0 - Phase 3
Street-level semantic segmentation and walkability scoring.
"""

import os
import requests
import torch
from PIL import Image
from transformers import AutoImageProcessor, SegformerForSemanticSegmentation

MODEL_NAME = "nvidia/segformer-b0-finetuned-cityscapes-1024-1024"

CLASS_NAMES = {
    0: "road",
    1: "sidewalk",
    2: "building",
    8: "vegetation",
    10: "sky",
    13: "car",
}

processor = None
model = None

MAPILLARY_TOKEN = os.getenv("MAPILLARY_TOKEN")

if not MAPILLARY_TOKEN and os.path.exists("config/mapillary_token.txt"):
    with open("config/mapillary_token.txt", "r") as f:
        MAPILLARY_TOKEN = f.read().strip()


def _load_model():
    global processor, model

    if processor is None or model is None:
        print("Loading SegFormer model...")

        processor = AutoImageProcessor.from_pretrained(
            MODEL_NAME,
            use_safetensors=True,
        )

        model = SegformerForSemanticSegmentation.from_pretrained(
            MODEL_NAME,
            use_safetensors=True,
        )

        model.eval()

    return processor, model


def find_images_in_bbox(min_lat, min_lon, max_lat, max_lon, limit=10):
    url = "https://graph.mapillary.com/images"

    params = {
        "access_token": MAPILLARY_TOKEN,
        "bbox": f"{min_lon},{min_lat},{max_lon},{max_lat}",
        "fields": "id,computed_geometry,thumb_1024_url",
        "limit": limit,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Mapillary API error: {response.status_code}")
        return []

    data = response.json()

    images = []

    for item in data.get("data", []):
        images.append({
            "id": item["id"],
            "thumb_url": item.get("thumb_1024_url"),
        })

    return images


def download_image(image_info):
    image_id = image_info["id"]
    thumb_url = image_info["thumb_url"]

    if thumb_url is None:
        return None

    os.makedirs("data/streetview/images", exist_ok=True)

    image_path = f"data/streetview/images/mapillary_{image_id}.jpg"

    if os.path.exists(image_path):
        return image_path

    response = requests.get(thumb_url)

    if response.status_code != 200:
        return None

    with open(image_path, "wb") as f:
        f.write(response.content)

    return image_path


def classify_image(image_path):
    processor, model = _load_model()

    image = Image.open(image_path).convert("RGB")

    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits

    predicted = logits.argmax(dim=1)

    predicted = predicted.squeeze(0)

    total_pixels = predicted.numel()

    composition = {}

    for class_id, class_name in CLASS_NAMES.items():
        count = int((predicted == class_id).sum())
        percent = round((count / total_pixels) * 100, 1)
        composition[class_name] = percent

    return composition


def compute_walkability_score(composition):
    sidewalk = composition.get("sidewalk", 0)
    vegetation = composition.get("vegetation", 0)
    car = composition.get("car", 0)

    score = (sidewalk * 0.4 + vegetation * 0.3 - car * 0.2) / 5

    score = max(0, min(10, score))

    return round(score, 2)


def analyze_location(lat, lon, radius_deg=0.0015):
    print()
    print("=" * 60)
    print(f"Analyzing location: {lat}, {lon}")
    print("=" * 60)

    min_lat = lat - radius_deg
    max_lat = lat + radius_deg
    min_lon = lon - radius_deg
    max_lon = lon + radius_deg

    images = find_images_in_bbox(min_lat, min_lon, max_lat, max_lon, limit=10)

    if not images:
        return {
            "latitude": lat,
            "longitude": lon,
            "error": "No street-level imagery found nearby.",
        }

    compositions = []

    for image_info in images:
        image_path = download_image(image_info)

        if image_path is None:
            continue

        composition = classify_image(image_path)
        compositions.append(composition)

    if not compositions:
        return {
            "latitude": lat,
            "longitude": lon,
            "error": "No images could be classified.",
        }

    scene_composition = {}

    for class_name in CLASS_NAMES.values():
        values = [c.get(class_name, 0) for c in compositions]
        average = round(sum(values) / len(values), 1)
        scene_composition[class_name] = average

    walkability_score = compute_walkability_score(scene_composition)

    return {
        "latitude": lat,
        "longitude": lon,
        "images_analyzed": len(compositions),
        "scene_composition": scene_composition,
        "walkability_score": walkability_score,
    }


def main():
    print("=" * 60)
    print("GeoSense Agent 2.0 - Street Walkability Analysis")
    print("=" * 60)

    locations = [
        (13.0827, 80.2707),
        (13.0500, 80.2824),
        (13.0418, 80.2341),
    ]

    for lat, lon in locations:
        result = analyze_location(lat, lon)
        print()
        print("Result:")
        print(result)

    print()
    print("=" * 60)
    print("Walkability analysis completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()