"""Diagnostic EPI toy: constant odd/even phase, not a scanner implementation.

Separates readout ordering, phase calibration, sampling and transport FEC.
The existing reconstruction/codec implementations are not changed.
"""

import json
from pathlib import Path

import numpy as np

if __package__:
    from . import mri_followup_checks as f
else:
    import mri_followup_checks as f

m, rs = f.m, f.rs


def reverse_odd_rows(values):
    """Known coordinate permutation; no identification of sample points."""
    result = values.copy()
    result[1::2] = result[1::2, ::-1]
    return result


def odd_phase(values, phi):
    result = values.copy()
    result[1::2] *= np.exp(1j*phi)
    return result


def acquire(image, phi=0.0):
    return reverse_odd_rows(odd_phase(m.fft2c(image), phi))


def reconstruct(raw, phi_estimate):
    """Apply an explicit finite real calibration in radians.

    Zero explicitly bypasses correction; missing calibration is not zero.
    Checking the parameter's format cannot establish that its value is right.
    Inputs never include a target image.
    """
    phase = np.asarray(phi_estimate)
    if phase.ndim != 0 or phase.dtype.kind not in "iuf" or not np.isfinite(phase):
        raise ValueError("Explicit finite real phase in radians required; use 0 to bypass")
    return m.ifft2c(odd_phase(reverse_odd_rows(raw), -float(phase)))


