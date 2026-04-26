"""
Task 01 — Evaluate a Given Transport Waveform

Loads a simplified transport waveform from input_waveform.csv, treats it as
the moving trap center x_c(t), simulates ion motion, and reports residual
excitation metrics.

Expected input CSV columns:
    time, position

Outputs:
    motion_trace.png
    residual_time_series.png
    excitation_summary.txt
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------
# Repo path bootstrap
# ----------------------------

def find_repo_root(start: Path) -> Path:
    """Walk upward until the repo root containing src/ is found."""
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "src" / "ion_transport_waveform").exists():
            return candidate
    raise RuntimeError("Could not find repo root containing src/ion_transport_waveform")


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


# ----------------------------
# I/O helpers
# ----------------------------

def load_waveform(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Load waveform CSV with columns time, position."""
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Copy or generate a waveform CSV and name it input_waveform.csv."
        )

    times = []
    positions = []

    with path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        required = {"time", "position"}
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise ValueError("CSV must contain columns: time, position")

        for row in reader:
            times.append(float(row["time"]))
            positions.append(float(row["position"]))

    t = np.asarray(times, dtype=float)
    x_c = np.asarray(positions, dtype=float)

    if t.ndim != 1 or x_c.ndim != 1 or len(t) != len(x_c):
        raise ValueError("Invalid waveform arrays")

    if len(t) < 3:
        raise ValueError("Waveform must contain at least 3 samples")

    if not np.all(np.diff(t) > 0):
        raise ValueError("time column must be strictly increasing")

    return t, x_c


def save_summary(
    path: Path,
    *,
    input_file: Path,
    duration_s: float,
    distance_m: float,
    residual_amp_m: float,
    residual_energy_j: float,
    max_residual_m: float,
    rms_residual_m: float,
) -> None:
    """Write a plain-text excitation summary."""
    text = f"""Task 01 — Evaluate a Given Transport Waveform

Input file:
  {input_file}

Transport:
  duration_s:        {duration_s:.6e}
  duration_us:       {duration_s * 1e6:.3f}
  distance_m:        {distance_m:.6e}
  distance_um:       {distance_m * 1e6:.3f}

Excitation metrics:
  residual_amplitude_m:   {residual_amp_m:.6e}
  residual_energy_J:      {residual_energy_j:.6e}
  max_abs_residual_m:     {max_residual_m:.6e}
  rms_residual_m:         {rms_residual_m:.6e}

Interpretation:
  Smaller residual amplitude and residual energy indicate lower motional excitation.
  Oscillatory residual motion indicates ringing after or during transport.
"""
    path.write_text(text)


# ----------------------------
# Main task
# ----------------------------

def main() -> None:
    cfg = TrapConfig()
    ion = IonSpecies()

    input_file = TASK_DIR / "input_waveform.csv"
    output_dir = TASK_DIR / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    t, x_c = load_waveform(input_file)

    x, v = simulate_ion_motion(t, x_c, cfg.omega_rad_s)

    residual = x - x_c
    amp = residual_amplitude(x, x_c)
    energy = residual_energy_proxy(x, v, x_c, cfg.omega_rad_s, mass_kg=ion.mass_kg)
    max_residual = float(np.max(np.abs(residual)))
    rms_residual = float(np.sqrt(np.mean(residual**2)))

    duration = float(t[-1] - t[0])
    distance = float(x_c[-1] - x_c[0])

    # Figure 1: target waveform vs ion trajectory
    plt.figure(figsize=(7.4, 4.3))
    plt.plot(t * 1e6, x_c * 1e6, label="target waveform $x_c(t)$")
    plt.plot(t * 1e6, x * 1e6, label="ion trajectory $x(t)$")
    plt.xlabel("time (µs)")
    plt.ylabel("position (µm)")
    plt.title("Ion response to supplied transport waveform")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "motion_trace.png", dpi=180)
    plt.close()

    # Figure 2: residual motion
    plt.figure(figsize=(7.4, 4.3))
    plt.plot(t * 1e6, residual * 1e9)
    plt.xlabel("time (µs)")
    plt.ylabel("residual $x(t)-x_c(t)$ (nm)")
    plt.title("Residual motion")
    plt.tight_layout()
    plt.savefig(output_dir / "residual_time_series.png", dpi=180)
    plt.close()

    # Summary
    save_summary(
        output_dir / "excitation_summary.txt",
        input_file=input_file,
        duration_s=duration,
        distance_m=distance,
        residual_amp_m=amp,
        residual_energy_j=energy,
        max_residual_m=max_residual,
        rms_residual_m=rms_residual,
    )

    print("\nTask 01 complete.")
    print(f"Input: {input_file}")
    print(f"Outputs: {output_dir}")
    print(f"Residual amplitude: {amp:.3e} m")
    print(f"Residual energy:    {energy:.3e} J")


if __name__ == "__main__":
    main()
