import os
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import shap
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]

LABELLED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "labelled_sites.csv"
)

MODEL_DIR = PROJECT_ROOT / "models" / "saved"
MODEL_FILE = MODEL_DIR / "site_scorer_model.pkl"

REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
SHAP_PLOT_FILE = REPORTS_DIR / "shap_importance.png"

FEATURE_COLUMNS = [
    "dist_road_m",
    "dist_hospital_m",
    "dist_market_m",
    "dist_traffic_m",
    "building_count_500m",
    "poi_count_500m",
    "commercial_poi_count_500m",
    "population_2011",
    "elevation_m",
    "slope_deg",
]

TARGET_COLUMN = "label"


def encode_flood_risk(df):
    """Convert flood_risk_proxy to numeric values."""

    flood_mapping = {
        "Low": 0,
        "Medium": 1,
        "High": 2,
    }

    df["flood_risk_encoded"] = (
        df["flood_risk_proxy"]
        .map(flood_mapping)
        .fillna(1)
    )

    return df


def train_and_evaluate():
    """Train Random Forest and XGBoost, compare and save best model."""

    print("=" * 70)
    print("EV CHARGING SITE SUITABILITY MODEL TRAINING")
    print("=" * 70)

    if not LABELLED_FILE.exists():
        raise FileNotFoundError(
            f"Labelled dataset not found:\n{LABELLED_FILE}"
        )

    print("\nLoading labelled dataset...")
    df = pd.read_csv(LABELLED_FILE, encoding="utf-8-sig")

    print(f"Total labelled samples: {len(df)}")
    print(f"Label distribution:")
    print(df[TARGET_COLUMN].value_counts().sort_index())

    print("\nEncoding flood_risk_proxy...")
    df = encode_flood_risk(df)

    X = df[FEATURE_COLUMNS + ["flood_risk_encoded"]].copy()
    y = df[TARGET_COLUMN].copy()

    print("\nFeature columns:")
    print(X.columns.tolist())

    print("\nPerforming train-test split (80% train, 20% test)...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    print("\n" + "=" * 70)
    print("RANDOM FOREST CLASSIFIER")
    print("=" * 70)

    rf = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
    )

    rf.fit(X_train, y_train)

    rf_train_score = rf.score(X_train, y_train)
    rf_test_score = rf.score(X_test, y_test)

    print(f"\nRandom Forest Training Accuracy: {rf_train_score:.3f}")
    print(f"Random Forest Testing Accuracy: {rf_test_score:.3f}")

    print("\nRandom Forest Classification Report:")
    print(classification_report(y_test, rf.predict(X_test)))

    print("\n" + "=" * 70)
    print("XGBOOST CLASSIFIER")
    print("=" * 70)

    xg = xgb.XGBClassifier(
        n_estimators=100,
        random_state=42,
        eval_metric="logloss",
        n_jobs=-1,
    )

    xg.fit(X_train, y_train)

    xg_train_score = xg.score(X_train, y_train)
    xg_test_score = xg.score(X_test, y_test)

    print(f"\nXGBoost Training Accuracy: {xg_train_score:.3f}")
    print(f"XGBoost Testing Accuracy: {xg_test_score:.3f}")

    print("\nXGBoost Classification Report:")
    print(classification_report(y_test, xg.predict(X_test)))

    print("\n" + "=" * 70)
    print("MODEL COMPARISON")
    print("=" * 70)

    print(f"\nRandom Forest Test Accuracy: {rf_test_score:.3f}")
    print(f"XGBoost Test Accuracy: {xg_test_score:.3f}")

    if rf_test_score >= xg_test_score:
        best_model = rf
        best_model_name = "Random Forest"
    else:
        best_model = xg
        best_model_name = "XGBoost"

    print(f"\nBest model: {best_model_name}")

    print("\n" + "=" * 70)
    print("SHAP FEATURE IMPORTANCE")
    print("=" * 70)

    explainer = shap.TreeExplainer(best_model)
    shap_values = explainer.shap_values(X_test)

    plt.figure(figsize=(10, 6))

    shap.summary_plot(
        shap_values,
        X_test,
        feature_names=X.columns.tolist(),
        show=False,
    )

    plt.tight_layout()

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        SHAP_PLOT_FILE,
        dpi=300,
        bbox_inches="tight"
    )

    print(f"\nSHAP summary plot saved to:")
    print(SHAP_PLOT_FILE)

    print("\n" + "=" * 70)
    print("SAVING BEST MODEL")
    print("=" * 70)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(best_model, MODEL_FILE)

    print(f"\nBest model saved to:")
    print(MODEL_FILE)

    print("\n" + "=" * 70)
    print("TRAINING COMPLETED SUCCESSFULLY")
    print("=" * 70)

    return best_model, best_model_name


if __name__ == "__main__":
    train_and_evaluate()