# Pipeline

The transport pipeline is:

```
electrode basis
→ potential well
→ transport path
→ voltage waveform
→ ion motion
→ excitation metric
→ tradeoff analysis
```

---

## 1. Electrode Basis

Construct spatial basis functions representing electrode potentials.

---

## 2. Potential Well

Solve for voltages that produce a harmonic well at a target position.

---

## 3. Transport Path

Define time-dependent well position:

- linear path
- minimum-jerk path (preferred)

---

## 4. Voltage Waveform

Map trajectory → electrode voltages over time.

---

## 5. Ion Motion

Simulate dynamics:

```
m ẍ = -m ω² (x - x_c(t))
```

---

## 6. Excitation Metric

Measure residual motion:

- displacement
- velocity
- energy proxy

---

## 7. Tradeoff Analysis

Evaluate:

- duration vs excitation
- velocity vs excitation
- acceleration vs excitation
