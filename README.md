# Ion Transport Waveform Pipeline

A minimal, reproducible pipeline for designing and evaluating
trapped-ion transport waveforms. Visit https://cosineconstraint.app/colab/ion_transport_waveform_pipeline.html 👈🏽

---

## Overview

This project connects waveform design directly to physical outcomes:

- transport trajectory
- ion motion
- residual excitation
- tradeoffs between speed and control

The implementation uses a transparent one-dimensional model so that
these relationships are directly visible.

---

## Key Result

Minimum-jerk transport suppresses excitation by orders of magnitude
relative to linear interpolation.

---

## Pipeline

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

## Quick Start

```bash
git clone https://github.com/thinkthoughts/ion-transport-waveform-pipeline.git
cd ion-transport-waveform-pipeline

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
export PYTHONPATH=$PWD/src

pytest -q
```

---

## Run Example

```bash
python scripts/run_transport_demo.py
```

Output:
- trajectory figure
- residual amplitude
- residual energy proxy

---

## Figures

See `figures/` or the paper for:

- trajectory tracking
- residual motion suppression
- excitation scaling
- frequency-domain behavior

---

## Paper

See:

```
paper/main.tex
```

or the compiled PDF.

---

## Documentation

- `docs/pipeline.md`
- `docs/glossary.md`
- `docs/figures.md`
- `docs/RESUME_connection.md`

---

## Tests

Run:

```bash
pytest -q
```

Expected:

```
3 passed
```

---

## Scope

This is a minimal computational model:

- harmonic trap approximation  
- trajectory-driven transport  
- excitation metrics and scaling  

It is intended to make transport–excitation relationships clear and
reproducible, not to model full experimental hardware.

---

## Repository

https://github.com/thinkthoughts/ion-transport-waveform-pipeline
