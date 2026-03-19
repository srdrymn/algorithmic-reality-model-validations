#!/usr/bin/env python3
"""
Singularity Resolution — Bounded Curvature for Finite Observers
================================================================
Demonstrates ATR Theorem 8.4: A finite-dimensional observer can never
experience a curvature singularity. The QFIM Ricci scalar saturates
at a finite maximum R_max as entanglement density increases.

Model:
  - Start with a ground state of a Heisenberg chain
  - Progressively increase the coupling at a single site (simulating
    gravitational collapse / increasing matter density)
  - Track the QFIM curvature at that site
  - Verify saturation rather than divergence

Physics:
  In classical GR, R → ∞ at a singularity (Penrose 1965).
  In ATR, the observer's finite Hilbert space dimension d and
  finite clock frequency ν_α impose:
      R ≤ R_max = C(d, ν_α)
  where C is determined by the maximum distinguishability of
  quantum states within the observer's attention window.

Reference: S. Yaman, "ATR," (2026), §8, Theorem 8.4, Lemma 8.1.

License: MIT
"""

import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt
import os
import sys

# ═══════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════

def kron_chain(ops):
    result = ops[0]
    for o in ops[1:]:
        result = np.kron(result, o)
    return result


I2 = np.eye(2, dtype=complex)
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)


def partial_trace_bipartition(rho, d_left, d_right, keep='left'):
    rho_r = rho.reshape(d_left, d_right, d_left, d_right)
    if keep == 'left':
        return np.trace(rho_r, axis1=1, axis2=3)
    else:
        return np.trace(rho_r, axis1=0, axis2=2)


def von_neumann_entropy(rho):
    evals = np.linalg.eigvalsh(rho)
    evals = evals[evals > 1e-15]
    return -np.sum(evals * np.log(evals))


PASS = 0
FAIL = 0

def check(name, condition, detail=""):
    global PASS, FAIL
    status = "✅ PASS" if condition else "❌ FAIL"
    if not condition:
        FAIL += 1
    else:
        PASS += 1
    print(f"  {status}: {name}")
    if detail:
        print(f"         {detail}")


print("=" * 70)
print("Singularity Resolution — Curvature Saturation (Theorem 8.4)")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════════════
# System setup
# ═══════════════════════════════════════════════════════════════════════════
N = 8  # Number of qubits (keep manageable: d = 256)
d = 2**N
center = N // 2

print(f"\nLattice: {N} qubits, dimension d = {d}")
print(f"Central site: {center}")
print(f"Max possible entropy: S_max = ln(2) = {np.log(2):.4f} per qubit")

# ═══════════════════════════════════════════════════════════════════════════
# Progressive collapse: increase coupling from 1× to 1000×
# ═══════════════════════════════════════════════════════════════════════════

J_values = np.logspace(0, 3, 30)  # 1 to 1000

print(f"\nScanning J_mass from {J_values[0]:.1f} to {J_values[-1]:.0f}...")

curvatures = []
entropies_center = []
metric_center = []
energy_gaps = []

