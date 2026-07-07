import unittest
from app import app
from core.config import LIMITS

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up Flask test client before each test."""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.client = app.test_client()

    def test_home_page(self):
        """Verify the landing page loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Rising Waters", response.data)
        self.assertIn(b"Know a flood is coming", response.data)

    def test_predict_form_get(self):
        """Verify the prediction form loads successfully."""
        response = self.client.get('/predict')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Enter Seasonal Hydrological Data", response.data)

    def test_legacy_redirect(self):
        """Verify legacy capitalized route redirects to lowercase /predict."""
        response = self.client.get('/Predict')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['Location'].endswith('/predict'))

    def test_valid_prediction_low_risk(self):
        """Verify low-risk prediction works with valid low rainfall inputs."""
        # Low values should lead to low risk (nochance.html)
        payload = {
            "cloudCover": "15.0",
            "annualRainfall": "800.0",
            "janFeb": "20.0",
            "marMay": "50.0",
            "junSep": "650.0"
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Low Flood Likelihood" in response.data)
        self.assertTrue(b"Conditions look safe for now" in response.data or b"Stable Conditions Detected" in response.data)
        self.assertIn(b"15.0%", response.data)  # Cloud Cover recap check

    def test_valid_prediction_high_risk(self):
        """Verify high-risk prediction works with valid high rainfall inputs."""
        # High values should lead to high risk (chance.html)
        payload = {
            "cloudCover": "85.0",
            "annualRainfall": "6000.0",
            "janFeb": "350.0",
            "marMay": "850.0",
            "junSep": "4500.0"
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"High Flood Likelihood" in response.data or b"likely flood" in response.data)
        self.assertIn(b"85.0%", response.data)  # Cloud Cover recap check

    def test_missing_fields_validation(self):
        """Verify server catches missing fields and doesn't crash."""
        payload = {
            "cloudCover": "50.0",
            "annualRainfall": "",  # Empty
            "janFeb": "10.0",
            "marMay": "40.0",
            "junSep": "500.0"
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please fill in all fields", response.data)
        self.assertIn(b"value=\"50.0\"", response.data)  # Check cloudCover was repopulated

    def test_non_numeric_validation(self):
        """Verify server catches non-numeric fields and doesn't crash."""
        payload = {
            "cloudCover": "fifty",
            "annualRainfall": "1200",
            "janFeb": "10.0",
            "marMay": "40.0",
            "junSep": "500.0"
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please enter valid numeric values for", response.data)
        self.assertIn(b"value=\"fifty\"", response.data)  # Check value was repopulated

    def test_out_of_bounds_validation(self):
        """Verify server catches out-of-bounds fields and doesn't crash."""
        payload = {
            "cloudCover": "120.0",  # Max is 100
            "annualRainfall": "1200",
            "janFeb": "10.0",
            "marMay": "-10.0",  # Min is 0
            "junSep": "500.0"
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Out-of-range values detected", response.data)
        self.assertIn(b"Cloud Cover (%) must be between 0.0 and 100.0", response.data)
        self.assertIn(b"March-May Rainfall (mm) must be between 0.0 and 5000.0", response.data)

if __name__ == '__main__':
    unittest.main()