def mix_pair(image, delta):
    """Same map as Fourier-domain odd-row phase; T swaps half-FOV partners."""
    u = np.exp(1j*delta)
    return ((1+u)*image+(1-u)*np.roll(image, len(image)//2, axis=0))/2


def parity_images(raw):
    kspace = reverse_odd_rows(raw)
    even, odd = f.half_masks(len(kspace))
    return (m.ifft2c(np.where(even, kspace, 0)),
            m.ifft2c(np.where(odd, kspace, 0)))


def estimate_from_known_unoverlapped_region(raw, region):
    """Conditional estimator, NOT a method for discovering a valid region.

    Assumes Tx=0 on the supplied object region, constant odd/even phase, and
    nonzero signal. Perfect correlation does not prove the support assumption.
    """
    even_image, odd_image = parity_images(raw)
    a, b = even_image[region], odd_image[region]
    scale = np.linalg.norm(a)*np.linalg.norm(b)
    correlation = np.vdot(a, b)
    if scale == 0 or abs(correlation) <= 1e-12*scale:
        return None, 0.0
    return float(np.angle(correlation)), float(abs(correlation)/scale)


def entropy(image):
    energy = np.abs(image)**2
    p = energy.ravel()/energy.sum()
    p = p[p > 0]
    return float(-np.sum(p*np.log(p)))


def run_probe():
    image = m.phantom(64)
    scenarios = {}
    for name, actual, estimate in (
        ("clean_no_correction", 0, 0),
        ("clean_wrong_correction", 0, .05),
        ("error_correction_bypassed", .6, 0),
        ("correct_phase", .6, .6),
        ("residual_phase_0_05", .6, .55),
        ("overcorrection", .6, 1.5),
        ("half_fov_swap", np.pi, 0),
    ):
        output = reconstruct(acquire(image, actual), estimate)
        delta = actual-estimate
        main = abs(np.cos(delta/2))
        ghost = abs(np.sin(delta/2))
        scenarios[name] = {
            "actual_phase": actual, "applied_estimate": estimate,
            "residual_phase": delta, "complex_nrmse": m.nrmse(output, image),
            "pair_formula_nrmse": m.nrmse(output, mix_pair(image, delta)),
            "norm_ratio": float(np.linalg.norm(output)/np.linalg.norm(image)),
            "main_coefficient_magnitude": main, "ghost_coefficient_magnitude": ghost,
            "ghost_main_coefficient_ratio": ghost/main if main > 1e-14 else None,
        }

    raw = acquire(image, .6)
    alternative_phase = .2
    alternative_image = reconstruct(raw, alternative_phase)
    raw_alternative = acquire(alternative_image, alternative_phase)
    swapped = np.roll(image, len(image)//2, axis=0)
    ambiguity = {
        "phase_a": .6, "phase_b": alternative_phase,
        "images_nrmse": m.nrmse(alternative_image, image),
        "raw_samples_nrmse": m.nrmse(raw_alternative, raw),
        "swap_and_add_pi_raw_nrmse": m.nrmse(acquire(swapped, .6+np.pi), raw),
        "entropy_original": entropy(image), "entropy_shifted": entropy(swapped),
    }

    # A small support declared before measurement: its half-FOV partner is empty.
    region = np.zeros((64, 64), dtype=bool)
    region[4:20, 16:48] = True
    rng = np.random.default_rng(20260909)
    restricted = np.zeros_like(image)
    restricted[region] = 1+.1*(rng.normal(size=region.sum())+1j*rng.normal(size=region.sum()))
    restricted_raw = acquire(restricted, .6)
    estimate, coherence = estimate_from_known_unoverlapped_region(restricted_raw, region)
    global_estimate, global_coherence = estimate_from_known_unoverlapped_region(restricted_raw, np.ones_like(region))
    # Violate the support assumption without reducing observed coherence.
    violated = restricted+1j*np.roll(restricted, 32, axis=0)
    violated_raw = acquire(violated, .6)
    wrong_estimate, wrong_coherence = estimate_from_known_unoverlapped_region(violated_raw, region)
    conditional = {
        "true_phase": .6, "estimated_phase": estimate,
        "coherence": coherence,
        "reconstruction_nrmse": m.nrmse(reconstruct(restricted_raw, estimate), restricted),
        "all_image_estimate": global_estimate, "all_image_coherence": global_coherence,
        "violated_support_estimated_phase": wrong_estimate,
        "violated_support_coherence": wrong_coherence,
        "violated_support_reconstruction_nrmse": m.nrmse(reconstruct(violated_raw, wrong_estimate), violated),
    }

    # Exact tile permutation changes coordinates, not the missing dimension.
    mask, _ = f.half_masks(8)
    operator = m.explicit_fourier_operator(8, mask)
    tiles = np.arange(64).reshape(8, 8).reshape(2, 4, 2, 4).transpose(0, 2, 1, 3).reshape(4, 4, 4)
    permutation = np.concatenate([np.rot90(tiles[i], turns).ravel()
                                 for i, turns in ((2, 1), (0, 2), (3, 3), (1, 0))])
    repacked = operator[:, permutation]
    before = np.linalg.eigvalsh(operator.conj().T@operator)
    after = np.linalg.eigvalsh(repacked.conj().T@repacked)
    # Full acquisition with any phase remains unitary: normal-spectrum zeta blind.
    full_normal_errors = []
    for phi in (0, .05, .6, np.pi):
        full_operator = np.column_stack([acquire(np.eye(64, dtype=complex)[:, i].reshape(8, 8), phi).ravel()
                                         for i in range(64)])
        full_normal_errors.append(float(np.linalg.norm(full_operator.conj().T@full_operator-np.eye(64))))

    return {
        "scope": "Noiseless constant-phase EPI diagnostic; not clinical validation or implemented production fix.",
        "phase_scenarios": scenarios, "unknown_phase_ambiguity": ambiguity,
        "conditional_one_correlation_estimator": conditional,
        "tile_permutation": {"before": m.spectral_summary(before), "after": m.spectral_summary(after),
                             "max_normal_spectral_change": float(np.max(np.abs(before-after))),
                             "literal_14_piece_stomachion_enumeration": False},
        "full_acquisition_zeta": {"zeta_H_any_s": 64, "normal_identity_errors": full_normal_errors},
    }


if __name__ == "__main__":
    result = run_probe()
    path = Path(__file__).with_name("mri_benchmark")/"epi_phase_probe.json"
    path.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(json.dumps(result, indent=2, allow_nan=False))
