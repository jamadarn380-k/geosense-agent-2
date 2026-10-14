import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src" / "phase1_ml"))

from site_scorer import sites_df

features = []
for _, row in sites_df.iterrows():
    features.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(row["longitude"]), float(row["latitude"])]
        },
        "properties": {
            "location_id": int(row["location_id"]),
            "zone_name": str(row["zone_name"]),
            "label": int(row["label"])
        }
    })

geojson = {
    "type": "FeatureCollection",
    "features": features
}

out = ROOT / "sites.geojson"
out.write_text(json.dumps(geojson), encoding="utf-8")
print(f"Exported {len(features)} sites to {out}")