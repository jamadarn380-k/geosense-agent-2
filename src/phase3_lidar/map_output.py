"""
GeoSense Agent 2.0 - Phase 3
Generate a satellite basemap PNG from the unified site profile.
"""

import os
import json
import matplotlib.pyplot as plt
import contextily as cx
from pyproj import Transformer

PROFILE_PATH = "outputs/reports/enhanced_site_profile_32.77_-117.15.json"


def main():
    with open(PROFILE_PATH, "r") as file:
        profile = json.load(file)

    lat = profile["latitude"]
    lon = profile["longitude"]
    walkability = profile["walkability_score"]

    if walkability >= 5:
        color = "green"
        label = "High walkability"
    elif walkability >= 2:
        color = "orange"
        label = "Medium walkability"
    else:
        color = "red"
        label = "Low walkability"

    transformer = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:3857",
        always_xy=True,
    )

    x, y = transformer.transform(lon, lat)

    fig, ax = plt.subplots(figsize=(12, 10))

    buffer = 2000

    ax.set_xlim(x - buffer, x + buffer)
    ax.set_ylim(y - buffer, y + buffer)

    try:
        cx.add_basemap(
            ax,
            source=cx.providers.Esri.WorldImagery,
            zoom=15,
            attribution="Esri World Imagery",
        )
    except Exception as error:
        print("Satellite basemap could not load:", error)
        print("Creating map without satellite image.")

    ax.scatter(
        x,
        y,
        c=color,
        s=250,
        edgecolors="black",
        linewidths=1.5,
        zorder=5,
        label=label,
    )

    metrics_text = (
        f"Site Profile\n"
        f"Walkability: {walkability}\n"
        f"Building height: {profile['avg_building_height_m']} m\n"
        f"Canopy cover: {profile['canopy_cover_pct']}%\n"
        f"Impervious surface: {profile['impervious_surface_pct']}%\n"
        f"Slope risk: {profile['slope_risk_score']}\n"
        f"Vegetation: {profile['scene_composition'].get('vegetation', 0)}%\n"
        f"Road: {profile['scene_composition'].get('road', 0)}%\n"
        f"Sidewalk: {profile['scene_composition'].get('sidewalk', 0)}%"
    )

    ax.annotate(
        metrics_text,
        (x, y),
        textcoords="offset points",
        xytext=(20, 20),
        fontsize=9,
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor="white",
            edgecolor="black",
            alpha=0.88,
        ),
        zorder=6,
    )

    ax.set_title(
        "GeoSense Agent 2.0 - Unified Site Profile",
        fontsize=16,
        fontweight="bold",
        pad=15,
    )

    ax.legend(loc="lower right")

    ax.set_xlabel("Web Mercator Easting (m)")
    ax.set_ylabel("Web Mercator Northing (m)")

    os.makedirs("outputs/reports", exist_ok=True)

    output_path = "outputs/reports/site_map_satellite.png"

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    full_path = os.path.abspath(output_path)

    print(f"Satellite map saved to: {full_path}")

    os.startfile(full_path)


if __name__ == "__main__":
    main()