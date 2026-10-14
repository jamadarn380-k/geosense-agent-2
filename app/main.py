from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(
    title="GeoSense MCP Tool Server",
    description="Phase 4 tool server for geospatial AI workflows",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "service": "GeoSense MCP Tool Server",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/tools")
def list_tools():
    return {
        "tools": [
            {"name": "geocode_city", "description": "Convert a city name to coordinates"},
            {"name": "get_weather", "description": "Get current weather for a city"},
            {"name": "get_air_quality", "description": "Get air quality for a city"},
            {"name": "get_route", "description": "Get driving distance and duration between two coordinates"}
        ]
    }

@app.get("/tools/geocode")
async def geocode_city(city: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "en", "format": "json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    if not data.get("results"):
        raise HTTPException(status_code=404, detail=f"City not found: {city}")

    result = data["results"][0]

    return {
        "city": result.get("name"),
        "country": result.get("country"),
        "latitude": result.get("latitude"),
        "longitude": result.get("longitude"),
        "timezone": result.get("timezone")
    }

@app.get("/tools/weather")
async def get_weather(city: str):
    geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
    geocode_params = {"name": city, "count": 1, "language": "en", "format": "json"}

    async with httpx.AsyncClient() as client:
        geo_response = await client.get(geocode_url, params=geocode_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

    if not geo_data.get("results"):
        raise HTTPException(status_code=404, detail=f"City not found: {city}")

    location = geo_data["results"][0]
    lat = location["latitude"]
    lon = location["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    }

    async with httpx.AsyncClient() as client:
        weather_response = await client.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

    current = weather_data["current"]

    return {
        "city": location.get("name"),
        "country": location.get("country"),
        "latitude": lat,
        "longitude": lon,
        "temperature_c": current.get("temperature_2m"),
        "humidity_percent": current.get("relative_humidity_2m"),
        "wind_speed_kmh": current.get("wind_speed_10m"),
        "weather_code": current.get("weather_code")
    }

@app.get("/tools/air-quality")
async def get_air_quality(city: str):
    geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
    geocode_params = {"name": city, "count": 1, "language": "en", "format": "json"}

    async with httpx.AsyncClient() as client:
        geo_response = await client.get(geocode_url, params=geocode_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

    if not geo_data.get("results"):
        raise HTTPException(status_code=404, detail=f"City not found: {city}")

    location = geo_data["results"][0]
    lat = location["latitude"]
    lon = location["longitude"]

    air_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    air_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "european_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide"
    }

    async with httpx.AsyncClient() as client:
        air_response = await client.get(air_url, params=air_params)
        air_response.raise_for_status()
        air_data = air_response.json()

    current = air_data["current"]

    return {
        "city": location.get("name"),
        "country": location.get("country"),
        "latitude": lat,
        "longitude": lon,
        "european_aqi": current.get("european_aqi"),
        "pm10": current.get("pm10"),
        "pm2_5": current.get("pm2_5"),
        "carbon_monoxide": current.get("carbon_monoxide"),
        "nitrogen_dioxide": current.get("nitrogen_dioxide")
    }

@app.get("/tools/route")
async def get_route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float
):
    url = "https://router.project-osrm.org/route/v1/driving/"
    request_url = f"{url}{start_lon},{start_lat};{end_lon},{end_lat}?overview=false"

    async with httpx.AsyncClient() as client:
        response = await client.get(request_url)
        response.raise_for_status()
        data = response.json()

    if data.get("code") != "Ok" or not data.get("routes"):
        raise HTTPException(status_code=404, detail="No route found")

    route = data["routes"][0]

    return {
        "distance_km": round(route["distance"] / 1000, 2),
        "duration_minutes": round(route["duration"] / 60, 2),
        "start": {"latitude": start_lat, "longitude": start_lon},
        "end": {"latitude": end_lat, "longitude": end_lon}
    }