# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import traceback

# Import your feature extractor
from url_extractor import FeatureExtractor  # adjust if class name differs

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (adjust origins in production)

# -------------------------------
# Load model bundle
# -------------------------------
BUNDLE_PATH = "rf_phishing_model.pkl"
try:
    bundle = joblib.load(BUNDLE_PATH)
    model = bundle["model"]
    FEATURES = bundle["features"]
    print(f"Loaded model bundle from {BUNDLE_PATH}. Features: {FEATURES}")
except Exception as e:
    print("Failed to load model bundle:", e)
    model = None
    FEATURES = []

# -------------------------------
# Feature extraction wrapper
# -------------------------------
def extract_features_from_url(url: str):
    """
    Uses url_extractor.py to compute the same features used for model training.
    Returns a dict mapping feature name -> value for every feature in FEATURES.
    """
    fe = FeatureExtractor(url)
    feats = fe.get_features()  # should return a dict with all features

    # Align features in the same order as the model
    aligned = {f: feats.get(f, 0) for f in FEATURES}
    return aligned

# -------------------------------
# Routes
# -------------------------------
@app.route("/")
def index():
    return jsonify({"status": "Phishing detection API is running"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded on server"}), 500

    try:
        data = request.get_json(force=True)
        url = data.get("url", "")
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        feats = extract_features_from_url(url)
        X = pd.DataFrame([[feats[f] for f in FEATURES]], columns=FEATURES)

        pred = int(model.predict(X)[0])
        proba = None
        if hasattr(model, "predict_proba"):
            proba = float(model.predict_proba(X)[0][1])

        return jsonify({
            "url": url,
            "prediction": pred,
            "probability": proba,
            "message": "Phishing 🚨" if pred == 1 else "Safe ✅"
        }), 200

    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"error": str(e), "trace": tb}), 500

# -------------------------------
# Run server
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
