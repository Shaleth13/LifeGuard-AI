"""LifeGuard AI interactive browser dashboard."""
import time
import streamlit as st
import pandas as pd

from app.simulator import generate_reading
from app.risk_engine import predict_risk

st.set_page_config(page_title="LifeGuard AI", page_icon="❤", layout="wide")

st.title("LifeGuard AI")
st.caption("Personalized, edge-style predictive emergency detection — hackathon prototype")

BASELINE = {"heart_rate": 72.0, "spo2": 98.0, "temperature": 98.4, "motion": .2}

with st.sidebar:
    st.header("Simulation")
    scenario = st.radio("Scenario", ["Normal", "Gradual deterioration"])
    duration = st.slider("Samples", 20, 60, 40)
    run = st.button("▶ Run live demo", use_container_width=True)

c1, c2, c3, c4 = st.columns(4)
risk_box = c1.empty()
hr_box = c2.empty()
spo2_box = c3.empty()
temp_box = c4.empty()
status_box = st.empty()
chart_box = st.empty()

if run:
    rows = []
    recent = []

    for step in range(duration):
        reading = generate_reading(step, scenario == "Gradual deterioration")
        result = predict_risk(reading, recent[-12:], BASELINE)
        recent.append(reading)

        rows.append({
            "Sample": step + 1,
            "Heart Rate": reading["heart_rate"],
            "SpO₂": reading["spo2"],
            "Temperature": reading["temperature"],
            "Risk Score": result["risk_score"],
        })

        risk_box.metric("Risk Score", result["risk_score"], result["risk_level"])
        hr_box.metric("Heart Rate", f'{reading["heart_rate"]:.0f} bpm')
        spo2_box.metric("SpO₂", f'{reading["spo2"]:.1f}%')
        temp_box.metric("Temperature", f'{reading["temperature"]:.1f} °F')

        if result["alert"]:
            status_box.error(
                "🚨 HIGH RISK — " + ", ".join(result["reasons"]) +
                " | Caregiver alert triggered"
            )
        elif result["risk_level"] == "MODERATE":
            status_box.warning("⚠ Moderate deviation — continue monitoring")
        else:
            status_box.success("✓ Vitals are close to the personalized baseline")

        chart_box.line_chart(pd.DataFrame(rows).set_index("Sample"))
        time.sleep(.12)

st.divider()
st.subheader("Personalized Baseline")
b1, b2, b3 = st.columns(3)
b1.metric("Heart rate", "72 bpm")
b2.metric("SpO₂", "98%")
b3.metric("Temperature", "98.4 °F")

st.info(
    "Prototype only: the score is not a diagnosis and the system is not a clinically "
    "validated emergency medical device."
)
