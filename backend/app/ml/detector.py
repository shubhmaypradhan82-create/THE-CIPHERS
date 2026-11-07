
"""Local ML email threat detector.

The trained TF-IDF + calibrated Linear SVM model is loaded lazily from the
same package directory, so the backend does not depend on the AI ZIP's
working directory or on a second web service.
"""
from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

MODEL_PATH = Path(__file__).resolve().parent / "calibrated_svm.pkl"
_MODEL: tuple[Any, Any] | None = None


def _load_model() -> tuple[Any, Any]:
    global _MODEL
    if _MODEL is None:
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(f"ML model not found: {MODEL_PATH}")
        with MODEL_PATH.open("rb") as file:
            _MODEL = pickle.load(file)
        if not isinstance(_MODEL, tuple) or len(_MODEL) != 2:
            raise RuntimeError("Invalid ML model bundle.")
    return _MODEL


def analyze_email_text(email_text: str) -> dict[str, Any]:
    """Classify email text and return stable API-friendly ML metadata."""
    if not isinstance(email_text, str):
        raise TypeError("email_text must be a string")
    if not email_text.strip():
        raise ValueError("email_text cannot be empty")

    vectorizer, model = _load_model()
    features = vectorizer.transform([email_text])
    prediction = str(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]
    classes = [str(c) for c in model.classes_]

    spam_probability = (
        float(probabilities[classes.index("spam")]) if "spam" in classes else 0.0
    )
    ham_probability = (
        float(probabilities[classes.index("ham")]) if "ham" in classes else 0.0
    )

    return {
        "classification": prediction,
        "spam_probability": round(spam_probability * 100, 2),
        "ham_probability": round(ham_probability * 100, 2),
        "model": "TF-IDF + Calibrated Linear SVM",
        "provider": "local-ml",
    }


def model_status() -> dict[str, Any]:
    """Return health information without crashing the application."""
    try:
        vectorizer, model = _load_model()
        return {
            "available": True,
            "model": "TF-IDF + Calibrated Linear SVM",
            "classes": [str(c) for c in model.classes_],
            "vocabulary_size": len(getattr(vectorizer, "vocabulary_", {})),
        }
    except Exception as exc:
        return {"available": False, "error": str(exc)}
