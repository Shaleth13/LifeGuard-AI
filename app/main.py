"""FastAPI API for LifeGuard AI."""
from collections import deque
from fastapi import FastAPI
from pydantic import BaseModel, Field
from .risk_engine import predict_risk

app = FastAPI(title="LifeGuard AI API", version="2.0")

baseline = {
    "heart_rate": 72.0,
    "spo2": 98.0,
    "temperature": 98.4,
    "motion": .2,
}
recent = deque(maxlen=12)


class Vitals(BaseModel):
    heart_rate: float = Field(..., ge=20, le=240)
    spo2: float = Field(..., ge=50, le=100)
    temperature: float = Field(..., ge=80, le=110)
    motion: float = Field(default=0, ge=0, le=20)


@app.get("/health")
def health():
    """Simple health endpoint for deployment checks."""
    return {"status": "ok", "model": "xgboost-or-fallback"}


@app.get("/baseline")
def get_baseline():
    """Return the current personalized baseline."""
    return baseline


@app.post("/predict")
def predict(vitals: Vitals):
    """Score one incoming wearable observation."""
    current = vitals.model_dump()
    result = predict_risk(current, list(recent), baseline)
    recent.append(current)

    # In production this event would be sent through a notification service.
    if result["alert"]:
        result["caregiver_action"] = "CARE_GIVER_ALERT_TRIGGERED"
    else:
        result["caregiver_action"] = "NO_ALERT"

    return {"vitals": current, **result}
