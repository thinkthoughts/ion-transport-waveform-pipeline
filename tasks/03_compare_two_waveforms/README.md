# Task 03 — Compare Two Waveforms

## Objective

You are given two transport waveforms and asked to compare their effect on
ion motion and residual excitation.

The goal is to quantify which waveform produces lower excitation and explain why.

---

## Inputs

This task uses shared example waveforms from:

```text
tasks/example_waveforms/
```

Default comparison:

- `input_waveform_linear.csv`
- `input_waveform_minimum_jerk.csv`

In this simplified task, each waveform is treated as the moving trap center
\(x_c(t)\), not electrode voltages.

---

## Tasks

1. Load both waveforms
2. Simulate ion motion for each waveform
3. Compute residual motion:

   \[
   r(t) = x(t) - x_c(t)
   \]

4. Compute excitation metrics:
   - residual amplitude
   - residual energy proxy
   - RMS residual

5. Save comparison plots and a summary

---

## Outputs

- `outputs/comparison_motion.png`  
  Target waveforms and ion trajectories

- `outputs/comparison_residual.png`  
  Residual motion for both waveforms

- `outputs/comparison_summary.txt`  
  Metric comparison and interpretation

---

## Evaluation Criteria

A good comparison should identify:

- which waveform produces smaller residual motion
- which waveform produces lower residual energy
- whether residual ringing is present
- why smoothness affects excitation

---

## Context

This task reflects a common analysis workflow:

> Given two candidate transport strategies, simulate both and select the lower-excitation option.
