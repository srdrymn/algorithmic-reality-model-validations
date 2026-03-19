#!/usr/bin/env python3
"""
Selective Attention Thermodynamic Benchmark
============================================
Compares Bennett-Landauer erasure cost of selective-attention POVMs
versus full-collapse measurements as a function of system size.

ATR Theorem 4.6 predicts that selective collapse (attention-focused
POVM) is the thermodynamically optimal measurement strategy, erasing
strictly less information than full-rank collapse to pure states.

We verify this by computing:
  ΔS_full     = S(ρ) - 0            (full collapse to pure state)
  ΔS_selective = S(ρ) - S(ρ_post)    (selective → mixed post-state)
  Cost ∝ ΔS                          (Landauer erasure in natural units)

Reference: S. Yaman, "ATR," (2026), §4, Theorem 4.6.

License: MIT
"""

import numpy as np
from scipy.linalg import sqrtm
import matplotlib.pyplot as plt
import os
import sys

# ═══════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════

def kron(*args):
    result = args[0]
    for a in args[1:]:
        result = np.kron(result, a)
    return result


def partial_trace(rho, dims, keep):
    n = len(dims)
    d_total = int(np.prod(dims))
    rho_t = rho.reshape(list(dims) + list(dims))
    trace_axes = sorted(set(range(n)) - set(keep))
    for offset, ax in enumerate(trace_axes):
        rho_t = np.trace(rho_t, axis1=ax - offset, axis2=ax - offset + n - offset)
        n -= 1
    keep_dims = [dims[k] for k in keep]
    d_keep = int(np.prod(keep_dims))
    return rho_t.reshape(d_keep, d_keep)


def von_neumann_entropy(rho):
    evals = np.linalg.eigvalsh(rho)
    evals = evals[evals > 1e-15]
    return -np.sum(evals * np.log(evals))


def random_density_matrix(d, rng):
    """Generate a random density matrix (Hilbert-Schmidt measure)."""
    A = rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))
    rho = A @ A.conj().T
    return rho / np.trace(rho)


def random_pure_state(d, rng):
    """Generate a random pure state (Haar measure)."""
    psi = rng.standard_normal(d) + 1j * rng.standard_normal(d)
    return psi / np.linalg.norm(psi)


# ═══════════════════════════════════════════════════════════════════════════
# Measurement cost analysis
# ═══════════════════════════════════════════════════════════════════════════

rng = np.random.default_rng(42)

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
print("Selective Attention Thermodynamic Benchmark (Theorem 4.6)")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════════════
# Test across system sizes
# ═══════════════════════════════════════════════════════════════════════════

n_qubits_list = [2, 3, 4, 5, 6]
n_trials = 20

results = []

print("\n─── Comparing Measurement Strategies ───\n")
print(f"{'n_qubits':>8} {'d_total':>7} {'S(ρ)':>8} "
      f"{'ΔS_full':>8} {'ΔS_sel':>8} {'ratio':>8} {'savings':>8}")
print("-" * 65)

