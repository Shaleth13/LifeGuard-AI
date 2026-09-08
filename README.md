# LifeGuard AI — Working Hackathon Prototype

**Edge-Based Predictive Emergency Detection for Healthcare**

LifeGuard AI monitors multiple vital signals, learns a personalized baseline,
detects deviations and trends, produces a risk score, and triggers a
caregiver-style alert.

> **Important:** This is a hackathon prototype. It is not a clinically
> validated diagnostic or emergency medical device.

## What is actually implemented

### Working software demo
- Personalized baseline for HR, SpO₂ and temperature
- Synthetic wearable sensor stream
- Gradual deterioration scenario
- Multi-vital trend features
- XGBoost risk classifier
- Transparent fallback scoring
- Live Streamlit dashboard
- FastAPI prediction API
- Caregiver alert event
- Offline-capable local scoring path
- Docker deployment
- Optional LSTM forecasting module

### Hardware starter
`firmware/esp32_s3_lifeguard.ino` demonstrates real I2C acquisition from:
- MAX30102
- MPU6050

The comments identify the remaining production steps for SpO₂/HR filtering,
body-temperature hardware, and TinyML/TFLite inference.

### Not claimed as completed
The repository does **not** pretend that a Flutter app, Firebase backend,
React production dashboard, or medical validation already exists. Those are
integration paths for the next iteration.

## Quick start

### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python ml/train_xgboost.py
streamlit run app/dashboard.py
```

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ml/train_xgboost.py
streamlit run app/dashboard.py
```

Choose **Gradual deterioration** and click **Run live demo**.

The demonstration shows:
1. Normal personalized readings
2. Gradual HR rise and SpO₂ drift
3. Increasing risk score
4. High-risk classification
5. Caregiver alert trigger

## API

Start:

```bash
uvicorn app.main:app --reload
```

Then:
- `GET /health`
- `GET /baseline`
- `POST /predict`

Example:

```json
{
  "heart_rate": 112,
  "spo2": 94.2,
  "temperature": 99.3,
  "motion": 1.5
}
```

A high-risk response contains:
- `risk_score`
- `risk_level`
- `reasons`
- `caregiver_action`

## Docker

```bash
docker compose up --build
```

## ML

`ml/train_xgboost.py` creates a small synthetic XGBoost classifier.
`ml/lstm_forecaster.py` provides a PyTorch LSTM architecture for short-window
vital forecasting.

The synthetic training labels are for demonstration only.

## Architecture

```text
MAX30102 ─┐
MPU6050 ──┼──> ESP32-S3 ──> Personal baseline
Temp ─────┘                    ↓
                           Trend features
                                ↓
                           XGBoost risk
                                ↓
                         Risk score / level
                                ↓
                       Caregiver alert event
                                ↓
                    Dashboard / sync when online
```

## Judge demo

1. Start Streamlit.
2. Show the baseline.
3. Run **Normal**.
4. Explain that the risk stays low because readings resemble the user's baseline.
5. Run **Gradual deterioration**.
6. Point out that the risk responds as HR rises and SpO₂ drifts.
7. Show the high-risk caregiver alert.
8. Mention that the local scoring path does not need a cloud request to detect the event.

## Future integration

- TensorFlow Lite Micro on ESP32-S3
- Quantized TinyML model
- Real body-temperature sensor
- Flutter mobile companion
- Firebase sync / authentication
- React production dashboard
- SMS/push/WhatsApp-style notification provider
- Edge Impulse training pipeline
- Clinical validation and safety review
