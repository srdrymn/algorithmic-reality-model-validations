# Black Hole Information Paradox — Computational Verification

[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ATR Paper](https://img.shields.io/badge/ATR%20Paper-10.5281%2Fzenodo.19120294-blue)](https://doi.org/10.5281/zenodo.19120294)
[![Paper 2](https://img.shields.io/badge/Paper%202-10.5281%2Fzenodo.19120350-blue)](https://doi.org/10.5281/zenodo.19120350)

**Numerical verification of the derivation in:**

> **Addressing the Black Hole Information Paradox through the Algorithmic Theory of Reality**
> Serdar Yaman (2026)

Based on the **Algorithmic Theory of Reality (ATR)** framework:
> S. Yaman, *"The Algorithmic Theory of Reality: Rigorous Mathematical Foundations,"* Zenodo, 2026.
> DOI: [10.5281/zenodo.19120294](https://doi.org/10.5281/zenodo.19120294)

And the preceding derivations in the same series:
> S. Yaman, *"Holographic Dark Energy from Algorithmic Thermodynamics,"* 2026. DOI: [10.5281/zenodo.19120350](https://doi.org/10.5281/zenodo.19120350)
>
> S. Yaman, *"The Galactic Acceleration Anomaly as an Algorithmic Noise Floor: Deriving the MOND Scale from Entropic Thermodynamics,"* 2026. DOI:[10.5281/zenodo.19120376](https://doi.org/10.5281/zenodo.19120376)
>
> S. Yaman, *"Wavefunction Collapse as Algorithmic Garbage Collection: Deriving the Born Rule from the Bennett-Landauer Bound,"* 2026. DOI:[10.5281/zenodo.19057971](https://doi.org/10.5281/zenodo.19057971)

---

## The Core Claim

The black hole information paradox — the 50-year conflict between general relativity and quantum unitarity — is addressed by identifying the event horizon as a **dynamic rendering boundary**: the surface where the local algorithmic complexity of a mass condensation exceeds the holographic Bennett-Landauer processing limit. The system responds by compressing the interior data into a 2D holographic boundary, storing the detailed information in the unrendered Singleton backend.

Hawking radiation is reinterpreted as the **thermodynamic exhaust** of the universe's operating system slowly decompressing this stored data, at the Landauer-minimum rate: each Hawking quantum carries exactly **one nat of entropy** at the minimum energy cost $k_B T_H$.

Global unitarity is preserved because the underlying Singleton $|\Omega\rangle$ is unchanged — information is not destroyed, only rerouted between the rendered (spatial) and unrendered (backend) representations.

---

## What This Script Verifies

The script performs **10 independent checks**, spanning algebraic identities, astrophysical examples, a dynamic graph simulation, and a four-paper unification identity:

| Check | Description | Result |
|:-----:|-------------|:------:|
| 1 | Bekenstein bound = Holographic bound at $r = r_s$ | ✅ Exact identity |
| 2 | Independent derivation of Hawking temperature from $T = (\partial S/\partial E)^{-1}$ matches Hawking's formula | ✅ Exact (15 d.p.) |
| 3 | Each Hawking quantum carries exactly 1 nat of entropy | ✅ $\Delta S / k_B = 1.000$ |
| 4 | Total emitted entropy = initial BH entropy (unitarity) | ✅ Exact |
| 5 | Event horizon emerges from bandwidth overflow (graph dynamics) | ✅ Complete disconnection |
| 6 | Bekenstein-Hawking area law $S \propto A$ from graph dynamics | ✅ $S/r^2 \approx \text{const}$ |
| 7 | Page-like curve from finite-bandwidth evaporation (lattice roughening) | ✅ Rise → peak → fall |
| 8 | Evaporation timescale $t_{\text{evap}} \propto M^3$ | ✅ Exponent = 3.0000 |
| 9 | Holographic overflow at $r < r_s$ for astrophysical black holes | ✅ All 4 cases |
| 10 | Four-scale Bennett-Landauer unification identity | ✅ $a_0^2 = (8\pi G/3)\rho_\Lambda$ |

### Key Numerical Results

| Quantity | Value |
|----------|-------|
| $S_{\text{Bek}} / S_{\text{BH}}$ at $r = r_s$ | $1.000000000000000$ (exact identity) |
| $\Delta S$ per Hawking quantum | $k_B$ (1 nat — exact) |
| Evaporation time (10 $M_\odot$) | $6.619 \times 10^{77}$ s ($2.1 \times 10^{70}$ years) |
| Sgr A* BH entropy | $2.318 \times 10^{67}$ J/K ($2.423 \times 10^{90}$ bits) |
| Page-like curve peak | Step 5 of 30 (boundary edge count rises then falls to near-zero) |
| Graph horizon | 136 interior nodes, 0 boundary edges (perfect disconnection) |

---

## Quick Start

```bash
# No dependencies required — pure Python 3.6+ standard library only
python verify_black_hole.py
```

### Expected Output

```
══════════════════════════════════════════════════════════════════════
  COMPUTATIONAL VERIFICATION
  Addressing the Black Hole Information Paradox
  via the Algorithmic Theory of Reality (ATR)
══════════════════════════════════════════════════════════════════════

  ...

══════════════════════════════════════════════════════════════════════
                         VERIFICATION SUMMARY
══════════════════════════════════════════════════════════════════════

  ✅ PASS  Bekenstein = Holographic at r = r_s
  ✅ PASS  Hawking T independently derived from dS/dE
  ✅ PASS  Each Hawking quantum = 1 nat
  ✅ PASS  Total emitted entropy = S_BH (unitarity)
  ✅ PASS  Event horizon emerges from bandwidth overflow
  ✅ PASS  Bekenstein-Hawking area law S ∝ A (graph)
  ✅ PASS  Page-like curve from finite-bandwidth evaporation
  ✅ PASS  Evaporation timescale t ∝ M³
  ✅ PASS  Holographic overflow at r < r_s
  ✅ PASS  Four-scale Bennett-Landauer unification

══════════════════════════════════════════════════════════════════════
  ALL 10/10 CHECKS PASSED — DERIVATION NUMERICALLY VERIFIED
══════════════════════════════════════════════════════════════════════
```

---

## The Simulation: Growing an Event Horizon

The centerpiece of this script is a **dynamic spatial graph** that demonstrates how an event horizon emerges from algorithmic thermodynamics alone — no general relativity, no horizon conditions, no metric:

1. **Build the lattice:** A 12×12×12 cubic grid of nodes (spatial degrees of freedom) connected by nearest-neighbor edges.
2. **Inject mass:** Data packets are injected into a central cluster of nodes, increasing their processing load.
3. **Enforce bandwidth:** Each node has a strict throughput cap (the Bennett-Landauer limit). When a node's load exceeds its cap, it drops external edges and connects only to other overloaded nodes.
4. **Watch the horizon form:** The overloaded nodes spontaneously disconnect from the exterior grid, forming an isolated interior clique — a computational event horizon with zero boundary edges.
5. **Evaporate:** Gradually reducing the interior data load causes boundary nodes to reconnect, and the boundary edge count traces a Page-like curve.

> **Transparency note:** The Page-like curve in Check 7 arises from **lattice roughening** — randomly evaporating boundary nodes creates a rough, pitted surface with higher boundary edge count than a perfectly smooth sphere of the same radius. The curve is a discrete geometric effect. It demonstrates that the correct qualitative shape (rise → peak → fall) is reproduced by this mechanism, but it does not constitute an independent derivation of the quantum Page curve or of von Neumann entanglement entropy.

---

## Verification Steps in Detail

| Step | What it computes | Paper section |
|:----:|------------------|:-------------:|
| 1 | Bekenstein-Holographic saturation for 4 astrophysical BHs | §3.1 |
| 2 | Independent Hawking T from $T = (\partial S/\partial E)^{-1}$, compared to Hawking's formula | §4.2 |
| 3 | Entropy per Hawking quantum = $k_B$ (1 nat) | §4.2 |
| 4 | Total entropy conservation across full evaporation | §5.1 |
| 5 | Graph-based event horizon formation with bandwidth caps | §7 |
| 6 | Area-law scaling across multiple injection radii | §7 |
| 7 | Page-like curve from sequential evaporation steps (lattice roughening mechanism) | §7 |
| 8 | Evaporation timescale $\propto M^3$ scaling | §4.3 |
| 9 | Holographic overflow verification at $r = 0.9\,r_s$ for astrophysical BHs | §3.1 |
| 10 | Four-scale unification identity: $a_0^2 = (8\pi G/3)\rho_\Lambda$ | §6 |

---

## Physical Constants Used

All constants are from CODATA 2018 / IAU.

| Constant | Symbol | Value |
|----------|--------|-------|
| Speed of light | $c$ | $2.99792458 \times 10^8$ m/s |
| Reduced Planck constant | $\hbar$ | $1.054571817 \times 10^{-34}$ J·s |
| Gravitational constant | $G$ | $6.67430 \times 10^{-11}$ m³/(kg·s²) |
| Boltzmann constant | $k_B$ | $1.380649 \times 10^{-23}$ J/K (exact) |
| Planck length | $\ell_P$ | $1.616255 \times 10^{-35}$ m (derived) |
| Solar mass | $M_\odot$ | $1.989 \times 10^{30}$ kg |

---

## ATR Paper Series

This script is part of the computational verification suite for the ATR framework. Other repos in the series:

| Paper | Topic | Repo |
|-------|-------|------|
| ATR (foundations) | Emergent spacetime & gravity from information theory | [zenodo.19120294](https://doi.org/10.5281/zenodo.19120294) |
| Paper 2 | Cosmological constant / dark energy | [atr-holographic-dark-energy](https://github.com/srdrymn/atr-holographic-dark-energy) |
| Paper 3 | MOND acceleration scale | [atr-verifiy-mond-scale](https://github.com/srdrymn/atr-verifiy-mond-scale) |
| Paper 4 | Born Rule / wavefunction collapse | [atr-wavefunction-collapse](https://github.com/srdrymn/atr-wavefunction-collapse) |
| **Paper 5 (this repo)** | **Black hole information paradox** | **[atr-resolving-black-hole-information-paradox](https://github.com/srdrymn/atr-resolving-black-hole-information-paradox)** |

---

## References

1. S. Yaman, "The Algorithmic Theory of Reality: Rigorous Mathematical Foundations," *Zenodo* (2026). [DOI: 10.5281/zenodo.19120294](https://doi.org/10.5281/zenodo.19120294)
2. S. Yaman, "Holographic Dark Energy from Algorithmic Thermodynamics," (2026). [DOI: 10.5281/zenodo.19120350](https://doi.org/10.5281/zenodo.19120350)
3. S. Yaman, "The Galactic Acceleration Anomaly as an Algorithmic Noise Floor," (2026). [DOI: 10.5281/zenodo.19120376](https://doi.org/10.5281/zenodo.19120376)
4. S. Yaman, "Wavefunction Collapse as Algorithmic Garbage Collection," (2026). [DOI: 10.5281/zenodo.19057971](https://doi.org/10.5281/zenodo.19057971)
5. S. W. Hawking, "Particle creation by black holes," *Commun. Math. Phys.* **43**, 199 (1975).
6. J. D. Bekenstein, "Universal upper bound on the entropy-to-energy ratio for bounded systems," *Phys. Rev. D* **23**, 287 (1981).
7. D. N. Page, "Average entropy of a subsystem," *Phys. Rev. Lett.* **71**, 1291 (1993).
8. R. Landauer, "Irreversibility and heat generation in the computing process," *IBM J. Res. Dev.* **5**, 183 (1961).
9. C. H. Bennett, "The thermodynamics of computation — a review," *Int. J. Theor. Phys.* **21**, 905 (1982).

---

## License

MIT License — see [LICENSE](LICENSE).

## Author

**Serdar Yaman** — Independent Researcher, MSc Physics, United Kingdom
