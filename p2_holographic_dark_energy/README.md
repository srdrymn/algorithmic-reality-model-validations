# Holographic Dark Energy — Computational Verification

[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI](https://img.shields.io/badge/ATR%20Paper-10.5281%2Fzenodo.19120294-blue)](https://doi.org/10.5281/zenodo.19120294)

**Numerical verification of the derivation in:**

> **Holographic Dark Energy from Algorithmic Thermodynamics: Resolving the Vacuum Catastrophe via the Bennett-Landauer Limit**
> Serdar Yaman (2026)

Based on the **Algorithmic Theory of Reality (ATR)** framework:
> S. Yaman, *"The Algorithmic Theory of Reality: Rigorous Mathematical Foundations,"* Zenodo, 2026.
> DOI: [10.5281/zenodo.19120294](https://doi.org/10.5281/zenodo.19120294)

---

## The Result

The cosmological constant problem — a $10^{120}$ discrepancy between QFT's predicted vacuum energy and the observed value — is resolved by replacing the divergent volume-scaling mode count of continuum QFT with the finite area-scaling holographic bound of the observer's event horizon.

The derivation yields:

$$\rho_\Lambda = \frac{3c^4}{8\pi G R_E^2}$$

where $R_E$ is the cosmological event horizon radius. Remarkably, $\hbar$ enters through both the Gibbons-Hawking temperature and the Planck area, and **cancels exactly** — producing a purely classical result from quantum ingredients.

## What This Script Verifies

The script walks through every algebraic step using **CODATA 2018 physical constants** and **Planck 2018 cosmological parameters**, confirming:

| Check | Description | Result |
|-------|-------------|--------|
| 1 | Step-by-step $E_\text{vac}$ matches simplified closed form | ✅ Exact (15 d.p.) |
| 2 | $\hbar$ cancellation: $\rho(\text{steps}) = 3c^4/(8\pi G R_E^2)$ | ✅ Exact (15 d.p.) |
| 3 | Friedmann self-consistency: $\rho_\text{ATR} = \rho_\text{critical}$ | ✅ Exact (15 d.p.) |
| 4 | Agreement with Planck 2018 observed $\rho_\text{obs}$ | ✅ Ratio = 1.0000 |
| 5 | $(R_E/\ell_P)^2 \approx 10^{122}$ matches QFT/ATR ratio | ✅ Confirmed |

### Key Numerical Results

| Quantity | Value |
|----------|-------|
| Holographic bit count $N$ | $3.31 \times 10^{122}$ |
| Gibbons-Hawking temperature $T_\text{mod}$ | $2.20 \times 10^{-30}$ K |
| **ATR dark energy density $\rho_\Lambda$** | **$5.25 \times 10^{-10}$ J/m³** |
| Observed $\rho_\text{obs}$ (Planck 2018) | $5.25 \times 10^{-10}$ J/m³ |
| QFT prediction $\rho_\text{QFT}$ | $4.63 \times 10^{113}$ J/m³ |
| QFT/observed ratio | $\sim 10^{123}$ — the catastrophe |

## Quick Start

```bash
# No dependencies required — pure Python 3.6+ standard library
python verify_dark_energy.py
```

### Expected Output

```
══════════════════════════════════════════════════════════════════════
  COMPUTATIONAL VERIFICATION
  Holographic Dark Energy from Algorithmic Thermodynamics
══════════════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────────────
  Step 0: Physical & Cosmological Constants
──────────────────────────────────────────────────────────────────────
  c       = 2.99792458e+08 m/s
  ℏ       = 1.054571817e-34 J·s
  ...

  ✅ PASS  E_vac(steps) = E_vac(simplified)
  ✅ PASS  ℏ cancellation: ρ(steps) = 3c⁴/(8πGR²)
  ✅ PASS  Friedmann self-consistency: ρ_ATR = ρ_critical
  ✅ PASS  Agreement with Planck 2018: |ATR/obs − 1| < 1%
  ✅ PASS  Scaling ratio: (R_E/ℓ_P)² ≈ ρ_QFT/ρ_ATR (within 1 decade)

══════════════════════════════════════════════════════════════════════
  ALL 5 CHECKS PASSED — DERIVATION NUMERICALLY VERIFIED
══════════════════════════════════════════════════════════════════════
```

## The Derivation in Four Steps

1. **Identify the boundary:** The observer's context window is bounded by the cosmological event horizon $R_E$ — the surface of permanent causal disconnection.

2. **Count the bits:** The event horizon has a maximum informational capacity of $N = \pi R_E^2 / \ell_P^2$ degrees of freedom (holographic area law, Susskind 1995; Bekenstein-Hawking).

3. **Price the bits:** Each degree of freedom carries a thermodynamic energy of $k_B T_\text{mod} = \hbar c / (2\pi R_E)$ (Gibbons-Hawking temperature, 1977; Bennett-Landauer bound, 1961/1982).

4. **Compute the density:** Dividing total energy $E = Nk_BT$ by volume $V = \frac{4}{3}\pi R_E^3$ yields $\rho_\Lambda = 3c^4 / (8\pi G R_E^2)$. The $\hbar$ cancels exactly.

## Physical Constants Used

| Constant | Symbol | Value | Source |
|----------|--------|-------|--------|
| Speed of light | $c$ | $2.99792458 \times 10^8$ m/s | CODATA 2018 |
| Reduced Planck constant | $\hbar$ | $1.054571817 \times 10^{-34}$ J·s | CODATA 2018 |
| Gravitational constant | $G$ | $6.67430 \times 10^{-11}$ m³/(kg·s²) | CODATA 2018 |
| Boltzmann constant | $k_B$ | $1.380649 \times 10^{-23}$ J/K | CODATA 2018 (exact) |
| Hubble constant | $H_0$ | 67.4 km/s/Mpc | Planck 2018 |
| Dark energy fraction | $\Omega_\Lambda$ | 0.685 | Planck 2018 |

## References

1. S. Yaman, "The Algorithmic Theory of Reality: Rigorous Mathematical Foundations," *Zenodo* (2026). [DOI: 10.5281/zenodo.19120294](https://doi.org/10.5281/zenodo.19120294)
2. D. N. Page and W. K. Wootters, "Evolution without evolution," *Phys. Rev. D* **27**, 2885 (1983).
3. L. Susskind, "The World as a Hologram," *J. Math. Phys.* **36**, 6377 (1995). [arXiv:hep-th/9409089](https://arxiv.org/abs/hep-th/9409089)
4. R. Landauer, "Irreversibility and heat generation in the computing process," *IBM J. Res. Dev.* **5**, 183 (1961).
5. C. H. Bennett, "The thermodynamics of computation — a review," *Int. J. Theor. Phys.* **21**, 905 (1982).
6. D. Reeb and M. M. Wolf, "An improved Landauer principle with finite-size corrections," *New J. Phys.* **16**, 103011 (2014). [arXiv:1306.4352](https://arxiv.org/abs/1306.4352)
7. M. Li, "A model of holographic dark energy," *Phys. Lett. B* **603**, 1 (2004). [arXiv:hep-th/0403127](https://arxiv.org/abs/hep-th/0403127)
8. G. W. Gibbons and S. W. Hawking, "Cosmological event horizons, thermodynamics, and particle creation," *Phys. Rev. D* **15**, 2738 (1977).
9. N. Aghanim et al. (Planck Collaboration), "Planck 2018 results. VI. Cosmological parameters," *Astron. Astrophys.* **641**, A6 (2020). [arXiv:1807.06209](https://arxiv.org/abs/1807.06209)

## License

MIT License — see [LICENSE](LICENSE).

## Author

**Serdar Yaman** — Independent Researcher, London, United Kingdom
