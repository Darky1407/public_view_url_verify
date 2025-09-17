import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

# ---------- CONFIG ----------
INPUT_CSV = r"testing_data.csv"
OUTPUT_MODEL = "rf_phishing_model.pkl"
OUTPUT_RESULTS = "rf_results.csv"
RANDOM_STATE = 42
# ---------------------------

# Load dataset
assert os.path.exists(INPUT_CSV), f"Input CSV not found: {INPUT_CSV}"
df = pd.read_csv(INPUT_CSV)

# Keep original URLs for reporting
urls = df["url"] if "url" in df.columns else None

# Clean dataset
df = df.dropna(subset=['label'])
df['label'] = df['label'].astype(int)

# Separate features & labels
X = df.drop(columns=["url", "label"], errors="ignore")
y = df["label"]

# Split train/test (keep track of URLs if available)
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
print("Model saved to", OUTPUT_MODEL)

# Predictions
y_pred = rf.predict(X_test)
y_proba = rf.predict_proba(X_test)[:, 1]

# Evaluation metrics
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, zero_division=0)
rec = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print("\n=== Evaluation Metrics ===")
print(f"Accuracy: {acc:.3f}")
print(f"Precision: {prec:.3f}")
print(f"Recall: {rec:.3f}")
print(f"F1 Score: {f1:.3f}")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Build results DataFrame
results = pd.DataFrame({
    "url": urls_test.values if urls_test is not None else range(len(y_pred)),
    "true_label": y_test.values,
    "predicted_label": y_pred,
    "phishing_probability": y_proba
})

# Save to CSV
results.to_csv(OUTPUT_RESULTS, index=False)
print(f"\nResults saved to {OUTPUT_RESULTS}")
print(results.head())
