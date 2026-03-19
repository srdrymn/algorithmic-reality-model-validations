#!/usr/bin/env python3
"""
Generate publication-quality figures for the ATR Double-Slit paper.

Usage:
    python3 generate_figures.py

Outputs:
    fig1_interference_patterns.png  — Coherent vs Z-breached detection patterns
    fig2_entropy_growth.png         — Entanglement entropy growth with Z-Scale thresholds
    fig3_wavefunction_snapshot.png  — 2D |ψ|² snapshot during slit passage
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Import the simulation core
from simulate_double_slit import (
    NX, NY, DT, N_STEPS, J_HOP, K0, LAMBDA_DB,
    BARRIER_X, BAR_W, SLIT_W, SLIT_SEP, S1_CTR, S2_CTR, DET_X,
    X0, Y0, SIGMA_X, SIGMA_Y,
    build_potential, build_absorber, make_packet,
    build_kinetic_propagator, propagate, propagate_with_detector,
    norm_pat, truncate_born_rule,
)

import os
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Matplotlib styling ───────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'lines.linewidth': 1.5,
})


def run_simulation():
    """Run the full simulation and return all data needed for figures."""
    print("Running simulation...")
    Va = build_absorber()
    V_both = build_potential(True, True)
    fullT = build_kinetic_propagator()
    psi0 = make_packet()

    # Run A: coherent (no detector)
    print("  Run A: coherent propagation...")
    I_coh_raw, norms, psi_coh = propagate(psi0.copy(), V_both, Va, fullT)

    # Single-slit runs
    print("  Single-slit runs...")
    I_s1_raw, _, _ = propagate(psi0.copy(), build_potential(True, False), Va, fullT)
    I_s2_raw, _, _ = propagate(psi0.copy(), build_potential(False, True), Va, fullT)

    # Run B: with detector
    print("  Run B: which-path detector...")
    I_det_raw, S_trace, psi_d0, psi_d1 = propagate_with_detector(
        psi0.copy(), V_both, Va, fullT, coupling_strength=0.15
    )

    # Snapshots at several time steps for Figure 3
    print("  Snapshot run...")
    snapshots = {}
    snap_steps = [50, 120, 200, 350]  # before barrier, at barrier, after, at detector
    halfV = np.exp(-0.5j * V_both * DT - 0.5 * Va * DT)
    psi_snap = psi0.copy()
    for s in range(max(snap_steps) + 1):
        if s in snap_steps:
            snapshots[s] = np.abs(psi_snap)**2
        psi_snap *= halfV
        psi_snap = np.fft.ifft2(fullT * np.fft.fft2(psi_snap))
        psi_snap *= halfV

    # Born Rule truncation
    p0, p1 = truncate_born_rule(psi_d0, psi_d1)

    # Incoherent sum (= Z-breached pattern)
    I_inc_raw = I_s1_raw + I_s2_raw

    print("  Done.\n")
    return {
        'I_coh_raw': I_coh_raw,
        'I_s1_raw': I_s1_raw,
        'I_s2_raw': I_s2_raw,
        'I_inc_raw': I_inc_raw,
        'S_trace': S_trace,
        'snapshots': snapshots,
        'snap_steps': snap_steps,
        'V_both': V_both,
        'p0': p0, 'p1': p1,
    }


def fig1_interference_patterns(data):
    """Figure 1: Coherent vs Z-breached detection patterns."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    y = np.arange(NY)
    C = NY // 2

    # Normalize
    I_coh = data['I_coh_raw'] / data['I_coh_raw'].max()
    I_inc = data['I_inc_raw'] / data['I_inc_raw'].max()

    # Left panel: coherent pattern
    ax1.fill_betweenx(y, 0, I_coh, alpha=0.3, color='#2563EB')
    ax1.plot(I_coh, y, color='#1E40AF', linewidth=1.8, label='$|\\psi_1 + \\psi_2|^2$')
    ax1.set_xlabel('Normalized Intensity')
    ax1.set_ylabel('Detector position $y$ (lattice units)')
    ax1.set_title('(a) Coherent — No Z-Scale Breach\nInterference fringes', fontweight='bold')
    ax1.set_xlim(-0.02, 1.1)
    ax1.set_ylim(20, 125)
    ax1.legend(loc='upper right', framealpha=0.9)
    ax1.axhline(C, color='gray', linestyle=':', alpha=0.5, linewidth=0.8)

    # Right panel: Z-breached (incoherent)
    ax2.fill_betweenx(y, 0, I_inc, alpha=0.3, color='#DC2626')
    ax2.plot(I_inc, y, color='#991B1B', linewidth=1.8, label='$|\\psi_1|^2 + |\\psi_2|^2$')
    ax2.set_xlabel('Normalized Intensity')
    ax2.set_title('(b) Z-Scale Breached — Born Truncation\nFringes destroyed', fontweight='bold')
    ax2.set_xlim(-0.02, 1.1)
    ax2.legend(loc='upper right', framealpha=0.9)
    ax2.axhline(C, color='gray', linestyle=':', alpha=0.5, linewidth=0.8)

    fig.suptitle('Figure 1: The Z-Scale in the Double-Slit Experiment',
                 fontsize=15, fontweight='bold', y=1.02)

    path = os.path.join(OUT_DIR, 'fig1_interference_patterns.png')
    fig.savefig(path, facecolor='white', pad_inches=0.2)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def fig2_entropy_growth(data):
    """Figure 2: Entanglement entropy growth with Z-Scale thresholds."""
    fig, ax = plt.subplots(figsize=(10, 5.5))

    S = data['S_trace']
    steps = np.arange(len(S))
    S_max = math.log(2)

    # Main entropy curve
    ax.plot(steps, S, color='#2563EB', linewidth=2.0, label='$\\mathcal{S}(t)$',
            zorder=5)

    # Fill under the curve
    ax.fill_between(steps, 0, S, alpha=0.15, color='#2563EB')

    # Z-Scale threshold lines
    z_scales = [
        (0.10, '#EF4444', 'Strict $Z_\\alpha = 0.10$'),
        (0.30, '#F59E0B', 'Medium $Z_\\alpha = 0.30$'),
        (0.60, '#22C55E', 'Loose $Z_\\alpha = 0.60$'),
    ]
    for z_val, color, label in z_scales:
        ax.axhline(z_val, color=color, linestyle='--', linewidth=1.5,
                   alpha=0.8, label=label)
        # Find breach point
        breach_step = None
        for i, s in enumerate(S):
            if s >= z_val:
                breach_step = i
                break
        if breach_step is not None:
            ax.plot(breach_step, z_val, 'o', color=color, markersize=8,
                    zorder=10, markeredgecolor='white', markeredgewidth=1.5)
            ax.annotate(f'Breach\nstep {breach_step}',
                        xy=(breach_step, z_val),
                        xytext=(breach_step + 30, z_val + 0.03),
                        fontsize=8, color=color, fontweight='bold',
                        arrowprops=dict(arrowstyle='->', color=color,
                                        lw=1.2),
                        ha='left')

    # S_max line
    ax.axhline(S_max, color='#7C3AED', linestyle='-.', linewidth=1.5,
               alpha=0.6, label=f'$S_{{\\max}} = \\ln 2 \\approx {S_max:.3f}$')

    ax.set_xlabel('Time step')
    ax.set_ylabel('Entanglement entropy $\\mathcal{S}$ (nats)')
    ax.set_title('Figure 2: Entanglement Entropy Growth and Z-Scale Breach Points',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='center right', framealpha=0.95, fontsize=9)
    ax.set_xlim(0, len(S) - 1)
    ax.set_ylim(-0.02, S_max + 0.1)

    path = os.path.join(OUT_DIR, 'fig2_entropy_growth.png')
    fig.savefig(path, facecolor='white', pad_inches=0.2)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def fig3_wavefunction_snapshot(data):
    """Figure 3: 2D |ψ|² snapshots during slit passage."""
    snapshots = data['snapshots']
    snap_steps = data['snap_steps']
    V_both = data['V_both']

    n = len(snap_steps)
    fig, axes = plt.subplots(1, n, figsize=(3.5 * n, 5), sharey=True)

    titles = [
        f'(a) $t = {snap_steps[0]}$\nApproaching barrier',
        f'(b) $t = {snap_steps[1]}$\nAt the slits',
        f'(c) $t = {snap_steps[2]}$\nDiffraction + interference',
        f'(d) $t = {snap_steps[3]}$\nArrival at detector',
    ]

    for idx, (step, ax) in enumerate(zip(snap_steps, axes)):
        prob = snapshots[step].T  # transpose for (y, x) display

        # Log scale for visibility
        prob_plot = np.log10(prob + 1e-12)
        vmin = -6
        vmax = prob_plot.max()

        im = ax.imshow(prob_plot, aspect='auto', origin='lower',
                       extent=[0, NX, 0, NY],
                       cmap='inferno', vmin=vmin, vmax=vmax)

        # Barrier outline
        barrier_mask = (V_both > 1e3).T
        ax.contour(barrier_mask, levels=[0.5], colors='white',
                   linewidths=1.0, alpha=0.7,
                   extent=[0, NX, 0, NY])

        # Detector screen line
        ax.axvline(DET_X, color='cyan', linestyle='--', linewidth=0.8,
                   alpha=0.6)

        ax.set_title(titles[idx], fontsize=10, fontweight='bold')
        ax.set_xlabel('$x$ (lattice units)')
        if idx == 0:
            ax.set_ylabel('$y$ (lattice units)')

    fig.suptitle('Figure 3: Wave Packet Propagation Through Double Slit',
                 fontsize=14, fontweight='bold', y=1.02)

    # Colorbar
    cbar = fig.colorbar(im, ax=axes, shrink=0.85, pad=0.02,
                         label='$\\log_{10}|\\psi(x,y)|^2$')

    path = os.path.join(OUT_DIR, 'fig3_wavefunction_snapshot.png')
    fig.savefig(path, facecolor='white', pad_inches=0.2)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def main():
    print("=" * 60)
    print("  Generating publication figures for ATR Double-Slit paper")
    print("=" * 60)

    data = run_simulation()

    print("Generating figures...")
    p1 = fig1_interference_patterns(data)
    p2 = fig2_entropy_growth(data)
    p3 = fig3_wavefunction_snapshot(data)

    print(f"\n{'=' * 60}")
    print(f"  All figures generated successfully!")
    print(f"  {p1}")
    print(f"  {p2}")
    print(f"  {p3}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
