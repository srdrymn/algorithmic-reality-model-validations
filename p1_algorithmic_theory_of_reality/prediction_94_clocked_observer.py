#!/usr/bin/env python3
"""
Prediction 9.4 -- finite-clock observer derivation.

This script upgrades the Prediction 9.4 computation from a phenomenological
staircase ansatz to an explicit clocked-observer model:

1. The data qubit evolves under the Lindblad dynamics stated in the paper.
2. The observer is allowed one POVM update per clock tick.
3. The observer's memory holds the most recent outcome between ticks.
4. The reported two-time correlator is computed from that discrete
   measurement process.

For the paper's nominal parameters (omega / 2pi = 5 GHz, T_tick = 1 ns),
the phase accumulated in one tick is 10*pi, so the derived clocked-observer
correlator coincides with the paper's floor() staircase formula. This is
not true generically; the script includes an off-resonant control to show
the distinction.
"""

from __future__ import annotations

import argparse
import json
import os

import matplotlib.pyplot as plt
import numpy as np


IDENTITY = np.eye(2, dtype=np.complex128)
SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
PROJECTOR_PLUS_X = 0.5 * (IDENTITY + SIGMA_X)
PROJECTOR_MINUS_X = 0.5 * (IDENTITY - SIGMA_X)
PROJECTORS_X = np.stack([PROJECTOR_PLUS_X, PROJECTOR_MINUS_X])
OUTCOME_SIGNS = np.array([1.0, -1.0], dtype=np.float64)
RHO_REFERENCE = 0.5 * IDENTITY
EPS_PROB = 1.0e-12


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Finite-clock observer derivation for Prediction 9.4."
    )
    parser.add_argument("--omega-ghz", type=float, default=5.0)
    parser.add_argument("--t2-ns", type=float, default=20.0)
    parser.add_argument("--nu-alpha-ghz", type=float, default=1.0)
    parser.add_argument("--clock-jitter-ps", type=float, default=50.0)
    parser.add_argument("--n-shots", type=int, default=10_000)
    parser.add_argument("--n-experiments", type=int, default=500)
    parser.add_argument("--t-max-ns", type=float, default=6.5)
    parser.add_argument("--dt-data-ps", type=float, default=50.0)
    parser.add_argument("--dt-fine-ps", type=float, default=0.5)
    parser.add_argument("--quadrature-order", type=int, default=61)
    parser.add_argument("--omega-fit-min-ghz", type=float, default=4.5)
    parser.add_argument("--omega-fit-max-ghz", type=float, default=5.5)
    parser.add_argument("--omega-fit-points", type=int, default=81)
    parser.add_argument("--t2-fit-min-ns", type=float, default=10.0)
    parser.add_argument("--t2-fit-max-ns", type=float, default=40.0)
    parser.add_argument("--t2-fit-points", type=int, default=81)
    parser.add_argument(
        "--control-omega-ghz",
        type=float,
        default=5.1,
        help="Off-resonant control frequency used to show clocked != floor() generically.",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output-prefix",
        default="prediction_94_clocked_observer",
        help="Prefix for figure and JSON outputs written in this directory.",
    )
    return parser.parse_args()


def vec(matrix: np.ndarray) -> np.ndarray:
    return np.asarray(matrix, dtype=np.complex128).reshape(-1, order="F")


def unvec(vector: np.ndarray) -> np.ndarray:
    return np.asarray(vector, dtype=np.complex128).reshape((2, 2), order="F")


def liouvillian_matrix(omega: float, gamma: float) -> np.ndarray:
    hamiltonian = 0.5 * omega * SIGMA_Z
    lindblad = np.sqrt(gamma / 2.0) * SIGMA_Z
    lindblad_norm = lindblad.conj().T @ lindblad

    coherent = -1j * (
        np.kron(IDENTITY, hamiltonian) - np.kron(hamiltonian.T, IDENTITY)
    )
    dissipator = (
        np.kron(lindblad.conj(), lindblad)
        - 0.5 * np.kron(IDENTITY, lindblad_norm)
        - 0.5 * np.kron(lindblad_norm.T, IDENTITY)
    )
    return coherent + dissipator


