"""
Generate example transport waveforms for task demos.

Outputs are written to:

    tasks/example_waveforms/

Generated files:
    input_waveform_linear.csv
    input_waveform_minimum_jerk.csv
    input_waveform_bad_spike.csv
    input_waveform_fast_transport.csv

CSV format:
    time,position

In these simplified task demos, position is treated as the moving trap
center x_c(t), not electrode voltages.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


# ----------------------------
# Paths
# ----------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "tasks" / "example_waveforms"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ----------------------------
# Helpers
# ----------------------------

def save_csv(filename: str, t: np.ndarray, x: np.ndarray) -> None:
    """Save time/position waveform CSV."""
    path = OUT_DIR / filename
    data = np.column_stack((t, x))

    np.savetxt(
        path,
        data,
        delimiter=",",
        header="time,position",
        comments="",
    )

    print(f"saved {path.relative_to(REPO_ROOT)}")


def minimum_jerk(t: np.ndarray, x0: float, x1: float, duration: float) -> np.ndarray:
    """Minimum-jerk interpolation between x0 and x1."""
    u = np.clip(t / duration, 0.0, 1.0)
    s = 10 * u**3 - 15 * u**4 + 6 * u**5
    return x0 + (x1 - x0) * s


def linear(t: np.ndarray, x0: float, x1: float, duration: float) -> np.ndarray:
    """Linear interpolation between x0 and x1."""
    u = np.clip(t / duration, 0.0, 1.0)
    return x0 + (x1 - x0) * u


# ----------------------------
# Main
# ----------------------------

def main() -> None:
    x0 = -80e-6
    x1 = 80e-6

    # Standard 20 µs task waveforms
    duration = 20e-6
    t = np.linspace(0, duration, 500)

    # 1. Linear waveform: simple but excitation-prone
    x_linear = linear(t, x0=x0, x1=x1, duration=duration)
    save_csv("input_waveform_linear.csv", t, x_linear)

    # 2. Minimum-jerk waveform: smooth reference case
    x_mj = minimum_jerk(t, x0=x0, x1=x1, duration=duration)
    save_csv("input_waveform_minimum_jerk.csv", t, x_mj)

    # 3. Bad spike waveform: debug case with a local discontinuity
    x_spike = x_linear.copy()
    x_spike[200:210] += 10e-6
    save_csv("input_waveform_bad_spike.csv", t, x_spike)

    # 4. Fast transport waveform: smooth but short duration
    fast_duration = 5e-6
    t_fast = np.linspace(0, fast_duration, 500)
    x_fast = minimum_jerk(t_fast, x0=x0, x1=x1, duration=fast_duration)
    save_csv("input_waveform_fast_transport.csv", t_fast, x_fast)

    print("\nExample waveforms complete.")
    print(f"Output directory: {OUT_DIR.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
