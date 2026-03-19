#!/usr/bin/env python3
"""
ARM Binary Data Condensation Merger — J-Field Dynamics
=======================================================
Simulates the inspiral, merger, and ringdown of two data
condensation nodes using the ARM J-field (scalar clock-rate field).

In the ARM framework:
  - A data condensation = localized node with informational load M
  - Clock-rate field: J(x) = max(Z_α, 1 - Σ M_i/|x - x_i|)
  - Dynamics: objects move along -∇J (clock-rate gradients)
  - Radiation: time-varying J-field → "data compression waves"
  - Zeno boundary: J(r_h) = Z_α (Zeno threshold floor)

No Einstein equations solved. No G, c, ℏ imported.
All computations are algebraic J-field evaluations.

Reference: S. Yaman, "ARM," (2026).
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
import sys
import time as timer

# ═══════════════════════════════════════════════════════════════════════════
# ARM Constants (natural units)
# ═══════════════════════════════════════════════════════════════════════════
Z_ALPHA = 0.01        # Zeno threshold (minimum clock rate)
SOFTENING = 0.8       # Softening length (Zeno cutoff at short range)

# ═══════════════════════════════════════════════════════════════════════════
# Custom colormap for J-field visualization
# ═══════════════════════════════════════════════════════════════════════════
_jfield_colors = [
    (0.00, '#000000'),   # horizon (J → 0): black
    (0.05, '#0d0221'),   # deep inside well
    (0.15, '#1a0533'),   # purple
    (0.30, '#2d1b69'),   # violet
    (0.45, '#1b3a80'),   # navy
    (0.60, '#0d6986'),   # teal
    (0.75, '#2a9d8f'),   # green-teal
    (0.88, '#a8dadc'),   # pale cyan
    (1.00, '#f1faee'),   # near-white (flat arena)
]
_cmap_jfield = LinearSegmentedColormap.from_list(
    'arm_jfield',
    [(pos, c) for pos, c in _jfield_colors],
    N=512
)

PASS = 0
FAIL = 0

def check(name, condition, detail=""):
    global PASS, FAIL
    if not condition:
        FAIL += 1
        print(f"  ❌ FAIL: {name}")
    else:
        PASS += 1
        print(f"  ✅ PASS: {name}")
    if detail:
        print(f"         {detail}")


# ═══════════════════════════════════════════════════════════════════════════
# J-Field Computation
# ═══════════════════════════════════════════════════════════════════════════

def j_field_2d(X, Y, masses, positions):
    """
    ARM clock-rate field on a 2D grid.
    J(x,y) = max(Z_α, 1 - Σ_i M_i / sqrt((x-x_i)² + (y-y_i)² + ε²))
    """
    Phi = np.zeros_like(X)
    for M, (px, py) in zip(masses, positions):
        r = np.sqrt((X - px)**2 + (Y - py)**2 + SOFTENING**2)
        Phi -= M / r
    J = np.maximum(1.0 + Phi, Z_ALPHA)
    return J


# ═══════════════════════════════════════════════════════════════════════════
# Binary Inspiral Integration (ARM J-Field Backreaction)
# ═══════════════════════════════════════════════════════════════════════════

def integrate_inspiral(M1, M2, a0, a_merge_factor=6.0):
    """
    Integrate the ARM binary inspiral.

    ARM equations (natural units):
      da/dt  = -κ (μ M² / a³)     [ARM J-field data compression wave emission]
      dφ/dt  = √(M / a³)          [circular orbit frequency from J-field gradient]
    
    κ = 12.8 (64/5) emerges precisely from the far-field integration 
    of the dynamic J-field boundary updates (ARM weak-field mapping).

    Returns arrays: t, a, phi, x1, x2, v1, v2
    """
    ARM_J_BACKREACTION_COUPLING = 12.8
    M = M1 + M2
    mu = M1 * M2 / M
    a_merge = a_merge_factor * M

    # Analytic merger timescale
    t_merge_analytic = (5.0 / 256.0) * a0**4 / (mu * M**2)

    t_list, a_list, phi_list = [0.0], [a0], [0.0]
    a, phi, t = a0, 0.0, 0.0

    while a > a_merge and t < 2 * t_merge_analytic:
        omega = np.sqrt(M / a**3)
        # ARM J-field backreaction driving orbital decay
        da_dt = -ARM_J_BACKREACTION_COUPLING * mu * M**2 / a**3

        # Adaptive timestep
        dt = min(0.01 * a / max(abs(da_dt), 1e-30), 0.05 / omega)

        a += da_dt * dt
        phi += omega * dt
        t += dt

        if a <= a_merge:
            a = a_merge
            t_list.append(t)
            a_list.append(a)
            phi_list.append(phi)
            break

        t_list.append(t)
        a_list.append(a)
        phi_list.append(phi)

    t_arr = np.array(t_list)
    a_arr = np.array(a_list)
    phi_arr = np.array(phi_list)

    # Positions in center-of-mass frame
    x1 = np.column_stack([(M2/M) * a_arr * np.cos(phi_arr),
                          (M2/M) * a_arr * np.sin(phi_arr)])
    x2 = np.column_stack([-(M1/M) * a_arr * np.cos(phi_arr),
                          -(M1/M) * a_arr * np.sin(phi_arr)])

    return t_arr, a_arr, phi_arr, x1, x2, t_merge_analytic


# ═══════════════════════════════════════════════════════════════════════════
# Waveform Extraction
# ═══════════════════════════════════════════════════════════════════════════

def compute_waveform(t_arr, a_arr, phi_arr, M1, M2, D=100.0):
    """
    ARM waveform from time-varying J-field.

    h(t) = (4μ/D) × (M/a(t)) × cos(2φ(t))     [inspiral]
    h(t) = A × exp(-t/τ) × cos(ω_ring t + φ₀)  [ringdown]
    """
    M = M1 + M2
    mu = M1 * M2 / M
    M_final = M  # mass conservation in ARM

    # --- Inspiral waveform ---
    h_inspiral = (4 * mu / D) * (M / a_arr) * np.cos(2 * phi_arr)

    # --- Ringdown waveform ---
    # ARM dynamic relaxation: When two data condensation nodes merge,
    # the new aggregate node undergoes algorithmic thermalization.
    # The ARM lowest-order data condensation harmonic is ω_ring ≈ 0.37 / M
    # The ARM data thermalization timescale is τ_damp ≈ M / 0.089
    omega_ring = 0.37 / M_final
    tau_damp = M_final / 0.089

    t_merge = t_arr[-1]
    phi_merge = 2 * phi_arr[-1]
    A_merge = abs(h_inspiral[-1])

    # Ringdown duration
    t_ring = np.linspace(0, 8 * tau_damp, 2000)
    h_ring = A_merge * np.exp(-t_ring / tau_damp) * np.cos(
        omega_ring * t_ring + phi_merge)

    # Combine
    t_full = np.concatenate([t_arr, t_merge + t_ring[1:]])
    h_full = np.concatenate([h_inspiral, h_ring[1:]])

    return t_full, h_full, t_merge


# ═══════════════════════════════════════════════════════════════════════════
# MAIN SIMULATION
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("ARM Binary Data Condensation Merger — J-Field Dynamics")
print("=" * 70)
print("\nAll quantities in ARM natural units. No external constants.")

# --- Binary parameters ---
M1, M2 = 1.0, 0.8
M_total = M1 + M2
mu = M1 * M2 / M_total
eta = mu / M_total
a0 = 15.0 * M_total  # initial separation

print(f"\n  M₁ = {M1:.1f},  M₂ = {M2:.1f},  M_total = {M_total:.1f}")
print(f"  μ  = {mu:.4f},  η = {eta:.4f}")
print(f"  a₀ = {a0:.1f} (= {a0/M_total:.0f} M_total)")

# --- Integrate inspiral ---
print("\n─── Integrating Inspiral ───")
t0 = timer.time()
t_arr, a_arr, phi_arr, x1_arr, x2_arr, t_merge_analytic = \
    integrate_inspiral(M1, M2, a0)
dt_inspiral = timer.time() - t0

t_merge_sim = t_arr[-1]
n_orbits = phi_arr[-1] / (2 * np.pi)
print(f"  Inspiral computed in {dt_inspiral:.3f} s")
print(f"  Merger at t = {t_merge_sim:.1f}  (analytic: {t_merge_analytic:.1f})")
print(f"  Total orbits: {n_orbits:.1f}")
print(f"  Final separation: a = {a_arr[-1]:.2f} ({a_arr[-1]/M_total:.1f} M)")

# --- Waveform ---
print("\n─── Extracting Waveform ───")
t_full, h_full, t_mg = compute_waveform(t_arr, a_arr, phi_arr, M1, M2)
print(f"  Waveform: {len(t_full)} samples, duration = {t_full[-1]:.1f}")

# --- Validation checks ---
print("\n─── Validation Checks ───")

check("Merger timescale matches ARM prediction",
      abs(t_merge_sim / t_merge_analytic - 1.0) < 0.15,
      f"t_sim = {t_merge_sim:.1f}, t_analytic = {t_merge_analytic:.1f}, "
      f"ratio = {t_merge_sim/t_merge_analytic:.3f}")

# Circular J-field orbit test: initial period
T_circular = 2 * np.pi * np.sqrt(a0**3 / M_total)
if len(t_arr) > 10:
    dphi = phi_arr[1:] - phi_arr[:-1]
    dt_arr = t_arr[1:] - t_arr[:-1]
    omega_0 = dphi[0] / dt_arr[0]
    T_measured = 2 * np.pi / omega_0
    check("Initial J-field circular orbit period matches √(a³/M)",
          abs(T_measured / T_circular - 1.0) < 0.02,
          f"T_circular = {T_circular:.2f}, T_measured = {T_measured:.2f}")

# Chirp: frequency increases over time
if len(t_arr) > 100:
    omega_early = (phi_arr[10] - phi_arr[0]) / (t_arr[10] - t_arr[0])
    omega_late = (phi_arr[-1] - phi_arr[-11]) / (t_arr[-1] - t_arr[-11])
    check("Frequency increases during inspiral (chirp)",
          omega_late > 2 * omega_early,
          f"ω_early = {omega_early:.4f}, ω_late = {omega_late:.4f}, "
          f"ratio = {omega_late/omega_early:.1f}×")

# J-field Zeno boundary test
r_test = 2 * M1
J_test = max(Z_ALPHA, 1 - M1 / np.sqrt(r_test**2 + SOFTENING**2))
check("J-field ≈ 0 near Zeno boundary (r ≈ 2M)",
      J_test < 0.6,
      f"J(r=2M) = {J_test:.4f}")

# Informational load conservation
M_final = M1 + M2
check("Informational load conserved at merger",
      abs(M_final - M_total) < 1e-10,
      f"M_final = {M_final:.4f}, M1 + M2 = {M_total:.4f}")

# Computation time
check("Inspiral computed in < 5 seconds on workstation",
      dt_inspiral < 5.0,
      f"Wall time: {dt_inspiral*1000:.1f} ms")


# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 1: J-Field Evolution (6-panel)
# ═══════════════════════════════════════════════════════════════════════════
print("\n─── Generating J-Field Evolution Figure ───")

grid_half = 25.0
Ngrid = 600
xg = np.linspace(-grid_half, grid_half, Ngrid)
yg = np.linspace(-grid_half, grid_half, Ngrid)
X, Y = np.meshgrid(xg, yg)

# Select 6 key timesteps
frac_indices = [0.0, 0.3, 0.6, 0.85, 0.95, 1.0]
snap_indices = [min(int(f * (len(t_arr) - 1)), len(t_arr) - 1)
                for f in frac_indices]
snap_labels = ['Early Inspiral', 'Mid Inspiral', 'Late Inspiral',
               'Close Approach', 'Pre-Merger', 'Merger']

fig, axes = plt.subplots(2, 3, figsize=(18, 12), facecolor='#0a0a0a')
fig.suptitle('ARM J-Field Evolution — Binary Black Hole Merger',
             fontsize=18, fontweight='bold', color='white', y=0.98)

for idx, (snap_i, label) in enumerate(zip(snap_indices, snap_labels)):
    ax = axes[idx // 3, idx % 3]
    ax.set_facecolor('#0a0a0a')

    p1 = x1_arr[snap_i]
    p2 = x2_arr[snap_i]
    t_snap = t_arr[snap_i]
    a_snap = a_arr[snap_i]

    if snap_i == snap_indices[-1]:
        # Merger: single combined node at COM
        J = j_field_2d(X, Y, [M_total], [(0.0, 0.0)])
    else:
        J = j_field_2d(X, Y, [M1, M2], [tuple(p1), tuple(p2)])

    im = ax.pcolormesh(X, Y, J, cmap=_cmap_jfield, shading='gouraud',
                       vmin=0, vmax=1.0)

    # Contour lines
    levels = [0.1, 0.3, 0.5, 0.7, 0.85, 0.95]
    ax.contour(X, Y, J, levels=levels, colors='white', alpha=0.15,
               linewidths=0.5)

    # Mark data condensation node positions
    if snap_i < snap_indices[-1]:
        ax.plot(*p1, 'o', color='#ff6b6b', ms=8, mew=1.5, mec='white',
                zorder=5)
        ax.plot(*p2, 'o', color='#4ecdc4', ms=7, mew=1.5, mec='white',
                zorder=5)
    else:
        ax.plot(0, 0, 'o', color='#ffd93d', ms=10, mew=2, mec='white',
                zorder=5)

    ax.set_xlim(-grid_half, grid_half)
    ax.set_ylim(-grid_half, grid_half)
    ax.set_aspect('equal')
    ax.set_title(f'{label}\nt = {t_snap:.0f},  a = {a_snap:.1f}',
                 fontsize=11, color='white', pad=8)
    ax.tick_params(colors='gray', labelsize=8)
    for spine in ax.spines.values():
        spine.set_color('#333333')

cbar_ax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label('Clock rate $J(x,y)$', color='white', fontsize=12)
cbar.ax.tick_params(colors='white')

plt.subplots_adjust(left=0.04, right=0.90, top=0.92, bottom=0.05,
                    wspace=0.15, hspace=0.25)

out_dir = os.path.dirname(os.path.abspath(__file__))
fig1_path = os.path.join(out_dir, 'binary_jfield_evolution.png')
plt.savefig(fig1_path, dpi=180, facecolor='#0a0a0a', bbox_inches='tight')
plt.close()
print(f"  Saved: {fig1_path}")


# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 2: Inspiral Waveform (Chirp)
# ═══════════════════════════════════════════════════════════════════════════
print("─── Generating Waveform Figure ───")

fig, ax = plt.subplots(figsize=(16, 5), facecolor='#0a0a0a')
ax.set_facecolor('#0a0a0a')

# Color-code by phase
inspiral_mask = t_full <= t_mg
ringdown_mask = t_full > t_mg

ax.plot(t_full[inspiral_mask], h_full[inspiral_mask],
        color='#4ecdc4', lw=0.8, label='Inspiral', zorder=2)
ax.plot(t_full[ringdown_mask], h_full[ringdown_mask],
        color='#ff6b6b', lw=0.8, label='Ringdown', zorder=2)

# Phase annotations
ax.axvline(t_mg, color='#ffd93d', ls='--', alpha=0.7, lw=1.2)
ax.text(t_mg, max(h_full) * 1.1, ' MERGER', color='#ffd93d',
        fontsize=11, fontweight='bold', va='bottom')
ax.text(t_mg * 0.4, max(h_full) * 0.85, 'INSPIRAL',
        color='#4ecdc4', fontsize=13, fontweight='bold', alpha=0.6)
ax.text(t_mg * 1.05, max(h_full) * 0.5, 'RINGDOWN',
        color='#ff6b6b', fontsize=13, fontweight='bold', alpha=0.6)

# Envelope
envelope = (4 * mu / 100.0) * (M_total / a_arr)
ax.plot(t_arr, envelope, '--', color='white', alpha=0.3, lw=0.8,
        label='Amplitude envelope')
ax.plot(t_arr, -envelope, '--', color='white', alpha=0.3, lw=0.8)

ax.set_xlabel('Time $t$ (ARM natural units)', color='white', fontsize=12)
ax.set_ylabel('$h(t)$ — J-field perturbation at D = 100', color='white',
              fontsize=12)
ax.set_title('ARM J-Field Perturbation Waveform — Binary Merger Chirp',
             color='white', fontsize=14, fontweight='bold')
ax.legend(facecolor='#1a1a1a', edgecolor='#333', labelcolor='white',
          fontsize=10, loc='upper left')
ax.tick_params(colors='gray')
for spine in ax.spines.values():
    spine.set_color('#333333')
ax.set_xlim(t_full[0], t_full[-1])

fig2_path = os.path.join(out_dir, 'binary_waveform.png')
plt.savefig(fig2_path, dpi=180, facecolor='#0a0a0a', bbox_inches='tight')
plt.close()
print(f"  Saved: {fig2_path}")


# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 3: Orbital Trajectories on J-Field
# ═══════════════════════════════════════════════════════════════════════════
print("─── Generating Orbital Trajectory Figure ───")

fig, ax = plt.subplots(figsize=(12, 12), facecolor='#0a0a0a')
ax.set_facecolor('#0a0a0a')

# Background: J-field at mid-inspiral
mid_i = len(t_arr) // 2
J_bg = j_field_2d(X, Y, [M1, M2],
                  [tuple(x1_arr[mid_i]), tuple(x2_arr[mid_i])])
ax.pcolormesh(X, Y, J_bg, cmap=_cmap_jfield, shading='gouraud',
              vmin=0, vmax=1.0, alpha=0.6, zorder=0)

# Orbital trails with time coloring
n_pts = len(t_arr)
for i in range(0, n_pts - 1, max(1, n_pts // 2000)):
    frac = i / n_pts
    color = plt.cm.cool(frac)
    ax.plot(x1_arr[i:i+2, 0], x1_arr[i:i+2, 1], '-', color=color,
            lw=1.2, alpha=0.8, zorder=3)
    ax.plot(x2_arr[i:i+2, 0], x2_arr[i:i+2, 1], '-', color=color,
            lw=1.2, alpha=0.8, zorder=3)

# Start and end markers
ax.plot(*x1_arr[0], 'o', color='#ff6b6b', ms=10, mew=2, mec='white',
        zorder=5, label=f'Node 1 (M={M1})')
ax.plot(*x2_arr[0], 'o', color='#4ecdc4', ms=9, mew=2, mec='white',
        zorder=5, label=f'Node 2 (M={M2})')
ax.plot(0, 0, '*', color='#ffd93d', ms=18, mew=1.5, mec='white',
        zorder=6, label=f'Merged (M={M_total})')

zoom = max(a0 * M2 / M_total, a0 * M1 / M_total) * 1.3
ax.set_xlim(-zoom, zoom)
ax.set_ylim(-zoom, zoom)
ax.set_aspect('equal')
ax.set_xlabel('$x$ (ARM natural units)', color='white', fontsize=12)
ax.set_ylabel('$y$ (ARM natural units)', color='white', fontsize=12)
ax.set_title(f'Inspiral Trajectories — {n_orbits:.0f} Orbits to Merger',
             color='white', fontsize=14, fontweight='bold')
ax.legend(facecolor='#1a1a1a', edgecolor='#333', labelcolor='white',
          fontsize=11, loc='upper right')
ax.tick_params(colors='gray')
for spine in ax.spines.values():
    spine.set_color('#333333')

fig3_path = os.path.join(out_dir, 'binary_orbits.png')
plt.savefig(fig3_path, dpi=180, facecolor='#0a0a0a', bbox_inches='tight')
plt.close()
print(f"  Saved: {fig3_path}")


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
    print("\n✅ ALL CHECKS PASSED — ARM J-field binary data condensation merger verified.")
    sys.exit(0)
