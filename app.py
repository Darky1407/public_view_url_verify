from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
from features import FeatureExtractor  # import the class

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Load trained model
rf = joblib.load("rf_phishing_model.pkl")  # directly load the RandomForestClassifier
# Specify the feature columns used in training
features = ["having_ip","url_length","shortening_service","having_at_symbol",
            "double_slash_redirect","prefix_suffix","having_sub_domain",
            "https_token","port","ssl_final_state","dns_record","ssl_certificate"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    fe = FeatureExtractor(url)
    feats = fe.get_features()
    # Ensure all columns exist in the same order as training
    X = pd.DataFrame([feats]).reindex(columns=features, fill_value=0)

    y_pred = rf.predict(X)[0]
    y_proba = rf.predict_proba(X)[0]

    return jsonify({
        "url": url,
        "result": "Phishing" if int(y_pred) == 1 else "Legitimate",
        "phishing_prob": round(float(y_proba[1]) * 100, 2),
        "legit_prob": round(float(y_proba[0]) * 100, 2),
        "confidence": round(float(max(y_proba)) * 100, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
