import numpy as np
from ion_transport_waveform.motion_sim import simulate_ion_motion

def test_motion_sim_runs():
    t = np.linspace(0, 1e-5, 100)
    path = np.zeros_like(t)
    x, v = simulate_ion_motion(t, path, omega_rad_s=2*np.pi*1e6)
    assert x.shape == t.shape
    assert v.shape == t.shape