def propagator_matrix(omega: float, gamma: float, delta_t: float) -> np.ndarray:
    liouvillian = liouvillian_matrix(omega, gamma)
    eigenvalues, eigenvectors = np.linalg.eig(liouvillian)
    eigenvectors_inv = np.linalg.inv(eigenvectors)
    return eigenvectors @ np.diag(np.exp(eigenvalues * delta_t)) @ eigenvectors_inv


def propagate_density_matrix(
    rho: np.ndarray,
    omega: float,
    gamma: float,
    delta_t: float,
) -> np.ndarray:
    propagator = propagator_matrix(omega, gamma, delta_t)
    return unvec(propagator @ vec(rho))


def qrt_correlator_exact(times: np.ndarray, omega: float, gamma: float) -> np.ndarray:
    propagator_eig = liouvillian_matrix(omega, gamma)
    eigenvalues, eigenvectors = np.linalg.eig(propagator_eig)
    eigenvectors_inv = np.linalg.inv(eigenvectors)

    seeded_operator = SIGMA_X @ RHO_REFERENCE
    coefficients = eigenvectors_inv @ vec(seeded_operator)
    propagated = eigenvectors @ (
        np.exp(np.outer(eigenvalues, times)) * coefficients[:, None]
    )
    correlator = np.conjugate(vec(SIGMA_X)) @ propagated
    return np.real_if_close(correlator).astype(np.float64)


def qm_correlator_analytic(times: np.ndarray, omega: float, gamma: float) -> np.ndarray:
    clipped_times = np.clip(times, 0.0, None)
    return np.exp(-gamma * clipped_times) * np.cos(omega * clipped_times)


def gaussian_expectation(
    times: np.ndarray,
    sigma: float,
    quadrature_order: int,
    base_function,
) -> np.ndarray:
    if sigma <= 0.0:
        return base_function(times)

    nodes, weights = np.polynomial.hermite.hermgauss(quadrature_order)
    shifted = times[:, None] + np.sqrt(2.0) * sigma * nodes[None, :]
    values = base_function(shifted)
    return (values * weights[None, :]).sum(axis=1) / np.sqrt(np.pi)


def build_transition_matrix(omega: float, gamma: float, tick_period: float) -> np.ndarray:
    propagator = propagator_matrix(omega, gamma, tick_period)
    transition = np.zeros((2, 2), dtype=np.float64)
    for old_idx, projector_old in enumerate(PROJECTORS_X):
        evolved = unvec(propagator @ vec(projector_old))
        for new_idx, projector_new in enumerate(PROJECTORS_X):
            probability = np.real_if_close(np.trace(projector_new @ evolved)).item()
            transition[new_idx, old_idx] = float(np.clip(probability, 0.0, 1.0))
    return transition


def discrete_clocked_correlator(
    max_ticks: int,
    omega: float,
    gamma: float,
    tick_period: float,
) -> tuple[np.ndarray, np.ndarray]:
    transition = build_transition_matrix(omega, gamma, tick_period)
    transition_powers = np.eye(2)
    correlator_ticks = np.empty(max_ticks + 1, dtype=np.float64)
    correlator_ticks[0] = 1.0

    for tick in range(1, max_ticks + 1):
        transition_powers = transition @ transition_powers
        total = 0.0
        for initial_idx in range(2):
            for final_idx in range(2):
                total += (
                    0.5
                    * OUTCOME_SIGNS[initial_idx]
                    * OUTCOME_SIGNS[final_idx]
                    * transition_powers[final_idx, initial_idx]
                )
        correlator_ticks[tick] = total
    return correlator_ticks, transition


def held_clocked_correlator(times: np.ndarray, correlator_ticks: np.ndarray, tick_period: float) -> np.ndarray:
    indices = np.floor(np.clip(times, 0.0, None) / tick_period).astype(int)
    indices = np.clip(indices, 0, len(correlator_ticks) - 1)
    return correlator_ticks[indices]


