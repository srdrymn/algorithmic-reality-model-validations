# Algorithmic Reality Model — Computational Validations

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Open-source computational validation suite for the **Algorithmic Reality Model (ARM)** paper series by Serdar Yaman.

Each subfolder contains the simulation scripts, verification code, and generated figures for one paper in the series. Every claim tagged as "computationally verified" in the papers can be reproduced by running the corresponding script.

---

## Repository Structure

```
algorithmic-reality-model-validations/
├── p1_algorithmic_theory_of_reality/
├── p2_holographic_dark_energy/
├── p3_mond_scale/
├── p4_wavefunction_collapse/
├── p5_black_hole_information_paradox/
├── p6_epr_paradox/
├── p7_double_slit_simulation/
├── p8_hilbert_space/
├── p9_emergent_spacetime/
└── README.md
```

---

## Validation Summaries

### [`p1_algorithmic_theory_of_reality/`](p1_algorithmic_theory_of_reality/)

**Prediction 9.4: Sub-Tick Correlation Plateaus.** Simulates the discriminating prediction of ATR — that a measurement apparatus with discrete clock frequency ν_α produces step-like correlation plateaus rather than smooth exponential decay. Models a 5.0 GHz transmon qubit under Lindblad dephasing with realistic clock jitter. Demonstrates the ATR signal exceeds shot noise by **107σ (RMS)** with N = 10,000 shots.

- `prediction_94_subtick_correlation.py` — Simulation script
- `prediction_94_simulation.png` — Three-panel output figure

### [`p2_holographic_dark_energy/`](p2_holographic_dark_energy/)

**Holographic Dark Energy Verification.** Numerically verifies the ATR derivation of the cosmological constant as Bennett-Landauer thermodynamic overhead of the cosmological event horizon. Computes the predicted dark energy density ρ_Λ = 3c⁴/(8πGR_E²) and compares against Planck 2018 observational constraints.

- `verify_dark_energy.py` — Verification script

### [`p3_mond_scale/`](p3_mond_scale/)

**MOND Acceleration Scale Verification.** Verifies the derivation of the MOND acceleration threshold a₀ ≈ 1.2 × 10⁻¹⁰ m/s² as the entropic noise floor where the local Unruh temperature drops below the Gibbons-Hawking temperature of the cosmological event horizon. Reproduces the Radial Acceleration Relation across galactic data.

- `verify_mond_scale.py` — Verification script

### [`p4_wavefunction_collapse/`](p4_wavefunction_collapse/)

**Wavefunction Collapse & Zeno Threshold Verification.** Verifies the derivation of the Born Rule from the Bennett-Landauer erasure bound and simulates the quantum Zeno threshold — the critical measurement frequency at which continuous observation freezes quantum evolution.

- `verify_zeno_threshold.py` — Verification script
- `v1/` — Earlier version of the verification

### [`p5_black_hole_information_paradox/`](p5_black_hole_information_paradox/)

**Black Hole Information Paradox Verification.** Simulates algorithmic data compression in emergent spacetime to verify the resolution of the black hole information paradox via thermodynamic graph dynamics. Tests information conservation across the event horizon under ATR's Landauer barrier model.

- `verify_black_hole.py` — Verification script

### [`p6_epr_paradox/`](p6_epr_paradox/)

**EPR Paradox Verification.** Verifies the resolution of the EPR paradox via algorithmic graph routing in the Singleton. Simulates entanglement correlations as backend memory aliasing and confirms that Bell inequality violations emerge naturally from the non-spatial Singleton structure without superluminal signaling.

- `verify_epr.py` — Verification script

### [`p7_double_slit_simulation/`](p7_double_slit_simulation/)

**Double-Slit Experiment: Zeno Threshold in Action.** Full lattice simulation of the double-slit experiment demonstrating interference, which-path erasure, and the Zeno threshold on a discrete grid. Generates publication-quality figures showing how the Z-scale (measurement frequency / system frequency) controls the transition from quantum to classical behavior.

- `simulate_double_slit.py` — Full lattice simulation
- `generate_figures.py` — Figure generation script
- `fig1_interference_patterns.png` — Interference pattern output
- `fig2_entropy_growth.png` — Entropy evolution output
- `fig3_wavefunction_snapshot.png` — Wavefunction visualization

### [`p8_hilbert_space/`](p8_hilbert_space/)

**Why Complex Numbers? Z-Scale Selection of Hilbert Space.** Verifies computationally that the Zeno threshold uniquely selects the complex Hilbert space structure over real and quaternionic alternatives. Demonstrates that only the standard complex quantum mechanics (ℝ, ℂ, ℍ, 𝕆) satisfies the ATR axioms with optimal Landauer cost.

