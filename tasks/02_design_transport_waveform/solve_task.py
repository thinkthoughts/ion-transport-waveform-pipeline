"""
Task 02 — Design a Transport Waveform

Designs a minimum-jerk transport waveform from requirements, simulates ion
motion, and evaluates residual excitation.

Outputs:
    designed_waveform.csv
    outputs/designed_waveform.png
    outputs/motion_trace.png
    outputs/residual_time_series.png
    outputs/excitation_summary.txt
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


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
from ion_transport_waveform.transport_path import minimum_jerk_path
from ion_transport_waveform.motion_sim import simulate_ion_motion
from ion_transport_waveform.excitation_metrics import (
    residual_amplitude,
    residual_energy_proxy,
)


START_POSITION_M = -80e-6
END_POSITION_M = 80e-6
DURATION_S = 20e-6
NUM_SAMPLES = 500


def save_waveform_csv(path: Path, t: np.ndarray, x_c: np.ndarray) -> None:
    """Save designed waveform as CSV with columns time, position."""
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "position"])
        for ti, xi in zip(t, x_c):
            writer.writerow([f"{ti:.12e}", f"{xi:.12e}"])


def save_summary(
    path: Path,
    *,
    duration_s: float,
    start_m: float,
    end_m: float,
    residual_amp_m: float,
    residual_energy_j: float,
    max_residual_m: float,
    rms_residual_m: float,
) -> None:
    """Write a plain-text excitation summary."""
    text = f"""Task 02 — Design a Transport Waveform

Design requirements:
  start_position_m:   {start_m:.6e}
  start_position_um:  {start_m * 1e6:.3f}
  end_position_m:     {end_m:.6e}
  end_position_um:    {end_m * 1e6:.3f}
  duration_s:         {duration_s:.6e}
  duration_us:        {duration_s * 1e6:.3f}
  method:             minimum-jerk

Excitation metrics:
  residual_amplitude_m:   {residual_amp_m:.6e}
  residual_energy_J:      {residual_energy_j:.6e}
  max_abs_residual_m:     {max_residual_m:.6e}
  rms_residual_m:         {rms_residual_m:.6e}

Interpretation:
  The designed waveform uses smooth endpoint constraints to reduce
  impulsive forcing. Smaller residual amplitude and residual energy
  indicate lower motional excitation.
"""
    path.write_text(text)


def main() -> None:
    cfg = TrapConfig()
    ion = IonSpecies()

    output_dir = TASK_DIR / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    t = np.linspace(0.0, DURATION_S, NUM_SAMPLES)
    x_c = minimum_jerk_path(
        t,
        x0=START_POSITION_M,
        x1=END_POSITION_M,
        duration=DURATION_S,
    )

    waveform_path = TASK_DIR / "designed_waveform.csv"
    save_waveform_csv(waveform_path, t, x_c)

    x, v = simulate_ion_motion(t, x_c, cfg.omega_rad_s)

    residual = x - x_c
    amp = residual_amplitude(x, x_c)
    energy = residual_energy_proxy(x, v, x_c, cfg.omega_rad_s, mass_kg=ion.mass_kg)
    max_residual = float(np.max(np.abs(residual)))
    rms_residual = float(np.sqrt(np.mean(residual**2)))

    plt.figure(figsize=(7.4, 4.3))
    plt.plot(t * 1e6, x_c * 1e6)
    plt.xlabel("time (µs)")
    plt.ylabel("trap center $x_c(t)$ (µm)")
    plt.title("Designed minimum-jerk transport waveform")
    plt.tight_layout()
    plt.savefig(output_dir / "designed_waveform.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.4, 4.3))
    plt.plot(t * 1e6, x_c * 1e6, label="designed waveform $x_c(t)$")
    plt.plot(t * 1e6, x * 1e6, label="ion trajectory $x(t)$")
    plt.xlabel("time (µs)")
    plt.ylabel("position (µm)")
    plt.title("Ion response to designed transport waveform")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "motion_trace.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.4, 4.3))
    plt.plot(t * 1e6, residual * 1e9)
    plt.xlabel("time (µs)")
    plt.ylabel("residual $x(t)-x_c(t)$ (nm)")
    plt.title("Residual motion for designed waveform")
    plt.tight_layout()
    plt.savefig(output_dir / "residual_time_series.png", dpi=180)
    plt.close()

    save_summary(
        output_dir / "excitation_summary.txt",
        duration_s=DURATION_S,
        start_m=START_POSITION_M,
        end_m=END_POSITION_M,
        residual_amp_m=amp,
        residual_energy_j=energy,
        max_residual_m=max_residual,
        rms_residual_m=rms_residual,
    )

    print("\nTask 02 complete.")
    print(f"Designed waveform: {waveform_path}")
    print(f"Outputs: {output_dir}")
    print(f"Residual amplitude: {amp:.3e} m")
    print(f"Residual energy:    {energy:.3e} J")


if __name__ == "__main__":
    main()