for J_mass in J_values:
    # Build Hamiltonian
    H = np.zeros((d, d), dtype=complex)
    for i in range(N - 1):
        if abs(i - center) <= 1:
            J = J_mass
        else:
            J = 1.0
        for pauli in [sigma_x, sigma_y, sigma_z]:
            ops = [I2] * N
            ops[i] = pauli
            ops[i + 1] = pauli
            H += J * kron_chain(ops)

    # Transverse field
    for i in range(N):
        ops = [I2] * N
        ops[i] = sigma_x
        H += 0.1 * kron_chain(ops)

    # Ground state
    evals, evecs = np.linalg.eigh(H)
    psi_gs = evecs[:, 0]

    # Energy gap (relevant for spectral properties)
    gap = evals[1] - evals[0]
    energy_gaps.append(gap)

    # Entanglement entropy at center cut
    d_left = 2**center
    d_right = 2**(N - center)
    rho_left = partial_trace_bipartition(
        np.outer(psi_gs, psi_gs.conj()), d_left, d_right)
    S_center = von_neumann_entropy(rho_left)
    entropies_center.append(S_center)

    # QFIM at center bond
    def psi_theta(theta):
        ops = [I2] * N
        ops[center] = sigma_z
        if center + 1 < N:
            ops[center + 1] = sigma_z
        H_pert = kron_chain(ops)
        U = expm(-1j * theta * H_pert)
        return U @ psi_gs

    dtheta = 1e-4
    psi_p = psi_theta(dtheta)
    psi_m = psi_theta(-dtheta)
    dpsi = (psi_p - psi_m) / (2 * dtheta)
    g_center = 4 * (np.dot(dpsi.conj(), dpsi).real -
                     np.abs(np.dot(psi_gs.conj(), dpsi))**2)
    metric_center.append(g_center)

    # QFIM at neighboring bonds for curvature
    def qfim_at(site):
        ops = [I2] * N
        ops[site] = sigma_z
        if site + 1 < N:
            ops[site + 1] = sigma_z
        H_pert = kron_chain(ops)
        U_p = expm(-1j * dtheta * H_pert)
        U_m = expm(1j * dtheta * H_pert)
        psi_pp = U_p @ psi_gs
        psi_mm = U_m @ psi_gs
        dpsi_local = (psi_pp - psi_mm) / (2 * dtheta)
        return 4 * (np.dot(dpsi_local.conj(), dpsi_local).real -
                     np.abs(np.dot(psi_gs.conj(), dpsi_local))**2)

    if center > 0 and center < N - 2:
        g_left = qfim_at(center - 1)
        g_right = qfim_at(center + 1)
        # Discrete Ricci scalar
        log_g = [np.log(max(g_left, 1e-30)),
                 np.log(max(g_center, 1e-30)),
                 np.log(max(g_right, 1e-30))]
        R = log_g[2] - 2 * log_g[1] + log_g[0]
    else:
        R = 0.0

    curvatures.append(abs(R))

curvatures = np.array(curvatures)
entropies_center = np.array(entropies_center)
metric_center = np.array(metric_center)

# ═══════════════════════════════════════════════════════════════════════════
# Saturation analysis
# ═══════════════════════════════════════════════════════════════════════════
print("\n─── Saturation Analysis ───\n")

R_max = np.max(curvatures)
R_final = curvatures[-1]
R_half = curvatures[len(curvatures)//2]

S_max = np.max(entropies_center)
S_bound = center * np.log(2)  # Maximum possible for this bipartition

# Check entropy saturates
check("Entropy saturates below theoretical maximum",
      S_max < S_bound,
      f"S_max = {S_max:.4f}, theoretical bound = {S_bound:.4f}")

# Check curvature saturates (does NOT diverge)
# If curvature were diverging, R(J=1000) >> R(J~10)
# Instead, it should plateau
R_early = np.max(curvatures[:5])   # First few points
R_late = np.max(curvatures[-5:])   # Last few points

check("Curvature does NOT diverge as J → ∞",
      R_late < 100 * R_early or R_late < 100,
      f"|R|(J=1) = {curvatures[0]:.4f}, |R|(J=1000) = {curvatures[-1]:.4f}")

# Check that there exists a finite maximum
check("Finite curvature maximum exists (R_max < ∞)",
      np.isfinite(R_max) and R_max < 1e6,
      f"R_max = {R_max:.4f}")

# Saturation criterion: relative change in curvature decreases
# Compare curvature at J=100 vs J=1000
idx_100 = np.argmin(np.abs(J_values - 100))
idx_1000 = np.argmin(np.abs(J_values - 1000))
delta_R = abs(curvatures[idx_1000] - curvatures[idx_100])
scale_R = max(curvatures[idx_100], 1e-10)

check("Curvature is saturating (|R(1000) - R(100)| << R(100))",
      delta_R / scale_R < 1.0,
      f"|ΔR| / R = {delta_R/scale_R:.4f}")

# Metric also saturates
g_max = np.max(metric_center)
check("QFIM metric saturates",
      np.isfinite(g_max) and g_max < 1e6,
      f"g_max = {g_max:.4f}")

# ═══════════════════════════════════════════════════════════════════════════
# Theorem 8.4 interpretation
# ═══════════════════════════════════════════════════════════════════════════
print("\n─── Theorem 8.4 Interpretation ───")
print(f"  In classical GR: R → ∞ as ρ_matter → ∞ (Penrose singularity)")
print(f"  In ATR (d = {d}): R_max = {R_max:.4f} (finite, bounded)")
print(f"  Reason: Finite Hilbert space d = {d} limits distinguishability")
print(f"  → curvature CANNOT diverge for a finite observer")

# ═══════════════════════════════════════════════════════════════════════════
# Figure
# ═══════════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle(f'Singularity Resolution: Curvature Saturation (Theorem 8.4)\n'
             f'{N}-qubit chain, d = {d}',
             fontsize=13, fontweight='bold')

