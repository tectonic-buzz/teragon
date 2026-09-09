"""Synthetic complex Fourier imaging: acquisition != digital transport.

Research fixture, NOT scanner software, an MR physics simulator, or a clinical
reconstruction method. NumPy is required; Pillow only exports preview images.
The two exact zeta/moment checks reuse the previously audited byte decoder.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
import hashlib
import json
import math
from pathlib import Path
import platform
import time

import numpy as np

if __package__:
    from .test_mobius_fourier_readout import (
        decode_one_error_from_zeta_channels, zeta_check_channels,
    )
else:
    from test_mobius_fourier_readout import (
        decode_one_error_from_zeta_channels, zeta_check_channels,
    )


FRAME_BYTES = 256
DEFAULT_SEED = 20260909


@dataclass(frozen=True)
class ComplexLayout:
    """Trusted header; its own transmission/protection is outside this fixture."""

    shape: tuple[int, int]
    scale: float
    dtype: str = "<i2"
    components: str = "real,imag interleaved; C order"


@dataclass(frozen=True)
class FrameReference:
    """Trusted c0, c1 and digest. This class does NOT protect their transport."""

    length: int
    moments: tuple[int, int]
    digest: bytes


@dataclass(frozen=True)
class Recovery:
    payload: bytes | None
    statuses: tuple[str, ...]


class FrameRejected(ValueError):
    pass


def fft2c(image):
    return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(image), norm="ortho"))


def ifft2c(kspace):
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(kspace), norm="ortho"))


def phantom(size=64):
    """Original deterministic ellipse fixture, not an anatomical patient image."""
    if size < 16 or size % 2:
        raise ValueError("Use an even image size >= 16")
    axis = np.linspace(-1, 1, size, endpoint=False)
    xx, yy = np.meshgrid(axis, axis)
    magnitude = np.zeros((size, size))
    ellipses = (
        (0, 0, .76, .91, .18),
        (0, -.04, .61, .75, .35),
        (-.25, -.25, .16, .22, .42),
        (.27, -.04, .13, .35, .25),
        (-.13, .45, .22, .09, .36),
        (.32, .51, .065, .065, .47),
    )
    for cx, cy, rx, ry, value in ellipses:
        magnitude[((xx-cx)/rx)**2 + ((yy-cy)/ry)**2 <= 1] += value
    magnitude /= magnitude.max()
    phase = .9*xx - .7*yy + .3*xx*yy
    return magnitude * np.exp(1j*phase)


def nrmse(actual, reference):
    denominator = float(np.linalg.norm(reference))
    if denominator == 0:
        raise ValueError("NRMSE needs a nonzero reference")
    return float(np.linalg.norm(actual-reference) / denominator)


def quantize_complex(kspace):
    """One acquisition-storage conversion, not repeated magnitude/arg casts."""
    if kspace.ndim != 2 or not np.isfinite(kspace).all():
        raise ValueError("Finite two-dimensional complex data required")
    components = np.stack((kspace.real, kspace.imag), axis=-1)
    peak = float(np.max(np.abs(components)))
    scale = peak/30000 if peak else 1.0  # Keep headroom; never saturate silently.
    rounded = np.rint(components/scale)
    if np.max(np.abs(rounded)) > 32767:
        raise ValueError("Storage range exceeded")
    return rounded.astype("<i2").tobytes(), ComplexLayout(kspace.shape, scale)


def unpack_complex(payload, layout):
    if layout.dtype != "<i2" or layout.components != "real,imag interleaved; C order":
        raise ValueError("Unknown encoding")
    if not math.isfinite(layout.scale) or layout.scale <= 0:
        raise ValueError("Invalid scale")
    expected = math.prod(layout.shape)*4
    if len(payload) != expected:
        raise ValueError("Payload length does not match protected shape")
    parts = np.frombuffer(payload, dtype="<i2").astype(np.float64)
    parts = parts.reshape(*layout.shape, 2)*layout.scale
    return parts[..., 0]+1j*parts[..., 1]


def digest_frame(data, index):
    # Bind both position and length. No secret: integrity check, NOT a MAC.
    context = index.to_bytes(8, "little")+len(data).to_bytes(4, "little")
    return hashlib.sha256(context+data).digest()


def protect_payload(payload, frame_bytes=FRAME_BYTES):
    """Generate reference values, not a protected wire channel for those values.

    The legacy function name describes the payload checks only. Callers must
    independently preserve all references, the frame order, and the layout.
    """
    if not payload or frame_bytes <= 0:
        raise ValueError("Positive frame length and nonempty payload required")
    return tuple(
        FrameReference(len(frame), zeta_check_channels(frame), digest_frame(frame, i))
        for i, offset in enumerate(range(0, len(payload), frame_bytes))
        for frame in (payload[offset:offset+frame_bytes],)
    )


def recover_payload(received, references):
    """Receiver gets only received bytes + trusted references, never clean data.

    Correct <=1 changed byte per frame. More errors can mimic a valid syndrome;
    SHA-256 is a separate practical integrity check, not an absolute proof.
    A rejected frame prevents release of an image from this packet.
    Every reference includes trusted c0, c1, digest and length; this function
    neither repairs those references nor authenticates their origin.
    """
    if len(received) != sum(ref.length for ref in references):
        raise FrameRejected("Packet truncated or expanded")
    output, statuses = [], []
    offset = 0
    for index, ref in enumerate(references):
        frame = received[offset:offset+ref.length]
        offset += ref.length
        try:
            candidate = bytes(decode_one_error_from_zeta_channels(frame, ref.moments))
        except ValueError:
            candidate = None
        if candidate is None or digest_frame(candidate, index) != ref.digest:
            statuses.append("rejected")
        else:
            statuses.append("unchanged" if candidate == frame else "corrected")
            output.append(candidate)
    return Recovery(None if "rejected" in statuses else b"".join(output), tuple(statuses))


def corrupt_one_byte_per_frame(payload, rng, frame_bytes=FRAME_BYTES):
    result = bytearray(payload)
    positions = []
    for offset in range(0, len(payload), frame_bytes):
        position = offset+int(rng.integers(min(frame_bytes, len(payload)-offset)))
        result[position] = (result[position]+int(rng.integers(1, 256))) % 256
        positions.append(position)
    return bytes(result), positions


def reference_storage_bytes(frame_bytes=FRAME_BYTES):
    """Minimum fixed-width unsigned storage of the two checks + SHA-256.

    Excludes frame ids, lengths, layout, authentication and reference protection.
    """
    maxima = (256*frame_bytes, 128*frame_bytes*(frame_bytes+1))
    return sum((maximum.bit_length()+7)//8 for maximum in maxima)+32


def spectral_summary(eigenvalues, tolerance=1e-10):
    """Finite-dimensional PSD spectrum, with zeros omitted in zeta.

    Exactly: zeta_H(0)=rank(H); if H=E*E, nullity(E)=n-rank(H). No projection
    assumption. Numerically this counts eigenvalues > tolerance, which is not
    a certificate that the discarded eigenvalues are mathematically zero.
    zeta_H(1)=tr(H^+) also depends on nonzero eigenvalue magnitudes.
    """
    values = np.asarray(eigenvalues, dtype=float)
    if np.min(values) < -tolerance:
        raise ValueError("A positive semidefinite normal operator is required")
    positive = values[values > tolerance]
    return {
        "input_dimension": int(values.size),
        "zeta_at_0": int(positive.size),
        "zeta_at_1": float(np.sum(1/positive)),
        "nullity": int(values.size-positive.size),
        "eigenvalue_tolerance": tolerance,
    }


def sampling_summary(mask):
    # Special-case shortcut, NOT a hypothesis of the general rank identity:
    # F unitary and P selects distinct rows => F*P*PF has this 0/1 spectrum.
    return spectral_summary(np.asarray(mask, dtype=float).ravel())


def explicit_fourier_operator(size, mask):
    """Small independent construction, to audit the analytic rank shortcut."""
    columns = []
    for j in range(size*size):
        basis = np.zeros((size, size), dtype=complex)
        basis.flat[j] = 1
        columns.append(fft2c(basis)[mask])
    return np.column_stack(columns)


def scenario(seed=DEFAULT_SEED, size=64, snr_db=40):
    rng = np.random.default_rng(seed)
    image = phantom(size)
    clean_k = fft2c(image)
    sigma = np.linalg.norm(clean_k)/math.sqrt(clean_k.size)*10**(-snr_db/20)
    noise = sigma/math.sqrt(2)*(rng.normal(size=image.shape)+1j*rng.normal(size=image.shape))
    acquired_k = clean_k+noise

    # References are captured AFTER acquisition noise and quantization.
    payload, layout = quantize_complex(acquired_k)
    references = protect_payload(payload)
    baseline_k = unpack_complex(payload, layout)
    baseline = ifft2c(baseline_k)
    damaged, positions = corrupt_one_byte_per_frame(payload, rng)
    started = time.perf_counter()
    recovered = recover_payload(damaged, references)
    decoder_seconds = time.perf_counter()-started
    if recovered.payload != payload:
        raise AssertionError("One-byte-per-frame recovery did not reproduce sender bytes")
    restored = ifft2c(unpack_complex(recovered.payload, layout))
    damaged_image = ifft2c(unpack_complex(damaged, layout))

    # Second layer: acquisition missing alternate ky rows. FEC cannot supply them.
    full_mask = np.ones(image.shape, dtype=bool)
    half_mask = full_mask.copy()
    half_mask[1::2] = False
    observed_k = np.where(half_mask, baseline_k, 0)
    half = ifft2c(observed_k)
    # Receiver needs an ACTUAL second acquisition here, represented by the
    # otherwise withheld complementary samples of the same frozen object.
    complementary_k = np.where(~half_mask, baseline_k, 0)
    reacquired = ifft2c(observed_k+complementary_k)

    # Construct an indistinguishable alternative without touching acquired rows.
    hidden_k = np.zeros_like(clean_k)
    hidden_k[1, size//4] = .25*np.linalg.norm(image)
    hidden_image = ifft2c(hidden_k)
    ambiguity = float(np.linalg.norm(hidden_k[half_mask]))

    frames = len(references)
    arrays = {
        "truth": image, "sender_baseline": baseline,
        "damaged_transport": damaged_image, "recovered_transport": restored,
        "half_sampling": half, "complementary_acquisition": reacquired,
        "acquired_kspace": acquired_k, "quantized_kspace": baseline_k,
        "half_mask": half_mask, "unobservable_perturbation": hidden_image,
    }
    metrics = {
        name: {
            "complex_nrmse_vs_truth": nrmse(arrays[name], image),
            "magnitude_nrmse_vs_truth": nrmse(np.abs(arrays[name]), np.abs(image)),
            "complex_nrmse_vs_sender": nrmse(arrays[name], baseline),
        }
        for name in ("sender_baseline", "damaged_transport", "recovered_transport",
                     "half_sampling", "complementary_acquisition")
    }
    result = {
        "seed": seed, "shape": [size, size], "expected_snr_db": snr_db,
        "realized_snr_db": float(20*np.log10(np.linalg.norm(clean_k)/np.linalg.norm(noise))),
        "fft_roundtrip_nrmse": nrmse(ifft2c(clean_k), image),
        "quantization_scale": layout.scale,
        "quantization_complex_nrmse": nrmse(baseline_k, acquired_k),
        "metrics": metrics,
        "digital_transport": {
            "payload_bytes": len(payload), "frame_bytes": FRAME_BYTES,
            "frames": frames, "changed_bytes": len(positions),
            "changed_byte_fraction": len(positions)/len(payload),
            "corrected_frames": recovered.statuses.count("corrected"),
            "rejected_frames": recovered.statuses.count("rejected"),
            "byte_identical_recovery": recovered.payload == payload,
            "payload_sha256": hashlib.sha256(payload).hexdigest(),
            "metadata_bytes_per_full_frame_lower_bound": reference_storage_bytes(),
            "metadata_fraction_lower_bound": reference_storage_bytes()/FRAME_BYTES,
            "decoder_seconds_local_python_not_scanner_benchmark": decoder_seconds,
        },
        "operator_zeta": {
            "full_sampling": sampling_summary(full_mask),
            "corrupted_full_sampling": sampling_summary(full_mask),
            "half_sampling": sampling_summary(half_mask),
            "after_extra_acquisition": sampling_summary(full_mask),
        },
        "ambiguity_control": {
            "unmeasured_perturbation_nrmse": nrmse(image+hidden_image, image),
            "change_to_measured_kspace_norm": ambiguity,
            "extra_complex_samples_needed_for_complement": int((~half_mask).sum()),
            "interpretation": "Non-injective acquisition; known mask/rank cannot recover missing values.",
        },
    }
    return result, arrays


def negative_controls():
    controls = {}
    # Identical two moments, different payload. Old decoder passes it unchanged.
    original, collision = bytes((2, 2, 2, 2)), bytes((3, 0, 3, 2))
    recovered = recover_payload(collision, protect_payload(original))
    controls["two_moment_collision"] = {
        "same_moments": zeta_check_channels(original) == zeta_check_channels(collision),
        "released_payload": recovered.payload is not None,
        "statuses": list(recovered.statuses),
    }
    # Two corruptions masquerade as one: raw decoder outputs another wrong word.
    original, damaged = bytes((2, 2, 2)), bytes((3, 2, 3))
    refs = protect_payload(original)
    raw = decode_one_error_from_zeta_channels(damaged, refs[0].moments)
    recovered = recover_payload(damaged, refs)
    controls["multi_error_miscorrection"] = {
        "moment_decoder_candidate": list(raw),
        "candidate_is_original": bytes(raw) == original,
        "released_payload": recovered.payload is not None,
        "statuses": list(recovered.statuses),
    }
    # A 'protected' checksum of already bad data certifies that bad data.
    prior_damage = bytes((8, 9, 10))
    controls["damage_before_reference"] = {
        "preserved_not_corrected": recover_payload(prior_damage, protect_payload(prior_damage)).payload == prior_damage,
    }
    controls["rank_is_not_conditioning"] = {
        "well_conditioned": spectral_summary([1, 1, 1]),
        "ill_conditioned": spectral_summary([1, 1, .01**2]),
    }
    operator = np.array([[2, 0, 0], [0, .5j, 0]], dtype=complex)
    normal = operator.conj().T@operator
    controls["rank_identity_without_projection"] = {
        "normal_eigenvalues": np.linalg.eigvalsh(normal).tolist(),
        "normal_is_projection": bool(np.allclose(normal@normal, normal)),
        "spectral_summary": spectral_summary(np.linalg.eigvalsh(normal)),
    }
    original = bytes((10, 10, 10, 10))
    ref, = protect_payload(original)
    bad_moments = replace(ref, moments=(ref.moments[0]-1, ref.moments[1]-3))
    untrusted_data = bytes((10, 10, 9, 10))
    controls["reference_channel_outside_guarantee"] = {
        "wrong_moments_intact_digest_released_payload":
            recover_payload(original, (bad_moments,)).payload is not None,
        "coherently_replaced_data_and_references_are_accepted":
            recover_payload(untrusted_data, protect_payload(untrusted_data)).payload == untrusted_data,
        "interpretation": "Detection is not reference repair; coherent replacement needs an independent trust boundary.",
    }
    return controls


def export_reconstructions(arrays, metrics, directory):
    """Scientific image outputs, not an anatomy claim or independently windowed plots.

    Preview contract: compare six 64x64 reconstructions of one synthetic input;
    fixed [0, truth peak] grayscale, nearest-neighbor only, 3x2 panels. No
    per-image contrast tuning. Complex errors are printed, though pixels show
    magnitude only. Actual clipping rates are reported below every image.
    """
    from PIL import Image, ImageDraw, ImageFont

    names = ("truth", "sender_baseline", "damaged_transport", "recovered_transport",
             "half_sampling", "complementary_acquisition")
    labels = ("1. Synthetic input", "2. Noisy + quantized sender", "3. Digital corruption",
              "4. Recovered transport", "5. Half k-space: zero fill", "6. Additional acquisition")
    panel, margin, cell_w, cell_h = 256, 24, 320, 340
    canvas = Image.new("RGB", (3*cell_w+2*margin, 2*cell_h+110), "white")
    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.load_default(size=20)
    font = ImageFont.load_default(size=15)
    small = ImageFont.load_default(size=13)
    draw.text((margin, 16), "Synthetic complex Fourier imaging - not a clinical test", fill="#202020", font=title_font)
    draw.text((margin, 44), "Same grayscale window and scale. Labels report complex NRMSE vs known input.", fill="#404040", font=font)
    peak = float(np.abs(arrays["truth"]).max())
    clipping = {}
    for i, (name, label) in enumerate(zip(names, labels)):
        amplitude = np.abs(arrays[name])
        clipping[name] = float(np.mean(amplitude > peak))
        pixel_array = np.rint(255*np.clip(amplitude/peak, 0, 1)).astype(np.uint8)
        tile = Image.fromarray(pixel_array)
        tile.save(directory/f"{name}.png")
        x, y = margin+(i % 3)*cell_w, 82+(i//3)*cell_h
        draw.text((x, y), label, fill="#202020", font=font)
        canvas.paste(tile.resize((panel, panel), Image.Resampling.NEAREST), (x, y+26))
        error = 0 if name == "truth" else metrics[name]["complex_nrmse_vs_truth"]
        draw.text((x, y+290), f"Complex NRMSE: {100*error:.3f}%", fill="#202020", font=small)
        draw.text((x, y+309), f"Clipped above window: {100*clipping[name]:.2f}%", fill="#404040", font=small)
    canvas.save(directory/"reconstructions.png")
    return clipping


def run_benchmark(seed=DEFAULT_SEED, size=64, runs=20, snr_db=40):
    if runs < 1 or not math.isfinite(snr_db):
        raise ValueError("Positive run count and finite SNR required")
    trials, primary_arrays = [], None
    for i in range(runs):
        result, arrays = scenario(seed+i, size, snr_db)
        trials.append(result)
        if i == 0:
            primary_arrays = arrays
    metrics = {}
    for name in trials[0]["metrics"]:
        values = [trial["metrics"][name]["complex_nrmse_vs_truth"] for trial in trials]
        metrics[name] = {"min": min(values), "mean": float(np.mean(values)), "max": max(values)}
    result = {
        "scope": "Synthetic single-coil discrete Fourier fixture; no patient or scanner data.",
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "runs": runs, "first_seed": seed,
        "primary": trials[0],
        "summary": {
            "byte_identical_recoveries": sum(t["digital_transport"]["byte_identical_recovery"] for t in trials),
            "corrected_frames": sum(t["digital_transport"]["corrected_frames"] for t in trials),
            "complex_nrmse_vs_truth": metrics,
        },
        "negative_controls": negative_controls(),
        "trials": trials,
        "limits": [
            "At most one changed byte per frame; no erasure/insertion/burst guarantee.",
            "Header and reference channel assumed trusted and intact; their protection costs extra.",
            "SHA-256 is an integrity check, not authentication or an absolute non-collision proof.",
            "No removal of acquisition noise, aliasing, motion, field inhomogeneity or coil effects.",
            "Extra-acquisition control has access to genuinely additional samples of a frozen object.",
            "No clinical efficacy, scanner timing, comparison with a vendor codec, or Riemann-zeta benefit established.",
        ],
    }
    return result, primary_arrays


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--runs", type=int, default=20)
    parser.add_argument("--snr-db", type=float, default=40)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent/"mri_benchmark")
    parser.add_argument("--no-images", action="store_true")
    args = parser.parse_args()
    result, arrays = run_benchmark(args.seed, args.size, args.runs, args.snr_db)
    args.output.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.output/"primary_arrays.npz", **arrays)
    if not args.no_images:
        result["preview_clipping_fractions"] = export_reconstructions(arrays, result["primary"]["metrics"], args.output)
    (args.output/"results.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"output": str(args.output.resolve()), "summary": result["summary"],
                      "negative_controls": result["negative_controls"]}, indent=2))


if __name__ == "__main__":
    main()
