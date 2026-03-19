#!/usr/bin/env python3
"""
Prediction 9.4 — Sub-Tick Correlation Plateaus
===============================================
Computational validation for:
  S. Yaman, "The Algorithmic Theory of Reality: Rigorous Mathematical
  Foundations," (2026), §9.2–9.3.

Theory
------
ATR Prediction 9.4 states that an observer with discrete clock frequency
ν_α produces a step-like correlation function C_ATR(Δt), constant within
each tick interval [n/ν_α, (n+1)/ν_α), rather than the smooth decay
predicted by standard quantum mechanics.

Model Hamiltonian (ATR §9.3.1)
------------------------------
Single transmon qubit:
    Ĥ_S = (ω/2) σ_z,   ω/2π = 5.0 GHz
Dephasing Lindblad channel:
    L = √(Γ/2) σ_z,     Γ = 1/T₂,  T₂ = 20 ns
Observable: σ_x (sensitive to off-diagonal coherence).

Standard QM correlation (ATR §9.3.2):
    C_QM(Δt) = exp(−Γ|Δt|) cos(ω Δt)

ATR prediction (ATR §9.3.2):
    C_ATR(Δt) = C_QM( ⌊Δt · ν_α⌋ / ν_α )
i.e. the correlator is frozen at the tick-boundary value within each
inter-tick interval.

Noise model (ATR §9.3.3):
    1. Shot noise: σ_shot = 1/√N,  N = 10,000 shots per delay point.
    2. Clock jitter: Gaussian timing jitter σ_jitter = 50 ps (5% of T_tick).

Statistical analysis
--------------------
We report both RMS-based and peak-based signal-to-noise ratios:
    SNR_RMS  = √⟨ΔC²⟩ / σ_shot     (average detectability, standard χ² metric)
    SNR_peak = max|ΔC| / σ_shot      (best single-point detectability)

The RMS metric is the scientifically preferred measure because it is not
inflated by the look-elsewhere effect over ~13,000 time bins.

Output
------
    prediction_94_simulation.png — Three-panel figure (Fig. 1 of ATR §9.3.4)

License: MIT (see LICENSE in repository root)
"""

import numpy as np
import matplotlib.pyplot as plt

# ═══════════════════════════════════════════════════════════════════════════
# Physical parameters (ATR §9.3.1)
# ═══════════════════════════════════════════════════════════════════════════
OMEGA = 2 * np.pi * 5.0e9       # qubit angular frequency [rad/s]
T2 = 20e-9                       # coherence time [s]
GAMMA = 1.0 / T2                  # dephasing rate [1/s]
NU_ALPHA = 1.0e9                  # ATR clock frequency [Hz]
T_TICK = 1.0 / NU_ALPHA           # tick period = 1 ns
SIGMA_JITTER = 50e-12             # clock jitter RMS [s]
N_SHOTS = 10_000                  # measurement repetitions per delay point
SIGMA_SHOT = 1.0 / np.sqrt(N_SHOTS)  # shot noise std

# ═══════════════════════════════════════════════════════════════════════════
# Time grid
# ═══════════════════════════════════════════════════════════════════════════
T_MAX = 6.5e-9       # total time window [s]
DT_FINE = 0.5e-12    # fine grid step (0.5 ps) for smooth curves
DT_DATA = 50e-12     # simulated data sampling interval (50 ps)

t_fine = np.arange(0, T_MAX, DT_FINE)
t_data = np.arange(0, T_MAX, DT_DATA)


def C_QM(t):
    """Standard QM σ_x two-point correlator under Lindblad dephasing."""
    return np.exp(-GAMMA * np.abs(t)) * np.cos(OMEGA * t)


def C_ATR_ideal(t):
    """Ideal ATR correlator: snap time to tick boundary."""
    t_snap = np.floor(t / T_TICK) * T_TICK
    return C_QM(t_snap)


def C_ATR_realistic(t_arr, rng, n_jitter_samples=N_SHOTS):
    """
    Realistic ATR correlator with Gaussian clock jitter.

    For each nominal delay t, we draw n_jitter_samples from
    N(t, σ_jitter²), snap each to its tick boundary, evaluate C_QM
    at the snapped time, and average.  This Monte Carlo convolution
    produces soft sigmoid transitions at tick boundaries.
    """
    out = np.empty_like(t_arr)
    for i, ti in enumerate(t_arr):
        t_jittered = ti + rng.normal(0, SIGMA_JITTER, n_jitter_samples)
        t_jittered = np.clip(t_jittered, 0, T_MAX - DT_FINE)
        t_snap = np.floor(t_jittered / T_TICK) * T_TICK
        out[i] = np.mean(C_QM(t_snap))
    return out


