# Task 02 — Design a Transport Waveform

## Objective

You are given transport requirements and asked to design a waveform.

The goal is to construct a smooth transport path, simulate ion motion, and
evaluate residual excitation.

---

## Requirements

Design a transport waveform with:

- start position: `-80 µm`
- end position: `+80 µm`
- duration: `20 µs`
- method: minimum-jerk trajectory

---

## Tasks

1. Generate a minimum-jerk waveform:

   \[
   x_c(t) = x_0 + (x_1 - x_0)(10u^3 - 15u^4 + 6u^5)
   \]

   where:

   \[
   u = t/T
   \]

2. Save the designed waveform as:

   ```text
   designed_waveform.csv
   ```

3. Simulate ion motion using:

   \[
   m\ddot{x}(t) = -m\omega^2\big[x(t) - x_c(t)\big]
   \]

4. Compute residual motion:

   \[
   r(t) = x(t) - x_c(t)
   \]

5. Evaluate excitation using:
   - residual amplitude
   - residual energy proxy
   - trajectory tracking

---

## Outputs

- `designed_waveform.csv`  
  Generated time/position waveform

- `outputs/designed_waveform.png`  
  Designed transport path

- `outputs/motion_trace.png`  
  Ion trajectory vs designed waveform

- `outputs/residual_time_series.png`  
  Residual motion

- `outputs/excitation_summary.txt`  
  Key metrics and interpretation

---

## Evaluation Criteria

A good designed waveform:

- starts and ends at the requested positions
- has smooth endpoints
- produces low residual motion
- avoids large oscillatory ringing

---

## Context

This task reflects a common design workflow:

> Given transport requirements, design a waveform and test whether it meets excitation constraints.

This is distinct from Task 01, where the waveform is already provided.
