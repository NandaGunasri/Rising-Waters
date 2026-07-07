import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Root directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model and scaler paths
MODEL_PATH = os.path.join(BASE_DIR, "models", "floods.save")
SCALER_PATH = os.path.join(BASE_DIR, "models", "transform.save")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "dataset", "flood_dataset.csv")
RAW_DATA_DIR = os.path.join(BASE_DIR, "raw_data")
UPLOADED_DATASET_PATH = os.path.join(BASE_DIR, "flood dataset.xlsx")

# Feature columns used during training and inference (MUST match exactly)
FEATURE_COLUMNS = [
    "CLOUD_COVER",
    "ANNUAL_RAINFALL",
    "JAN_FEB",
    "MAR_MAY",
    "JUN_SEP"
]

# Validation thresholds (Min/Max values)
LIMITS = {
    "cloudCover": {"min": 0.0, "max": 100.0, "label": "Cloud Cover (%)"},
    "annualRainfall": {"min": 0.0, "max": 10000.0, "label": "Annual Rainfall (mm)"},
    "janFeb": {"min": 0.0, "max": 5000.0, "label": "Jan-Feb Rainfall (mm)"},
    "marMay": {"min": 0.0, "max": 5000.0, "label": "March-May Rainfall (mm)"},
    "junSep": {"min": 0.0, "max": 8000.0, "label": "June-September Rainfall (mm)"}
}

# Flask settings
FLASK_ENV = os.getenv("FLASK_ENV", "production")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
PORT = int(os.getenv("PORT", 5000))
HOST = os.getenv("HOST", "0.0.0.0")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-1329841890")