# ═══════════════════════════════════════════════════════════════════════════
# Compute signals
# ═══════════════════════════════════════════════════════════════════════════
rng = np.random.default_rng(42)

c_qm_fine = C_QM(t_fine)
c_ideal_fine = C_ATR_ideal(t_fine)

# Realistic ATR on a coarse grid, then interpolate to fine grid
t_coarse = np.arange(0, T_MAX, 5e-12)   # 5 ps steps (adequate for 50 ps jitter)
c_realistic_coarse = C_ATR_realistic(t_coarse, rng)
c_realistic_fine = np.interp(t_fine, t_coarse, c_realistic_coarse)

# Simulated experimental data points
c_data = np.interp(t_data, t_coarse, c_realistic_coarse)
c_data_noisy = c_data + rng.normal(0, SIGMA_SHOT, len(t_data))

# ═══════════════════════════════════════════════════════════════════════════
# Statistical analysis
# ═══════════════════════════════════════════════════════════════════════════
delta_C = c_realistic_fine - c_qm_fine
rms_raw = np.sqrt(np.mean(delta_C**2))
max_raw = np.max(np.abs(delta_C))

snr_rms = rms_raw / SIGMA_SHOT
snr_peak = max_raw / SIGMA_SHOT

# Formal χ² test: would a smooth-QM fit be rejected?
# Under H₀ (smooth QM), each ΔC/σ is ≈ N(0,1). χ² = Σ(ΔC/σ)² ~ χ²(n).
n_data = len(t_data)
c_data_qm = C_QM(t_data)
chi2_per_dof = np.sum(((c_data_noisy - c_data_qm) / SIGMA_SHOT)**2) / n_data

print("=" * 60)
print("Prediction 9.4 — Sub-Tick Correlation Plateaus")
print("=" * 60)
print(f"  ω/2π          = {OMEGA / (2*np.pi) / 1e9:.1f} GHz")
print(f"  T₂            = {T2*1e9:.0f} ns")
print(f"  ν_α           = {NU_ALPHA/1e9:.1f} GHz")
print(f"  σ_jitter      = {SIGMA_JITTER*1e12:.0f} ps")
print(f"  N_shots        = {N_SHOTS:,}")
print(f"  σ_shot         = {SIGMA_SHOT:.4f}")
print("-" * 60)
print(f"  RMS deviation  = {rms_raw:.4f}")
print(f"  Peak deviation = {max_raw:.4f}")
print(f"  SNR (RMS)      = {snr_rms:.0f}σ")
print(f"  SNR (peak)     = {snr_peak:.0f}σ")
print(f"  χ²/dof (H₀: smooth QM) = {chi2_per_dof:.1f}")
print("=" * 60)

# ═══════════════════════════════════════════════════════════════════════════
# Figure (ATR §9.3.4, Figure 1)
# ═══════════════════════════════════════════════════════════════════════════
tick_positions = np.arange(0, T_MAX, T_TICK)
t_ns = t_fine * 1e9

fig, axes = plt.subplots(3, 1, figsize=(10, 11),
                         gridspec_kw={'height_ratios': [2, 2, 1.2]})
fig.suptitle(
    'Prediction 9.4: Sub-Tick Correlation Plateaus\n'
    r'Transmon qubit: $\omega/2\pi = 5.0$ GHz, '
    r'$T_2 = 20$ ns, $\nu_\alpha = 1.0$ GHz',
    fontsize=13, fontweight='bold')

# ── Panel (a): Full comparison ───────────────────────────────────────────
ax = axes[0]
ax.plot(t_ns, c_qm_fine, color='steelblue', lw=1.2,
        label=r'Standard QM: $C(\Delta t)=e^{-\Gamma\Delta t}\cos(\omega\Delta t)$')
ax.plot(t_ns, c_ideal_fine, color='lightgray', lw=0.8,
        label='ATR ideal (sharp ticks)', zorder=2)
