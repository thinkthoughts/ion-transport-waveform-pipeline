from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from ion_transport_waveform.config import TrapConfig, IonSpecies
from ion_transport_waveform.transport_path import minimum_jerk_path
from ion_transport_waveform.motion_sim import simulate_ion_motion
from ion_transport_waveform.excitation_metrics import (
    residual_amplitude,
    residual_energy_proxy,
)

# ----------------------------
# Configuration
# ----------------------------

cfg = TrapConfig()
ion = IonSpecies()

duration = 20e-6  # 20 µs
num_points = 1200

x0 = -80e-6
x1 = 80e-6

# ----------------------------
# Time + trajectory
# ----------------------------

t = np.linspace(0, duration, num_points)
path = minimum_jerk_path(t, x0=x0, x1=x1, duration=duration)

# ----------------------------
# Simulation
# ----------------------------

x, v = simulate_ion_motion(t, path, cfg.omega_rad_s)

# ----------------------------
# Metrics
# ----------------------------

amp = residual_amplitude(x, path)
energy = residual_energy_proxy(
    x, v, path, cfg.omega_rad_s, mass_kg=ion.mass_kg
)

# ----------------------------
# Output directory
# ----------------------------

figures = Path("figures")
figures.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Plot: trajectory
# ----------------------------

plt.figure(figsize=(7, 4))
plt.plot(t * 1e6, path * 1e6, label="target well")
plt.plot(t * 1e6, x * 1e6, label="ion trajectory")
plt.xlabel("time (µs)")
plt.ylabel("position (µm)")
plt.title("Ion transport trajectory")
plt.legend()
plt.tight_layout()

outfile = figures / "motion_trace.png"
plt.savefig(outfile, dpi=180)
plt.close()

# ----------------------------
# Print summary
# ----------------------------

print("\n--- Transport Summary ---")
print(f"Duration: {duration * 1e6:.1f} µs")
print(f"Start → End: {x0 * 1e6:.1f} → {x1 * 1e6:.1f} µm")
print(f"Residual amplitude: {amp:.3e} m")
print(f"Residual energy proxy: {energy:.3e} J")
print(f"Saved: {outfile}")
