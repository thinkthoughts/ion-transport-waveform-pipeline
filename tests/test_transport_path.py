import numpy as np
from ion_transport_waveform.transport_path import minimum_jerk_path

def test_minimum_jerk_endpoints():
    t = np.linspace(0, 1.0, 101)
    x = minimum_jerk_path(t, -1.0, 2.0, 1.0)
    assert np.isclose(x[0], -1.0)
    assert np.isclose(x[-1], 2.0)
