"""
GeoSense Agent 2.0 - Phase 3
Automatic Mapillary street-view image downloader.
Tries multiple small areas in San Diego and downloads up to 20 images.
"""

import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

MAPILLARY_TOKEN = os.getenv("MAPILLARY_TOKEN")

if not MAPILLARY_TOKEN:
    raise ValueError(
        "MAPILLARY_TOKEN not found in .env file. "
        "Please add: MAPILLARY_TOKEN=your_token"
    )

OUTPUT_DIR = Path("data/streetview/images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_IMAGES = 20

GRAPH_URL = "https://graph.mapillary.com/images"

HEADERS = {
    "Authorization": f"OAuth {MAPILLARY_TOKEN}"
}

# Multiple very small areas in San Diego.
# Format: min_lon, min_lat, max_lon, max_lat
BBOX_LIST = [
    "-117.161,32.715,-117.158,32.718",
    "-117.164,32.720,-117.161,32.723",
    "-117.168,32.725,-117.165,32.728",
    "-117.155,32.730,-117.152,32.733",
    "-117.285,32.850,-117.282,32.853",
    "-117.275,32.840,-117.272,32.843",
    "-117.190,32.780,-117.187,32.783",
    "-117.130,32.790,-117.127,32.793",
]


def try_download_bbox(bbox):
    """Try one very small bbox and download available images."""

    params = {
        "bbox": bbox,
        "fields": "id,thumb_2048_url",
        "limit": 10,
    }

    print(f"\nTrying bbox: {bbox}")

    try:
        response = requests.get(
            GRAPH_URL,
            headers=HEADERS,
            params=params,
            timeout=30,
        )
    except Exception as e:
        print(f"Network error: {e}")
        return 0

    print(f"Status code: {response.status_code}")

    if response.status_code != 200:
        print("This bbox did not work.")
        return 0

    data = response.json()
    images = data.get("data", [])

    print(f"Found {len(images)} images.")

    downloaded = 0

    for image in images:

        if downloaded >= 5:
            break

        image_id = image.get("id")
        thumb_url = image.get("thumb_2048_url")

        if not image_id or not thumb_url:
            continue

        file_path = OUTPUT_DIR / f"mapillary_{image_id}.jpg"

        if file_path.exists():
            print(f"Already downloaded: {file_path.name}")
            downloaded += 1
            continue

        try:
            img_response = requests.get(thumb_url, timeout=30)

            if img_response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(img_response.content)

                print(f"Saved: {file_path.name}")
                downloaded += 1

            else:
                print(
                    f"Download failed for {image_id}. "
                    f"Status: {img_response.status_code}"
                )

        except Exception as e:
            print(f"Error downloading {image_id}: {e}")

        time.sleep(0.3)

    return downloaded


def main():
    print("=" * 60)
    print("GeoSense Agent 2.0 - Automatic Mapillary Downloader")
    print("=" * 60)

    total_downloaded = 0

    for bbox in BBOX_LIST:

        if total_downloaded >= MAX_IMAGES:
            break

        downloaded = try_download_bbox(bbox)
        total_downloaded += downloaded

        print(f"Images downloaded so far: {total_downloaded}")

        time.sleep(1)

    print()
    print("=" * 60)
    print(f"Finished. Total images downloaded: {total_downloaded}")
    print(f"Images folder: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()