"""
app.py
------
Flask backend for the Floods Prediction web app.
Clean architecture, modular design, and robust error handling.
"""

import logging
from flask import Flask, render_template, request, redirect, url_for
from core.config import SECRET_KEY, FLASK_DEBUG, PORT, HOST
from core.validation import validate_inputs
from core.predictor import predict_flood_risk

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY

# ---------------------------------------------------------------------
# Route Handlers
# ---------------------------------------------------------------------

@app.route('/')
def home():
    """Render landing page."""
    return render_template('home.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    Unified route for prediction form.
    GET: Render prediction form.
    POST: Validate input, run prediction, render results.
    """
    if request.method == 'GET':
        return render_template("index.html")
        
    # POST: Process form data
    # 1. Server-side validation
    is_valid, error_msg, cleaned_data = validate_inputs(request.form)
    if not is_valid:
        logger.warning(f"Validation failed: {error_msg}")
        return render_template(
            "index.html",
            error=error_msg,
            # Repopulate fields so user doesn't lose inputs
            cloudCover=request.form.get("cloudCover", ""),
            annualRainfall=request.form.get("annualRainfall", ""),
            janFeb=request.form.get("janFeb", ""),
            marMay=request.form.get("marMay", ""),
            junSep=request.form.get("junSep", "")
        )
        
    try:
        # 2. Run prediction model
        prediction, probability = predict_flood_risk(cleaned_data)
        logger.info(f"Prediction result: {prediction} (Probability: {probability:.2f}%)")
        
        # 3. Route to results template
        template_name = 'chance.html' if prediction == 1 else 'nochance.html'
        return render_template(
            template_name,
            probability=round(probability, 1),
            cloud_cover=cleaned_data["cloudCover"],
            annual_rainfall=cleaned_data["annualRainfall"],
            jan_feb=cleaned_data["janFeb"],
            mar_may=cleaned_data["marMay"],
            jun_sep=cleaned_data["junSep"]
        )
        
    except Exception as e:
        logger.error(f"Internal prediction error: {str(e)}", exc_info=True)
        return render_template(
            "index.html",
            error="An internal error occurred during prediction. Please try again later.",
            **request.form
        )


@app.route('/Predict')
def legacy_predict():
    """Redirect capitalized legacy GET route to lowercase /predict."""
    return redirect(url_for('predict'))


# ---------------------------------------------------------------------
# Error Pages
# ---------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template("index.html", error="Page not found. Redirected to form page."), 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {str(e)}")
    return render_template("index.html", error="An internal server error occurred."), 500


# ---------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=FLASK_DEBUG)
