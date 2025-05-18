"""Unit conversion functions."""
import numpy as np

# Convert RPM to rad/s
def rpm_to_radps(rpm):
    return rpm * 2 * np.pi / 60

def feet_to_meter(feet):
    return feet * 0.3048  # 1 ft = 0.3048 m
