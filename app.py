from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import traceback

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (adjust origins in production)

# Load model bundle (expects {"model": ..., "features": [...]} )
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

def extract_features_from_url(url: str):
    """
    Template extractor. **MUST** be updated to match the exact features used during training.
    The function returns a dict mapping feature name -> value for every feature in FEATURES.
    """
    # Basic example features — expand/replace to match your pipeline:
    parsed = url or ""
    feats = {
        "url_length": len(parsed),
        "having_at_symbol": 1 if "@" in parsed else 0,
        "having_ip": 1 if any(part.isdigit() for part in parsed.split("/")[2:3]) else 0,
        "count_dots": parsed.count("."),
        "count_hyphens": parsed.count("-"),
        # add placeholders for other features your model expects
    }

    # Ensure all FEATURES are present; missing features default to 0
    aligned = {f: feats.get(f, 0) for f in FEATURES}
    return aligned

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
        # Create dataframe with one row in the same feature order the model expects
        X = pd.DataFrame([[feats[f] for f in FEATURES]], columns=FEATURES)

        pred = model.predict(X)[0]
        proba = None
        if hasattr(model, "predict_proba"):
            proba = float(model.predict_proba(X)[0][1])

        return jsonify({
            "url": url,
            "prediction": int(pred),
            "probability": proba,
            "message": "Phishing 🚨" if int(pred) == 1 else "Safe ✅"
        }), 200

    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"error": str(e), "trace": tb}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
