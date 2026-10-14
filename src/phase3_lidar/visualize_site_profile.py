"""
GeoSense Agent 2.0 - Phase 3
Visualize unified site profile as an interactive map (auto-open).
"""

import os
import json
import webbrowser
import folium

PROFILE_PATH = "outputs/reports/enhanced_site_profile_32.77_-117.15.json"


def main():
    with open(PROFILE_PATH, "r") as f:
        profile = json.load(f)

    lat = profile["latitude"]
    lon = profile["longitude"]

    walkability = profile["walkability_score"]

    if walkability >= 5:
        color = "green"
    elif walkability >= 2:
        color = "orange"
    else:
        color = "red"

    m = folium.Map(
        location=[lat, lon],
        zoom_start=15,
    )

    popup_html = f"""
    <h3>Site Profile</h3>
    <b>Walkability Score:</b> {walkability}<br>
    <b>Avg Building Height:</b> {profile['avg_building_height_m']} m<br>
    <b>Canopy Cover:</b> {profile['canopy_cover_pct']}%<br>
    <b>Impervious Surface:</b> {profile['impervious_surface_pct']}%<br>
    <b>Slope Risk:</b> {profile['slope_risk_score']}<br>
    <b>Vegetation:</b> {profile['scene_composition'].get('vegetation', 0)}%<br>
    <b>Road:</b> {profile['scene_composition'].get('road', 0)}%<br>
    <b>Sidewalk:</b> {profile['scene_composition'].get('sidewalk', 0)}%<br>
    """

    folium.CircleMarker(
        location=[lat, lon],
        radius=15,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip="Click for site details",
    ).add_to(m)

    os.makedirs("outputs/reports", exist_ok=True)

    output_path = "outputs/reports/site_map.html"

    m.save(output_path)

    full_path = os.path.abspath(output_path)

    webbrowser.open_new_tab(f"file:///{full_path}")

    print(f"Map saved and opened: {output_path}")


if __name__ == "__main__":
    main()