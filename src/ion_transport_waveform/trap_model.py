import numpy as np

def gaussian_electrode_basis(x_grid: np.ndarray, electrode_positions: np.ndarray, width: float) -> np.ndarray:
    """Return basis matrix B[i, j] = potential at x_i from unit voltage on electrode j."""
    x = np.asarray(x_grid)[:, None]
    centers = np.asarray(electrode_positions)[None, :]
    return np.exp(-0.5 * ((x - centers) / width) ** 2)

def potential_from_voltages(basis: np.ndarray, voltages: np.ndarray) -> np.ndarray:
    """Linear superposition V(x) = B @ v."""
    return np.asarray(basis) @ np.asarray(voltages)

def electric_field(x_grid: np.ndarray, potential: np.ndarray) -> np.ndarray:
    """Return E = -dV/dx using finite differences."""
    return -np.gradient(np.asarray(potential), np.asarray(x_grid))

def curvature_at_target(x_grid: np.ndarray, potential: np.ndarray, target_x: float) -> float:
    """Estimate second derivative d²V/dx² near target position."""
    d1 = np.gradient(np.asarray(potential), np.asarray(x_grid))
    d2 = np.gradient(d1, np.asarray(x_grid))
    idx = int(np.argmin(np.abs(np.asarray(x_grid) - target_x)))
    return float(d2[idx])
