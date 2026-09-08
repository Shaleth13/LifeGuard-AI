"""LifeGuard AI risk engine.

The prototype combines:
- Personalized baseline deviations
- Multi-vital trend features
- A trained XGBoost classifier
- A transparent risk score used for the UI

This is a hackathon prototype, not a clinically validated medical device.
"""

from pathlib import Path
import json
import numpy as np
import joblib

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "xgb_risk_model.joblib"


def features_from_window(current, recent, baseline):
    """Create ML features from current, recent and personalized-baseline data."""
    def avg(key):
        return float(np.mean([r[key] for r in recent])) if recent else baseline[key]

    return np.array([[
        current["heart_rate"],
        current["spo2"],
        current["temperature"],
        current.get("motion", 0.0),
        current["heart_rate"] - baseline["heart_rate"],
        baseline["spo2"] - current["spo2"],
        current["temperature"] - baseline["temperature"],
        current["heart_rate"] - avg("heart_rate"),
        avg("spo2") - current["spo2"],
    ]], dtype=float)


def fallback_score(current, recent, baseline):
    """Transparent fallback when the trained model has not been generated."""
    hr = min(abs(current["heart_rate"] - baseline["heart_rate"]) / 30, 1)
    spo2 = min(abs(current["spo2"] - baseline["spo2"]) / 5, 1)
    temp = min(abs(current["temperature"] - baseline["temperature"]) / 3, 1)
    trend = 0
    if recent:
        avg_hr = np.mean([x["heart_rate"] for x in recent])
        avg_spo2 = np.mean([x["spo2"] for x in recent])
        trend = min((max(0, current["heart_rate"] - avg_hr)/20 +
                     max(0, avg_spo2 - current["spo2"])/3)/2, 1)
    return round(100*(.4*hr + .35*spo2 + .1*temp + .15*trend))


def predict_risk(current, recent, baseline):
    """Return risk score, class and reasons."""
    score = fallback_score(current, recent, baseline)
    model_used = False

    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        x = features_from_window(current, recent, baseline)
        probability = float(model.predict_proba(x)[0, 1])
        score = round(probability * 100)
        model_used = True

    if score < 30:
        level = "LOW"
    elif score < 60:
        level = "MODERATE"
    else:
        level = "HIGH"

    reasons = []
    if current["heart_rate"] > baseline["heart_rate"] + 15:
        reasons.append("elevated heart-rate trend")
    if current["spo2"] < baseline["spo2"] - 2:
        reasons.append("SpO₂ below personal baseline")
    if current["temperature"] > baseline["temperature"] + 1:
        reasons.append("temperature deviation")
    if not reasons:
        reasons.append("vitals close to personalized baseline")

    return {
        "risk_score": score,
        "risk_level": level,
        "alert": level == "HIGH",
        "reasons": reasons,
        "model_used": model_used,
    }
