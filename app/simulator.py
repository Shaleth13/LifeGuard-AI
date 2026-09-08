"""Synthetic wearable stream used for the live hackathon demonstration."""
import random


def generate_reading(step: int, deterioration: bool = False):
    """Generate realistic-looking normal or gradually deteriorating vitals."""
    if deterioration and step >= 15:
        p = min((step - 15) / 25, 1.0)
        hr = 72 + 45*p + random.gauss(0, 1.8)
        spo2 = 98 - 4.0*p + random.gauss(0, .18)
        temp = 98.4 + 1.1*p + random.gauss(0, .08)
        motion = .2 + 1.4*p + random.random()*.2
    else:
        hr = 72 + random.gauss(0, 2)
        spo2 = 98 + random.gauss(0, .2)
        temp = 98.4 + random.gauss(0, .08)
        motion = .2 + random.random()*.15

    return {
        "heart_rate": round(hr, 2),
        "spo2": round(max(85, min(100, spo2)), 2),
        "temperature": round(temp, 2),
        "motion": round(motion, 2),
    }