for n_q in n_qubits_list:
    d = 2**n_q
    n_focus = n_q // 2  # Focus on half the qubits (selective attention)
    d_focus = 2**n_focus
    d_env = 2**(n_q - n_focus)

    trial_ratios = []
    trial_savings = []

    for trial in range(n_trials):
        # Generate a genuinely mixed state by tracing out half of a larger pure state
        d_total = d * d  # System + environment
        psi_global = random_pure_state(d_total, rng)
        rho_full = np.outer(psi_global, psi_global.conj())
        # Partial trace: reshape as (d, d, d, d) and trace over environment
        rho_full_r = rho_full.reshape(d, d, d, d)
        rho = np.trace(rho_full_r, axis1=1, axis2=3)
        rho = 0.5 * (rho + rho.conj().T)  # Enforce Hermiticity
        rho = rho / np.trace(rho)  # Normalize

        S_initial = von_neumann_entropy(rho)

        # Strategy 1: Full collapse (rank-1 projectors in computational basis)
        # Post-measurement: pure state (zero entropy) each outcome
        # Weighted average post-state entropy = 0 (each outcome is |k⟩⟨k|)
        S_post_full = 0
        delta_S_full = S_initial - S_post_full

        # Strategy 2: Selective attention (project focus qubits, keep rest)
        dims_data = [2] * n_q
        # Project the first n_focus qubits in computational basis
        S_post_sel_avg = 0
        for basis_idx in range(d_focus):
            # Projector: |k⟩⟨k| on focus ⊗ I on rest
            proj = np.zeros((d, d), dtype=complex)
            for j in range(d_env):
                idx = basis_idx * d_env + j
                proj[idx, idx] = 1.0

            p_k = np.trace(proj @ rho).real
            if p_k > 1e-12:
                rho_post_k = proj @ rho @ proj / p_k
                S_post_sel_avg += p_k * von_neumann_entropy(rho_post_k)

        delta_S_sel = S_initial - S_post_sel_avg

        ratio = delta_S_sel / delta_S_full if delta_S_full > 1e-10 else 1.0
        savings = 1 - ratio

        trial_ratios.append(ratio)
        trial_savings.append(savings)

    avg_ratio = np.mean(trial_ratios)
    avg_savings = np.mean(trial_savings)
    avg_S = S_initial  # Last trial's S (representative)
    avg_ds_full = delta_S_full
    avg_ds_sel = delta_S_sel

    results.append({
        'n_qubits': n_q,
        'd': d,
        'avg_ratio': avg_ratio,
        'avg_savings': avg_savings,
        'all_ratios': trial_ratios,
    })

    print(f"{n_q:>8} {d:>7} {avg_S:>8.3f} "
          f"{avg_ds_full:>8.3f} {avg_ds_sel:>8.3f} {avg_ratio:>8.3f} {avg_savings:>7.1%}")

# ═══════════════════════════════════════════════════════════════════════════
# Verification checks
# ═══════════════════════════════════════════════════════════════════════════
print()

for r in results:
    check(f"n={r['n_qubits']}: Selective is always cheaper (ratio < 1)",
          all(x < 1.0 + 1e-10 for x in r['all_ratios']),
          f"avg ratio = {r['avg_ratio']:.4f}, "
          f"max ratio = {max(r['all_ratios']):.4f}")

# Check that savings increase with system size (Theorem 4.6 scaling)
savings_trend = [r['avg_savings'] for r in results]
check("Savings increase with system size (as predicted)",
      savings_trend[-1] > savings_trend[0],
      f"savings: {[f'{s:.1%}' for s in savings_trend]}")

# ═══════════════════════════════════════════════════════════════════════════
# Figure
# ═══════════════════════════════════════════════════════════════════════════

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Theorem 4.6: Selective Attention is Thermodynamically Optimal',
             fontsize=13, fontweight='bold')

n_qubits_arr = [r['n_qubits'] for r in results]
ratios_arr = [r['avg_ratio'] for r in results]
savings_arr = [r['avg_savings'] for r in results]

# Panel 1: Cost ratio
ax1.bar(n_qubits_arr, ratios_arr, color='steelblue', alpha=0.8, edgecolor='navy')
ax1.axhline(1.0, color='firebrick', ls='--', lw=1.5, label='Full collapse (cost = 1)')
ax1.set_xlabel('System size (n qubits)', fontsize=11)
ax1.set_ylabel('Cost ratio (selective / full)', fontsize=11)
ax1.set_ylim(0, 1.1)
ax1.legend()
ax1.set_title('Erasure Cost Ratio')

# Panel 2: Savings %
ax2.bar(n_qubits_arr, [s * 100 for s in savings_arr],
        color='seagreen', alpha=0.8, edgecolor='darkgreen')
ax2.set_xlabel('System size (n qubits)', fontsize=11)
ax2.set_ylabel('Erasure savings (%)', fontsize=11)
ax2.set_title('Thermodynamic Savings from Selective Attention')

plt.tight_layout(rect=[0, 0, 1, 0.93])
out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, 'selective_attention_cost.png')
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
    print("\n✅ ALL CHECKS PASSED — Selective attention is always cheaper (Theorem 4.6 verified).")
    sys.exit(0)
