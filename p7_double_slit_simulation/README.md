# ATR Double-Slit v3: The Z-Scale in Action

[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ATR Paper](https://img.shields.io/badge/ATR%20Paper-10.5281%2Fzenodo.19042891-blue)](https://doi.org/10.5281/zenodo.19042891)

**Computational verification for:**

> **Interference and Erasure on a Discrete Lattice: A Computational Demonstration of the Zeno Threshold (Z-Scale) in the Double-Slit Experiment**
> Serdar Yaman (2026)

Based on:
> S. Yaman, *"The Zeno Threshold: Wavefunction Collapse and the Emergence of Time via Landauer Erasure Limits,"* March 2026.

---

## The Experiment

The double-slit experiment is the canonical test for any interpretation of quantum mechanics. This simulation demonstrates the **Zeno Threshold (Z-Scale)** mechanism on a discrete lattice:

**Run A — No Detector (Z-Scale NOT breached):**
A Gaussian wave packet propagates through both slits on a 256×128 tight-binding lattice. No which-path information is recorded. Entanglement entropy = 0 at all times. The observer can track the full coherent superposition. **Interference fringes emerge from pure lattice unitarity.**

**Run B — Which-Path Detector (Z-Scale breached):**
A detector qubit entangles with the particle via a controlled rotation in the slit region. The full state lives in $\mathcal{H}_\text{particle} \otimes \mathcal{H}_\text{detector}$. As the particle passes through the slits, entanglement entropy grows from 0 toward $S_\text{max} = \ln 2$. When $S > Z_\alpha$, the observer's rendering engine is forced to truncate (Born Rule garbage collection). **Interference fringes are destroyed.**

### The Derivation Chain

```
ATR Axiom 2: Information conservation
    ↓
Unitarity: U†U = I  →  U = exp(-iHΔt)  ← the i is FORCED
    ↓
Graph topology: H = -J Σ |i⟩⟨j|  →  E(kx,ky) = 2J(2 - cos kx - cos ky)
    ↓
Phase per hop is COMPLEX  →  path interference EMERGES
    ↓
Which-path detector: |particle⟩ ⊗ |detector⟩  →  entanglement entropy grows
    ↓
S > Z_α  →  Landauer cost exceeds budget  →  Born Rule truncation
    ↓
Cross-terms erased  →  FRINGES DESTROYED
```

---

## Results

### Figure 1: Coherent vs. Z-Breached Detection Patterns

![Figure 1](fig1_interference_patterns.png)

**(a)** Coherent propagation: interference fringes from $|\psi_1 + \psi_2|^2$.
**(b)** Z-Scale breached: fringes destroyed, only $|\psi_1|^2 + |\psi_2|^2$ remains.

### Figure 2: Entanglement Entropy Growth

![Figure 2](fig2_entropy_growth.png)

Entropy grows from 0 to $\ln 2$ as the particle entangles with the detector qubit. Three Z-Scale thresholds are marked — strict ($Z_\alpha = 0.10$) breaches at step 2, medium ($Z_\alpha = 0.30$) at step 5, loose ($Z_\alpha = 0.60$) at step 11.

### Figure 3: Wave Packet Propagation

![Figure 3](fig3_wavefunction_snapshot.png)

Four time snapshots of $|\psi|^2$ on the lattice: approach → slit passage → diffraction + interference → arrival at detector.

### 18/18 Checks Pass

| # | Section | Check | Result |
|---|---------|-------|:------:|
| 1 | §2 | Interference EMERGES from lattice unitarity | ✅ |
| 2 | §2 | Unitarity preserved (modulo absorbing boundaries) | ✅ |
| 3 | §2 | Dispersion $E(k_x,k_y) = 2J(2-\cos k_x-\cos k_y)$ from graph topology | ✅ |
| 4 | §2 | $\exp(-iH\Delta t)$: $\lvert U\rvert^2 = 1$ for all $\mathbf{k}$ (probability conserved) | ✅ |
| 5 | §2 | $\exp(-H\Delta t)$: $\lvert U\rvert^2 \neq 1$ (real propagator LEAKS probability) | ✅ |
| 6 | §3 | No detector → $S_\text{ent}$ = 0 (product state) | ✅ |
| 7 | §3 | With detector: entropy grows during slit passage | ✅ |
| 8 | §3 | Entropy approaches $S_\text{max}$ = ln(2) | ✅ |
| 9 | §4 | Strict Z-Scale breaches FIRST (lowest tolerance) | ✅ |
| 10 | §4 | Truncation: $\text{Tr}(\rho) = 1$ preserved | ✅ |
| 11 | §4 | Z-Scale breach: fringes → no fringes | ✅ |
| 12 | §4 | Detector entropy + Born probabilities → incoherent sum | ✅ |
| 13 | §5 | Born Rule statistics: $\chi^2$ test at 95% ($N = 10^5$) | ✅ |
| 14 | §5 | Measurable fringe spacing from lattice dispersion | ✅ |
| 15 | §5 | Single slit: less modulation than double-slit | ✅ |
| 16 | §5 | Entropy trace: grows from near-zero to stable value | ✅ |
| 17 | §X | Scope: only information-thermodynamic quantities used | ✅ |
| 18 | §X | Landauer: hopping energy = information cost per hop | ✅ |

---

## What Each Check Proves

**Checks 1–5 (Lattice Emergence):** No wave equation is typed. No `exp(ikr)`. The tight-binding Hamiltonian `H = -J Σ |i⟩⟨j|` is pure graph topology. The propagator `U = exp(-iHΔt)` is the UNIQUE unitary form (checked: the real alternative `exp(-HΔt)` leaks probability). Interference fringes emerge as a consequence.

**Checks 6–8 (Entanglement Entropy):** Without a detector, the state is a product state → zero entropy → Z-Scale is never breached → fringes survive. With a detector, the particle-detector tensor product builds up entanglement entropy from 0 toward ln(2), creating real which-path information.

**Checks 9–12 (Z-Scale Mechanism):** Multiple Z-Scales are tested (strict Z=0.10, medium Z=0.30, loose Z=0.60, infinite). The strictest breaches first. At breach, Born Rule truncation erases cross-terms. The coherent pattern has multiple fringe minima; the truncated pattern has none. The incoherent sum $|ψ_1|^2 + |ψ_2|^2$ IS the truncated pattern.

**Checks 13–18 (Validation):** Monte Carlo sampling confirms Born Rule statistics. Fringe spacing is measured from lattice dispersion. No gravitational constant G or Planck length appears anywhere.

---

## Quick Start

```bash
pip install numpy matplotlib   # dependencies
python3 simulate_double_slit.py  # run verification (18 checks)
python3 generate_figures.py      # generate publication figures
```

### Expected Output

```
╔══════════════════════════════════════════════════════════════════════╗
║  ATR Double-Slit v3 — The Z-Scale in Action                        ║
║  Author: Serdar Yaman | Date: March 2026                            ║
╚══════════════════════════════════════════════════════════════════════╝

  ...

════════════════════════════════════════════════════════════════════════
  SUMMARY: 18/18 passed
════════════════════════════════════════════════════════════════════════
```

### Generated Figures

```
fig1_interference_patterns.png   — Coherent vs. Z-breached detection patterns
fig2_entropy_growth.png          — Entanglement entropy with Z-Scale thresholds
fig3_wavefunction_snapshot.png   — 2D wave propagation snapshots
```

---

## Files

| File | Description |
|------|-------------|
| `simulate_double_slit.py` | Main verification script (18 automated checks) |
| `generate_figures.py` | Publication figure generator (3 matplotlib figures) |
| `fig1_interference_patterns.png` | Figure 1: coherent vs Z-breached patterns |
| `fig2_entropy_growth.png` | Figure 2: entropy growth curve |
| `fig3_wavefunction_snapshot.png` | Figure 3: 2D wavefunction snapshots |

---

## Physical Constants

| Constant | Symbol | Value |
|----------|--------|-------|
| Reduced Planck constant | $\hbar$ | $1.0546 \times 10^{-34}$ J·s |
| Boltzmann constant | $k_B$ | $1.381 \times 10^{-23}$ J/K |

> **Note:** No gravitational constant $G$ or Planck length $\ell_P$ appears. This simulation is strictly information-thermodynamic.

---

## References

1. S. Yaman, *"The Algorithmic Theory of Reality: Rigorous Mathematical Foundations,"* Zenodo (2026).
2. S. Yaman, *"The Zeno Threshold: Wavefunction Collapse and the Emergence of Time via Landauer Erasure Limits,"* March 2026.
3. R. P. Feynman, R. B. Leighton, and M. Sands, *The Feynman Lectures on Physics*, Vol. III (Addison-Wesley, 1965).
4. E. Joos and H. D. Zeh, "The emergence of classical properties through interaction with the environment," *Z. Phys. B* **59**, 223 (1985).
5. W. H. Zurek, "Decoherence, einselection, and the quantum origins of the classical," *Rev. Mod. Phys.* **75**, 715 (2003).
6. B. Misra and E. C. G. Sudarshan, "The Zeno's paradox in quantum theory," *J. Math. Phys.* **18**, 756 (1977).
7. R. Landauer, "Irreversibility and heat generation in the computing process," *IBM J. Res. Dev.* **5**, 183 (1961).
8. C. H. Bennett, "The thermodynamics of computation — a review," *Int. J. Theor. Phys.* **21**, 905 (1982).

## License

MIT License — see [LICENSE](LICENSE).

## Author

**Serdar Yaman** — Independent Researcher, MSc Physics, United Kingdom
