# Task 01 — Evaluate a Given Transport Waveform

## Objective

You are given a transport waveform and asked to evaluate its effect on ion motion.

The goal is to simulate the ion response and quantify residual excitation.

---

## Inputs

- `input_waveform.csv`  
  Time-series data representing a transport waveform.

  Format:

  ```
  time (s), position (m)
  ```

  *(In this simplified task, the waveform is treated as the moving trap center \(x_c(t)\).)*

---

## Tasks

1. Load the waveform from `input_waveform.csv`
2. Simulate ion motion using the equation:

   \[
   m\ddot{x}(t) = -m\omega^2\big[x(t) - x_c(t)\big]
   \]

3. Compute residual motion:

   \[
   r(t) = x(t) - x_c(t)
   \]

4. Evaluate excitation using:
   - residual amplitude  
   - energy proxy  
   - (optional) frequency-domain analysis  

---

## Outputs

- `motion_trace.png`  
  Ion trajectory vs target waveform

- `residual_time_series.png`  
  Residual motion \(r(t)\)

- `excitation_summary.txt`  
  Key metrics:
  - residual amplitude  
  - residual energy  

---

## Evaluation Criteria

A good waveform:

- produces small residual motion  
- avoids oscillatory ringing  
- minimizes energy at the trap frequency  

---

## Notes

- This task uses a simplified 1D harmonic trap model  
- The waveform represents the trap center \(x_c(t)\), not electrode voltages  
- The goal is to evaluate behavior, not redesign the waveform  

---

## Context

This task reflects a common simulation workflow:

> Given a transport waveform, simulate ion motion and determine whether it meets excitation constraints.
