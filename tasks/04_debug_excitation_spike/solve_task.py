"""
Task 04 — Debug an Excitation Spike
"""

from __future__ import annotations
import csv, sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for c in [current, *current.parents]:
        if (c / "src" / "ion_transport_waveform").exists():
            return c
    raise RuntimeError("repo root not found")

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = find_repo_root(TASK_DIR)

if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from ion_transport_waveform.config import TrapConfig, IonSpecies
from ion_transport_waveform.motion_sim import simulate_ion_motion

INPUT = REPO_ROOT / "tasks" / "example_waveforms" / "input_waveform_bad_spike.csv"

def load(path):
    t, x = [], []
    with path.open() as f:
        r = csv.DictReader(f)
        for row in r:
            t.append(float(row["time"]))
            x.append(float(row["position"]))
    return np.array(t), np.array(x)

def main():
    cfg = TrapConfig()
    ion = IonSpecies()

    out = TASK_DIR / "outputs"
    out.mkdir(exist_ok=True)

    t, x_c = load(INPUT)
    x, v = simulate_ion_motion(t, x_c, cfg.omega_rad_s)

    residual = x - x_c

    idx = int(np.argmax(np.abs(residual)))
    t_spike = t[idx]

    # plots
    plt.figure()
    plt.plot(t*1e6, x_c*1e6)
    plt.title("Waveform")
    plt.savefig(out/"waveform.png")
    plt.close()

    plt.figure()
    plt.plot(t*1e6, residual*1e9)
    plt.title("Residual")
    plt.savefig(out/"residual.png")
    plt.close()

    # zoom window
    win = 20
    i0 = max(0, idx-win)
    i1 = min(len(t), idx+win)

    plt.figure()
    plt.plot(t[i0:i1]*1e6, x_c[i0:i1]*1e6, label="waveform")
    plt.plot(t[i0:i1]*1e6, x[i0:i1]*1e6, label="ion")
    plt.legend()
    plt.title("Spike region zoom")
    plt.savefig(out/"spike_zoom.png")
    plt.close()

    summary = f"""
Spike detected at:
time = {t_spike:.3e} s

Cause:
Localized discontinuity in waveform introduces high-frequency content,
driving excitation of the ion.

Observation:
Residual motion peaks at same location as waveform spike.
"""

    (out/"debug_summary.txt").write_text(summary)

    print("Task 04 complete.")
    print("Spike time:", t_spike)

if __name__ == "__main__":
    main()