ax.plot(t_ns, c_realistic_fine, color='firebrick', lw=2.0,
        label=r'ATR ($\nu_\alpha = 1$ GHz, $\sigma_{\rm jitter} = 50$ ps)',
        zorder=3)
for tk in tick_positions:
    ax.axvline(tk * 1e9, color='gray', lw=0.5, ls=':', alpha=0.7)
for i, tk in enumerate(tick_positions[:4]):
    ax.text(tk * 1e9 + 0.05, 1.07, f'tick {i}', fontsize=8, color='gray',
            transform=ax.get_xaxis_transform())
ax.set_ylabel(r'$C(\Delta t) = \langle\sigma_x(0)\sigma_x(\Delta t)\rangle$',
              fontsize=11)
ax.set_xlim(0, T_MAX * 1e9)
ax.set_ylim(-1.15, 1.15)
ax.legend(loc='upper right', fontsize=8.5)
ax.tick_params(labelbottom=False)
ax.grid(False)

# ── Panel (b): Smoothed comparison + data ────────────────────────────────
ax = axes[1]
ax.plot(t_ns, c_qm_fine, color='steelblue', lw=1.5, label='Standard QM')
ax.plot(t_ns, c_realistic_fine, color='firebrick', lw=2.0,
        label='ATR (realistic)', zorder=3)
ax.errorbar(t_data * 1e9, c_data_noisy,
            yerr=2 * SIGMA_SHOT, fmt='o', color='firebrick',
            ms=2.5, elinewidth=0.8, capsize=1.5, alpha=0.6,
            label=f'Simulated data ($N = {N_SHOTS:,}$ shots)', zorder=4)
for tk in tick_positions:
    ax.axvline(tk * 1e9, color='gray', lw=0.5, ls=':', alpha=0.7)
ax.annotate('', xy=(tick_positions[2] * 1e9, -0.85),
            xytext=(tick_positions[1] * 1e9, -0.85),
            arrowprops=dict(arrowstyle='<->', color='firebrick', lw=1.5))
ax.text((tick_positions[1] + tick_positions[2]) * 0.5e9, -0.92,
        r'$T_{\rm tick} = 1/\nu_\alpha = 1$ ns',
        ha='center', color='firebrick', fontsize=9)
ax.set_ylabel(r'$C(\Delta t)$', fontsize=11)
ax.set_xlim(0, T_MAX * 1e9)
ax.set_ylim(-1.15, 1.05)
ax.legend(loc='upper right', fontsize=8.5)
ax.tick_params(labelbottom=False)
ax.grid(False)

# ── Panel (c): Residuals ─────────────────────────────────────────────────
ax = axes[2]
ax.axhspan(-2 * SIGMA_SHOT, 2 * SIGMA_SHOT, color='steelblue', alpha=0.2,
           label=r'$\pm 2\sigma$ shot noise ($N = 10^4$)')
ax.plot(t_ns, delta_C, color='firebrick', lw=1.0,
        label=r'$\Delta C = C_{\rm ATR} - C_{\rm QM}$')
ax.axhline(0, color='k', lw=0.5)
for tk in tick_positions:
    ax.axvline(tk * 1e9, color='gray', lw=0.5, ls=':', alpha=0.7)

stats_text = (
    f'RMS deviation: {rms_raw:.3f}\n'
    f'Max deviation: {max_raw:.3f}\n'
    f'Shot noise (1σ): {SIGMA_SHOT:.3f}\n'
    f'SNR (RMS): {snr_rms:.0f}σ\n'
    f'SNR (peak): {snr_peak:.0f}σ'
)
ax.text(0.02, 0.97, stats_text, transform=ax.transAxes,
        fontsize=8, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
ax.legend(loc='upper right', fontsize=8.5)
ax.set_xlabel(r'Delay $\Delta t$ (ns)', fontsize=11)
ax.set_ylabel(r'$\Delta C(\Delta t)$', fontsize=11)
ax.set_xlim(0, T_MAX * 1e9)
ax.set_ylim(-0.35, 0.35)
ax.grid(False)

plt.tight_layout(rect=[0, 0, 1, 0.96])

import os
out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, 'prediction_94_simulation.png')
plt.savefig(out_path, dpi=150, bbox_inches='tight')
print(f'\nFigure saved to {out_path}')
plt.close()
