# Emergent Lorentzian Spacetime — Computational Verification

[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI](https://img.shields.io/badge/ATR%20Paper-10.5281%2Fzenodo.19042891-blue)](https://doi.org/10.5281/zenodo.19042891)

**Numerical verification of the derivation in:**

> **Emergent Lorentzian Spacetime from Informational Geometry — Unifying the QFIM Spatial Metric with Tomita-Takesaki Temporal Flow**
> Serdar Yaman (2026)

Based on the **Algorithmic Theory of Reality (ATR)** framework:
> S. Yaman, *"The Algorithmic Theory of Reality: Rigorous Mathematical Foundations,"* Zenodo, 2026.
> DOI: [10.5281/zenodo.19042891](https://doi.org/10.5281/zenodo.19042891)

---

## The Result

The Lorentzian signature $(-,+,+,+)$, the curvature of spacetime, geodesic motion, and the Einstein field equations are not fundamental postulates. They are mathematical consequences of a single physical situation: a thermodynamically bounded observer with restricted access to a global data state.

The derivation yields:

1. **Lorentzian signature** from the compact/non-compact algebraic structure of QFIM + modular flow
2. **Christoffel symbols** $\Gamma^\tau_{i\tau} = -\partial_i \ln T_{mod}$ from the spatial variation of the modular Hamiltonian
3. **Newtonian gravity** $\vec{a} = -c^2 \nabla \Phi = c^2 \nabla \ln T_{mod}$ from the geodesic equation
4. **Einstein field equations** $G_{\mu\nu} = (8\pi G / c^4) T_{\mu\nu}$ from Clausius-Landauer consistency on Rindler horizons

## What This Repository Verifies

Three independent verification suites confirm every mathematical claim.

### Suite 1: Physical Verification (`verify_spacetime.py` — 8 checks)

| Check | Description | Result |
|-------|-------------|--------|
| 1 | QFIM positive-definite on Bloch sphere (100 random points) | ✅ All positive |
| 2 | Lorentzian signature $g_{\tau\tau} < 0$ for all $T > 0$ | ✅ Confirmed |
| 3 | Christoffel $\Gamma_{ATR}$ matches Schwarzschild $\Gamma_{GR}$ | ✅ Ratio = 1.000000000000000 |
| 4 | Gravitational time dilation matches GR | ✅ Exact |
| 5 | $T_{mod} = T_{Unruh}$ from density matrix construction | ✅ 4 scales verified |
| 6 | Einstein equation dimensional consistency | ✅ |
| 7 | Clausius-Landauer energy balance $\delta Q / T\delta S = 1$ | ✅ Exact (10 d.p.) |
| 8 | Cross-paper unification $a_0^2 = (8\pi G/3)\rho_\Lambda$ | ✅ Exact (15 d.p.) |

### Suite 2: Deep Mathematical Audit (`p9_deep_audit.py` — 46 checks)

Tests every individual calculation step including:
- SLD well-definedness and Fubini-Study reduction
- Dimensional analysis on every equation ($g_{\tau\tau}$, $dt$, $\kappa$, $T_U$)
- Independent Christoffel derivation from scratch
- $\tau \to t$ chain-rule conversion
- $c^2$ factor in Newtonian limit
- All three terms of the Riemann curvature expansion
- Bisognano-Wichmann logical chain (no circularity)
- Equivalence principle preservation ($T_{\mu\nu}$ independent of $T_{Unruh}$)
- Cross-cutting notation and assumption consistency

### Suite 3: Full Foundation Chain Audit (`atr_full_chain_audit.py`)

This script contains two distinct types of verification, **honestly separated**:

**Part I — Dependency Map (21 structural assertions)**

A logical manifest of the derivation chain from Axiom 0 to Einstein's equations. These are **NOT computed tests** — they are assertions about the paper's logical structure, printed for human review. A reader should verify each against the cited theorem.

**Part II — Computed Checks (68 genuine calculations)**

Every check is determined by actual computation, including:

| Section | What it computes | Engine |
|---------|-----------------|--------|
| A: Symbolic Tensors | QFIM Fubini-Study metric, Christoffel symbolic proof, First Law, Killing form, Unruh temp derivation, Bekenstein-Hawking saturation, Hawking ΔS=k_B, Einstein coefficient | **SymPy** |
| B: Numerical Physics | Christoffel matching, Unruh temperatures, BW error bound, Landauer costs, g_ττ dimensional analysis | Numerical |
| C: Dark Energy | Full step-by-step derivation vs closed form, Friedmann consistency, vacuum catastrophe ratio | Numerical |
| D: MOND Scale | a₀ = cH_∞, unification identity a₀² = (8πG/3)ρ_Λ | Numerical |
| E: Black Holes | Schwarzschild radius, Hawking temperature, 1-nat Landauer consistency, evaporation time | Numerical |
| F: Complex Hilbert Space | Local tomography parameter counting (R, C, H), excess scaling exponent | Algorithmic |
| G: Clausius-Landauer | δQ/(T·δS) = 1 at cosmological horizon, metric finiteness across all scales | Numerical |

## Quick Start

```bash
# Suite 1 & 2: pure Python 3.6+, no dependencies
python verify_spacetime.py       # 8 physical checks
python p9_deep_audit.py          # 46 mathematical audit checks

# Suite 3: requires SymPy (pip install sympy)
python atr_full_chain_audit.py   # 21 dependency assertions + 68 computed checks
```

### Expected Output (verify_spacetime.py)

```
══════════════════════════════════════════════════════════════════════
  ATR VERIFICATION
  Emergent Lorentzian Spacetime from Informational Geometry
══════════════════════════════════════════════════════════════════════

  ✅ PASS  QFIM is positive-definite (100 random Bloch sphere points)
  ✅ PASS  Lorentzian signature (-,+,+,+) from compact/non-compact algebra
  ✅ PASS  Christoffel symbols: ATR Tolman derivative matches GR
  ✅ PASS  Gravitational time dilation matches GR
  ✅ PASS  T_mod = T_Unruh (from density matrix, not by definition)
  ✅ PASS  Einstein equation dimensional analysis consistent
  ✅ PASS  Clausius-Landauer energy balance: δQ = T·δS
  ✅ PASS  Cross-paper unification: a₀² = (8πG/3)ρ_Λ

══════════════════════════════════════════════════════════════════════
  ALL 8/8 CHECKS PASSED — DERIVATION VERIFIED
══════════════════════════════════════════════════════════════════════
```

### Expected Output (p9_deep_audit.py)

```
══════════════════════════════════════════════════════════════════════
  DEEP AUDIT RESULTS
══════════════════════════════════════════════════════════════════════

  ALL 46 CHECKS PASSED — PAPER IS MATHEMATICALLY VALID
══════════════════════════════════════════════════════════════════════
```

## The Derivation Chain

| Physical law | ATR derivation | Source |
|-------------|----------------|--------|
| Complex Hilbert space | Landauer cost minimization | ATR Paper: Hilbert Space |
| Lorentzian signature $(-,+,+,+)$ | Compact (QFIM) + non-compact (modular flow) | **This paper**, Thm 3.1 |
| Spatial geometry | QFIM on observer parameters | ATR Foundations |
| Temporal flow | Tomita-Takesaki modular theory | §2.2, Connes-Rovelli |
| Gravitational time dilation | $\Gamma^\tau_{i\tau} = -\partial_i \ln T_{mod}$ | **This paper**, Thm 4.1 |
| Newtonian gravity | $\Gamma^i_{\tau\tau}$ from geodesic equation | **This paper**, Cor 4.2 |
| Einstein field equations | Clausius-Landauer on Rindler horizons | **This paper**, Thm 6.1 |
| Dark energy density | Horizon Landauer cost | ATR Paper: Dark Energy |
| MOND scale | Horizon noise floor | ATR Paper: MOND Scale |

## Physical Constants Used

| Constant | Symbol | Value | Source |
|----------|--------|-------|--------|
| Speed of light | $c$ | $2.998 \times 10^8$ m/s | CODATA 2018 |
| Reduced Planck constant | $\hbar$ | $1.0546 \times 10^{-34}$ J·s | CODATA 2018 |
| Gravitational constant | $G$ | $6.674 \times 10^{-11}$ m³/(kg·s²) | CODATA 2018 |
| Boltzmann constant | $k_B$ | $1.381 \times 10^{-23}$ J/K | CODATA 2018 |
| Hubble parameter | $H_\infty$ | $1.807 \times 10^{-18}$ 1/s | Planck 2018 |

## References

1. T. Jacobson, "Thermodynamics of Spacetime: The Einstein Equation of State," *Phys. Rev. Lett.* **75**, 1260 (1995).
2. S. Yaman, "The Algorithmic Theory of Reality: Rigorous Mathematical Foundations," *Zenodo* (2026). [DOI: 10.5281/zenodo.19042891](https://doi.org/10.5281/zenodo.19042891)
3. M. Takesaki, "Tomita's Theory of Modular Hilbert Algebras and its Applications," *Lecture Notes in Mathematics* **128**, Springer (1970).
4. A. Connes and C. Rovelli, "Von Neumann Algebra Automorphisms and Time-Thermodynamics Relation," *Class. Quantum Grav.* **11**, 2899 (1994).
5. J. J. Bisognano and E. H. Wichmann, "On the Duality Condition for Quantum Fields," *J. Math. Phys.* **17**, 303 (1976).
6. R. Landauer, "Irreversibility and Heat Generation in the Computing Process," *IBM J. Res. Dev.* **5**, 183 (1961).
7. C. H. Bennett, "The Thermodynamics of Computation — A Review," *Int. J. Theor. Phys.* **21**, 905 (1982).
8. D. Petz, "Monotone Metrics on Matrix Spaces," *Linear Algebra Appl.* **244**, 81 (1996).

## License

MIT License — see [LICENSE](LICENSE).

## Author

**Serdar Yaman** — Independent Researcher, London, United Kingdom
