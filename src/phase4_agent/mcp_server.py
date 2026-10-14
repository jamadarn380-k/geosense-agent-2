import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src" / "phase1_ml"))

from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn

from site_scorer import score_location

app = FastAPI(title="GeoSense Agent MCP Server", version="1.0")


class LocationInput(BaseModel):
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")


@app.post("/tools/score_location", summary="Score a location for EV charging suitability")
def tool_score_location(payload: LocationInput):
    """Score a location using the Phase 1 EV charging suitability model.

    Args:
        payload: latitude and longitude.

    Returns:
        dict with the Phase 1 suitability result.
    """
    result = score_location(payload.latitude, payload.longitude)
    return {
        "tool": "score_location",
        "input": {"latitude": payload.latitude, "longitude": payload.longitude},
        "result": result,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)