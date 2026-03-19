# EPR Paradox — Computational Verification

[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ATR Paper](https://img.shields.io/badge/ATR%20Paper-10.5281%2Fzenodo.19120294-blue)](https://doi.org/10.5281/zenodo.19120294)

**Numerical verification of the derivation in:**

> **Entanglement as Backend Memory Aliasing: Resolving the EPR Paradox via Algorithmic Graph Routing in the Singleton**
> Serdar Yaman (2026)

Based on the **Algorithmic Theory of Reality (ATR)** framework:
> S. Yaman, *"The Algorithmic Theory of Reality: Rigorous Mathematical Foundations,"* Zenodo, 2026.
> DOI: [10.5281/zenodo.19120294](https://doi.org/10.5281/zenodo.19120294)

---

## The Core Claim

Quantum entanglement is not "spooky action at a distance." It is **backend memory aliasing**: two rendering-pointers in 3D space referencing a single shared data entry in the pre-geometric Singleton. When Alice measures her particle, her macroscopic apparatus entangles with the system, driving the local entanglement entropy rate $\dot{\mathcal{S}}(t)$ above her **Zeno Threshold** ($Z_\alpha$). This Z-Scale breach forces a **Born Rule truncation** — the rendering engine overwrites the shared backend address. Because Bob's pointer references the same address, any subsequent query through Bob's pointer reads the *already updated* state. No signal traverses 3D space. The update occurs at topological distance **zero** in the Singleton graph.

Bell's theorem is not violated — it is *explained*. The CHSH bound $|S| \leq 2$ applies to protocols routing exclusively through the 3D spatial grid. The quantum bound $|S| = 2\sqrt{2}$ is achieved because entangled systems share a backend address at topological distance **zero**.

---

## What This Script Verifies

The script performs **9 independent checks**, comparing local hidden variable protocols against the ATR backend aliasing model:

| Check | Description | Result |
|:-----:|-------------|:------:|
| 1 | Local realism CHSH bound: $\|S\| \leq 2$ | ✅ $\|S\| = 2.001$ |
| 2 | Backend aliasing CHSH: $\|S\| = 2\sqrt{2}$ | ✅ $\|S\| = 2.831$ |
| 3 | Correlation function $E(a,b) = -\cos(a-b)$ over 36 angles | ✅ max error $< 0.02$ |
| 4 | No-signaling: Bob's marginals independent of Alice's choice | ✅ All within 0.5% of 0.5 |
| 5 | Tsirelson bound $2\sqrt{2}$ confirmed algebraically | ✅ Exact |
| 6 | Monogamy: max A–B entanglement precludes A–C correlation | ✅ $E_{AC} \approx 0$ |
| 7 | Backend aliasing saves $2\ln 2$ nats per pair | ✅ Exact |
| 8 | Frontend distance $\gg$ backend distance (0) | ✅ 19 vs 0 hops |
| 9 | Scope: only $\hbar$, $k_B$, $Z_\alpha$ used (no $G$) | ✅ Clean |

---

## Quick Start

```bash
# No dependencies — pure Python 3.6+ standard library only
python verify_epr.py
```

### Expected Output

```
══════════════════════════════════════════════════════════════════════
  COMPUTATIONAL VERIFICATION
  Entanglement as Backend Memory Aliasing:
  Resolving the EPR Paradox via Algorithmic Graph Routing
══════════════════════════════════════════════════════════════════════

  ...

══════════════════════════════════════════════════════════════════════
                         VERIFICATION SUMMARY
══════════════════════════════════════════════════════════════════════

  ✅ PASS  Local realism CHSH ≤ 2
  ✅ PASS  Backend aliasing CHSH = 2√2
  ✅ PASS  E(a,b) = -cos(a-b) verified
  ✅ PASS  No-signaling: Bob's marginals independent of Alice
  ✅ PASS  Tsirelson bound 2√2 confirmed algebraically
  ✅ PASS  Monogamy (CKW): max A-B entanglement → zero A-C entanglement
  ✅ PASS  Backend aliasing saves 2 ln 2 nats per pair
  ✅ PASS  Grid routing: BFS O(L) vs backend O(0)
  ✅ PASS  Scope: only ℏ, k_B, Z_α used (no G, no c)

══════════════════════════════════════════════════════════════════════
  ALL 9/9 CHECKS PASSED — DERIVATION NUMERICALLY VERIFIED
══════════════════════════════════════════════════════════════════════
```

---

## The Simulation: Memory Aliasing vs Local Realism

The script implements two protocols on the same spatial grid:

### Local Realism Protocol (Bell-bounded)
- Each particle carries a **predetermined hidden variable** $\lambda$ assigned at the source
- Outcomes: $A(a, \lambda) = \text{sign}(\cos(a - \lambda))$ — deterministic, local
- Result: CHSH $|S| \leq 2$

### Backend Aliasing Protocol (Tsirelson-bounded)
- A **single shared state** is stored in a `SingletonBackend` object
- Two pointers (array indices) reference the **same address**
- Alice dereferences her pointer → Z-Scale breach → Born Rule truncation → backend state updated
- Bob dereferences his pointer → reads the **already truncated** state
- Result: CHSH $|S| = 2\sqrt{2}$

The key difference: in the local protocol, each particle's data is independent. In the backend protocol, both measurements route through the same memory address — **no data travels between Alice and Bob**.

---

## ATR Paper Series

| Paper | Topic | Repo |
|-------|-------|------|
| ATR (foundations) | Emergent spacetime & gravity | [zenodo.19120294](https://doi.org/10.5281/zenodo.19120294) |
| Dark Energy | Cosmological constant / vacuum catastrophe | [atr-holographic-dark-energy](https://github.com/srdrymn/atr-holographic-dark-energy) |
| MOND Scale | Galactic acceleration anomaly | [atr-verifiy-mond-scale](https://github.com/srdrymn/atr-verifiy-mond-scale) |
| Zeno Threshold | Born Rule / wavefunction collapse | [atr-wavefunction-collapse](https://github.com/srdrymn/atr-wavefunction-collapse) |
| Black Hole | Information paradox resolution | [atr-resolving-black-hole-information-paradox](https://github.com/srdrymn/atr-resolving-black-hole-information-paradox) |
| **EPR Paradox (this repo)** | **Bell inequality / entanglement** | **[atr-epr-paradox](https://github.com/srdrymn/atr-epr-paradox)** |
| Double Slit | Z-Scale demonstration on lattice | [atr-zeno-double-slit-simulation](https://github.com/srdrymn/atr-zeno-double-slit-simulation) |
| Hilbert Space | Why complex numbers | [atr-zeno-hilbert-space-derivation](https://github.com/srdrymn/atr-zeno-hilbert-space-derivation) |

---

## References

1. A. Einstein, B. Podolsky, N. Rosen, "Can quantum-mechanical description of physical reality be considered complete?" *Phys. Rev.* **47**, 777 (1935).
2. J. S. Bell, "On the Einstein Podolsky Rosen paradox," *Physics* **1**, 195 (1964).
3. J. F. Clauser et al., "Proposed experiment to test local hidden-variable theories," *Phys. Rev. Lett.* **23**, 880 (1969).
4. B. S. Tsirelson, "Quantum generalizations of Bell's inequality," *Lett. Math. Phys.* **4**, 93 (1980).
5. A. Aspect et al., "Experimental realization of EPR-Bohm Gedankenexperiment," *Phys. Rev. Lett.* **49**, 91 (1982).
6. R. Landauer, "Irreversibility and heat generation in the computing process," *IBM J. Res. Dev.* **5**, 183 (1961).
7. C. H. Bennett, "The thermodynamics of computation — a review," *Int. J. Theor. Phys.* **21**, 905 (1982).
8. S. Yaman, "The Algorithmic Theory of Reality," *Zenodo* (2026). [DOI: 10.5281/zenodo.19120294](https://doi.org/10.5281/zenodo.19120294)
9. S. Yaman, "The Zeno Threshold: Wavefunction Collapse and the Emergence of Time via Landauer Erasure Limits," (2026).

## License

MIT License — see [LICENSE](LICENSE).

## Author

**Serdar Yaman** — Independent Researcher, MSc Physics, United Kingdom