def floor_ansatz_correlator(
    times: np.ndarray,
    omega: float,
    gamma: float,
    tick_period: float,
) -> np.ndarray:
    snapped = np.floor(np.clip(times, 0.0, None) / tick_period) * tick_period
    return qm_correlator_analytic(snapped, omega, gamma)


def jittered_clocked_correlator(
    times: np.ndarray,
    correlator_ticks: np.ndarray,
    tick_period: float,
    clock_jitter_sigma: float,
    quadrature_order: int,
) -> np.ndarray:
    return gaussian_expectation(
        times,
        clock_jitter_sigma,
        quadrature_order,
        lambda shifted: held_clocked_correlator(shifted, correlator_ticks, tick_period),
    )


def correlation_to_probability(correlation: np.ndarray) -> np.ndarray:
    bounded = np.clip(correlation, -1.0, 1.0)
    return np.clip(0.5 * (1.0 + bounded), EPS_PROB, 1.0 - EPS_PROB)


def sample_counts(
    mean_correlation: np.ndarray,
    n_shots: int,
    n_experiments: int,
    rng: np.random.Generator,
) -> np.ndarray:
    probabilities = correlation_to_probability(mean_correlation)
    return rng.binomial(
        n_shots, probabilities[None, :], size=(n_experiments, probabilities.size)
    )


def counts_to_correlations(counts: np.ndarray, n_shots: int) -> np.ndarray:
    return 2.0 * counts / float(n_shots) - 1.0


def log_likelihood_matrix(
    counts: np.ndarray,
    n_shots: int,
    mean_bank: np.ndarray,
) -> np.ndarray:
    probabilities = correlation_to_probability(mean_bank)
    log_p = np.log(probabilities)
    log_one_minus_p = np.log1p(-probabilities)
    return counts @ log_p.T + (n_shots - counts) @ log_one_minus_p.T


