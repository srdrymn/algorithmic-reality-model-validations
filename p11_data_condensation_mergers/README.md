# P11 — Data Condensation Mergers via ARM J-Field Dynamics

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19117800-blue)](https://doi.org/10.5281/zenodo.19117800)

> S. Yaman, *"Multi-Body Data Condensation Dynamics in the Algorithmic Reality Model: Computational Validation of J-Field N-Body Mergers,"* Zenodo (2026).
> DOI: [10.5281/zenodo.19117800](https://doi.org/10.5281/zenodo.19117800)

Computational validation of the ARM framework for multi-body data condensation dynamics. Demonstrates that the ARM J-field formulation reproduces the standard phenomenology of compact object inspiral, merger, and ringdown from a scalar clock-rate field.

---

## Important Transparencies

### Correspondences with Known Physics

The ARM dynamics presented here correspond to established results in the weak-field limit:

| ARM Result | Known Correspondence | Reference |
|-----------|---------------------|-----------|
| Acceleration $\propto M/r^2$ (§2.2) | Newton's law of gravitation | Newton (1687) |
| Inspiral $da/dt \propto \mu M^2 / a^3$ | GR quadrupole formula | Peters (1964) |
| Orbital frequency $\omega \propto a^{-3/2}$ | Kepler's third law | Kepler (1619) |
| Velocity factor $\gamma = (1-v^2)^{-1/2}$ | Lorentz factor | Lorentz (1904) |
| Ringdown $\omega_{\text{th}} = 0.37/M_f$ | Schwarzschild QNM | Leaver (1985) |

These correspondences are expected: ARM derives Newtonian gravity and GR as limiting cases of its informational dynamics. The novelty is that these results emerge from a single scalar clock-rate field $J(\mathbf{x})$ without tensor field equations — not that the dynamical laws themselves are new.

### Why ARM Does Not Need General Relativity

In conventional physics, simulating two merging compact objects requires solving Einstein's 10 coupled, non-linear partial differential equations across millions of 3D grid points. ARM replaces this with:

- A **scalar clock-rate field** $J(\mathbf{x})$: a simple algebraic sum
- **Node dynamics**: $\mathbf{a}_i = -\nabla_i J$
- **Zeno aggregation**: deterministic merger when $J$ saturates at $Z_\alpha$

No tensors. No PDEs. No mesh refinement. The resulting dynamics in the weak field are **mathematically equivalent to Newtonian gravity** — this is a feature, not a limitation, since ARM derives Newtonian gravity as a limit.

### Computational Comparison (Honest Assessment)

The ARM simulations run on a consumer workstation in milliseconds. However, a direct comparison with numerical relativity is **not appropriate**: NR solves the full Einstein field equations (metric tensor at every point, gauge evolution, constraint propagation), while ARM evaluates pairwise $1/r$ potential gradients — a fundamentally simpler problem. A fair comparison is ARM vs. a Newtonian N-body code (e.g., REBOUND, GADGET-4), where runtimes are comparable.

---

## The ARM Approach

In the ARM framework, a data condensation is a localised node with informational load *M*. The clock-rate field encodes the computational slowdown:

```
J(x,y) = max(Z_α, 1 - Σ M_i / |x - x_i|)
```

- **J ≈ 1**: far from any informational load (flat arena)
- **J → Z_α**: near the Zeno boundary (maximum clock slowdown = Zeno threshold)
- **Dynamics**: nodes move along −∇J (equivalent to Newtonian gravity with G = 1)
- **Clock-rate perturbations**: time-varying J-field disturbances propagating through the arena

---

## Scripts

| Script | Checks | Description |
|--------|--------|-------------|
| `arm_binary_merger.py` | **6** | Binary inspiral → merger → ringdown. Produces J-field evolution, chirp waveform, orbital trajectories |
| `arm_nbody_cluster.py` | **5** | N-body scaling proof (N = 2..100). Produces 100-node cluster visualization, timing analysis |
| `arm_nbody_latency_merger.py` | **7** | Network latency retardation + Zeno aggregation. 6-node system with inspiral decay, informational load conservation, energy dissipation diagnostics |

## Key Results

| Metric | Value |
|--------|-------|
| Binary inspiral computation | **1.2 ms** |
| 100-node J-field computation | **36 ms** |
| 6-node latency merger (4000 ticks) | **330 ms** |
| J-field gradient scaling | **O(N²)** confirmed |
| Informational load conservation (latency sim) | **< 10⁻¹⁰ relative error** |

## Generated Figures

| Figure | Description |
|--------|-------------|
| `binary_jfield_evolution.png` | 6-panel J-field snapshots: inspiral → merger |
| `binary_waveform.png` | Inspiral chirp J-field perturbation waveform with ringdown |
| `binary_orbits.png` | Spiral-in trajectories on J-field background |
| `nbody_jfield_100.png` | 100 data condensation nodes — full J-field visualization |
| `nbody_scaling.png` | Computation time scaling |
| `nbody_evolution.png` | 20-node cluster dynamical evolution |
| `latency_nbody_mergers.png` | N-body trajectories with Zeno aggregation events |
| `latency_separation_energy.png` | Separation distances + kinetic energy timeline |

### Binary Data Condensation Merger

![ARM J-Field Evolution — Binary Data Condensation Merger](binary_jfield_evolution.png)

![ARM J-Field Perturbation Waveform — Binary Merger Chirp](binary_waveform.png)

![Inspiral Trajectories on J-Field Background](binary_orbits.png)

### N-Body Data Condensation Cluster

![ARM J-Field — 100 Data Condensation Nodes](nbody_jfield_100.png)

![Computation Time Scaling](nbody_scaling.png)

![20-Node Cluster Dynamical Evolution](nbody_evolution.png)

### Latency-Driven N-Body Mergers

![ARM N-Body: Network Latency & Zeno Aggregation Trajectories](latency_nbody_mergers.png)

![Separation Distances & Energy Dissipation via Algorithmic Latency](latency_separation_energy.png)

## Open Problems

1. **Independent derivation of $\kappa = 64/5$** from the J-field wave equation (currently matches GR quadrupole formula)
2. **QNM spectrum from ARM** — ringdown parameters currently match known Schwarzschild values
3. **Extension to 3D** — current latency simulation operates in 2D with 3D force law
4. **Spin** — no angular momentum structure on nodes; spin-orbit coupling absent
5. **Quantitative NR waveform comparison** — e.g., against SXS catalogue

## Quick Start

```bash
python3 arm_binary_merger.py           # ~10s (6 checks, 3 figures)
python3 arm_nbody_cluster.py           # ~30s (5 checks, 3 figures)
python3 arm_nbody_latency_merger.py    # ~1s  (7 checks, 2 figures)
```

## Dependencies

- Python 3.8+, NumPy, SciPy, Matplotlib

## License

MIT
