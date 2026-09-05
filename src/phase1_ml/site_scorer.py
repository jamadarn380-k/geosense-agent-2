import joblib
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\jamad\Documents\geosense")

MODEL_PATH = PROJECT_ROOT / "models" / "site_suitability_model.pkl"
SCALER_PATH = PROJECT_ROOT / "models" / "site_feature_scaler.pkl"
FEATURE_PATH = PROJECT_ROOT / "models" / "site_feature_list.pkl"
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "labelled_sites.csv"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_cols = joblib.load(FEATURE_PATH)

sites_df = pd.read_csv(DATA_PATH)

def score_location(latitude, longitude):
    """
    जवळच्या dataset locationची features घेऊन त्या siteचा
    Opportunity Score, Risk Score आणि Verdict देतो.
    """

    distances = (
        (sites_df["latitude"] - latitude) ** 2
        + (sites_df["longitude"] - longitude) ** 2
    )

    nearest_index = distances.idxmin()
    nearest_site = sites_df.loc[nearest_index]

    X = pd.DataFrame(
        [nearest_site[feature_cols].to_dict()],
        columns=feature_cols
    )

    X_scaled = scaler.transform(X)

    probability_good_site = float(model.predict_proba(X_scaled)[0, 1])

    opportunity_score = round(probability_good_site * 10, 2)
    risk_score = round((1 - probability_good_site) * 10, 2)

    if probability_good_site >= 0.50:
        verdict = "GOOD SITE"
    else:
        verdict = "POOR SITE"

    return {
        "input_latitude": latitude,
        "input_longitude": longitude,
        "nearest_location_id": int(nearest_site["location_id"]),
        "nearest_latitude": float(nearest_site["latitude"]),
        "nearest_longitude": float(nearest_site["longitude"]),
        "zone_name": nearest_site["zone_name"],
        "opportunity_score": opportunity_score,
        "risk_score": risk_score,
        "verdict": verdict,
        "probability_good_site": probability_good_site,
        "features": nearest_site[feature_cols].to_dict(),
    }

if __name__ == "__main__":
    test_latitude = 18.500419
    test_longitude = 73.765995

    result = score_location(test_latitude, test_longitude)

    print("=" * 70)
    print("GEOSENSE SITE SCORER")
    print("=" * 70)

    print("\nINPUT LOCATION")
    print(f"Latitude:  {result['input_latitude']}")
    print(f"Longitude: {result['input_longitude']}")

    print("\nNEAREST DATASET LOCATION")
    print(f"Location ID: {result['nearest_location_id']}")
    print(f"Latitude:    {result['nearest_latitude']}")
    print(f"Longitude:   {result['nearest_longitude']}")
    print(f"Zone:        {result['zone_name']}")

    print("\nMODEL RESULT")
    print(f"Good-site probability: {result['probability_good_site']:.4f}")
    print(f"Opportunity Score:     {result['opportunity_score']}/10")
    print(f"Risk Score:            {result['risk_score']}/10")
    print(f"Verdict:               {result['verdict']}")

    print("\nFEATURES USED")
    for name, value in result["features"].items():
        print(f"{name}: {value}")