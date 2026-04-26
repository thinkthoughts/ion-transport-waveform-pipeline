"""
Task 03 — Compare Two Waveforms

Loads two example transport waveforms, simulates ion motion for both, and
compares residual excitation metrics.

Default comparison:
    linear transport vs minimum-jerk transport

Outputs:
    outputs/comparison_motion.png
    outputs/comparison_residual.png
    outputs/comparison_summary.txt
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


def load_waveform(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Load waveform CSV with columns time, position."""
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run tasks/utils/generate_example_waveforms.py first."
        )

    times = []
    positions = []

    with path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        required = {"time", "position"}
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"{path} must contain columns: time, position")

        for row in reader:
            times.append(float(row["time"]))
            positions.append(float(row["position"]))

    t = np.asarray(times, dtype=float)
    x_c = np.asarray(positions, dtype=float)

    if not np.all(np.diff(t) > 0):
        raise ValueError(f"{path} time column must be strictly increasing")

    return t, x_c


def analyze_waveform(label: str, path: Path, cfg: TrapConfig, ion: IonSpecies) -> dict:
    """Simulate and compute metrics for one waveform."""
    t, x_c = load_waveform(path)
    x, v = simulate_ion_motion(t, x_c, cfg.omega_rad_s)
    residual = x - x_c

    return {
        "label": label,
        "path": path,
        "t": t,
        "x_c": x_c,
        "x": x,
        "v": v,
        "residual": residual,
        "residual_amplitude": residual_amplitude(x, x_c),
        "residual_energy": residual_energy_proxy(
            x, v, x_c, cfg.omega_rad_s, mass_kg=ion.mass_kg
        ),
        "max_abs_residual": float(np.max(np.abs(residual))),
        "rms_residual": float(np.sqrt(np.mean(residual**2))),
    }


def save_summary(path: Path, results: list[dict]) -> None:
    """Write comparison summary."""
    sorted_by_amp = sorted(results, key=lambda r: r["residual_amplitude"])
    best = sorted_by_amp[0]
    worst = sorted_by_amp[-1]

    amp_ratio = worst["residual_amplitude"] / best["residual_amplitude"]
    energy_ratio = worst["residual_energy"] / best["residual_energy"]

    lines = [
        "Task 03 — Compare Two Waveforms",
        "",
        "Compared waveforms:",
    ]

    for r in results:
        lines.extend([
            f"  {r['label']}:",
            f"    file: {r['path'].relative_to(path.parents[2]) if len(path.parents) > 2 else r['path']}",
            f"    residual_amplitude_m: {r['residual_amplitude']:.6e}",
            f"    residual_energy_J:    {r['residual_energy']:.6e}",
            f"    max_abs_residual_m:   {r['max_abs_residual']:.6e}",
            f"    rms_residual_m:       {r['rms_residual']:.6e}",
            "",
        ])

    lines.extend([
        "Result:",
        f"  Lower-excitation waveform: {best['label']}",
        f"  Higher-excitation waveform: {worst['label']}",
        f"  Residual amplitude ratio (higher/lower): {amp_ratio:.3e}",
        f"  Residual energy ratio (higher/lower):    {energy_ratio:.3e}",
        "",
        "Interpretation:",
        "  Smooth endpoint constraints reduce impulsive forcing.",
        "  The minimum-jerk waveform should produce less residual ringing than",
        "  a linear waveform with sharper endpoint behavior.",
        "",
    ])

    path.write_text("\n".join(lines))


def main() -> None:
    cfg = TrapConfig()
    ion = IonSpecies()

    output_dir = TASK_DIR / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    results = [
        analyze_waveform(label, waveform_path, cfg, ion)
        for label, waveform_path in WAVEFORMS.items()
    ]

    # Figure 1: waveform/trajectory comparisons
    plt.figure(figsize=(8.2, 4.8))
    for r in results:
        t_us = r["t"] * 1e6
        plt.plot(t_us, r["x_c"] * 1e6, linestyle="--", label=f"{r['label']} target")
        plt.plot(t_us, r["x"] * 1e6, label=f"{r['label']} ion")

    plt.xlabel("time (µs)")
    plt.ylabel("position (µm)")
    plt.title("Waveform comparison: target paths and ion trajectories")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(output_dir / "comparison_motion.png", dpi=180)
    plt.close()

    # Figure 2: residual comparison
    plt.figure(figsize=(8.2, 4.8))
    for r in results:
        plt.plot(r["t"] * 1e6, r["residual"] * 1e9, label=r["label"])

    plt.xlabel("time (µs)")
    plt.ylabel("residual $x(t)-x_c(t)$ (nm)")
    plt.title("Residual motion comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "comparison_residual.png", dpi=180)
    plt.close()

    save_summary(output_dir / "comparison_summary.txt", results)

    print("\nTask 03 complete.")
    print(f"Outputs: {output_dir}")
    for r in results:
        print(
            f"{r['label']:>14s} | "
            f"amp={r['residual_amplitude']:.3e} m | "
            f"energy={r['residual_energy']:.3e} J"
        )


if __name__ == "__main__":
    main()
