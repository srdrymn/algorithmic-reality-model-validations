# P1 -- Prediction 9.4 Finite-Clock Observer Derivation

This folder contains the paper's current computational workflow for Prediction
9.4 in `p1_atr/atr.md`.

The goal is to make the **ATR side itself explicit**, so the plateau is derived
from a discrete observer-update model rather than inserted as a direct
`floor()` ansatz.

## Core idea

The script implements the paper's prediction as a **clocked observer process**:

1. The data qubit evolves under the same Lindblad dynamics used in the paper.
2. The observer can apply one `sigma_x` POVM update per ATR tick.
3. Between ticks, the observer's memory is held fixed.
4. The reported correlator at delay `dt` is the correlation between the
   initial outcome and the outcome stored at the most recent completed tick.

This produces a piecewise-constant, experimentally accessible correlator
without hard-coding the final staircase curve by hand.

## Why this matters

For the paper's nominal parameters,

- `omega / 2pi = 5 GHz`
- `nu_alpha = 1 GHz`
- `T_tick = 1 ns`

the phase accumulated in one tick is

- `omega * T_tick = 10 pi`

so the derived finite-clock correlator matches the paper's floor-sampled
formula at tick boundaries. In that special resonant case, the paper's
staircase is therefore not just an arbitrary ansatz; it follows from the
clocked measurement/update model.

The computation also evaluates an off-resonant control case to show that this
agreement is **not** generic.

## Files

- `prediction_94_clocked_observer.py`
  - Computes the finite-clock ATR correlator and comparison metrics.
- `prediction_94_clocked_observer.png`
  - Figure written by the script.
- `prediction_94_clocked_observer_summary.json`
  - Machine-readable output summary.

## Requirements

- Python 3.8+
- NumPy
- Matplotlib

Example setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install numpy matplotlib
```

## Run

```bash
python prediction_94_clocked_observer.py
```

## Main outputs

- `Nominal max diff vs floor`
  - Should be numerically tiny for the paper's default parameter set.

- `Off-resonant control diff`
  - Shows that the clocked model and the floor ansatz separate once the frequency is moved off
    the special tick-commensurate point.

- `Peak/RMS residual vs smooth QM`
  - Separation between the discrete ATR observer model and smooth QM.

- `Power at 1% / 5% FPR`
  - Empirical discrimination power against the best-fit smooth-QM null.

## Interpretation

This workflow is stronger than the earlier toy-model version because the
plateau now comes from an explicit finite-clock observer dynamics rather than
being imposed directly.

What this workflow still does **not** do is derive ATR clock quantization from a deeper
microscopic Hamiltonian below the paper's stated observer-clock postulates.
It is best viewed as an operational derivation from the paper's own
measurement/update rules.
