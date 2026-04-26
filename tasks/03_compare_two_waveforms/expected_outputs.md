# Expected Outputs — Task 03

## Overview

Running `solve_task.py` compares two candidate waveforms and writes:

```text
outputs/
  comparison_motion.png
  comparison_residual.png
  comparison_summary.txt
```

---

## comparison_motion.png

Shows target paths and simulated ion trajectories for:

- linear transport
- minimum-jerk transport

### Expected behavior

- Both target paths move from `-80 µm` to `+80 µm`
- Minimum-jerk path is smooth at endpoints
- Linear path has sharper endpoint behavior

---

## comparison_residual.png

Shows residual motion:

\[
r(t)=x(t)-x_c(t)
\]

### Expected behavior

- Linear waveform produces larger oscillatory residual motion
- Minimum-jerk waveform produces smaller residual motion
- Difference is visible in time-domain ringing

---

## comparison_summary.txt

Contains:

- residual amplitude for both waveforms
- residual energy for both waveforms
- max residual and RMS residual
- lower-excitation waveform identification
- amplitude and energy ratios

---

## Success Criteria

The task is successful if:

- both waveforms load successfully
- both simulations run without errors
- comparison figures are generated
- summary identifies minimum-jerk as the lower-excitation waveform

---

## Notes

This task demonstrates design comparison, not hardware-specific waveform
implementation. It uses shared example waveform CSVs from:

```text
tasks/example_waveforms/
```
