# ion-transport-waveform-pipeline

Voltage waveforms for low-excitation trapped-ion transport in segmented RF Paul traps.

**electrode basis → transport path → waveform → ion motion → excitation metric**

This repository develops a compact computational pipeline for ion transport and waveform design:
- build simplified segmented-trap electrode basis potentials
- solve control voltages for moving potential wells
- generate smooth transport trajectories
- simulate ion motion through time-dependent potentials
- measure residual excitation under speed, bandwidth, and noise constraints

## Motivation

This project is designed as a public technical artifact connecting:
- recent trapped-ion transport / waveform-design literature
- numerical simulation and optimization workflows
- low-excitation shuttling in segmented RF Paul traps
- constraint-gated control synthesis (CGCS) framing

The target deliverables are:
1. reusable Python modules in `src/`
2. Colab-ready notebooks in `notebooks/`
3. figures in `figures/`
4. a short site page in `site/`
5. a CGCS-style paper in `paper/`

## Repository layout

```text
ion-transport-waveform-pipeline/
├── src/ion_transport_waveform/
├── notebooks/
├── docs/
├── figures/
├── data/
├── paper/
├── site/
└── tests/
```

## Quick start

```bash
git clone https://github.com/thinkthoughts/ion-transport-waveform-pipeline.git
cd ion-transport-waveform-pipeline
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

Run a minimal simulation:

```bash
python scripts/run_demo.py
```

## Colab notebooks

Planned notebook sequence:

| Notebook | Purpose |
|---|---|
| `00_trap_basis.ipynb` | Build simplified electrode-basis potentials |
| `01_well_positioning.ipynb` | Solve voltages for target harmonic wells |
| `02_transport_path.ipynb` | Generate smooth shuttling trajectories |
| `03_waveform_generation.ipynb` | Convert paths into voltage waveforms |
| `04_motion_simulation.ipynb` | Simulate ion motion |
| `05_excitation_metric.ipynb` | Measure residual excitation |
| `06_tradeoff_analysis.ipynb` | Compare speed, smoothness, bandwidth, and excitation |

## Core equation

The basic 1D simulation model is

```math
m \ddot{x}(t) = -\frac{\partial V(x,t)}{\partial x}.
```

The repo starts with a deliberately simplified 1D trap model so the workflow is transparent before expanding toward richer segmented-trap geometry.

## Status

Scaffold initialized. First target: produce figures for the site and CGCS PDF.
