"""
train.py
--------
Trains an XGBoost classifier for flood prediction and scales the features
with StandardScaler. Saves both artifacts with joblib so app.py can load them at runtime.

Prioritizes:
1. The official 'flood dataset.xlsx' in the root directory (contains Cloud Cover, Temp, flood target, etc.)
2. A raw rainfall dataset in raw_data/ (derives proxy cloud cover & flood target)
3. Fallback: Synthetic data generation
"""

import os
import glob
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from xgboost import XGBClassifier
from joblib import dump

# Use path-safe directory resolution relative to the file location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
RAW_DATA_DIR = os.path.join(BASE_DIR, "raw_data")

UPLOADED_DATASET = os.path.join(BASE_DIR, "flood dataset.xlsx")
OUTPUT_CSV_PATH = os.path.join(DATASET_DIR, "flood_dataset.csv")
MODEL_SAVE_PATH = os.path.join(MODELS_DIR, "floods.save")
SCALER_SAVE_PATH = os.path.join(MODELS_DIR, "transform.save")

# Set random seed
np.random.seed(42)


def find_raw_rainfall_file():
    """Look for rainfall CSV or Excel file in raw_data/."""
    if not os.path.isdir(RAW_DATA_DIR):
        return None
    candidates = glob.glob(os.path.join(RAW_DATA_DIR, "*rainfall*")) or \
                 glob.glob(os.path.join(RAW_DATA_DIR, "*"))
    candidates = [c for c in candidates if c.lower().endswith((".csv", ".xlsx", ".xls"))]
    return candidates[0] if candidates else None


def load_uploaded_dataset(path):
    """
    Loader for the official 'flood dataset.xlsx' containing the columns:
    Temp, Humidity, Cloud Cover, ANNUAL, Jan-Feb, Mar-May, Jun-Sep, Oct-Dec, flood, etc.
    """
    print(f"[INFO] Loading uploaded flood dataset: {path}")
    raw = pd.read_excel(path)
    
    # Rename columns to standard uppercase representation used in app.py
    rename_map = {
        "Cloud Cover": "CLOUD_COVER",
        "ANNUAL": "ANNUAL_RAINFALL",
        "Jan-Feb": "JAN_FEB",
        "Mar-May": "MAR_MAY",
        "Jun-Sep": "JUN_SEP",
        "flood": "FLOODS"
    }
    raw = raw.rename(columns=rename_map)
    
    required = ["CLOUD_COVER", "ANNUAL_RAINFALL", "JAN_FEB", "MAR_MAY", "JUN_SEP", "FLOODS"]
    missing = [c for c in required if c not in raw.columns]
    if missing:
        raise ValueError(
            f"Uploaded dataset is missing expected columns: {missing}. "
            f"Available columns: {list(raw.columns)}"
        )
        
    df = raw[required].dropna().reset_index(drop=True)
    # Convert datatypes to floats for features and int for label
    for col in required[:-1]:
        df[col] = df[col].astype(float)
    df["FLOODS"] = df["FLOODS"].astype(int)
    
    return df


def load_real_dataset(path):
    """
    Loader for the classic 'rainfall in india 1901-2015' style dataset.
    Since it lacks Cloud Cover, we derive a proxy from monsoon intensity.
    """
    print(f"[INFO] Loading public rainfall dataset: {path}")
    raw = pd.read_csv(path) if path.lower().endswith(".csv") else pd.read_excel(path)
    raw.columns = [c.strip().upper().replace(" ", "_").replace("-", "_") for c in raw.columns]

    rename_map = {
        "ANNUAL": "ANNUAL_RAINFALL",
        "JAN_FEB": "JAN_FEB",
        "MAR_MAY": "MAR_MAY",
        "JUN_SEP": "JUN_SEP",
    }
    raw = raw.rename(columns=rename_map)

    required = ["ANNUAL_RAINFALL", "JAN_FEB", "MAR_MAY", "JUN_SEP"]
    missing = [c for c in required if c not in raw.columns]
    if missing:
        raise ValueError(
            f"raw_data file is missing expected columns: {missing}. "
            f"Found columns: {list(raw.columns)}"
        )

    df = raw[required].dropna().reset_index(drop=True)

    # Derive a Cloud Cover proxy (0-100%) from monsoon rainfall intensity
    df["CLOUD_COVER"] = 30 + 70 * (df["JUN_SEP"] - df["JUN_SEP"].min()) / (
        df["JUN_SEP"].max() - df["JUN_SEP"].min()
    )

    # Flood label: annual rainfall well above the mean is treated as flood-prone
    mean_annual = df["ANNUAL_RAINFALL"].mean()
    std_annual = df["ANNUAL_RAINFALL"].std()
    df["FLOODS"] = (df["ANNUAL_RAINFALL"] > (mean_annual + 0.25 * std_annual)).astype(int)

    return df[["CLOUD_COVER", "ANNUAL_RAINFALL", "JAN_FEB", "MAR_MAY", "JUN_SEP", "FLOODS"]]


