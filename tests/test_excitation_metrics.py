import numpy as np
from ion_transport_waveform.excitation_metrics import residual_amplitude

def test_residual_amplitude_zero_for_identical_paths():
    x = np.linspace(0, 1, 100)
    assert residual_amplitude(x, x) == 0.0
