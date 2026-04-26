import numpy as np

def solve_voltages_for_target_well(
    basis: np.ndarray,
    x_grid: np.ndarray,
    target_x: float,
    voltage_limit: float = 10.0,
    ridge: float = 1e-6,
) -> np.ndarray:
    """Solve a simple constrained least-squares proxy for a well centered at target_x.

    This creates a target harmonic-like shape around target_x and solves Bv ≈ target.
    It is intentionally simplified for a transparent first-pass pipeline.
    """
    x = np.asarray(x_grid)
    B = np.asarray(basis)
    scale = np.max(np.abs(x - target_x)) or 1.0
    target = ((x - target_x) / scale) ** 2
    target = target - target.min()

    lhs = B.T @ B + ridge * np.eye(B.shape[1])
    rhs = B.T @ target
    v = np.linalg.solve(lhs, rhs)

    max_abs = np.max(np.abs(v))
    if max_abs > voltage_limit:
        v = v * (voltage_limit / max_abs)
    return v

def waveform_for_path(basis: np.ndarray, x_grid: np.ndarray, path_x: np.ndarray, voltage_limit: float = 10.0) -> np.ndarray:
    """Generate voltage waveform V[t, electrode] for a target path."""
    return np.vstack([
        solve_voltages_for_target_well(basis, x_grid, x_t, voltage_limit=voltage_limit)
        for x_t in path_x
    ])
