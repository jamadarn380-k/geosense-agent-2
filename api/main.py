from pathlib import Path
import sys

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.phase1_ml.site_scorer import score_location

app = FastAPI(title="GeoSense Site Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LocationRequest(BaseModel):
    latitude: float
    longitude: float


@app.get("/")
def home():
    return {"status": "GeoSense Site Intelligence API is running"}


@app.post("/score-location")
def score_site(request: LocationRequest):
    result = score_location(request.latitude, request.longitude)
    return result