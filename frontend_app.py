import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="GeoSense Site Intelligence",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 GeoSense Site Intelligence")
st.caption("ML-based site scoring using Phase 1 model")

st.sidebar.header("Enter Location")
latitude = st.sidebar.number_input(
    "Latitude",
    value=18.500419,
    format="%.6f"
)

longitude = st.sidebar.number_input(
    "Longitude",
    value=73.765995,
    format="%.6f"
)

if st.sidebar.button("Get Site Score"):
    try:
        response = requests.post(
            f"{API_URL}/score-location",
            json={
                "latitude": latitude,
                "longitude": longitude
            }
        )
        response.raise_for_status()
        result = response.json()

        st.success("Site score generated successfully")

        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Opportunity Score",
            f"{result['opportunity_score']}/10"
        )
        col2.metric(
            "Risk Score",
            f"{result['risk_score']}/10"
        )
        col3.metric(
            "Verdict",
            result["verdict"]
        )

        st.subheader("Nearest Dataset Location")
        st.write(f"**Location ID:** {result['nearest_location_id']}")
        st.write(f"**Zone:** {result['zone_name']}")
        st.write(
            f"**Nearest Coordinates:** "
            f"{result['nearest_latitude']}, "
            f"{result['nearest_longitude']}"
        )

        st.subheader("Features Used")
        st.json(result["features"])

    except Exception as e:
        st.error(f"API request failed: {e}")