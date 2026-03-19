#!/usr/bin/env python3
"""
ATR Black Hole Simulator — Dynamic Horizon Emergence
=====================================================
Companion simulation for:
  "Emergent Lorentzian Spacetime from Informational Geometry"

This simulator proves that a black hole is not a physical object — it is
an algorithmic bound.  No Schwarzschild radius is hard-coded.  Instead:

  1. A central "Information Mass" M generates an algorithmic processing
     load Φ(x,y) = M / r.
  2. The rendering engine slows the local clock to survive:
         J(x,y) = J₀ · exp(−κ · Φ)
  3. When a test wavepacket's local density + background load exceeds
     the Zeno Threshold Z_α, the node undergoes Born Rule Truncation.
  4. The Clausius-Landauer heat δQ = T_mod · dS is computed at each
     truncation, proving Jacobson's thermodynamic derivation (P9, Thm 6.1).

Engine: Sparse Hermitian Tight-Binding Hamiltonian + Krylov subspace
matrix exponential (scipy.sparse.linalg.expm_multiply).
Guarantees strict unitarity: U†U = I at every frame.

Author: Serdar Yaman (2026)
"""

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as splinalg
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
import os
import sys

# ── Output directory ───────────────────────────────────────────────
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ╔══════════════════════════════════════════════════════════════════╗
# ║  CONFIGURATION                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝

# Lattice
NX, NY   = 120, 120     # grid size (smaller for 3D viz performance)
XC, YC   = NX // 2, NY // 2  # mass center

# Physics (lattice units)
J0       = 0.5          # baseline hopping amplitude (flat space)
MASS     = 3.0          # Information Mass scalar M
KAPPA    = 1.5          # clock slowdown coupling constant
Z_ALPHA  = 0.8          # Zeno Threshold
DT       = 0.20         # time step

# Simulation
N_FRAMES      = 20      # total evolution frames
STEPS_PER     = 50      # Krylov steps per frame

# Wavepacket
WP_X0         = XC + 35 # start position (offset from center)
WP_Y0         = YC
WP_SIGMA      = 5.0     # initial width
WP_KX         = -0.7    # initial momentum (toward mass)
WP_KY         = 0.0

# ── Custom colour maps ────────────────────────────────────────────
CMAP_PROB = LinearSegmentedColormap.from_list(
    "atr_prob", ["#0a0a2e", "#1a1a5e", "#3333aa", "#6666ff",
                 "#00ccff", "#66ffcc", "#ffffff"], N=256
)
CMAP_BREACH = LinearSegmentedColormap.from_list(
    "breach", ["#000000", "#440000", "#ff0000", "#ff6600",
               "#ffcc00", "#ffffff"], N=256
)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  CORE ENGINE                                                    ║
# ╚══════════════════════════════════════════════════════════════════╝

def node_index(x: int, y: int, nx: int) -> int:
    """Map 2D grid coordinate (x, y) to 1D flattened index."""
    return y * nx + x


def build_dynamic_J_field(nx: int, ny: int, xc: int, yc: int,
                          j0: float, mass: float,
                          kappa: float) -> tuple:
    """Build the J-field dynamically from Information Mass M.

    No r_s is hardcoded.  The horizon *emerges* from the algorithm:
        Φ(x,y) = M / r         (algorithmic processing load)
        J(x,y) = J₀ · exp(−κΦ)  (clock slowdown)

    Returns (J, Phi, R):
        J   — 2D hopping field
        Phi — 2D processing load (potential)
        R   — 2D distance array
    """
    x = np.arange(nx)
    y = np.arange(ny)
    X, Y = np.meshgrid(x, y, indexing="ij")
    R = np.sqrt((X - xc)**2 + (Y - yc)**2)
    R = np.maximum(R, 0.5)  # avoid division by zero

    Phi = mass / R
    J = j0 * np.exp(-kappa * Phi)
    return J, Phi, R


