"""Optional LSTM forecasting module.

This module forecasts the next heart-rate value from a short sequence.
It is included to make the trend-forecasting component reproducible.

The live dashboard does not require PyTorch; the XGBoost model powers the
default demo for fast startup.
"""
import torch
from torch import nn


class VitalLSTM(nn.Module):
    """Small LSTM for short-window vital forecasting."""

    def __init__(self, input_size=3, hidden_size=32):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.head = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.head(out[:, -1, :])


def make_model():
    """Return an untrained model ready for project-specific training."""
    return VitalLSTM()
