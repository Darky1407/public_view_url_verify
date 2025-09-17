import pandas as pd

# Load dataset
df = pd.read_csv(r"DataQuest 2.0\training_data.csv")
print(df.head())
print(df.columns)
# Drop non-numeric columns like 'url'
X = df.drop(columns=["url","label"], errors="ignore")  
y = df["label"]
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Train size:", len(X_train))
print("Test size:", len(X_test))
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=200,       # number of trees
    random_state=42,        # reproducibility
    class_weight="balanced",# handle imbalanced data
    n_jobs=-1               # use all CPU cores
)
rf.fit(X_train, y_train)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

y_pred = rf.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
# Get prediction probabilities for all data
y_proba = rf.predict_proba(X)

# Make results table with % values
results_all = pd.DataFrame({
    "url": df["url"],
    "prediction": ["yes (phishing)" if p == 1 else "no (legit)" for p in rf.predict(X)],
    "confidence (%)": (y_proba.max(axis=1) * 100).round(2),
    "phishing_prob (%)": (y_proba[:,1] * 100).round(2),
    "legit_prob (%)": (y_proba[:,0] * 100).round(2)
})

# Save to CSV
results_all.to_csv("phishing_predictions_with_confidence.csv", index=False)
print("Saved", len(results_all), "rows with % confidence scores.")



