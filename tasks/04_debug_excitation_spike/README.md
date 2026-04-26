# Task 04 — Debug an Excitation Spike

## Objective

Given a waveform that produces unexpectedly high excitation, identify
where and why the excitation occurs.

---

## Input

```text
tasks/example_waveforms/input_waveform_bad_spike.csv
```

This waveform contains a localized discontinuity (spike).

---

## Tasks

1. Load the waveform
2. Simulate ion motion
3. Compute residual motion:
   r(t) = x(t) - x_c(t)
4. Identify time index of maximum residual
5. Inspect waveform around that region
6. Plot:
   - waveform
   - residual
   - zoomed region of spike
7. Explain cause of excitation

---

## Outputs

```text
outputs/
  waveform.png
  residual.png
  spike_zoom.png
  debug_summary.txt
```

---

## Evaluation Criteria

- Spike location correctly identified
- Residual spike corresponds to waveform discontinuity
- Explanation links sharp features → excitation

---

## Context

This reflects real debugging:

> A waveform causes unexpected excitation → find and fix the cause.
