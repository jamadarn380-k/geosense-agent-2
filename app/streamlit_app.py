import streamlit as st
import requests

MCP_SERVER_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="GeoSense GeoAI Assistant",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 GeoSense GeoAI Assistant")
st.caption("Phase 4 — MCP Tool Server + Streamlit Interface")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Geocode", "Weather", "Air Quality", "Route"]
)

with tab1:
    st.subheader("City Geocoding")
    city = st.text_input("Enter city name", value="Pune", key="geo_city")

    if st.button("Get Coordinates", key="geo_button"):
        try:
            response = requests.get(
                f"{MCP_SERVER_URL}/tools/geocode",
                params={"city": city}
            )
            response.raise_for_status()
            data = response.json()

            st.success(f"Found {data['city']}, {data['country']}")
            st.metric("Latitude", data["latitude"])
            st.metric("Longitude", data["longitude"])
            st.info(f"Timezone: {data['timezone']}")
        except Exception as e:
            st.error(f"Tool request failed: {e}")

with tab2:
    st.subheader("Current Weather")
    weather_city = st.text_input("Enter city name", value="Pune", key="weather_city")

    if st.button("Get Weather", key="weather_button"):
        try:
            response = requests.get(
                f"{MCP_SERVER_URL}/tools/weather",
                params={"city": weather_city}
            )
            response.raise_for_status()
            data = response.json()

            st.success(f"Weather for {data['city']}, {data['country']}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{data['temperature_c']} °C")
            col2.metric("Humidity", f"{data['humidity_percent']}%")
            col3.metric("Wind Speed", f"{data['wind_speed_kmh']} km/h")
        except Exception as e:
            st.error(f"Tool request failed: {e}")

with tab3:
    st.subheader("Air Quality")
    air_city = st.text_input("Enter city name", value="Pune", key="air_city")

    if st.button("Get Air Quality", key="air_button"):
        try:
            response = requests.get(
                f"{MCP_SERVER_URL}/tools/air-quality",
                params={"city": air_city}
            )
            response.raise_for_status()
            data = response.json()

            st.success(f"Air quality for {data['city']}, {data['country']}")
            col1, col2 = st.columns(2)
            col1.metric("European AQI", data["european_aqi"])
            col2.metric("PM2.5", f"{data['pm2_5']} µg/m³")
            st.metric("PM10", f"{data['pm10']} µg/m³")
        except Exception as e:
            st.error(f"Tool request failed: {e}")

with tab4:
    st.subheader("Route Planner")
    col1, col2 = st.columns(2)

    with col1:
        start_lat = st.number_input("Start latitude", value=18.51957, format="%.5f")
        start_lon = st.number_input("Start longitude", value=73.85535, format="%.5f")

    with col2:
        end_lat = st.number_input("End latitude", value=19.076, format="%.5f")
        end_lon = st.number_input("End longitude", value=72.8777, format="%.5f")

    if st.button("Calculate Route", key="route_button"):
        try:
            response = requests.get(
                f"{MCP_SERVER_URL}/tools/route",
                params={
                    "start_lat": start_lat,
                    "start_lon": start_lon,
                    "end_lat": end_lat,
                    "end_lon": end_lon
                }
            )
            response.raise_for_status()
            data = response.json()

            st.success("Route calculated successfully")
            col1, col2 = st.columns(2)
            col1.metric("Distance", f"{data['distance_km']} km")
            col2.metric("Duration", f"{data['duration_minutes']} minutes")
        except Exception as e:
            st.error(f"Tool request failed: {e}")