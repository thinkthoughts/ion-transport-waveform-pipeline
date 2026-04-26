import numpy as np
from scipy.integrate import solve_ivp

def simulate_ion_motion(t_eval, path_x, omega_rad_s, x0=None, v0=0.0):
    """Simulate ion as harmonic oscillator whose center follows path_x(t).

    Equation:
        x'' = -omega^2 * (x - x_center(t))

    This proxy isolates transport excitation before adding full electrode-field dynamics.
    """
    t_eval = np.asarray(t_eval)
    path_x = np.asarray(path_x)
    if x0 is None:
        x0 = float(path_x[0])

    def center(t):
        return np.interp(t, t_eval, path_x)

    def rhs(t, y):
        x, v = y
        return [v, -(omega_rad_s ** 2) * (x - center(t))]

    sol = solve_ivp(
        rhs,
        (float(t_eval[0]), float(t_eval[-1])),
        [x0, v0],
        t_eval=t_eval,
        rtol=1e-8,
        atol=1e-10,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[0], sol.y[1]
