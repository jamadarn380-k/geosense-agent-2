import os
from pathlib import Path

from dotenv import load_dotenv
import streamlit as st

load_dotenv()

CESIUM_TOKEN = os.getenv("CESIUM_ION_TOKEN")

st.set_page_config(
    page_title="GeoSense Cesium Digital Twin",
    page_icon="🛰️",
    layout="wide"
)

st.title("🛰️ GeoSense Cesium Digital Twin")
st.caption("Phase 4 — CesiumJS 3D globe embedded in Streamlit")

if not CESIUM_TOKEN:
    st.error("CESIUM_ION_TOKEN is missing. Add your Cesium ion token in the .env file.")
    st.stop()

latitude = st.number_input("Latitude", value=18.5204, format="%.5f")
longitude = st.number_input("Longitude", value=73.8567, format="%.5f")
height = st.slider("Camera height (meters)", 500, 20000, 5000)

cesium_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <script src="/Documents/geosense/Build/Cesium/Cesium.js"></script>
    <link href="/Documents/geosense/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
    <style>
        html, body, #cesiumContainer {{
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }}
    </style>
</head>
<body>
    <div id="cesiumContainer"></div>

    <script>
        Cesium.Ion.defaultAccessToken = "{CESIUM_TOKEN}";

        const esriProvider = new Cesium.UrlTemplateImageryProvider({{
            url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}",
            credit: "Esri, Maxar, Earthstar Geographics"
        }});

        const viewer = new Cesium.Viewer("cesiumContainer", {{
            animation: false,
            timeline: false,
            baseLayerPicker: false,
            geocoder: false,
            homeButton: false,
            sceneModePicker: false,
            navigationHelpButton: false,
            fullscreenButton: false,
            infoBox: false,
            selectionIndicator: false,
            baseLayer: new Cesium.ImageryLayer(esriProvider)
        }});

        window.viewer = viewer;

        viewer.camera.setView({{
            destination: Cesium.Cartesian3.fromDegrees(
                {longitude}, {latitude}, {height}
            )
        }});

        viewer.entities.add({{
            name: "Selected Location",
            position: Cesium.Cartesian3.fromDegrees({longitude}, {latitude}),
            point: {{
                pixelSize: 14,
                color: Cesium.Color.RED,
                outlineColor: Cesium.Color.WHITE,
                outlineWidth: 2
            }},
            label: {{
                text: "Pune Location",
                font: "14pt sans-serif",
                fillColor: Cesium.Color.WHITE,
                outlineColor: Cesium.Color.BLACK,
                outlineWidth: 2,
                style: Cesium.LabelStyle.FILL_AND_OUTLINE,
                pixelOffset: new Cesium.Cartesian2(0, -25)
            }}
        }});

        viewer.scene.renderError.addEventListener(function(scene, error) {{
            console.error("Cesium render error:", error);
        }});
    </script>
</body>
</html>
"""

# Save the Cesium app where the local server can serve it
project_dir = Path(r"C:\Users\jamad\Documents\geosense")
cesium_file = project_dir / "cesium_app.html"
cesium_file.write_text(cesium_html, encoding="utf-8")

st.iframe("http://localhost:8000/Documents/geosense/cesium_app.html", height=650)

st.info("Change latitude, longitude, or camera height to move the red marker.")s