"""Train a small XGBoost risk classifier on synthetic personalized data.

Run:
    python ml/train_xgboost.py

The generated model is saved under models/xgb_risk_model.joblib.
The synthetic labels represent a hackathon demonstration only.
"""
from pathlib import Path
import numpy as np
import joblib
from xgboost import XGBClassifier

rng = np.random.default_rng(42)
rows, labels = [], []

for _ in range(5000):
    hr = rng.normal(72, 7)
    spo2 = rng.normal(98, .8)
    temp = rng.normal(98.4, .4)
    motion = rng.normal(.3, .2)

    hr_delta = hr - 72
    spo2_drop = 98 - spo2
    temp_delta = temp - 98.4
    hr_trend = hr_delta + rng.normal(0, 3)
    spo2_trend = spo2_drop + rng.normal(0, .3)

    # Synthetic deterioration rule used only to create training labels.
    severity = (
        0.055*max(hr_delta, 0) +
        0.75*max(spo2_drop, 0) +
        0.45*abs(temp_delta) +
        0.04*max(hr_trend, 0) +
        0.30*max(spo2_trend, 0) +
        0.05*motion
    )
    y = int(severity > 2.8)

    rows.append([
        hr, spo2, temp, motion,
        hr_delta, spo2_drop, temp_delta,
        hr_trend, spo2_trend
    ])
    labels.append(y)

X = np.asarray(rows)
y = np.asarray(labels)

model = XGBClassifier(
    n_estimators=120,
    max_depth=4,
    learning_rate=.08,
    subsample=.9,
    colsample_bytree=.9,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
)
model.fit(X, y)

out = Path(__file__).resolve().parent.parent/"models"/"xgb_risk_model.joblib"
joblib.dump(model, out)
print(f"Saved model: {out}")
print(f"Training samples: {len(y)}")
print(f"Positive-risk samples: {int(y.sum())}")
