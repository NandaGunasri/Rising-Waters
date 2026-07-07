import os
import logging
import pandas as pd
from joblib import load
from core.config import MODEL_PATH, SCALER_PATH, FEATURE_COLUMNS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_model = None
_scaler = None

def load_artifacts():
    """Load model and scaler files from disk."""
    global _model, _scaler
    
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model artifact not found at {MODEL_PATH}. Run train.py to train it.")
        
    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(f"Scaler artifact not found at {SCALER_PATH}. Run train.py to train it.")
        
    logger.info("Loading ML artifacts...")
    _model = load(MODEL_PATH)
    _scaler = load(SCALER_PATH)
    logger.info("ML artifacts loaded successfully.")

# Initial load attempt on import
try:
    load_artifacts()
except Exception as e:
    logger.error(f"Error loading artifacts during startup: {str(e)}")

def predict_flood_risk(features_dict):
    """
    Perform scaled prediction using the loaded model.
    
    Args:
        features_dict (dict): Dictionary mapping feature names (keys in LIMITS) 
                             to float values.
                             
    Returns:
        tuple: (prediction: int, probability: float)
    """
    global _model, _scaler
    
    # Reload artifacts if they weren't loaded correctly on startup
    if _model is None or _scaler is None:
        load_artifacts()
        
    # Standardize names to match FEATURE_COLUMNS order
    # Keys in form dict: cloudCover, annualRainfall, janFeb, marMay, junSep
    ordered_values = [
        features_dict["cloudCover"],
        features_dict["annualRainfall"],
        features_dict["janFeb"],
        features_dict["marMay"],
        features_dict["junSep"]
    ]
    
    # Create DataFrame to preserve column names and order
    input_df = pd.DataFrame([ordered_values], columns=FEATURE_COLUMNS)
    
    # Perform scaling
    scaled_features = _scaler.transform(input_df)
    
    # Run prediction
    prediction = int(_model.predict(scaled_features)[0])
    probability = float(_model.predict_proba(scaled_features)[0][1] * 100)
    
    return prediction, probability
