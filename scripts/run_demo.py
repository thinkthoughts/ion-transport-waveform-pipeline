from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from ion_transport_waveform.config import TrapConfig, IonSpecies
from ion_transport_waveform.transport_path import minimum_jerk_path
from ion_transport_waveform.motion_sim import simulate_ion_motion
from ion_transport_waveform.excitation_metrics import residual_amplitude, residual_energy_proxy

cfg = TrapConfig()
ion = IonSpecies()

duration = 20e-6
t = np.linspace(0, duration, 1200)
path = minimum_jerk_path(t, x0=-80e-6, x1=80e-6, duration=duration)
x, v = simulate_ion_motion(t, path, cfg.omega_rad_s)

amp = residual_amplitude(x, path)
energy = residual_energy_proxy(x, v, path, cfg.omega_rad_s, mass_kg=ion.mass_kg)

figures = Path("figures")
figures.mkdir(exist_ok=True)

plt.figure(figsize=(7, 4))
plt.plot(t * 1e6, path * 1e6, label="target well")
plt.plot(t * 1e6, x * 1e6, label="ion trajectory")
plt.xlabel("time (µs)")
plt.ylabel("position (µm)")
plt.title("Ion transport trajectory")
plt.legend()
plt.tight_layout()
plt.savefig(figures / "motion_trace.png", dpi=180)

print(f"Residual amplitude: {amp:.3e} m")
print(f"Residual energy proxy: {energy:.3e} J")
print("Saved figures/motion_trace.png")
