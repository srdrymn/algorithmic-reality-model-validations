# P1 — The Algorithmic Theory of Reality: Computational Validations

Computational validation suite for:

> S. Yaman, "The Algorithmic Theory of Reality: Rigorous Mathematical Foundations," (2026).

## Contents

| File | Description | Paper Section |
|------|-------------|---------------|
| `prediction_94_subtick_correlation.py` | Sub-tick correlation plateau simulation | §9.2–9.3 |
| `prediction_94_simulation.png` | Output figure (3-panel) | §9.3.4, Fig. 1 |

## Prediction 9.4 — Sub-Tick Correlation Plateaus

ATR predicts that a measurement apparatus with discrete clock frequency ν_α produces **step-like correlation plateaus** rather than the smooth exponential decay of standard quantum mechanics. Within each tick interval [n/ν_α, (n+1)/ν_α), the correlator is frozen at the tick-boundary value.

### Model

- **System:** Single transmon qubit, ω/2π = 5.0 GHz
- **Decoherence:** Lindblad dephasing, T₂ = 20 ns
- **Observable:** σ_x two-point correlator
- **ATR clock:** ν_α = 1.0 GHz (T_tick = 1 ns)
- **Noise:** Shot noise (N = 10,000 shots) + Gaussian clock jitter (σ = 50 ps)

### Results

```
RMS deviation  = 1.067
Peak deviation = 1.995
SNR (RMS)      = 107σ
SNR (peak)     = 200σ
χ²/dof (H₀: smooth QM) = 11,296
```

The ATR signal exceeds shot noise by **107σ (RMS)** — detectable with overwhelming statistical confidence using current superconducting qubit technology.

### Quick Start

```bash
# Requirements: Python 3.8+, NumPy, Matplotlib
pip install numpy matplotlib

# Run simulation
python prediction_94_subtick_correlation.py
```

Output: `prediction_94_simulation.png`

## License

MIT — see [LICENSE](LICENSE).
