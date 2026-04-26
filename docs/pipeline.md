# Pipeline

```text
Electrode Basis → Potential Well → Transport Path → Voltage Waveform
       ↓                ↓               ↓                  ↓
  Field Model     Position Target   Time Param      Control Signal
       ↓                ↓               ↓                  ↓
           Ion Motion Simulation → Excitation Metric
```

## Initial scope

The first version uses a simplified 1D model. That keeps the pipeline transparent:

1. define electrode basis functions
2. solve approximate voltages for target wells
3. move the target well along a smooth trajectory
4. simulate ion motion in a moving harmonic potential
5. measure residual excitation