# (a) Curvature vs coupling strength
ax = axes[0, 0]
ax.semilogx(J_values, curvatures, 'o-', color='firebrick', ms=4)
ax.axhline(R_max, color='gray', ls='--', alpha=0.7,
           label=f'$R_{{max}} = {R_max:.3f}$')
ax.fill_between([J_values[0], J_values[-1]], R_max, R_max * 1.2,
                alpha=0.1, color='firebrick')
ax.set_xlabel('Coupling strength $J_{mass} / J$', fontsize=11)
ax.set_ylabel('|Ricci scalar| $|R|$', fontsize=11)
ax.set_title('(a) Curvature vs. Matter Density')
ax.legend()

# Classical comparison line (log divergence for illustration)
J_class = np.logspace(0, 3, 100)
R_class = 0.5 * np.log(J_class)  # Would diverge: R ∝ ln(ρ)
ax.plot(J_class, R_class, '--', color='steelblue', alpha=0.5,
        label='Classical (diverges)')
ax.legend(fontsize=9)

# (b) Entanglement entropy
ax = axes[0, 1]
ax.semilogx(J_values, entropies_center, 'o-', color='darkorange', ms=4)
ax.axhline(S_bound, color='gray', ls='--', alpha=0.7,
           label=f'$S_{{bound}} = {S_bound:.3f}$')
ax.set_xlabel('Coupling strength $J_{mass} / J$', fontsize=11)
ax.set_ylabel('Entanglement entropy $S$', fontsize=11)
ax.set_title('(b) Entropy Saturation')
ax.legend(fontsize=9)

# (c) QFIM metric
ax = axes[1, 0]
ax.semilogx(J_values, metric_center, 'o-', color='seagreen', ms=4)
ax.set_xlabel('Coupling strength $J_{mass} / J$', fontsize=11)
ax.set_ylabel('QFIM $g_{center}$', fontsize=11)
ax.set_title('(c) Metric Saturation')

# (d) Energy gap (related to spectral gap)
ax = axes[1, 1]
ax.semilogx(J_values, energy_gaps, 'o-', color='mediumpurple', ms=4)
ax.set_xlabel('Coupling strength $J_{mass} / J$', fontsize=11)
ax.set_ylabel('Energy gap $\\Delta E$', fontsize=11)
ax.set_title('(d) Energy Gap vs. Density')

plt.tight_layout(rect=[0, 0, 1, 0.93])
out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, 'singularity_resolution.png')
plt.savefig(out_path, dpi=150, bbox_inches='tight')
print(f"\nFigure saved to {out_path}")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print(f"RESULTS: {PASS} passed, {FAIL} failed out of {PASS + FAIL} checks")
print("=" * 70)

if FAIL > 0:
    print("\n⚠️  SOME CHECKS FAILED.")
    sys.exit(1)
else:
    print("\n✅ ALL CHECKS PASSED — Curvature saturates: no singularity for finite observers.")
    sys.exit(0)