def build_qm_bank(
    times: np.ndarray,
    omega_grid_ghz: np.ndarray,
    t2_grid_ns: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    bank = []
    params = []
    for t2_ns in t2_grid_ns:
        gamma = 1.0 / (t2_ns * 1.0e-9)
        for omega_ghz in omega_grid_ghz:
            omega = 2.0 * np.pi * omega_ghz * 1.0e9
            bank.append(qm_correlator_analytic(times, omega, gamma))
            params.append((omega_ghz, t2_ns))
    return np.asarray(bank), np.asarray(params)


def summarize_distribution(values: np.ndarray) -> dict[str, float]:
    return {
        "median": float(np.median(values)),
        "p05": float(np.percentile(values, 5)),
        "p95": float(np.percentile(values, 95)),
    }


def main() -> None:
    args = parse_args()
    rng = np.random.default_rng(args.seed)

    omega = 2.0 * np.pi * args.omega_ghz * 1.0e9
    gamma = 1.0 / (args.t2_ns * 1.0e-9)
    tick_period = 1.0 / (args.nu_alpha_ghz * 1.0e9)
    clock_jitter_sigma = args.clock_jitter_ps * 1.0e-12
    control_omega = 2.0 * np.pi * args.control_omega_ghz * 1.0e9

    t_max = args.t_max_ns * 1.0e-9
    dt_fine = args.dt_fine_ps * 1.0e-12
    dt_data = args.dt_data_ps * 1.0e-12
    t_fine = np.arange(0.0, t_max, dt_fine)
    t_data = np.arange(0.0, t_max, dt_data)
    n_ticks = int(np.ceil(t_max / tick_period))

    qm_exact = qrt_correlator_exact(t_fine, omega, gamma)
    qm_formula = qm_correlator_analytic(t_fine, omega, gamma)
    qrt_max_abs_error = float(np.max(np.abs(qm_exact - qm_formula)))

    correlator_ticks_nominal, transition_nominal = discrete_clocked_correlator(
        n_ticks, omega, gamma, tick_period
    )
    clocked_nominal_fine = held_clocked_correlator(t_fine, correlator_ticks_nominal, tick_period)
    clocked_nominal_data = held_clocked_correlator(t_data, correlator_ticks_nominal, tick_period)
    clocked_nominal_jittered = jittered_clocked_correlator(
        t_fine,
        correlator_ticks_nominal,
        tick_period,
        clock_jitter_sigma,
        args.quadrature_order,
    )
    clocked_nominal_data_jittered = jittered_clocked_correlator(
        t_data,
        correlator_ticks_nominal,
        tick_period,
        clock_jitter_sigma,
        args.quadrature_order,
    )

    floor_nominal_fine = floor_ansatz_correlator(t_fine, omega, gamma, tick_period)
    floor_nominal_jittered = gaussian_expectation(
        t_fine,
        clock_jitter_sigma,
        args.quadrature_order,
        lambda shifted: floor_ansatz_correlator(shifted, omega, gamma, tick_period),
    )

    nominal_max_diff_unjittered = float(np.max(np.abs(clocked_nominal_fine - floor_nominal_fine)))
    nominal_max_diff_jittered = float(np.max(np.abs(clocked_nominal_jittered - floor_nominal_jittered)))

    correlator_ticks_control, transition_control = discrete_clocked_correlator(
        n_ticks, control_omega, gamma, tick_period
    )
    clocked_control_fine = held_clocked_correlator(t_fine, correlator_ticks_control, tick_period)
    floor_control_fine = floor_ansatz_correlator(t_fine, control_omega, gamma, tick_period)
    control_max_diff_unjittered = float(np.max(np.abs(clocked_control_fine - floor_control_fine)))

    sigma_shot_upper = 1.0 / np.sqrt(args.n_shots)
    residual_vs_qm = clocked_nominal_jittered - qm_formula
    peak_residual = float(np.max(np.abs(residual_vs_qm)))
    rms_residual = float(np.sqrt(np.mean(residual_vs_qm**2)))
    peak_sigma = peak_residual / sigma_shot_upper
    rms_sigma = rms_residual / sigma_shot_upper

    omega_grid_ghz = np.linspace(args.omega_fit_min_ghz, args.omega_fit_max_ghz, args.omega_fit_points)
    t2_grid_ns = np.linspace(args.t2_fit_min_ns, args.t2_fit_max_ns, args.t2_fit_points)
    qm_bank, qm_bank_params = build_qm_bank(t_data, omega_grid_ghz, t2_grid_ns)

    clocked_counts = sample_counts(clocked_nominal_data_jittered, args.n_shots, args.n_experiments, rng)
    qm_counts = sample_counts(qm_correlator_analytic(t_data, omega, gamma), args.n_shots, args.n_experiments, rng)

    ll_clocked_on_clocked = log_likelihood_matrix(
        clocked_counts,
        args.n_shots,
        clocked_nominal_data_jittered[None, :],
    )[:, 0]
    ll_qm_on_clocked = log_likelihood_matrix(clocked_counts, args.n_shots, qm_bank)
    ll_clocked_on_qm = log_likelihood_matrix(
        qm_counts,
        args.n_shots,
        clocked_nominal_data_jittered[None, :],
    )[:, 0]
    ll_qm_on_qm = log_likelihood_matrix(qm_counts, args.n_shots, qm_bank)

    best_qm_idx_clocked = np.argmax(ll_qm_on_clocked, axis=1)
    best_qm_idx_qm = np.argmax(ll_qm_on_qm, axis=1)
    ll_qm_best_clocked = ll_qm_on_clocked[np.arange(args.n_experiments), best_qm_idx_clocked]
    ll_qm_best_qm = ll_qm_on_qm[np.arange(args.n_experiments), best_qm_idx_qm]

    test_stat_clocked = 2.0 * (ll_clocked_on_clocked - ll_qm_best_clocked)
    test_stat_qm = 2.0 * (ll_clocked_on_qm - ll_qm_best_qm)

    threshold_99 = float(np.percentile(test_stat_qm, 99))
    threshold_95 = float(np.percentile(test_stat_qm, 95))
    power_99 = float(np.mean(test_stat_clocked > threshold_99))
    power_95 = float(np.mean(test_stat_clocked > threshold_95))

    summary = {
        "config": {
            "omega_ghz": args.omega_ghz,
            "t2_ns": args.t2_ns,
            "nu_alpha_ghz": args.nu_alpha_ghz,
            "clock_jitter_ps": args.clock_jitter_ps,
            "n_shots": args.n_shots,
            "n_experiments": args.n_experiments,
            "control_omega_ghz": args.control_omega_ghz,
        },
        "self_check": {
            "qrt_vs_analytic_max_abs_error": qrt_max_abs_error,
        },
        "nominal_model": {
            "transition_matrix": transition_nominal.tolist(),
            "step_correlator_ticks": correlator_ticks_nominal.tolist(),
            "max_abs_diff_vs_floor_unjittered": nominal_max_diff_unjittered,
            "max_abs_diff_vs_floor_jittered": nominal_max_diff_jittered,
            "peak_residual_vs_smooth_qm": peak_residual,
            "rms_residual_vs_smooth_qm": rms_residual,
            "peak_snr_upper_bound": peak_sigma,
            "rms_snr_upper_bound": rms_sigma,
        },
        "off_resonant_control": {
            "omega_ghz": args.control_omega_ghz,
            "transition_matrix": transition_control.tolist(),
            "max_abs_diff_vs_floor_unjittered": control_max_diff_unjittered,
        },
        "pseudoexperiment_discrimination": {
            "test_stat_clocked": summarize_distribution(test_stat_clocked),
            "test_stat_qm": summarize_distribution(test_stat_qm),
            "best_fit_qm_on_clocked_omega_ghz": summarize_distribution(qm_bank_params[best_qm_idx_clocked, 0]),
            "best_fit_qm_on_clocked_t2_ns": summarize_distribution(qm_bank_params[best_qm_idx_clocked, 1]),
            "threshold_95_false_positive": threshold_95,
            "threshold_99_false_positive": threshold_99,
            "power_at_95_threshold": power_95,
            "power_at_99_threshold": power_99,
        },
    }

    print("=" * 72)
    print("Prediction 9.4 -- finite-clock observer derivation")
    print("=" * 72)
    print(f"Nominal omega/2pi         : {args.omega_ghz:.3f} GHz")
    print(f"Nominal T2                : {args.t2_ns:.3f} ns")
    print(f"ATR tick frequency        : {args.nu_alpha_ghz:.3f} GHz")
    print(f"Clock jitter              : {args.clock_jitter_ps:.3f} ps")
    print(f"Shots per delay point     : {args.n_shots:,}")
    print(f"Pseudo-experiments        : {args.n_experiments}")
    print("-" * 72)
    print(f"QRT self-check max error  : {qrt_max_abs_error:.3e}")
    print(
        "Nominal transition matrix : "
        f"[[{transition_nominal[0,0]:.6f}, {transition_nominal[0,1]:.6f}], "
        f"[{transition_nominal[1,0]:.6f}, {transition_nominal[1,1]:.6f}]]"
    )
    print(f"Nominal max diff vs floor : {nominal_max_diff_unjittered:.3e} (unjittered)")
    print(f"Nominal max diff vs floor : {nominal_max_diff_jittered:.3e} (jittered)")
    print(f"Off-resonant control diff : {control_max_diff_unjittered:.6f} at {args.control_omega_ghz:.3f} GHz")
    print(f"Peak residual vs smooth QM: {peak_residual:.6f}")
    print(f"RMS residual vs smooth QM : {rms_residual:.6f}")
    print(f"Peak SNR upper bound      : {peak_sigma:.2f}")
    print(f"RMS SNR upper bound       : {rms_sigma:.2f}")
    print("-" * 72)
    print(
        "Clocked test statistic    : "
        f"{summary['pseudoexperiment_discrimination']['test_stat_clocked']['median']:.2f} "
        f"(median)"
    )
    print(
        "QM null test statistic    : "
        f"{summary['pseudoexperiment_discrimination']['test_stat_qm']['median']:.2f} "
        f"(median)"
    )
    print(f"Power at 1% FPR           : {power_99:.3f}")
    print(f"Power at 5% FPR           : {power_95:.3f}")
    print("=" * 72)

    t_fine_ns = t_fine * 1.0e9
    figure, axes = plt.subplots(3, 1, figsize=(10, 12), height_ratios=[2.0, 1.5, 1.5])
    figure.suptitle(
        "Prediction 9.4 -- finite-clock observer derivation\n"
        "Plateaus from discrete tick updates plus projective state update",
        fontsize=13,
        fontweight="bold",
    )
    figure.text(
        0.5,
        0.915,
        f"Peak/RMS separation vs smooth QM: {peak_sigma:.2f} sigma / {rms_sigma:.2f} sigma",
        ha="center",
        va="center",
        fontsize=10,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.9, "edgecolor": "0.7"},
    )

    ax = axes[0]
    ax.plot(t_fine_ns, qm_formula, color="steelblue", lw=1.4, label="Smooth QM")
    ax.plot(t_fine_ns, floor_nominal_fine, color="gray", lw=1.0, ls="--", label="Paper floor ansatz")
    ax.plot(t_fine_ns, clocked_nominal_fine, color="firebrick", lw=2.0, label="Derived clocked observer")
    ax.set_ylabel("Correlator")
    ax.set_xlim(0.0, args.t_max_ns)
    ax.set_ylim(-1.15, 1.15)
    ax.legend(loc="upper right", fontsize=8.5)
    ax.set_title("Nominal parameters: derived clocked observer matches the paper ansatz")

    ax = axes[1]
    ax.plot(t_fine_ns, clocked_nominal_fine - floor_nominal_fine, color="firebrick", lw=1.5, label="Nominal clocked - floor")
    ax.plot(t_fine_ns, clocked_control_fine - floor_control_fine, color="darkorange", lw=1.5, label=f"Control clocked - floor ({args.control_omega_ghz:.2f} GHz)")
    ax.axhline(0.0, color="black", lw=0.6)
    ax.set_ylabel("Difference")
    ax.set_xlim(0.0, args.t_max_ns)
    ax.legend(loc="upper right", fontsize=8.5)
    ax.set_title("Off-resonant control: agreement is not automatic")

    ax = axes[2]
    bins = np.linspace(
        min(np.min(test_stat_qm), np.min(test_stat_clocked)),
        max(np.max(test_stat_qm), np.max(test_stat_clocked)),
        50,
    )
    ax.hist(test_stat_qm, bins=bins, alpha=0.6, color="steelblue", label="Generated under smooth QM")
    ax.hist(test_stat_clocked, bins=bins, alpha=0.6, color="firebrick", label="Generated under clocked ATR")
    ax.axvline(threshold_99, color="black", lw=1.2, ls="--", label="1% false-positive threshold")
    ax.set_xlabel(r"Test statistic $2(\log L_{\rm clocked} - \log L_{\rm QM,best})$")
    ax.set_ylabel("Pseudo-experiment count")
    ax.legend(loc="upper right", fontsize=8.5)
    ax.set_title(
        f"Empirical discrimination: power at 1% FPR = {power_99:.3f}, "
        f"power at 5% FPR = {power_95:.3f}"
    )

    figure.tight_layout(rect=[0.0, 0.0, 1.0, 0.93])

    out_dir = os.path.dirname(os.path.abspath(__file__))
    figure_path = os.path.join(out_dir, f"{args.output_prefix}.png")
    summary_path = os.path.join(out_dir, f"{args.output_prefix}_summary.json")
    figure.savefig(figure_path, dpi=150, bbox_inches="tight")
    plt.close(figure)

    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print(f"Figure written to {figure_path}")
    print(f"Summary written to {summary_path}")


if __name__ == "__main__":
    main()
