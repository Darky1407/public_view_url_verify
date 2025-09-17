import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

# ---------- CONFIG ----------
INPUT_CSV = r"small_sample.csv"        # CSV with features (+ label if training)
OUTPUT_MODEL = "rf_phishing_model.pkl"
OUTPUT_RESULTS = "rf_results.csv"
RANDOM_STATE = 42
# ---------------------------

# Load dataset
assert os.path.exists(INPUT_CSV), f"Input CSV not found: {INPUT_CSV}"
df = pd.read_csv(INPUT_CSV)

# Keep URLs for reporting
urls = df["url"] if "url" in df.columns else None

# Automatically detect mode
TRAIN_MODE = 'label' in df.columns

if TRAIN_MODE:
    print("Training mode detected: label column found.")

    # Clean dataset
    df = df.dropna(subset=['label'])
    df['label'] = df['label'].astype(int)

    # Separate features and labels
    X = df.drop(columns=["url", "label"], errors="ignore")
    y = df["label"]

    # Train/test split
    X_train, X_test, y_train, y_test, urls_train, urls_test = train_test_split(
        X, y, urls, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    # Train RandomForest
    rf = RandomForestClassifier(
        n_estimators=200,
        random_state=RANDOM_STATE,
        class_weight="balanced",
        n_jobs=-1
    )
    rf.fit(X_train, y_train)

    # Save model + feature list
    bundle = {"model": rf, "features": list(X.columns)}
    joblib.dump(bundle, OUTPUT_MODEL)
    print("Model trained and saved to", OUTPUT_MODEL)

    # Predictions on test set
    y_pred = rf.predict(X_test)
    y_proba = rf.predict_proba(X_test)[:, 1]

    # Evaluation metrics
    print("\n=== Evaluation Metrics ===")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
    print(f"Precision: {precision_score(y_test, y_pred, zero_division=0):.3f}")
    print(f"Recall: {recall_score(y_test, y_pred, zero_division=0):.3f}")
    print(f"F1 Score: {f1_score(y_test, y_pred, zero_division=0):.3f}")
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    # Build results DataFrame for test set
    results = pd.DataFrame({
        "url": urls_test.values if urls_test is not None else range(len(y_pred)),
        "true_label": y_test.values,
        "predicted_label": y_pred,
        "phishing_probability": y_proba
    })

else:
    print("Deployment mode detected: no label column found.")

    # Load pre-trained model
    bundle = joblib.load(OUTPUT_MODEL)
    rf = bundle["model"]
    features = bundle["features"]
    print("Loaded pre-trained model for deployment.")

    # Features only
    X = df[features]

    # Predict on full dataset
    y_pred = rf.predict(X)
    y_proba = rf.predict_proba(X)[:, 1]

    # Build results DataFrame
    results = pd.DataFrame({
        "url": urls.values if urls is not None else range(len(y_pred)),
        "predicted_label": y_pred,
        "phishing_probability": y_proba
    })

# Save results
results.to_csv(OUTPUT_RESULTS, index=False)
print(f"\nResults saved to {OUTPUT_RESULTS}")
print(results.head())
