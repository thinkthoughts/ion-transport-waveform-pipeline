import numpy as np

def minimum_jerk_path(t: np.ndarray, x0: float, x1: float, duration: float) -> np.ndarray:
    """Minimum-jerk path from x0 to x1 over duration.

    s(u) = 10u^3 - 15u^4 + 6u^5, with zero velocity/acceleration at endpoints.
    """
    u = np.clip(np.asarray(t) / duration, 0.0, 1.0)
    s = 10*u**3 - 15*u**4 + 6*u**5
    return x0 + (x1 - x0) * s

def linear_path(t: np.ndarray, x0: float, x1: float, duration: float) -> np.ndarray:
    u = np.clip(np.asarray(t) / duration, 0.0, 1.0)
    return x0 + (x1 - x0) * u
