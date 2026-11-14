\# GeoSense Agent 2.0



GeoSense is a geospatial site intelligence project that helps identify suitable locations using satellite imagery, land-cover data, and machine learning.



\## What This Project Does



\- Analyzes locations using geospatial data.

\- Uses an XGBoost model to predict site suitability.

\- Generates an Opportunity Score and Risk Score.

\- Shows whether a location is a GOOD SITE or POOR SITE.

\- Provides a Streamlit interface for easy interaction.

\- Includes a Cesium-based digital twin with land-cover overlays.



\## Tech Stack



\- Python

\- pandas

\- scikit-learn

\- XGBoost

\- joblib

\- FastAPI

\- Streamlit

\- CesiumJS



\## Project Structure



\- `src/` — core geospatial and ML modules.

\- `api/` — FastAPI backend.

\- `frontend\_app.py` — Streamlit frontend.

\- `models/saved/` — trained ML model files.

\- `data/processed/` — processed site dataset.

\- `notebooks/` — data analysis and model training notebooks.

\- `outputs/` — generated results and visual outputs.



\## How to Run



\### Backend



```bash

uvicorn api.main:app --reload --port 8000

```



\### Frontend



```bash

streamlit run frontend\_app.py

```



Open:



```text

http://localhost:8501

```



Click \*\*Get Site Score\*\* to generate a site score.



\## Model Performance



The site suitability model was trained using 929 samples and achieved 97.8% accuracy using XGBoost.



\## Status



Phase 1 and Phase 2 are complete.



\## GitHub Repository



This project is available here:



https://github.com/jamadarn380-k/geosense-agent-2

