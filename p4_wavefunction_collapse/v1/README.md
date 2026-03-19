# Wavefunction Collapse — Computational Verification

[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ATR Paper](https://img.shields.io/badge/ATR%20Paper-10.5281%2Fzenodo.19042891-blue)](https://doi.org/10.5281/zenodo.19042891)
[![Paper 2](https://img.shields.io/badge/Paper%202-10.5281%2Fzenodo.19050917-blue)](https://doi.org/10.5281/zenodo.19050917)

**Numerical verification of the derivation in:**

> **Wavefunction Collapse as Algorithmic Garbage Collection: Deriving the Born Rule from the Bennett-Landauer Bound**
> Serdar Yaman (2026)

Based on the **Algorithmic Theory of Reality (ATR)** framework:
> S. Yaman, *"The Algorithmic Theory of Reality: Rigorous Mathematical Foundations,"* Zenodo, 2026.
> DOI: [10.5281/zenodo.19042891](https://doi.org/10.5281/zenodo.19042891)

And the preceding derivations:
> S. Yaman, *"Holographic Dark Energy from Algorithmic Thermodynamics,"* 2026. DOI: [10.5281/zenodo.19050917](https://doi.org/10.5281/zenodo.19050917)
>
> S. Yaman, *"The Galactic Acceleration Anomaly as an Algorithmic Noise Floor: Deriving the MOND Scale from Entropic Thermodynamics,"* 2026.

---

## The Result

The quantum measurement problem — why a coherent superposition collapses into a single definite outcome upon measurement — is resolved by identifying wavefunction collapse as **thermodynamic garbage collection**. When a microscopic superposition entangles with a macroscopic apparatus, the Bennett-Landauer processing cost of tracking the entangled state exceeds the local holographic energy budget, forcing a non-unitary state truncation.

The Born Rule $p_i = |c_i|^2$ is then derived as the **unique** truncation strategy that minimizes the Kullback-Leibler divergence (algorithmic information loss) between the pre- and post-measurement states.

## What This Script Verifies

The script walks through every algebraic step using standard numerical linear algebra (pure Python, no dependencies), confirming:

| Check | Description | Result |
|:-----:|-------------|:------:|
| 1 | KL-divergence minimization yields Born Rule (Theorem 4.2) | ✅ Strict minimum |
| 2 | Lagrange multiplier $\lambda = 1$ under normalization | ✅ Exact (15 d.p.) |
| 3 | Hessian positive-definite at $p_i = |c_i|^2$ | ✅ All eigenvalues > 0 |
| 4 | Entanglement entropy grows during measurement interaction | ✅ $S(0) = 0 \to S_\text{max}$ |
| 5 | Entropy saturates at $S_\text{max} = -\sum |c_i|^2 \ln |c_i|^2$ | ✅ Exact (4 d.p.) |
| 6 | Macroscopic decoherence faster than Planck time | ✅ $\tau_\text{dec} \ll t_P$ |
| 7 | Born Rule statistics ($\chi^2$ test, $N = 10^5$ trials) | ✅ $p > 0.05$ |
| 8 | Off-diagonal elements decay (pointer basis emergence) | ✅ $|\rho_{01}| \to 10^{-17}$ |
| 9 | Macroscopic measurement violates holographic capacity | ✅ For $N_A \geq 10^3$ |
| 10 | Cross-entropy reduces to classical form (pointer orthogonality) | ✅ Match $< 10^{-12}$ |

### Key Numerical Results

| Quantity | Value |
|----------|-------|
| KL minimum at Born Rule | Strict global minimum for all tested wavefunctions |
| Lagrange multiplier $\lambda$ | $1.000000000000000$ |
| Entanglement entropy (60/40 split) | $S_\text{max} = 0.6730$ (theory: $0.6730$) |
| Off-diagonal decay $|\rho_{01}|$ | $0.4899 \to 6.1 \times 10^{-17}$ |
| Dust grain $\tau_\text{dec}$ | $2.69 \times 10^{-46}$ s $\ll t_P = 5.39 \times 10^{-44}$ s |
| $\chi^2$ (50/50 superposition) | $0.17$ (critical: $3.84$) |

## Quick Start

```bash
# No dependencies required — pure Python 3.6+ standard library
python verify_wavefunction_collapse.py
```

### Expected Output

```
══════════════════════════════════════════════════════════════════════
  COMPUTATIONAL VERIFICATION
  Wavefunction Collapse as Algorithmic Garbage Collection
  Deriving the Born Rule from the Bennett-Landauer Bound
══════════════════════════════════════════════════════════════════════

  ...

══════════════════════════════════════════════════════════════════════
                         VERIFICATION SUMMARY
══════════════════════════════════════════════════════════════════════

  ✅ PASS  KL-divergence minimization yields Born Rule
  ✅ PASS  Lagrange multiplier λ = 1 under normalization
  ✅ PASS  Hessian positive-definite (strict minimum)
  ✅ PASS  Entanglement entropy grows during measurement
  ✅ PASS  Entropy saturates at S_max = -Σ|c_i|²ln|c_i|²
  ✅ PASS  Macroscopic decoherence faster than Planck time
  ✅ PASS  Born Rule statistics (χ² test, N=100000)
  ✅ PASS  Off-diagonal elements decay (pointer basis emergence)
  ✅ PASS  Macroscopic measurement violates holographic capacity
  ✅ PASS  Cross-entropy reduces to classical form (pointer orthogonality)

══════════════════════════════════════════════════════════════════════
  ALL 10/10 CHECKS PASSED — DERIVATION NUMERICALLY VERIFIED
══════════════════════════════════════════════════════════════════════
```

## The Derivation in Three Steps

1. **Identify the bottleneck:** During a measurement, the entanglement entropy between system and apparatus grows exponentially. The Bennett-Landauer bound sets an irreducible thermodynamic cost for each bit processed.

2. **Trigger the collapse:** When the Landauer processing cost exceeds the local holographic energy budget ($\dot{\mathcal{S}} > N_\text{max} \cdot \nu_\alpha$), the observer's rendering engine can no longer sustain unitary evolution. A forced truncation — garbage collection — occurs at the decoherence timescale $\tau_c \sim 1/\Gamma_\text{dec}$.

3. **Derive the statistics:** Given pointer-state orthogonality from environmental decoherence, the unique truncation that minimizes the Kullback-Leibler divergence is $p_i = |c_i|^2$ — the Born Rule. This is verified by Lagrange optimization (Theorem 4.2) and confirmed by positive-definite Hessian.

## Verification Steps

The script performs 10 computational checks:

| Step | What it computes |
|:----:|--------------------|
| 1 | KL-divergence minimization for diverse wavefunctions (§4.2) |
| 2 | Lagrange multiplier $\lambda = 1$ from normalization (§4.2, Step 4) |
| 3 | Hessian positive-definiteness (§4.2, Step 5) |
| 4 | Entanglement entropy growth from $S(0) = 0$ to $S_\text{max}$ (§2.2) |
| 5 | Entropy saturation at $S_\text{max} = -\sum |c_i|^2 \ln |c_i|^2$ (§2.2) |
| 6 | Decoherence timescale estimates for macroscopic systems (§3.3) |
| 7 | Monte Carlo Born Rule statistics with $\chi^2$ test (§6.3) |
| 8 | Off-diagonal density matrix decay (pointer basis emergence) (§5.3) |
| 9 | Holographic capacity violation for $N_A \geq 10^3$ particles (§3.1) |
| 10 | Quantum-to-classical cross-entropy reduction under pointer orthogonality (§4.2) |

## Physical Constants Used

| Constant | Symbol | Value | Source |
|----------|--------|-------|--------|
| Speed of light | $c$ | $2.99792458 \times 10^8$ m/s | CODATA 2018 |
| Reduced Planck constant | $\hbar$ | $1.054571817 \times 10^{-34}$ J·s | CODATA 2018 |
| Gravitational constant | $G$ | $6.67430 \times 10^{-11}$ m³/(kg·s²) | CODATA 2018 |
| Boltzmann constant | $k_B$ | $1.380649 \times 10^{-23}$ J/K | CODATA 2018 (exact) |
| Planck length | $\ell_P$ | $1.616255 \times 10^{-35}$ m | Derived |

## References

1. S. Yaman, "The Algorithmic Theory of Reality: Rigorous Mathematical Foundations," *Zenodo* (2026). [DOI: 10.5281/zenodo.19042891](https://doi.org/10.5281/zenodo.19042891)
2. S. Yaman, "Holographic Dark Energy from Algorithmic Thermodynamics: Resolving the Vacuum Catastrophe via the Bennett-Landauer Limit," (2026). [DOI: 10.5281/zenodo.19050917](https://doi.org/10.5281/zenodo.19050917)
3. S. Yaman, "The Galactic Acceleration Anomaly as an Algorithmic Noise Floor: Deriving the MOND Scale from Entropic Thermodynamics," (2026).
4. E. Joos and H. D. Zeh, "The emergence of classical properties through interaction with the environment," *Z. Phys. B* **59**, 223 (1985).
5. W. H. Zurek, "Decoherence, einselection, and the quantum origins of the classical," *Rev. Mod. Phys.* **75**, 715 (2003).
6. R. Landauer, "Irreversibility and heat generation in the computing process," *IBM J. Res. Dev.* **5**, 183 (1961).
7. C. H. Bennett, "The thermodynamics of computation — a review," *Int. J. Theor. Phys.* **21**, 905 (1982).
8. A. M. Gleason, "Measures on the closed subspaces of a Hilbert space," *J. Math. Mech.* **6**, 885 (1957).

## License

MIT License — see [LICENSE](LICENSE).

## Author

**Serdar Yaman** — Independent Researcher, MSc Physics, United Kingdom
