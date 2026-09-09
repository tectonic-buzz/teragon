"""Offline follow-up: code budget, Fourier sectors, calibrated coil unfolding.

Synthetic examples only. No scanner access, acquisition correction claim,
clinical validation, or learned prior. Decoder inputs never include the truth.
"""

import argparse
import json
from pathlib import Path
import platform
import random

import numpy as np

if __package__:
    from . import mri_rs_reference as rs
    from . import mri_transport_benchmark as m
else:
    import mri_rs_reference as rs
    import mri_transport_benchmark as m


def half_masks(size):
    # Keeps centered ky even too: an explicit convention, not an implicit shift.
    if size < 4 or size % 4:
        raise ValueError("Use square grid size divisible by four")
    even = np.zeros((size, size), dtype=bool)
    even[::2] = True
    return even, ~even


def sector(image, sign=1):
    return (image+sign*np.roll(image, image.shape[0]//2, axis=0))/2


def assemble_disjoint_samples(samples, masks):
    """Assemble distinct k-space locations, not add images indiscriminately.

    Same encoding/coil/epoch is a caller's contract. Duplicate locations are
    rejected even when values agree; a separate estimator would need to combine
    repeated noisy measurements. Missing locations remain explicitly zero.
    """
    if not masks or len(samples) != len(masks):
        raise ValueError("One sample vector per mask required")
    result = np.zeros(masks[0].shape, dtype=complex)
    occupied = np.zeros(result.shape, dtype=bool)
    for values, mask in zip(samples, masks):
        mask = np.asarray(mask, dtype=bool)
        values = np.asarray(values, dtype=complex)
        if mask.shape != result.shape or values.shape != (int(mask.sum()),):
            raise ValueError("Sample count or mask shape mismatch")
        if np.any(occupied & mask):
            raise ValueError("Overlapping samples: reject potential double counting")
        result[mask] = values
        occupied |= mask
    return result


def coil_maps(size, independent=True):
    """Deliberately ideal calibration, not measured or engineered hardware."""
    first = np.ones((size, size), dtype=complex)/np.sqrt(2)
    phase = np.exp(2j*np.pi*np.arange(size)/size)[:, None]
    second = np.broadcast_to(phase, first.shape)/np.sqrt(2) if independent else first.copy()
    return np.stack((first, second))


def measure_coils(image, sensitivities, mask):
    return tuple(m.fft2c(sensitivity*image)[mask] for sensitivity in sensitivities)


def unfold_twofold(samples, sensitivities, mask):
    """R=2, even-row, calibrated SENSE-style least-squares unmixing.

    Given only acquired samples, coil maps and mask. No truth, full k-space or
    complementary measurement is supplied. Singular calibration returns the
    minimum-norm member, not a fabricated missing antisymmetric channel.
    """
    size = mask.shape[0]
    expected, _ = half_masks(size)
    if not np.array_equal(mask, expected) or sensitivities.shape[1:] != mask.shape:
        raise ValueError("This reference implements only square even-row R=2")
    if len(samples) != len(sensitivities) or len(samples) < 2:
        raise ValueError("At least two matching coil channels are required")
    aliases = np.stack([m.ifft2c(assemble_disjoint_samples((values,), (mask,)))
                        for values in samples])
    half = size//2
    # At each folded pair, 2*y_c=s_c(y)*x(y)+s_c(y+N/2)*x(y+N/2).
    matrices = np.stack((sensitivities[:, :half], sensitivities[:, half:]), axis=-1)
    matrices = matrices.transpose(1, 2, 0, 3)
    rhs = (2*aliases[:, :half]).transpose(1, 2, 0)
    solution = (np.linalg.pinv(matrices, rcond=1e-12)@rhs[..., None])[..., 0]
    return np.concatenate((solution[..., 0], solution[..., 1]), axis=0)


def coil_operator(size, sensitivities, mask):
    columns = []
    for i in range(size*size):
        basis = np.zeros((size, size), dtype=complex)
        basis.flat[i] = 1
        columns.append(np.concatenate(measure_coils(basis, sensitivities, mask)))
    return np.column_stack(columns)


def fec_comparison(payload, trials=20):
    result = {}
    for nsym, integrity in ((2, "sha256"), (4, "sha256"), (4, "crc32-frame")):
        name = f"rs{nsym}_{integrity}"
        blocks = rs.encode_packet(payload, nsym, integrity)
        wire = sum(map(len, blocks))
        profiles = {}
        for model in ("one_bit_per_word", "capacity_symbols_per_word"):
            successes = 0
            changed = 0
            for trial in range(trials):
                rng = random.Random(20260909+trial)
                damaged = []
                for block in blocks:
                    word = bytearray(block)
                    count = 1 if model == "one_bit_per_word" else nsym//2
                    for position in rng.sample(range(len(word)), count):
                        error = 1 << rng.randrange(8) if model == "one_bit_per_word" else rng.randrange(1, 256)
                        word[position] ^= error
                        changed += 1
                    damaged.append(bytes(word))
                successes += rs.decode_packet(damaged, len(payload), nsym, integrity) == payload
            profiles[model] = {"identical_packets": successes, "trials": trials, "changed_symbols": changed}
        # Paired comparison: identical fault positions in the ORIGINAL user data,
        # one per 256-byte legacy frame. Reframing can put two in one RS word.
        chunk = 255-nsym-(4 if integrity == "crc32-frame" else 0)
        successes = rejections = wrong_releases = max_errors = 0
        for trial in range(trials):
            rng = random.Random(20260909+trial)
            damaged = [bytearray(block) for block in blocks]
            errors_per_word = [0]*len(blocks)
            for offset in range(0, len(payload), 256):
                position = offset+rng.randrange(min(256, len(payload)-offset))
                word, local_position = divmod(position, chunk)
                damaged[word][local_position] ^= rng.randrange(1, 256)
                errors_per_word[word] += 1
            max_errors = max(max_errors, max(errors_per_word))
            recovered = rs.decode_packet(damaged, len(payload), nsym, integrity)
            successes += recovered == payload
            rejections += recovered is None
            wrong_releases += recovered is not None and recovered != payload
        profiles["same_payload_positions_one_error_per_legacy_256B_frame"] = {
            "identical_packets": successes, "rejected_packets": rejections,
            "wrong_payload_releases": wrong_releases, "trials": trials,
            "maximum_errors_in_one_rs_word": max_errors,
        }
        result[name] = {
            "user_bytes": len(payload), "wire_bytes": wire, "codewords": len(blocks),
            "overhead_bytes": wire-len(payload), "overhead_percent_of_user": 100*(wire-len(payload))/len(payload),
            "correctable_symbols_per_word": nsym//2,
            "integrity_is_inband_rs_protected": True, "fault_models": profiles,
        }
    return result


def fourier_checks(image):
    even, odd = half_masks(len(image))
    full = m.fft2c(image)
    plus = m.ifft2c(assemble_disjoint_samples((full[even],), (even,)))
    minus = m.ifft2c(assemble_disjoint_samples((full[odd],), (odd,)))
    joined = m.ifft2c(assemble_disjoint_samples((full[even], full[odd]), (even, odd)))
    overlap = np.vdot(image, np.roll(image, len(image)//2, axis=0))/np.vdot(image, image)
    try:
        assemble_disjoint_samples((full[even], full[even]), (even, even))
    except ValueError:
        overlap_rejected = True
    else:
        overlap_rejected = False
    real = image.real
    real_lost = real-sector(real)
    return {
        "nrmse_plus_vs_projector_formula": m.nrmse(plus, sector(image)),
        "nrmse_minus_vs_projector_formula": m.nrmse(minus, sector(image, -1)),
        "nrmse_joined_vs_input": m.nrmse(joined, image),
        "relative_plus_minus_inner_product": float(abs(np.vdot(plus, minus))/np.vdot(image, image).real),
        "fold_nrmse": m.nrmse(plus, image),
        "predicted_fold_nrmse": float(np.sqrt((1-overlap.real)/2)),
        "half_shift_overlap_r": float(overlap.real),
        "adding_same_half_twice_nrmse": m.nrmse(plus+plus, image),
        "adding_same_full_image_twice_nrmse": m.nrmse(image+image, image),
        "duplicate_samples_rejected": overlap_rejected,
        "real_image_missing_channel_norm": float(np.linalg.norm(real_lost)),
        "real_image_missing_channel_measured_norm": float(np.linalg.norm(m.fft2c(real_lost)[even])),
        "zeta_H_0": int(even.sum()), "kernel_dimension": int(odd.sum()),
    }


def coil_checks(image):
    size = len(image)
    even, _ = half_masks(size)
    good = coil_maps(size)
    measured = measure_coils(image, good, even)
    reconstructed = unfold_twofold(measured, good, even)
    # Repeating a coil is not an extra independent measurement.
    repeated = coil_maps(size, independent=False)
    same_samples = measure_coils(image, repeated, even)
    unresolved = unfold_twofold(same_samples, repeated, even)
    # Calibration error: preserve raw data, use the wrong sensitivity phase.
    wrong = good.copy()
    wrong[1] *= np.exp(.15j)
    miscalibrated = unfold_twofold(measured, wrong, even)
    rng = np.random.default_rng(20260909)
    sigma = .01
    noise = tuple(sigma/np.sqrt(2)*(rng.normal(size=a.shape)+1j*rng.normal(size=a.shape)) for a in measured)
    noisy = unfold_twofold(tuple(a+b for a, b in zip(measured, noise)), good, even)
    # Independent rank readout from a small explicit E, not the large-image formula.
    small_mask, _ = half_masks(8)
    spectra = {}
    for independent in (True, False):
        operator = coil_operator(8, coil_maps(8, independent), small_mask)
        spectra["independent" if independent else "duplicate"] = m.spectral_summary(np.linalg.eigvalsh(operator.conj().T@operator))
    # Same rank can conceal arbitrarily large inverse noise gain.
    local = {}
    for name, matrix in (("orthogonal", np.array([[1, 1], [1, -1]])/np.sqrt(2)),
                         ("almost_duplicate", np.array([[1, 1], [1, 1.001]])/np.sqrt(2))):
        eigenvalues = np.linalg.eigvalsh(matrix.T@matrix)
        local[name] = {**m.spectral_summary(eigenvalues), "condition_number": float(np.linalg.cond(matrix))}
    return {
        "independent_coils_noiseless_nrmse": m.nrmse(reconstructed, image),
        "duplicate_coils_nrmse": m.nrmse(unresolved, image),
        "duplicate_coils_vs_plus_sector_nrmse": m.nrmse(unresolved, sector(image)),
        "wrong_phase_calibration_0_15_rad_nrmse": m.nrmse(miscalibrated, image),
        "noisy_nrmse": m.nrmse(noisy, image),
        "noise_retained_norm": float(np.linalg.norm(noisy-reconstructed)),
        "noise_norm_predicted_for_EstarE_half_identity": float(np.sqrt(2)*np.linalg.norm(np.concatenate(noise))),
        "samples_per_coil": int(even.sum()), "coils": 2, "total_complex_measurements": int(2*even.sum()),
        "explicit_normal_spectra_size8": spectra,
        "local_matrix_conditioning": local,
        "calibration": "Exactly specified artificial sensitivity maps; no hardware validation or independent calibration data.",
    }


def heat_checks():
    n = 16
    identity = np.eye(n)
    shift = np.roll(identity, 1, axis=0)
    laplacian = 2*identity-shift-shift.T
    eigenvalues, vectors = np.linalg.eigh(laplacian)
    time = 2.0
    heat = (vectors*np.exp(-time*eigenvalues))@vectors.T
    flip = np.roll(identity, n//2, axis=0)
    plus, minus = (identity+flip)/2, (identity-flip)/2
    return {
        "time": time, "commutator_norm": float(np.linalg.norm(heat@flip-flip@heat)),
        "minus_to_plus_leakage_norm": float(np.linalg.norm(plus@heat@minus)),
        "heat_matrix_condition_number": float(np.linalg.cond(heat)),
        "inverse_highest_mode_gain": float(np.exp(time*eigenvalues[-1])),
        "zeta_L_0": m.spectral_summary(eigenvalues)["zeta_at_0"],
        "interpretation": "Finite heat smoothing preserves symmetry sectors; inversion amplifies noise, not ramification removal.",
    }


def goldilocks_checks():
    p = 2**64-2**32+1
    factors = (2, 3, 5, 17, 257, 65537)
    import math
    prime_certificate = (p-1 == 2**32*3*5*17*257*65537 and pow(7, p-1, p) == 1
                         and all(math.gcd(pow(7, (p-1)//q, p)-1, p) == 1 for q in factors))
    inverse_two = (p+1)//2
    rng = random.Random(20260909)
    successes = 0
    for _ in range(1000):
        a, b = rng.randrange(p), rng.randrange(p)
        total, difference = (a+b) % p, (a-b) % p
        restored = ((total+difference)*inverse_two % p, (total-difference)*inverse_two % p)
        successes += restored == (a, b)
    return {
        "modulus": p, "lucas_prime_certificate_base7": prime_certificate,
        "inverse_two": inverse_two, "exact_sum_difference_roundtrips": successes, "trials": 1000,
        "sum_only_collision": [[1, 4], [2, 3]],
        "same_sum": (1+4) % p == (2+3) % p,
        "modular_wrap_collision": 1 % p == (1+p) % p,
        "interpretation": "An odd field makes the two-channel Fourier matrix invertible; it does not supply a missing channel or recover unbounded integers.",
    }


def run_checks():
    _, arrays = m.scenario()
    payload, _ = m.quantize_complex(arrays["acquired_kspace"])
    damaged_delta = m.fft2c(arrays["damaged_transport"]-arrays["sender_baseline"])
    image_delta = arrays["damaged_transport"]-arrays["sender_baseline"]
    return {
        "scope": "Offline synthetic transport and calibrated Fourier tests; not clinical MRI validation.",
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "seed": 20260909,
        "fec": fec_comparison(payload),
        "fourier_noiseless": fourier_checks(arrays["truth"]),
        "fourier_sender": fourier_checks(arrays["sender_baseline"]),
        "transport_error_parseval_norm_ratio": float(np.linalg.norm(damaged_delta)/np.linalg.norm(image_delta)),
        "coils": coil_checks(arrays["truth"]),
        "heat": heat_checks(),
        "goldilocks": goldilocks_checks(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("mri_benchmark")/"followup_results.json")
    args = parser.parse_args()
    result = run_checks()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+"\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
