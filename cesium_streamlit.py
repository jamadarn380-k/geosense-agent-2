import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="GeoSense Cesium Digital Twin",
    page_icon="🛰️",
    layout="wide"
)

st.title("🛰️ GeoSense Digital Twin")
st.caption("Phase 1 EV suitability + Phase 2 satellite land-cover + Phase 4 Cesium 3D globe")

BASE = Path(__file__).parent
PLOTS = BASE / "phase2_outputs" / "plots"
TABLES = BASE / "phase2_outputs" / "tables"
MCP_URL = "http://localhost:8001/tools/score_location"

tab1, tab2, tab3, tab4 = st.tabs(
    ["🌍 EV Charging Sites", "🗺️ Land Cover Maps", "📈 Change Detection", "🧠 Model Performance"]
)

# ---------------- TAB 1: Phase 1 + Phase 4 ----------------
with tab1:
    col1, col2 = st.columns([3, 1])

    with col1:
        latitude = st.number_input("Latitude", value=18.5204, format="%.5f")
        longitude = st.number_input("Longitude", value=73.8567, format="%.5f")

    with col2:
        st.write("")
        st.write("")
        check = st.button("Check Charging Site")

    if check:
        with st.spinner("Checking Phase 1 suitability model..."):
            try:
                response = requests.post(
                    MCP_URL,
                    json={"latitude": latitude, "longitude": longitude},
                    timeout=30,
                )
                result = response.json()["result"]
                st.success(
                    f"{result['verdict']} — Opportunity Score: {result['opportunity_score']} "
                    f"(Probability: {result['probability_good_site']:.1%})"
                )
                st.write(f"**Zone:** {result['zone_name']}")
                st.write(f"**Risk Score:** {result['risk_score']}")
            except Exception as e:
                st.error(f"MCP Server error: {e}")

    components.iframe(
              f"http://localhost:8000/cesium_app.html?lat={latitude}&lon={longitude}&v=6",
        height=650,
        scrolling=False
    )
    st.caption("Green = GOOD sites, Red = Bad sites, Yellow = selected location.")

# ---------------- TAB 2: Phase 2 land cover ----------------
with tab2:
    st.subheader("U-Net Land Cover Classification — Pune")
    year = st.radio("Select year", ["2018", "2023", "2025"], horizontal=True)
    img = PLOTS / f"label_map_{year}.png"
    if img.exists():
        st.image(str(img), use_container_width=True)
    else:
        st.warning(f"Image not found: {img}")

# ---------------- TAB 3: Phase 2 change detection ----------------
with tab3:
    st.subheader("Land Cover Change: 2018 → 2025")

    csv1 = TABLES / "landcover_summary_2018_2025.csv"
    csv2 = TABLES / "change_detection_overall_2018_2025.csv"
    csv3 = TABLES / "landcover_transitions_2018_2025.csv"

    if csv1.exists():
        st.write("**Land Cover Summary**")
        st.dataframe(pd.read_csv(csv1))
    if csv2.exists():
        st.write("**Overall Change Detection**")
        st.dataframe(pd.read_csv(csv2))
    if csv3.exists():
        st.write("**Land Cover Transitions**")
        st.dataframe(pd.read_csv(csv3))

    st.subheader("Charts")
    c1, c2 = st.columns(2)
    with c1:
        p = PLOTS / "landcover_comparison_2018_2025.png"
        if p.exists():
            st.image(str(p), caption="Land cover comparison", use_container_width=True)
    with c2:
        p = PLOTS / "ndvi_change_2018_2025.png"
        if p.exists():
            st.image(str(p), caption="NDVI change", use_container_width=True)

# ---------------- TAB 4: Phase 2 model ----------------
with tab4:
    st.subheader("U-Net Training & Evaluation")
    c1, c2 = st.columns(2)
    with c1:
        p = PLOTS / "unet_training_curves.png"
        if p.exists():
            st.image(str(p), caption="Training curves", use_container_width=True)
    with c2:
        p = PLOTS / "unet_confusion_matrix_2025.png"
        if p.exists():
            st.image(str(p), caption="Confusion matrix (2025)", use_container_width=True)