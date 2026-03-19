# Wavefunction Collapse — Computational Verification

[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ATR Paper](https://img.shields.io/badge/ATR%20Paper-10.5281%2Fzenodo.19042891-blue)](https://doi.org/10.5281/zenodo.19042891)

Numerical verification scripts for two papers on wavefunction collapse within the **Algorithmic Theory of Reality (ATR)** framework:

| Script | Paper | Version |
|--------|-------|---------|
| [`v1/verify_wavefunction_collapse.py`](v1/verify_wavefunction_collapse.py) | *Wavefunction Collapse as Algorithmic Garbage Collection* | v1 (original) |
| [`verify_zeno_threshold.py`](verify_zeno_threshold.py) | *The Zeno Threshold: Wavefunction Collapse and the Emergence of Time via Landauer Erasure Limits* | v2 (current) |

Both scripts use **pure Python 3.6+ standard library** — no NumPy, SciPy, or external dependencies.

---

## The Zeno Threshold (v2) — `verify_zeno_threshold.py`

**Paper:**
> Serdar Yaman, *"The Zeno Threshold: Wavefunction Collapse and the Emergence of Time via Landauer Erasure Limits,"* March 2026.

### The Result

v2 introduces the **Zeno Threshold ($Z_\alpha$)**: the strict, observer-dependent information-processing limit at which unitary evolution becomes thermodynamically unsustainable. Three consequences are derived:

1. **When collapse occurs** — the entanglement entropy growth rate during an amplification cascade breaches $Z_\alpha$, forcing a non-unitary truncation (garbage collection).
2. **With what statistics** — the Born Rule $p_i = |c_i|^2$ is the unique truncation that minimises the Kullback-Leibler divergence (algorithmic information loss), proved via Lagrange optimisation with positive-definite Hessian.
3. **How time emerges** — each forced erasure generates an irreversible burst of Landauer heat. This is the physical "tick" of the observer's clock; time is the thermodynamic exhaust of the Z-Scale.

### What This Script Verifies (38 checks)

| Section | Checks | What is verified |
|---------|--------|-----------------|
| §2 | 9 | Logistic entropy growth model: starts near zero, peaks at $t_0$, saturates at $S_\mathrm{max}$. Monotonic rise then fall. Quantum simulation: entropy trajectory and off-diagonal decay. |
| §2.3 | 1 | Parameter scaling $\mathcal{N} = 2 d_S \mathcal{N}_A - 2$ for pure bipartite states. |
| §3 | 4 | Z-Scale formula $Z_\alpha = C_\mathrm{max} \cdot \nu_\alpha$; macroscopic cascade rate vastly exceeds $Z_\alpha$; breach on rising edge ($\tau_c < t_0$); Landauer heat per tick. |
| §4 | 6 | Born Rule minimises cross-entropy for 5 wavefunction configs; $\lambda = 1$; Hessian positive-definite; strict convexity (uniqueness); $\mathcal{L}_\mathrm{min} = S_\mathrm{Shannon}$; quantum CE equals classical CE under pointer orthogonality. |
| §5 | 3 | Macroscopic tracking cost exceeds any finite $Z_\alpha$; microscopic cost is trivially small; exponential scaling gap between macro and micro. |
| §6 | 1 | Monte Carlo Born Rule statistics: $\chi^2$ test at 95% confidence, $N = 10^5$ trials, 4 wavefunction configs. |
| §X | 4 | Cross-cutting: Landauer dimensional analysis, $Z_\alpha$ dimensionality, logistic derivative identity, non-negativity of cross-entropy, scope check. |
| §7 | 8 | Dual-observer (Wigner's Friend via Z-Scale): backend unitarity, entropy growth, fly truncates before human, same backend → two realities, trace preservation, desynchronised clock ticks, Landauer heat comparison, pre-truncation identity. |

### Quick Start

```bash
python3 verify_zeno_threshold.py
```

### Expected Output

```
╔══════════════════════════════════════════════════════════════════════╗
║  Z-Scale Validation Suite — ATR-WC v2                              ║
║  Author: Serdar Yaman | Date: March 2026                           ║
╚══════════════════════════════════════════════════════════════════════╝

...

════════════════════════════════════════════════════════════════════════
  SUMMARY: 38/38 passed
════════════════════════════════════════════════════════════════════════
```

### Key Numerical Results

| Quantity | Value |
|----------|-------|
| Lagrange multiplier $\lambda$ | $1.000000000000000$ |
| Logistic: $\dot{S}(0) / \dot{S}(t_0)$ | $< 0.01$ (rate near zero at start) |
| Peak rate identity $k S_\mathrm{max}/4$ | Exact to $10^{-10}$ |
| Off-diagonal decay $|\rho_{01}|$ | $0.490 \to 0$ (full decoherence) |
| Macroscopic tracking log₁₀(cost) | $> 300$ vs. $Z_\mathrm{max} = 10^{120}$ |
| $\chi^2$ (50/50, $N=10^5$) | $< 3.841$ critical value |
| Backend purity after 16 unitary steps | $1.000000000000000$ |

### Physical Constants Used

| Constant | Symbol | Value |
|----------|--------|-------|
| Speed of light | $c$ | $2.99792458 \times 10^8$ m/s |
| Reduced Planck constant | $\hbar$ | $1.054571817 \times 10^{-34}$ J·s |
| Boltzmann constant | $k_B$ | $1.380649 \times 10^{-23}$ J/K |

> **Note:** No gravitational constant $G$ or Planck length $\ell_P$ appears anywhere — this paper is strictly information-thermodynamic.

---

## Original Paper (v1) — `v1/verify_wavefunction_collapse.py`

See [`v1/README.md`](v1/README.md) for full documentation of the original verification suite.

**Paper:**
> Serdar Yaman, *"Wavefunction Collapse as Algorithmic Garbage Collection: Deriving the Born Rule from the Bennett-Landauer Bound,"* March 2026.

```bash
python3 v1/verify_wavefunction_collapse.py
```

---

## Relationship Between v1 and v2

| Aspect | v1 | v2 |
|--------|----|----|
| Entropy model | Inverse-exponential saturation | **Logistic (S-curve)** — correctly models amplification cascade |
| Collapse criterion | $\dot{\mathcal{S}} > N_\mathrm{max} \cdot \nu_\alpha$ (holographic) | $\dot{\mathcal{S}} > Z_\alpha$ (Zeno Threshold — pure thermodynamic) |
| Time emergence | Not addressed | **Derived**: each erasure tick = one unit of time |
| Observer model | Measurement-capable environment | **Epistemic Horizon** with explicit Z-Scale |
| Dual-observer proof | Not included | **Added**: Wigner's Friend via Z-Scale (§7, 8 checks) |
| Gravity constants | $G$, $\ell_P$ used in §3 | **Removed**: scope limited to $\hbar$, $k_B$, $Z_\alpha$ |
| Total checks | 25 | **38** |

---

## References

1. S. Yaman, *"The Algorithmic Theory of Reality: Rigorous Mathematical Foundations,"* Zenodo (2026). [DOI: 10.5281/zenodo.19042891](https://doi.org/10.5281/zenodo.19042891)
2. E. Joos and H. D. Zeh, "The emergence of classical properties through interaction with the environment," *Z. Phys. B* **59**, 223 (1985).
3. W. H. Zurek, "Decoherence, einselection, and the quantum origins of the classical," *Rev. Mod. Phys.* **75**, 715 (2003).
4. B. Misra and E. C. G. Sudarshan, "The Zeno's paradox in quantum theory," *J. Math. Phys.* **18**, 756 (1977).
5. R. Landauer, "Irreversibility and heat generation in the computing process," *IBM J. Res. Dev.* **5**, 183 (1961).
6. C. H. Bennett, "The thermodynamics of computation — a review," *Int. J. Theor. Phys.* **21**, 905 (1982).
7. D. N. Page and W. K. Wootters, "Evolution without evolution: Dynamics described by stationary observables," *Phys. Rev. D* **27**, 2885 (1983).

---

## License

MIT License — see [LICENSE](LICENSE).

## Author

**Serdar Yaman** — Independent Researcher, MSc Physics, United Kingdom
