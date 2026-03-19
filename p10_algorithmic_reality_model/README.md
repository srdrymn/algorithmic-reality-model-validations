# P10 — Algorithmic Reality Model: Unified Validation Suite

This directory contains **six cross-cutting validation scripts** that verify the internal consistency and computability
of the entire Algorithmic Reality Model (ARM), as presented in:

> S. Yaman, *"The Algorithmic Reality Model: A Unified Framework Grounding Gravity, Quantum Mechanics and Consciousness in Finite Computation,"* Zenodo (2026).

These scripts go beyond individual paper validations. They test the **full derivation chain** from axioms to emergent gravity, verify **cross-paper constant consistency**, and demonstrate key theorems (singularity resolution, selective attention optimality) on concrete qubit systems.

---

## Scripts

| Script | Theorems Tested | Description |
|--------|----------------|-------------|
| `toy_model_4qubit.py` | Appendix B, Theorems 2.1, 3.1, 4.6, 5.2, 6.2, 7.5, 7.6, Def. 7.1 | End-to-end verification of **every ATR definition** on a 6-qubit system (C, A, B, E₁, E₂, E₃). Checks faithfulness, modular Hamiltonian, Page-Wootters time, POVM non-commutativity, no-signalling, spectral gap, area law, QFIM metric. |
| `arm_derivation_chain.py` | Full chain: §2→§3→§4→§5→§6→§7→§8 | **10-link derivation chain audit** from axioms through Born rule, emergent time, selective attention, energy-data equivalence, QFIM geometry, spectral gap, area law, to Einstein equations via Jacobson bridge. |
| `cross_paper_consistency.py` | P1 §7.5-7.7, P2 §3, P3 §4 | **Pure ARM cross-paper consistency**: computes η₀ from a lattice area law, derives G_ARM = 1/(4η₀), verifies ρ_Λ via two independent ARM roads (Landauer vs Jacobson), confirms a₀ = 1/R_E. **Zero CODATA constants imported.** |
| `selective_attention_cost.py` | Theorem 4.6 | Benchmarks selective-attention POVMs vs full-collapse measurements across system sizes (2–6 qubits), confirming selective collapse is **always thermodynamically cheaper** (40–70% Landauer savings). |
| `emergent_curvature.py` | Theorems 6.4, 7.4, Def. 7.1 | Demonstrates that localized entanglement enhancement ("data condensation") on a 10-qubit Heisenberg chain produces **emergent curvature** in the QFIM metric, with curvature peaking at the data condensation site. |
| `singularity_resolution.py` | Theorem 8.4, Lemma 8.1 | Shows QFIM curvature **saturates** at R_max rather than diverging as coupling strength increases from 1 to 1000, proving singularity resolution for finite-dimensional observers. |

## Quick Start

```bash
# Run all validations
cd p10_algorithmic_reality_model/
for f in *.py; do echo "=== $f ==="; python3 "$f"; echo; done
```

Or run individually:
```bash
python3 toy_model_4qubit.py           # ~2s
python3 arm_derivation_chain.py        # ~5s
python3 cross_paper_consistency.py     # ~10s (lattice computation)
python3 selective_attention_cost.py    # ~30s (generates figure)
python3 emergent_curvature.py          # ~15s (generates figure)
python3 singularity_resolution.py      # ~2min (generates figure)
```

## Dependencies

- Python 3.8+
- NumPy
- SciPy
- Matplotlib (for figure-generating scripts)

## Output

Each script prints a structured test report with ✅/❌ for each check.
Scripts that generate figures save them as `.png` in this directory:

| Figure | Description |
|--------|-------------|
| `selective_attention_cost.png` | Erasure cost ratio and thermodynamic savings vs system size |
| `emergent_curvature.png` | Entanglement, QFIM metric, metric perturbation, and Ricci scalar profiles |
| `singularity_resolution.png` | Curvature, entropy, metric, and energy gap saturation vs coupling strength |

## License

MIT — See repository root LICENSE.
