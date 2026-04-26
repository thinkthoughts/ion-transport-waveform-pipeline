# Task 03 — Compare Two Waveforms (updated solve_task.py)

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "src" / "ion_transport_waveform").exists():
            return candidate
    raise RuntimeError("Could not find repo root")


TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = find_repo_root(TASK_DIR)

if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from ion_transport_waveform.config import TrapConfig, IonSpecies
from ion_transport_waveform.motion_sim import simulate_ion_motion
from ion_transport_waveform.excitation_metrics import (
    residual_amplitude,
    residual_energy_proxy,
)

EXAMPLE_DIR = REPO_ROOT / "tasks" / "example_waveforms"

WAVEFORMS = {
    "linear": EXAMPLE_DIR / "input_waveform_linear.csv",
    "minimum_jerk": EXAMPLE_DIR / "input_waveform_minimum_jerk.csv",
}


def load_waveform(path: Path):
    times, positions = [], []
    with path.open("r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            times.append(float(row["time"]))
            positions.append(float(row["position"]))
    return np.array(times), np.array(positions)


def analyze_waveform(label, path, cfg, ion):
    t, x_c = load_waveform(path)
    x, v = simulate_ion_motion(t, x_c, cfg.omega_rad_s)
    residual = x - x_c

    omega = cfg.omega_rad_s
    E_norm = 0.5 * (v**2 + (omega * residual)**2)
    E_norm_rms = float(np.mean(E_norm))
    E_norm_peak = float(np.max(E_norm))

    return {
        "label": label,
        "t": t,
        "x_c": x_c,
        "x": x,
        "residual": residual,
        "residual_amplitude": residual_amplitude(x, x_c),
        "residual_energy": residual_energy_proxy(
            x, v, x_c, cfg.omega_rad_s, mass_kg=ion.mass_kg
        ),
        "energy_norm_rms": E_norm_rms,
        "energy_norm_peak": E_norm_peak,
    }


def main():
    cfg = TrapConfig()
    ion = IonSpecies()

    results = [
        analyze_waveform(label, path, cfg, ion)
        for label, path in WAVEFORMS.items()
    ]

    print("\nTask 03 complete.")
    for r in results:
        print(
            f"{r['label']:>14s} | "
            f"amp={r['residual_amplitude']:.3e} m | "
            f"E_norm_rms={r['energy_norm_rms']:.3e} | "
            f"E_norm_peak={r['energy_norm_peak']:.3e}"
        )


if __name__ == "__main__":
    main()
