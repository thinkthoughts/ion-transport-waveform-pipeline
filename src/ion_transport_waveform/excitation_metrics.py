import numpy as np

def residual_amplitude(x: np.ndarray, path_x: np.ndarray, tail_fraction: float = 0.25) -> float:
    """Estimate residual oscillation amplitude near the end of transport."""
    x = np.asarray(x)
    path_x = np.asarray(path_x)
    n0 = int((1.0 - tail_fraction) * len(x))
    residual = x[n0:] - path_x[n0:]
    return float(0.5 * (np.max(residual) - np.min(residual)))

def residual_energy_proxy(x: np.ndarray, v: np.ndarray, path_x: np.ndarray, omega_rad_s: float, mass_kg: float = 1.0) -> float:
    """Classical harmonic residual energy proxy at final time."""
    dx = float(np.asarray(x)[-1] - np.asarray(path_x)[-1])
    vf = float(np.asarray(v)[-1])
    return 0.5 * mass_kg * (vf**2 + (omega_rad_s * dx)**2)