def build_synthetic_dataset():
    """Fallback: synthetic but plausible dataset, used only when no files exist."""
    print("[INFO] No dataset files found. Generating synthetic fallback dataset...")
    cloud_cover = np.random.uniform(10, 100, 2000)
    jan_feb = np.random.gamma(shape=2.0, scale=15, size=2000)
    mar_may = np.random.gamma(shape=2.5, scale=40, size=2000)
    jun_sep = np.random.gamma(shape=3.0, scale=180, size=2000)
    annual_rainfall = jan_feb + mar_may + jun_sep + np.random.normal(0, 50, 2000)
    annual_rainfall = np.clip(annual_rainfall, 100, None)

    df = pd.DataFrame({
        "CLOUD_COVER": cloud_cover,
        "ANNUAL_RAINFALL": annual_rainfall,
        "JAN_FEB": jan_feb,
        "MAR_MAY": mar_may,
        "JUN_SEP": jun_sep,
    })

    risk_score = (
        0.35 * (df["JUN_SEP"] / df["JUN_SEP"].max()) +
        0.25 * (df["ANNUAL_RAINFALL"] / df["ANNUAL_RAINFALL"].max()) +
        0.20 * (df["CLOUD_COVER"] / 100) +
        0.10 * (df["MAR_MAY"] / df["MAR_MAY"].max()) +
        0.10 * (df["JAN_FEB"] / df["JAN_FEB"].max())
    )
    risk_score += np.random.normal(0, 0.05, 2000)
    threshold = np.percentile(risk_score, 60)
    df["FLOODS"] = (risk_score > threshold).astype(int)
    return df


def main():
    # 1. Load data
    if os.path.exists(UPLOADED_DATASET):
        df = load_uploaded_dataset(UPLOADED_DATASET)
        # Use notebook-specific test split parameters
        test_size = 0.25
        random_state = 10
        stratify = None  # Match notebook (no stratification)
    else:
        raw_file = find_raw_rainfall_file()
        if raw_file:
            df = load_real_dataset(raw_file)
        else:
            df = build_synthetic_dataset()
        test_size = 0.2
        random_state = 42
        stratify = df["FLOODS"]

    # 2. Extract features and target
    feature_cols = ["CLOUD_COVER", "ANNUAL_RAINFALL", "JAN_FEB", "MAR_MAY", "JUN_SEP"]
    X = df[feature_cols]
    y = df["FLOODS"]

    # 3. Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=stratify
    )

    # 4. Scale features
    sc = StandardScaler()
    X_train_scaled = sc.fit_transform(X_train)
    X_test_scaled = sc.transform(X_test)

    # 5. Train XGBoost model (matching notebook params)
    model = XGBClassifier(
        random_state=42,
        eval_metric="logloss"
    )
    model.fit(X_train_scaled, y_train)

    # 6. Evaluate
    preds = model.predict(X_test_scaled)
    print("\n--- MODEL PERFORMANCE ---")
    print(f"Accuracy: {accuracy_score(y_test, preds):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, preds))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, preds))

    # 7. Save outputs
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(DATASET_DIR, exist_ok=True)

    dump(model, MODEL_SAVE_PATH)
    dump(sc, SCALER_SAVE_PATH)
    df.to_csv(OUTPUT_CSV_PATH, index=False)

    print(f"\n[SUCCESS] Saved model -> {MODEL_SAVE_PATH}")
    print(f"[SUCCESS] Saved scaler -> {SCALER_SAVE_PATH}")
    print(f"[SUCCESS] Saved processed dataset -> {OUTPUT_CSV_PATH}")


if __name__ == "__main__":
    main()
