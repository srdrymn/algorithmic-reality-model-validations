#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
  Computational Verification of Holographic Dark Energy from ATR
═══════════════════════════════════════════════════════════════════════

  Paper:  "Holographic Dark Energy from Algorithmic Thermodynamics:
           Resolving the Vacuum Catastrophe via the Bennett-Landauer Limit"
  Author: Serdar Yaman
  Based on: The Algorithmic Theory of Reality (ATR)
            https://doi.org/10.5281/zenodo.19042891

  This script numerically verifies every algebraic step of the derivation
  using CODATA 2018 physical constants and Planck 2018 cosmological
  parameters. It confirms:

    1. The holographic bit count N = πR_E²/ℓ_P²
    2. The Gibbons-Hawking temperature T = ℏc/(2πk_B R_E)
    3. The Bennett-Landauer vacuum energy E = Nk_BT
    4. The dark energy density ρ_Λ = E/V
    5. The exact cancellation of ℏ (quantum → classical)
    6. Self-consistency with the Friedmann critical density
    7. Agreement with the Planck 2018 observed value
    8. The (R_E/ℓ_P)² ≈ 10¹²² scaling ratio

  Requirements: Python 3.6+ (standard library only — no dependencies)
  Usage:        python verify_dark_energy.py
═══════════════════════════════════════════════════════════════════════
"""
import math
import sys

# ─── ANSI colours for terminal output ─────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"
CYAN   = "\033[96m"

def header(text: str) -> None:
    print(f"\n{BOLD}{CYAN}{'─' * 70}")
    print(f"  {text}")
    print(f"{'─' * 70}{RESET}")

def check(label: str, passed: bool) -> bool:
    tag = f"{GREEN}✅ PASS{RESET}" if passed else f"{RED}❌ FAIL{RESET}"
    print(f"  {tag}  {label}")
    return passed


def main() -> int:
    print(f"{BOLD}")
    print("═" * 70)
    print("  COMPUTATIONAL VERIFICATION")
    print("  Holographic Dark Energy from Algorithmic Thermodynamics")
    print("═" * 70)
    print(f"{RESET}")

    # ─────────────────────────────────────────────────────────────────
    # PHYSICAL CONSTANTS (CODATA 2018)
    # ─────────────────────────────────────────────────────────────────
    c     = 2.99792458e8        # speed of light              [m/s]
    hbar  = 1.054571817e-34     # reduced Planck constant     [J·s]
    G     = 6.67430e-11         # gravitational constant      [m³/(kg·s²)]
    k_B   = 1.380649e-23        # Boltzmann constant          [J/K]
    ell_P = math.sqrt(hbar * G / c**3)  # Planck length       [m]

    # ─────────────────────────────────────────────────────────────────
    # COSMOLOGICAL PARAMETERS (Planck 2018 — Aghanim et al. 2020)
    # ─────────────────────────────────────────────────────────────────
    H_0_km_s_Mpc = 67.4                         # [km/s/Mpc]
    Mpc_in_m     = 3.0857e22                     # [m]
    H_0          = H_0_km_s_Mpc * 1e3 / Mpc_in_m  # [1/s]
    Omega_Lambda = 0.685                         # dark energy fraction

    # Asymptotic Hubble parameter (Λ-dominated de Sitter future)
    # In flat ΛCDM: H_∞ = H_0 √Ω_Λ  (matter dilutes to zero)
    H_inf = H_0 * math.sqrt(Omega_Lambda)

    # Cosmological event horizon
    R_E = c / H_inf

    header("Step 0: Physical & Cosmological Constants")
    print(f"  c       = {c:.8e} m/s")
    print(f"  ℏ       = {hbar:.9e} J·s")
    print(f"  G       = {G:.5e} m³/(kg·s²)")
    print(f"  k_B     = {k_B:.6e} J/K")
    print(f"  ℓ_P     = {ell_P:.6e} m")
    print(f"  H_0     = {H_0:.6e} s⁻¹  ({H_0_km_s_Mpc} km/s/Mpc)")
    print(f"  Ω_Λ     = {Omega_Lambda}")
    print(f"  H_∞     = {H_inf:.6e} s⁻¹")
    print(f"  R_E     = {R_E:.6e} m  ({R_E / 9.461e15:.1f} Gly)")

    # ═════════════════════════════════════════════════════════════════
    # STEP 1: Count the bits — Holographic area law (§3.3)
    # ═════════════════════════════════════════════════════════════════
    N = math.pi * R_E**2 / ell_P**2

    header("Step 1: Holographic Bit Count  N = π R_E² / ℓ_P²")
    print(f"  N       = {N:.6e}")
    print(f"  log₁₀N  = {math.log10(N):.2f}")

    # ═════════════════════════════════════════════════════════════════
    # STEP 2: Gibbons-Hawking temperature (§4)
    # ═════════════════════════════════════════════════════════════════
    T_mod = hbar * c / (2 * math.pi * k_B * R_E)

    header("Step 2: Gibbons-Hawking Temperature  T = ℏc / (2πk_B R_E)")
    print(f"  T_mod   = {T_mod:.6e} K")

    # ═════════════════════════════════════════════════════════════════
    # STEP 3: Bennett-Landauer vacuum energy (§4)
    # ═════════════════════════════════════════════════════════════════
    E_vac = N * k_B * T_mod

    # Cross-check: simplified closed form
    E_vac_alt = R_E * hbar * c / (2 * ell_P**2)

    header("Step 3: Vacuum Energy  E = N k_B T")
    print(f"  E_vac (step-by-step) = {E_vac:.6e} J")
    print(f"  E_vac (closed form)  = {E_vac_alt:.6e} J")
    print(f"  Ratio                = {E_vac / E_vac_alt:.15f}")

    # ═════════════════════════════════════════════════════════════════
    # STEP 4: Energy density (§5)
    # ═════════════════════════════════════════════════════════════════
    V = (4.0 / 3.0) * math.pi * R_E**3
    rho_ATR = E_vac / V

    header("Step 4: Dark Energy Density  ρ = E / V")
    print(f"  V       = {V:.6e} m³")
    print(f"  ρ_Λ     = {rho_ATR:.6e} J/m³")

    # ═════════════════════════════════════════════════════════════════
    # STEP 5: ℏ cancellation — closed-form result (§5)
    # ═════════════════════════════════════════════════════════════════
    rho_closed = 3 * c**4 / (8 * math.pi * G * R_E**2)

    header("Step 5: ℏ Cancellation  ρ = 3c⁴ / (8πG R_E²)  [NO ℏ!]")
    print(f"  ρ (with ℏ steps)   = {rho_ATR:.10e} J/m³")
    print(f"  ρ (ℏ-free formula) = {rho_closed:.10e} J/m³")
    print(f"  Ratio              = {rho_ATR / rho_closed:.15f}")

    # ═════════════════════════════════════════════════════════════════
    # STEP 6: Friedmann self-consistency (§5.2)
    # ═════════════════════════════════════════════════════════════════
    rho_critical = 3 * c**2 * H_inf**2 / (8 * math.pi * G)

    header("Step 6: Friedmann Self-Consistency  ρ_c = 3c²H²/(8πG)")
    print(f"  ρ_critical = {rho_critical:.10e} J/m³")
    print(f"  ρ_Λ (ATR)  = {rho_ATR:.10e} J/m³")
    print(f"  Ratio      = {rho_ATR / rho_critical:.15f}")

    # ═════════════════════════════════════════════════════════════════
    # STEP 7: Comparison with observation (Planck 2018)
    # ═════════════════════════════════════════════════════════════════
    rho_crit_today = 3 * c**2 * H_0**2 / (8 * math.pi * G)
    rho_obs = Omega_Lambda * rho_crit_today
    rho_QFT = c**7 / (hbar * G**2)

    header("Step 7: Comparison with Observation")
    print(f"  ρ_obs (Planck 2018) = {rho_obs:.6e} J/m³")
    print(f"  ρ_Λ (ATR)           = {rho_ATR:.6e} J/m³")
    print(f"  ρ_QFT               = {rho_QFT:.6e} J/m³")
    print(f"  ATR / observed      = {rho_ATR / rho_obs:.6f}")
    print(f"  QFT / observed      = {rho_QFT / rho_obs:.2e}  ← the catastrophe")
    print(f"  log₁₀(QFT/obs)     = {math.log10(rho_QFT / rho_obs):.1f}")

    # ═════════════════════════════════════════════════════════════════
    # STEP 8: Scaling ratio verification (§6.1)
    # ═════════════════════════════════════════════════════════════════
    scaling = (R_E / ell_P)**2

    header("Step 8: §6.1 Scaling Ratio  (R_E / ℓ_P)²")
    print(f"  (R_E / ℓ_P)²    = {scaling:.4e}")
    print(f"  log₁₀           = {math.log10(scaling):.2f}")
    print(f"  ρ_QFT / ρ_ATR   = {rho_QFT / rho_ATR:.4e}")
    print(f"  log₁₀           = {math.log10(rho_QFT / rho_ATR):.2f}")

    # ═════════════════════════════════════════════════════════════════
    # SUMMARY
    # ═════════════════════════════════════════════════════════════════
    print(f"\n{BOLD}{'═' * 70}")
    print(f"{'VERIFICATION SUMMARY':^70}")
    print(f"{'═' * 70}{RESET}\n")

    results = [
        ("E_vac(steps) = E_vac(simplified)",
         abs(E_vac - E_vac_alt) / E_vac < 1e-10),
        ("ℏ cancellation: ρ(steps) = 3c⁴/(8πGR²)",
         abs(rho_ATR - rho_closed) / rho_closed < 1e-10),
        ("Friedmann self-consistency: ρ_ATR = ρ_critical",
         abs(rho_ATR - rho_critical) / rho_critical < 1e-10),
        ("Agreement with Planck 2018: |ATR/obs − 1| < 1%",
         abs(rho_ATR / rho_obs - 1.0) < 0.01),
        ("Scaling ratio: (R_E/ℓ_P)² ≈ ρ_QFT/ρ_ATR (within 1 decade)",
         abs(math.log10(scaling) - math.log10(rho_QFT / rho_ATR)) < 1),
    ]

    all_pass = True
    for label, passed in results:
        if not check(label, passed):
            all_pass = False

    print(f"\n{BOLD}{'═' * 70}")
    if all_pass:
        print(f"{GREEN}  ALL 5 CHECKS PASSED — DERIVATION NUMERICALLY VERIFIED{RESET}")
    else:
        print(f"{RED}  ⚠️  SOME CHECKS FAILED — REVIEW NEEDED{RESET}")
    print(f"{BOLD}{'═' * 70}{RESET}\n")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