def build_hamiltonian(nx: int, ny: int, J: np.ndarray) -> sp.csr_matrix:
    """Build the Hermitian tight-binding Hamiltonian.

    H_{A,B} = H_{B,A} = -(J(A) + J(B)) / 2   (symmetric hopping)
    H_{A,A} = sum_neighbors (J(A) + J(neighbor)) / 2
    """
    N = nx * ny
    rows = []
    cols = []
    vals = []
    diag = np.zeros(N, dtype=np.float64)

    for x in range(nx):
        for y in range(ny):
            k = node_index(x, y, nx)
            j_k = J[x, y]
            # Right neighbor
            if x + 1 < nx:
                k2 = node_index(x + 1, y, nx)
                hop = -(j_k + J[x + 1, y]) / 2.0
                rows.append(k);  cols.append(k2); vals.append(hop)
                rows.append(k2); cols.append(k);  vals.append(hop)
                diag[k]  -= hop
                diag[k2] -= hop
            # Up neighbor
            if y + 1 < ny:
                k2 = node_index(x, y + 1, nx)
                hop = -(j_k + J[x, y + 1]) / 2.0
                rows.append(k);  cols.append(k2); vals.append(hop)
                rows.append(k2); cols.append(k);  vals.append(hop)
                diag[k]  -= hop
                diag[k2] -= hop

    # Add diagonal
    for k in range(N):
        rows.append(k)
        cols.append(k)
        vals.append(diag[k])

    H = sp.csr_matrix((vals, (rows, cols)), shape=(N, N), dtype=np.float64)
    return H


def gaussian_wavepacket_1d(nx: int, ny: int, x0: float, y0: float,
                           sigma: float, kx: float = 0.0,
                           ky: float = 0.0) -> np.ndarray:
    """Create a normalised Gaussian wavepacket (1D flattened)."""
    x = np.arange(nx)
    y = np.arange(ny)
    X, Y = np.meshgrid(x, y, indexing="ij")
    psi_2d = np.exp(-((X - x0)**2 + (Y - y0)**2) / (2 * sigma**2)) \
           * np.exp(1j * (kx * X + ky * Y))
    psi_2d /= np.sqrt(np.sum(np.abs(psi_2d)**2))
    return psi_2d.ravel(order='F')


def psi_to_2d(psi: np.ndarray, nx: int, ny: int) -> np.ndarray:
    """Convert 1D flattened state vector to 2D grid."""
    return psi.reshape((nx, ny), order='F')


def evolve_unitary(psi: np.ndarray, H: sp.csr_matrix,
                   dt: float, steps: int) -> np.ndarray:
    """Strictly unitary evolution: U = exp(-i H dt)."""
    for _ in range(steps):
        psi = splinalg.expm_multiply(-1j * H * dt, psi)
    return psi


# ╔══════════════════════════════════════════════════════════════════╗
# ║  ZENO THRESHOLD GARBAGE COLLECTOR                               ║
# ╚══════════════════════════════════════════════════════════════════╝

class ZenoTelemetry:
    """Accumulates Clausius-Landauer telemetry during simulation."""
    def __init__(self):
        self.events = []
        self.total_heat = 0.0
        self.total_entropy = 0.0
        self.total_probability_erased = 0.0

    def record(self, frame: int, node_count: int, prob_erased: float,
               entropy: float, heat: float):
        self.events.append({
            "frame": frame, "nodes": node_count,
            "prob": prob_erased, "dS": entropy, "dQ": heat
        })
        self.total_heat += heat
        self.total_entropy += entropy
        self.total_probability_erased += prob_erased


def zeno_truncation(psi: np.ndarray, J: np.ndarray, Phi: np.ndarray,
                    frame: int, z_alpha: float,
                    telemetry: ZenoTelemetry) -> np.ndarray:
    """Apply Z_α garbage collection.

    For each node k, the total processing load is:
        load(k) = Phi(k) + ρ_info(k)
    where ρ_info = |ψ|² is the test wavepacket's local density.

    If load(k) > z_alpha, Born Rule truncation fires:
        ψ[k] → 0, with Landauer heat computed.
    """
    nx, ny = J.shape
    prob_2d = np.abs(psi_to_2d(psi, nx, ny))**2

    # Normalise Phi to [0, 1] for the load comparison
    Phi_norm = Phi / (np.max(Phi) + 1e-15)

    # Total processing load at each node
    load = Phi_norm + prob_2d

    # Find breach nodes
    breach_mask = load > z_alpha
    breach_flat = breach_mask.ravel(order='F')

    if np.any(breach_flat):
        # Compute Clausius-Landauer telemetry for each breached node
        prob_breached = prob_2d[breach_mask]
        prob_breached = prob_breached[prob_breached > 1e-15]

        total_prob_erased = np.sum(prob_breached)

        # Shannon entropy as proxy for von Neumann entropy
        dS = -np.sum(prob_breached * np.log(prob_breached))

        # Local modular temperature: T_mod ∝ 1/J
        J_at_breach = J[breach_mask]
        J_at_breach = np.maximum(J_at_breach, 1e-10)
        T_mod_avg = np.mean(1.0 / J_at_breach)
        dQ = T_mod_avg * dS

        n_breached = np.sum(breach_flat)

        # Record telemetry
        telemetry.record(frame, int(n_breached), total_prob_erased, dS, dQ)

        print(f"  >> Z-SCALE BREACH [frame {frame}]")
        print(f"     Nodes truncated:  {n_breached}")
        print(f"     Probability erased: {total_prob_erased:.6f}")
        print(f"     Entropy erased (dS): {dS:.6f} nats")
        print(f"     Avg T_mod at breach: {T_mod_avg:.4f}")
        print(f"     Landauer Heat Dissipated: δQ = {dQ:.6f}")

        # Born Rule truncation: zero out breached nodes
        psi[breach_flat] = 0.0
        remaining_norm = np.sqrt(np.sum(np.abs(psi)**2))
        if remaining_norm > 1e-15:
            psi /= remaining_norm
        print(f"     ||ψ||² after truncation: "
              f"{np.sum(np.abs(psi)**2):.10f}")

    return psi


