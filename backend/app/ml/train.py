"""Retrain the bundled email classifier.

Run from the backend directory:
    python -m app.ml.train
"""
from pathlib import Path
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "ml" / "data" / "email_dataset.csv"
MODEL = ROOT / "ml" / "calibrated_svm.pkl"

df = pd.read_csv(DATA).dropna(subset=["email", "label"])
X_train, _, y_train, _ = train_test_split(
    df["email"].astype(str), df["label"].astype(str),
    test_size=0.20, random_state=42, stratify=df["label"]
)
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2), min_df=2, max_df=0.98,
    sublinear_tf=True, max_features=100000
)
X = vectorizer.fit_transform(X_train)
model = CalibratedClassifierCV(
    LinearSVC(C=1.5, class_weight="balanced"), cv=3, method="sigmoid"
)
model.fit(X, y_train)
with MODEL.open("wb") as f:
    pickle.dump((vectorizer, model), f, protocol=pickle.HIGHEST_PROTOCOL)
print(f"Saved {MODEL}")