- `verify_hilbert.py` — Verification script

### [`p9_emergent_spacetime/`](p9_emergent_spacetime/)

**Emergent Lorentzian Spacetime Verification.** The most comprehensive validation suite: full-chain audit from ATR axioms to emergent curvature. Simulates QFIM-based geometry on qubit lattices, verifies emergent time dilation, gravitational lensing, and black hole thermodynamics from informational first principles.

- `verify_spacetime.py` — Core spacetime verification
- `simulate_emergent_gravity.py` — Emergent gravity simulation
- `simulate_atr_blackhole.py` — Black hole simulation
- `atr_full_chain_audit.py` — Full derivation chain audit
- `p9_deep_audit.py` — Deep consistency audit
- `html_simulations/` — Interactive browser-based simulations
- `exp1_time_dilation.png` — Time dilation output
- `exp2_lensing.png` — Gravitational lensing output
- `exp3_black_hole.png` — Black hole formation output

---

## Paper Series

| # | Title | DOI |
|---|-------|-----|
| P1 | [The Algorithmic Theory of Reality: Rigorous Mathematical Foundations](https://doi.org/10.5281/zenodo.19042891) | [10.5281/zenodo.19042891](https://doi.org/10.5281/zenodo.19042891) |
| P2 | [Holographic Dark Energy from Algorithmic Thermodynamics: Resolving the Vacuum Catastrophe via the Bennett-Landauer Limit](https://doi.org/10.5281/zenodo.19050917) | [10.5281/zenodo.19050917](https://doi.org/10.5281/zenodo.19050917) |
| P3 | [The Galactic Acceleration Anomaly as an Algorithmic Noise Floor: Deriving the MOND Scale from Entropic Thermodynamics](https://doi.org/10.5281/zenodo.19054817) | [10.5281/zenodo.19054817](https://doi.org/10.5281/zenodo.19054817) |
| P4 | [The Zeno Threshold: Wavefunction Collapse and the Emergence of Time via Landauer Erasure Limits](https://doi.org/10.5281/zenodo.19079576) | [10.5281/zenodo.19079576](https://doi.org/10.5281/zenodo.19079576) |
| P5 | [Algorithmic Data Compression in Emergent Spacetime: Resolving the Black Hole Information Paradox via Thermodynamic Graph Dynamics](https://doi.org/10.5281/zenodo.19058635) | [10.5281/zenodo.19058635](https://doi.org/10.5281/zenodo.19058635) |
| P6 | [Entanglement as Backend Memory Aliasing: Resolving the EPR Paradox via Algorithmic Graph Routing in the Singleton](https://doi.org/10.5281/zenodo.19102619) | [10.5281/zenodo.19102619](https://doi.org/10.5281/zenodo.19102619) |
| P7 | [Interference and Erasure on a Discrete Lattice: A Computational Demonstration of the Zeno Threshold in the Double-Slit Experiment](https://doi.org/10.5281/zenodo.19091708) | [10.5281/zenodo.19091708](https://doi.org/10.5281/zenodo.19091708) |
| P8 | [Why Complex Numbers? Deriving the Hilbert Space Structure from the Zeno Threshold](https://doi.org/10.5281/zenodo.19095238) | [10.5281/zenodo.19095238](https://doi.org/10.5281/zenodo.19095238) |
| P9 | [Emergent Lorentzian Spacetime from Informational Geometry — Unifying the QFIM Spatial Metric with Tomita-Takesaki Temporal Flow](https://doi.org/10.5281/zenodo.19104254) | [10.5281/zenodo.19104254](https://doi.org/10.5281/zenodo.19104254) |
| P10 | [The Algorithmic Reality Model: Unifying Quantum Mechanics and General Relativity via the Zeno Threshold and Thermodynamic Graph Routing](https://doi.org/10.5281/zenodo.19111233) | [10.5281/zenodo.19111233](https://doi.org/10.5281/zenodo.19111233) |

---

## Quick Start

Each subfolder is self-contained. To run any validation:

```bash
# Install dependencies (common to all scripts)
pip install numpy matplotlib scipy

# Run any individual validation
cd p1_algorithmic_theory_of_reality/
python prediction_94_subtick_correlation.py

cd ../p9_emergent_spacetime/
python atr_full_chain_audit.py
```

All scripts are pure Python with standard scientific computing dependencies (NumPy, Matplotlib, SciPy). No GPU or specialized hardware required.

---

## License

MIT — see individual `LICENSE` files in each subfolder.

## Author

**Serdar Yaman**
Independent Researcher | MSc Physics, United Kingdom