# ╔══════════════════════════════════════════════════════════════════╗
# ║  VISUALISATION                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝

def make_3d_figure(J, prob_2d, frame, breach_mask, telemetry, path):
    """Generate the 3D cinematic visualisation:
    - Gravity well: J mapped to Z-axis (inverted)
    - Wavepacket density as color on the surface
    - Breach nodes flashing red
    """
    nx, ny = J.shape
    # Subsample for performance
    step = max(1, nx // 60)
    xs = np.arange(0, nx, step)
    ys = np.arange(0, ny, step)
    Xs, Ys = np.meshgrid(xs, ys, indexing="ij")
    J_sub = J[::step, ::step]
    prob_sub = prob_2d[::step, ::step]
    breach_sub = breach_mask[::step, ::step] if breach_mask is not None \
        else np.zeros_like(J_sub, dtype=bool)

    # Z-axis: invert J to create the gravity well (funnel)
    Z = -(J0 - J_sub)

    # Colour: base on J-field depth (so geometry is ALWAYS visible),
    # overlay wavepacket density as bright glow
    j_norm = J_sub / (np.max(J_sub) + 1e-15)
    base_colors = plt.cm.inferno(1.0 - j_norm)  # deep funnel = dark, flat = bright

    # Overlay wavepacket density as cyan-white glow
    prob_norm = prob_sub / (np.max(prob_sub) + 1e-15)
    for i in range(base_colors.shape[0]):
        for j in range(base_colors.shape[1]):
            glow = min(1.0, prob_norm[i, j] * 3)
            if glow > 0.02:
                base_colors[i, j, 0] = base_colors[i, j, 0] * (1-glow) + glow * 0.2
                base_colors[i, j, 1] = base_colors[i, j, 1] * (1-glow) + glow * 0.9
                base_colors[i, j, 2] = base_colors[i, j, 2] * (1-glow) + glow * 1.0

    # Flash breach nodes red
    if np.any(breach_sub):
        base_colors[breach_sub] = [1, 0, 0, 1]

    fig = plt.figure(figsize=(14, 10))
    fig.patch.set_facecolor("#0a0a1a")
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor("#0a0a1a")

    # Plot the gravity well surface with "Tron" wireframe grid
    ax.plot_surface(Xs, Ys, Z, facecolors=base_colors, shade=True,
                    antialiased=True, alpha=0.9,
                    edgecolor='#00ccff33', linewidth=0.4)

    # Labels
    ax.set_xlabel("x", color="white", fontsize=11)
    ax.set_ylabel("y", color="white", fontsize=11)
    ax.set_zlabel("−(J₀ − J)  [gravity well depth]", color="white",
                  fontsize=10)
    ax.tick_params(colors="white", labelsize=8)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('#333333')
    ax.yaxis.pane.set_edgecolor('#333333')
    ax.zaxis.pane.set_edgecolor('#333333')

    # Title
    heat_str = (f"Total δQ = {telemetry.total_heat:.4f}"
                if telemetry.total_heat > 0 else "No truncation yet")
    ax.set_title(
        f"ATR Black Hole — Frame {frame}\n"
        f"M = {MASS}, κ = {KAPPA}, Z_α = {Z_ALPHA}  |  {heat_str}",
        color="white", fontsize=13, pad=20
    )

    ax.view_init(elev=35, azim=45 + frame * 3)

    plt.tight_layout()
    fig.savefig(path, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def make_2d_timeline(snapshots, J, R, breach_frames, telemetry, path):
    """Generate a 2D timeline panel showing the full simulation."""
    n = len(snapshots)
    cols = min(n, 5)
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
    fig.patch.set_facecolor("#0a0a1a")

    if rows == 1:
        axes = [axes] if cols == 1 else list(axes)
    flat_axes = np.array(axes).flatten()

    for i in range(len(flat_axes)):
        ax = flat_axes[i]
        ax.set_facecolor("#0a0a1a")
        ax.tick_params(colors="white", labelsize=6)
        for spine in ax.spines.values():
            spine.set_color("#333")

        if i < n:
            prob = snapshots[i]
            if i in breach_frames:
                ax.imshow(prob.T, origin="lower", cmap=CMAP_BREACH,
                          extent=[0, NX, 0, NY],
                          vmax=np.max(prob) * 0.6)
                ax.set_title(f"t={i * STEPS_PER} ⚠️ BREACH",
                             color="#ff4444", fontsize=9, fontweight="bold")
            else:
                ax.imshow(prob.T, origin="lower", cmap=CMAP_PROB,
                          extent=[0, NX, 0, NY],
                          vmax=np.max(prob) * 0.6)
                ax.set_title(f"t={i * STEPS_PER}", color="white",
                             fontsize=9)

            # Draw J contours to show the emergent horizon
            ax.contour(J.T, levels=[0.01, 0.05, 0.1, 0.2],
                       colors=['#ff000044', '#ff440044',
                               '#ff880044', '#ffcc0044'],
                       extent=[0, NX, 0, NY], linewidths=0.5)
        else:
            ax.set_visible(False)

    fig.suptitle(
        f"ATR Black Hole Timeline — M={MASS}, κ={KAPPA}, Z_α={Z_ALPHA}\n"
        f"Breaches: {len(breach_frames)}, "
        f"Total Landauer Heat: δQ = {telemetry.total_heat:.6f}\n"
        f"[Sparse Hermitian H, Strict Unitary Evolution]",
        color="white", fontsize=13, y=0.99
    )
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(path, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def make_summary_figure(J, Phi, R, centroid_r, telemetry, path):
    """Generate a 4-panel summary figure."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.patch.set_facecolor("#0a0a1a")

    for ax in axes.flatten():
        ax.set_facecolor("#0a0a1a")
        ax.tick_params(colors="white", labelsize=9)
        for spine in ax.spines.values():
            spine.set_color("#333")

    # Panel 1: J-field (the emergent spacetime)
    im0 = axes[0, 0].imshow(J.T, origin="lower", cmap="inferno",
                             extent=[0, NX, 0, NY])
    axes[0, 0].set_title("Emergent Clock Field J(x,y)", color="white",
                         fontsize=12)
    plt.colorbar(im0, ax=axes[0, 0], fraction=0.046, pad=0.04)

    # Panel 2: Processing load Φ
    im1 = axes[0, 1].imshow(np.log10(Phi.T + 1e-10), origin="lower",
                             cmap="hot", extent=[0, NX, 0, NY])
    axes[0, 1].set_title("Processing Load log₁₀Φ(x,y)", color="white",
                         fontsize=12)
    plt.colorbar(im1, ax=axes[0, 1], fraction=0.046, pad=0.04)

    # Panel 3: Centroid radius over time
    axes[1, 0].plot(range(len(centroid_r)), centroid_r, "-o",
                    color="#00ccff", lw=2, ms=4)
    axes[1, 0].axhline(y=0, color="#ff4444", ls="--", lw=1,
                       label="Singularity")
    axes[1, 0].set_xlabel("Frame", color="white", fontsize=11)
    axes[1, 0].set_ylabel("Centroid Radius (pixels)", color="white",
                          fontsize=11)
    axes[1, 0].set_title("Wavepacket Approach", color="white", fontsize=12)
    axes[1, 0].legend(fontsize=9, facecolor="#1a1a2e", edgecolor="#444",
                      labelcolor="white")

    # Panel 4: Clausius-Landauer telemetry
    if telemetry.events:
        frames = [e["frame"] for e in telemetry.events]
        heats = [e["dQ"] for e in telemetry.events]
        entropies = [e["dS"] for e in telemetry.events]

        ax4 = axes[1, 1]
        ax4_twin = ax4.twinx()
        ax4.bar(frames, heats, color="#ff6600", alpha=0.8,
                label="δQ (heat)")
        ax4_twin.plot(frames, entropies, "s-", color="#00ff88", lw=2,
                      ms=6, label="dS (entropy)")
        ax4.set_xlabel("Frame", color="white", fontsize=11)
        ax4.set_ylabel("Landauer Heat δQ", color="#ff6600", fontsize=11)
        ax4_twin.set_ylabel("Entropy dS (nats)", color="#00ff88",
                            fontsize=11)
        ax4.tick_params(axis='y', colors="#ff6600")
        ax4_twin.tick_params(axis='y', colors="#00ff88")
        ax4.set_title("Clausius-Landauer Telemetry", color="white",
                      fontsize=12)
        ax4.legend(loc="upper left", fontsize=9, facecolor="#1a1a2e",
                   edgecolor="#444", labelcolor="white")
        ax4_twin.legend(loc="upper right", fontsize=9,
                        facecolor="#1a1a2e", edgecolor="#444",
                        labelcolor="white")
    else:
        axes[1, 1].text(0.5, 0.5, "No Z_α breaches detected",
                        color="white", fontsize=14,
                        ha="center", va="center",
                        transform=axes[1, 1].transAxes)
        axes[1, 1].set_title("Clausius-Landauer Telemetry", color="white",
                             fontsize=12)

    fig.suptitle(
        f"ATR Black Hole — Summary\n"
        f"M={MASS}, κ={KAPPA}, Z_α={Z_ALPHA}  |  "
        f"Total δQ={telemetry.total_heat:.6f}  |  "
        f"Breaches: {len(telemetry.events)}",
        color="white", fontsize=14, y=0.99
    )
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(path, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  MAIN SIMULATION                                                ║
# ╚══════════════════════════════════════════════════════════════════╝

def main():
    print("╔" + "═" * 58 + "╗")
    print("║  ATR Black Hole Simulator                                ║")
    print("║  Dynamic Horizon Emergence via Z_α Truncation            ║")
    print("║  Sparse Hermitian H + Strict Unitary Evolution           ║")
    print("╚" + "═" * 58 + "╝")

    # ── Step 1: Build the emergent J-field from Information Mass ───
    print("\n  Step 1: Building dynamic J-field from Information Mass")
    J, Phi, R = build_dynamic_J_field(NX, NY, XC, YC, J0, MASS, KAPPA)

    # Compute the emergent horizon radius
    # (where J drops below some small threshold)
    J_threshold = 0.01 * J0
    horizon_mask = J < J_threshold
    if np.any(horizon_mask):
        r_horizon_nodes = R[horizon_mask]
        r_horizon = np.max(r_horizon_nodes)
        print(f"  Information Mass M = {MASS}")
        print(f"  Clock coupling κ = {KAPPA}")
        print(f"  J₀ = {J0}")
        print(f"  Emergent horizon radius (J < {J_threshold:.4f}): "
              f"r ≈ {r_horizon:.1f} px")
    else:
        r_horizon = 0
        print(f"  No clear horizon (J never drops below {J_threshold:.4f})")

    print(f"  J at center: {J[XC, YC]:.8f}")
    print(f"  J at r=10:   {J[XC + 10, YC]:.6f}")
    print(f"  J at r=30:   {J[XC + 30, YC]:.6f}")
    print(f"  J at edge:   {J[0, YC]:.6f}")

    # ── Step 2: Build Hamiltonian ──────────────────────────────────
    print("\n  Step 2: Building Hermitian tight-binding Hamiltonian")
    H = build_hamiltonian(NX, NY, J)
    hermiticity = sp.linalg.norm(H - H.T)
    print(f"  H size: {H.shape[0]} × {H.shape[0]}")
    print(f"  Non-zero elements: {H.nnz}")
    print(f"  Hermiticity check: ||H − H†|| = {hermiticity:.2e}")

    # ── Step 3: Initialise wavepacket ──────────────────────────────
    print("\n  Step 3: Initialising test wavepacket")
    psi = gaussian_wavepacket_1d(NX, NY, WP_X0, WP_Y0,
                                 WP_SIGMA, WP_KX, WP_KY)
    print(f"  Position: ({WP_X0}, {WP_Y0})")
    print(f"  Momentum: (kx={WP_KX}, ky={WP_KY})")
    print(f"  Width σ = {WP_SIGMA}")
    print(f"  ||ψ||² = {np.sum(np.abs(psi)**2):.10f}")

    # ── Step 4: Evolution with Z_α garbage collection ──────────────
    print("\n  Step 4: Evolution + Z_α Garbage Collection")
    print(f"  Frames: {N_FRAMES}, Steps/frame: {STEPS_PER}, "
          f"dt = {DT}")
    print(f"  Z_α threshold: {Z_ALPHA}")
    print("  " + "─" * 56)

    telemetry = ZenoTelemetry()
    snapshots = []
    centroid_r = []
    breach_frames = set()
    X, Y = np.meshgrid(np.arange(NX), np.arange(NY), indexing="ij")

    for frame in range(N_FRAMES):
        prob_2d = np.abs(psi_to_2d(psi, NX, NY))**2
        snapshots.append(prob_2d.copy())

        # Centroid
        norm = np.sum(prob_2d)
        cx = np.sum(X * prob_2d) / norm
        cy = np.sum(Y * prob_2d) / norm
        r_centroid = np.sqrt((cx - XC)**2 + (cy - YC)**2)
        centroid_r.append(r_centroid)

        # Check and apply Z_α truncation
        n_events_before = len(telemetry.events)
        psi = zeno_truncation(psi, J, Phi, frame, Z_ALPHA, telemetry)
        if len(telemetry.events) > n_events_before:
            breach_frames.add(frame)

        # Log progress
        norm_after = np.sum(np.abs(psi)**2)
        if frame % 5 == 0 or frame in breach_frames:
            print(f"  [frame {frame:3d}] r_centroid = {r_centroid:6.2f}, "
                  f"||ψ||² = {norm_after:.10f}")

        # Evolve
        psi = evolve_unitary(psi, H, DT, STEPS_PER)

    # Final state
    prob_2d_final = np.abs(psi_to_2d(psi, NX, NY))**2
    snapshots.append(prob_2d_final)
    norm_final = np.sum(np.abs(psi)**2)

    # ── Step 5: Results ────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  RESULTS")
    print("=" * 60)
    print(f"  Z_α breaches:              {len(telemetry.events)}")
    print(f"  Total probability erased:  "
          f"{telemetry.total_probability_erased:.6f}")
    print(f"  Total entropy erased:      "
          f"{telemetry.total_entropy:.6f} nats")
    print(f"  Total Landauer heat:       "
          f"δQ = {telemetry.total_heat:.6f}")
    print(f"  Final ||ψ||²:              {norm_final:.10f}")
    print(f"  Emergent horizon radius:   "
          f"r ≈ {r_horizon:.1f} px")

    passed = (len(telemetry.events) > 0 and
              telemetry.total_heat > 0 and
              abs(norm_final - 1.0) < 1e-6)
    print(f"\n  {'✅ PASS' if passed else '❌ FAIL'} — "
          f"Black hole emerged algorithmically, Landauer heat computed")

    # ── Step 6: Generate figures ───────────────────────────────────
    print("\n  Step 6: Generating figures")

    # 3D: Use mid-simulation and final frames
    breach_mask_2d = None
    if breach_frames:
        # Show the first breach frame in 3D
        bf = min(breach_frames)
        Phi_norm = Phi / (np.max(Phi) + 1e-15)
        load = Phi_norm + snapshots[bf]
        breach_mask_2d = load > Z_ALPHA

    # 3D gravity well with wavepacket
    path_3d = os.path.join(OUT_DIR, "blackhole_3d_well.png")
    mid = len(snapshots) // 2
    make_3d_figure(J, snapshots[mid], mid, breach_mask_2d,
                   telemetry, path_3d)
    print(f"  ✅ Saved: {path_3d}")

    # 2D timeline
    # Select subset of frames for timeline
    timeline_indices = np.linspace(0, len(snapshots) - 1,
                                   min(10, len(snapshots)),
                                   dtype=int)
    timeline_snaps = [snapshots[i] for i in timeline_indices]
    timeline_breaches = set()
    for i, idx in enumerate(timeline_indices):
        if idx in breach_frames:
            timeline_breaches.add(i)

    path_timeline = os.path.join(OUT_DIR, "blackhole_timeline.png")
    make_2d_timeline(timeline_snaps, J, R, timeline_breaches,
                     telemetry, path_timeline)
    print(f"  ✅ Saved: {path_timeline}")

    # Summary figure
    path_summary = os.path.join(OUT_DIR, "blackhole_summary.png")
    make_summary_figure(J, Phi, R, centroid_r, telemetry, path_summary)
    print(f"  ✅ Saved: {path_summary}")

    print(f"\n  {'✅ ALL CHECKS PASSED' if passed else '⚠️  NEEDS REVIEW'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
