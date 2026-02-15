from __future__ import annotations

from pathlib import Path

import joblib

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "resume_classifier.pkl"


def load_classifier(model_path: Path | None = None):
    """Load and return the trained classifier pipeline from disk."""
    path = model_path or MODEL_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"Trained model not found at {path}. Train and export model first."
        )
    return joblib.load(path)
