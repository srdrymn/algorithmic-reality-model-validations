# Why Complex Numbers? Z-Scale Selection of Hilbert Space

[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ATR Paper](https://img.shields.io/badge/ATR%20Paper-10.5281%2Fzenodo.19042891-blue)](https://doi.org/10.5281/zenodo.19042891)

**Computational verification for:**

> **Why Complex Numbers? Deriving the Hilbert Space Structure from the Zeno Threshold**
> Serdar Yaman (2026)

Based on:
> S. Yaman, *"The Zeno Threshold: Wavefunction Collapse and the Emergence of Time via Landauer Erasure Limits,"* March 2026.

---

## The Question

Every textbook begins with: *"States live in a complex Hilbert space."* But why complex? Why not real numbers ($\mathbb{R}$), which are simpler? Why not quaternions ($\mathbb{H}$), which are richer? Why not octonions ($\mathbb{O}$)?

This verification script proves that $\mathbb{C}$ is the **unique** algebraic field that survives three filters:

### The Elimination Chain

```
Hurwitz's theorem: only R, C, H, O are normed division algebras
    ↓
O eliminated: non-associative → U(t1+t2) ≠ U(t1)U(t2) → Axiom 2 violated
    ↓
H eliminated: non-commutative → tensor product ill-defined → no composability
    ↓
R eliminated: O(K⁴) hidden parameters → Z-Scale breach → premature collapse
    ↓
C survives: zero excess entropy, perfect local tomography, maximal coherence
```

---

## Key Results

### Why Real Numbers Fail

In real QM, bipartite systems contain **hidden parameters** invisible to local measurements. The excess scales as $O(K^4)$:

| K | Hidden Parameters ($\Delta d$) | Z-Scale Impact |
|---|-------------------------------|----------------|
| 2 | 1 | σ_y⊗σ_y correlation invisible |
| 3 | 9 | Growing overhead |
| 4 | 36 | Severe Z-Scale strain |
| 5 | 100 | Unsustainable |
| 10 | 2,025 | Catastrophic breach |

These hidden parameters consume the observer's Z-Scale budget without providing locally observable information, triggering premature Born Rule truncation.

### Why Complex Numbers Win

For $\mathbb{C}$: $D_\mathbb{C}(K) = K^2$ is perfectly **multiplicative** — $D(K_1 K_2) = D(K_1) \cdot D(K_2)$ — meaning zero excess parameters for any bipartite system. The observer's Z-Scale is never strained by the algebra itself.

### The Goldilocks Symmetry

$\mathbb{C}$ is the unique field where the transformation group dimension equals the state-space dimension: $\dim \mathrm{SU}(K) = d_\mathbb{C}(K) = K^2 - 1$. This self-consistency is absent in $\mathbb{R}$ and $\mathbb{H}$.

---

## 12/12 Checks Pass

| # | Check | Result |
|---|-------|:------:|
| 1 | State dimensions $d(K)$ for $\mathbb{R}, \mathbb{C}, \mathbb{H}$ (K=2..5) | ✅ |
| 2a | Local tomography: Real FAILS | ✅ |
| 2b | Local tomography: Complex PASSES | ✅ |
| 2c | Local tomography: Quaternionic FAILS | ✅ |
| 3 | Excess $\Delta C = 0$ ONLY for Complex | ✅ |
| 4 | Hidden parameter $\langle\sigma_y \otimes \sigma_y\rangle$ identified | ✅ |
| 5 | Quaternionic tensor product fails (matrix proof) | ✅ |
| 6 | $D_\mathbb{C}(K) = K^2$ multiplicative for K={2..6} | ✅ |
| 7 | $\dim \mathrm{SU}(K) = d_\mathbb{C}(K)$ (unique to $\mathbb{C}$) | ✅ |
| 8 | Z-Scale breach rate: $O(K^4)$ for $\mathbb{R}$, zero for $\mathbb{C}$ | ✅ |
| 9 | Octonions eliminated by non-associativity (Hurwitz) | ✅ |
| 10 | Scope: only $\hbar$, $k_B$, $Z_\alpha$ used (no $G$) | ✅ |

---

## Quick Start

```bash
pip install numpy   # only standard library needed, but ensures compatibility
python3 verify_hilbert.py
```

### Expected Output

```
══════════════════════════════════════════════════════════════════════
  ATR VERIFICATION: Why Complex Numbers?
  Why Complex Numbers? -- Z-Scale Selection of Hilbert Space
══════════════════════════════════════════════════════════════════════

  ...

══════════════════════════════════════════════════════════════════════
  ALL 12/12 CHECKS PASSED -- DERIVATION VERIFIED
══════════════════════════════════════════════════════════════════════
```

---

## Files

| File | Description |
|------|-------------|
| `verify_hilbert.py` | Main verification script (12 automated checks) |
| `README.md` | This file |
| `LICENSE` | MIT License |

---

## Physical Constants

| Constant | Symbol | Value |
|----------|--------|-------|
| Reduced Planck constant | $\hbar$ | $1.0546 \times 10^{-34}$ J·s |
| Boltzmann constant | $k_B$ | $1.381 \times 10^{-23}$ J/K |

> **Note:** No gravitational constant $G$, speed of light $c$, or Planck length $\ell_P$ appears. This verification is strictly algebraic and information-theoretic.

---

## References

1. S. Yaman, *"The Algorithmic Theory of Reality: Rigorous Mathematical Foundations,"* Zenodo (2026).
2. S. Yaman, *"The Zeno Threshold: Wavefunction Collapse and the Emergence of Time via Landauer Erasure Limits,"* March 2026.
3. L. Hardy, "Quantum Theory From Five Reasonable Axioms," quant-ph/0101012 (2001).
4. G. Chiribella, G. M. D'Ariano, and P. Perinotti, "Informational derivation of quantum theory," *Phys. Rev. A* **84**, 012311 (2011).
5. L. Masanes and M. P. Müller, "A derivation of quantum theory from physical requirements," *New J. Phys.* **13**, 063001 (2011).
6. A. Hurwitz, "Über die Composition der quadratischen Formen," *Nachr. Ges. Wiss. Göttingen*, 309 (1898).
7. W. K. Wootters, "Quantum mechanics without complex numbers," *Found. Phys.* **20**, 1365 (1990).
8. R. Landauer, "Irreversibility and heat generation in the computing process," *IBM J. Res. Dev.* **5**, 183 (1961).
9. C. H. Bennett, "The thermodynamics of computation — a review," *Int. J. Theor. Phys.* **21**, 905 (1982).

## License

MIT License — see [LICENSE](LICENSE).

## Author

**Serdar Yaman** — Independent Researcher, MSc Physics, United Kingdom
