# 3-Minute Demo

**0:00–0:20 — Problem**
Traditional alarms often wait for fixed thresholds. LifeGuard AI focuses on
personalized baseline drift and trends.

**0:20–0:45 — Hardware**
Show ESP32-S3, MAX30102 and MPU6050. Explain that the firmware starter reads
the physical I2C sensors.

**0:45–1:15 — Personalized AI**
Show the Streamlit baseline and explain the HR/SpO₂/temperature baseline.
Explain that the prototype uses an XGBoost classifier over current and trend
features.

**1:15–2:10 — Live simulation**
Run Normal, then Gradual deterioration. Show the risk score increasing.

**2:10–2:35 — Action**
Point out the high-risk state and caregiver alert event.

**2:35–2:50 — Edge/offline**
Explain that the local scoring path can make the detection decision without
waiting for a cloud request.

**2:50–3:00 — Close**
"LifeGuard AI aims to move monitoring from reactive thresholds toward
personalized predictive trend detection."
