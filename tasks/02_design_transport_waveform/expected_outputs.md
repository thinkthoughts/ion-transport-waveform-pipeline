# Expected Outputs — Task 02

## Overview

Running `solve_task.py` should design a waveform, simulate the ion response,
and write outputs into:

```text
outputs/
  designed_waveform.png
  motion_trace.png
  residual_time_series.png
  excitation_summary.txt
```

It should also create:

```text
designed_waveform.csv
```

---

## designed_waveform.csv

The generated waveform should contain:

```text
time,position
```

### Expected behavior

- Starts near `-80 µm`
- Ends near `+80 µm`
- Uses smooth minimum-jerk interpolation
- Has no discontinuous jumps

---

## designed_waveform.png

Shows the designed trap-center path \(x_c(t)\).

### Expected behavior

- Smooth S-shaped curve
- Flat slope at beginning and end
- Continuous transition from start to end

---

## motion_trace.png

Shows:

- designed waveform \(x_c(t)\)
- simulated ion trajectory \(x(t)\)

### Expected behavior

- Ion trajectory closely follows the designed path
- Only small deviations occur during transport

---

## residual_time_series.png

Shows:

\[
r(t)=x(t)-x_c(t)
\]

### Expected behavior

- Residual remains small
- No large ringing after transport
- Smooth waveform produces low excitation

---

## excitation_summary.txt

Contains:

- design requirements
- residual amplitude
- residual energy
- max residual
- RMS residual

---

## Success Criteria

The task is successful if:

- `designed_waveform.csv` is generated
- all output figures are generated
- excitation metrics are written
- waveform endpoints match the design requirements
- residual excitation is small for the smooth waveform

---

## Notes

This task demonstrates waveform design from requirements.  
It remains a simplified 1D harmonic model and does not represent a full
hardware-specific electrode voltage solution.
