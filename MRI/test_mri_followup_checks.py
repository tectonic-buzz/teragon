"""Audit addition, independent receiver inputs, sectors, and calibration."""

from pathlib import Path
import unittest
from unittest.mock import patch

try:
    import numpy as np
except ImportError as exc:
    raise unittest.SkipTest("Follow-up requires NumPy; use bundled Python") from exc

if __package__:
    from . import mri_followup_checks as f
else:
    import mri_followup_checks as f

m, rs = f.m, f.rs


class FourierAndAddition(unittest.TestCase):
    def test_fft_matches_direct_matrix_dft_for_new_complex_data(self):
        n = 8
        rng = np.random.default_rng(20260913)
        x = rng.normal(size=(n, n))+1j*rng.normal(size=(n, n))
        coordinates = np.arange(n)-n//2
        matrix = np.exp(-2j*np.pi*np.outer(coordinates, coordinates)/n)/np.sqrt(n)
        direct = matrix@x@matrix.T
        np.testing.assert_allclose(m.fft2c(x), direct, atol=1e-14)
        np.testing.assert_allclose(m.ifft2c(direct), x, atol=1e-14)

    def test_sectors_are_orthogonal_not_two_copies_of_input(self):
        rng = np.random.default_rng(20260914)
        for n in (8, 16, 64):
            x = rng.normal(size=(n, n))+1j*rng.normal(size=(n, n))
            plus, minus = f.sector(x), f.sector(x, -1)
            np.testing.assert_allclose(plus+minus, x, atol=1e-14)
            self.assertLess(abs(np.vdot(plus, minus)), 1e-11)
            self.assertAlmostEqual(np.linalg.norm(plus)**2+np.linalg.norm(minus)**2,
                                   np.linalg.norm(x)**2, places=10)
            np.testing.assert_allclose(f.sector(plus), plus, atol=1e-14)
            self.assertLess(np.linalg.norm(f.sector(minus)), 1e-13)

    def test_masks_match_projectors_and_join_without_double_count(self):
        x = m.phantom(32)
        k = m.fft2c(x)
        even, odd = f.half_masks(32)
        plus = m.ifft2c(f.assemble_disjoint_samples((k[even],), (even,)))
        minus = m.ifft2c(f.assemble_disjoint_samples((k[odd],), (odd,)))
        np.testing.assert_allclose(plus, f.sector(x), atol=1e-14)
        np.testing.assert_allclose(minus, f.sector(x, -1), atol=1e-14)
        joined = f.assemble_disjoint_samples((k[even], k[odd]), (even, odd))
        np.testing.assert_array_equal(joined, k)
        self.assertLess(m.nrmse(m.ifft2c(joined), x), 1e-14)

    def test_duplicate_locations_are_rejected_not_added(self):
        even, _ = f.half_masks(16)
        data = np.ones(even.sum(), dtype=complex)
        with self.assertRaisesRegex(ValueError, "Overlapping"):
            f.assemble_disjoint_samples((data, data), (even, even))

    def test_invalid_sample_counts_rejected(self):
        even, _ = f.half_masks(16)
        for values in (np.zeros(even.sum()-1), np.zeros(even.shape)):
            with self.assertRaises(ValueError):
                f.assemble_disjoint_samples((values,), (even,))

    def test_double_sum_is_a_hundred_percent_error_not_recovery(self):
        x = m.phantom(64)
        self.assertAlmostEqual(m.nrmse(x+x, x), 1)
        self.assertAlmostEqual(m.nrmse(2*f.sector(x), x), 1)

    def test_phase_cancellation_requires_complex_signed_channels(self):
        x = np.zeros((16, 16), dtype=complex)
        x[1, 3] = 2+3j
        plus, minus = f.sector(x), f.sector(x, -1)
        self.assertNotEqual(plus[9, 3], 0)
        self.assertEqual((plus+minus)[9, 3], 0)
        self.assertGreater((np.abs(plus)+np.abs(minus))[9, 3], 0)
        self.assertGreater(m.nrmse(np.abs(plus)+np.abs(minus), np.abs(x)), .9)

    def test_real_nonnegative_images_are_ambiguous_under_alternate_rows(self):
        # Even positivity and reality do not supply the missing odd rows.
        a = np.zeros((16, 16))
        b = a.copy()
        a[1, 2], b[9, 2] = 1, 1
        even, _ = f.half_masks(16)
        np.testing.assert_allclose(m.fft2c(a)[even], m.fft2c(b)[even], atol=1e-14)
        self.assertGreater(np.linalg.norm(a-b), 1)
        self.assertTrue(all((-k) % 16 % 2 == k % 2 for k in range(16)))

    def test_overlap_formula_and_pseudoinverse(self):
        rng = np.random.default_rng(20260915)
        x = rng.normal(size=(8, 8))+1j*rng.normal(size=(8, 8))
        even, _ = f.half_masks(8)
        operator = m.explicit_fourier_operator(8, even)
        minimum_norm = (np.linalg.pinv(operator)@(operator@x.ravel())).reshape(x.shape)
        np.testing.assert_allclose(minimum_norm, f.sector(x), atol=1e-13)
        overlap = np.vdot(x, np.roll(x, 4, axis=0)).real/np.vdot(x, x).real
        self.assertAlmostEqual(m.nrmse(minimum_norm, x)**2, (1-overlap)/2)

    def test_corruption_energy_is_not_amplified_by_fourier(self):
        _, arrays = m.scenario()
        image_error = arrays["damaged_transport"]-arrays["sender_baseline"]
        self.assertAlmostEqual(np.linalg.norm(image_error), np.linalg.norm(m.fft2c(image_error)), places=10)
        impulse = np.zeros((16, 16), dtype=complex)
        impulse[2, 3] = 1j
        wave = m.ifft2c(impulse)
        self.assertEqual(np.count_nonzero(impulse), 1)
        self.assertEqual(np.count_nonzero(np.abs(wave) > 1e-14), 256)
        self.assertAlmostEqual(np.linalg.norm(wave), 1)

    def test_receiver_has_no_phantom_input_and_does_not_reuse_one(self):
        rng = np.random.default_rng(20260916)
        for x in (np.zeros((16, 16), dtype=complex),
                  rng.normal(size=(16, 16))+1j*rng.normal(size=(16, 16)),
                  1j*np.eye(16)):
            payload, layout = m.quantize_complex(m.fft2c(x))
            references = m.protect_payload(payload)
            damaged, _ = m.corrupt_one_byte_per_frame(payload, rng)
            wire = rs.encode_packet(payload, 4)
            with patch.object(m, "phantom", side_effect=AssertionError("No truth in receiver")):
                recovered = m.recover_payload(damaged, references).payload
                decoded = rs.decode_packet(wire, len(payload), 4)
                self.assertEqual(recovered, payload)
                self.assertEqual(decoded, payload)
                reconstruction = m.ifft2c(m.unpack_complex(decoded, layout))
            baseline = m.ifft2c(m.unpack_complex(payload, layout))
            np.testing.assert_array_equal(reconstruction, baseline)
            self.assertFalse(np.shares_memory(reconstruction, x))


class CoilUnfolding(unittest.TestCase):
    def test_independent_coils_recover_unseen_inputs_with_no_truth_argument(self):
        rng = np.random.default_rng(20260917)
        size = 16
        even, _ = f.half_masks(size)
        maps = f.coil_maps(size)
        inputs = (np.zeros((size, size), dtype=complex),
                  rng.normal(size=(size, size))+1j*rng.normal(size=(size, size)),
                  1j*np.eye(size), m.phantom(size))
        for x in inputs:
            data = f.measure_coils(x, maps, even)
            copies = tuple(a.copy() for a in data)
            with patch.object(m, "phantom", side_effect=AssertionError("No truth in unfolding")):
                restored = f.unfold_twofold(data, maps, even)
            np.testing.assert_allclose(restored, x, atol=1e-13)
            for actual, saved in zip(data, copies):
                np.testing.assert_array_equal(actual, saved)

    def test_duplicate_coils_do_not_fake_missing_channel(self):
        x = m.phantom(32)
        even, _ = f.half_masks(32)
        maps = f.coil_maps(32, False)
        restored = f.unfold_twofold(f.measure_coils(x, maps, even), maps, even)
        np.testing.assert_allclose(restored, f.sector(x), atol=1e-13)
        self.assertGreater(m.nrmse(restored, x), .5)

    def test_block_unfolding_matches_global_pseudoinverse(self):
        rng = np.random.default_rng(20260918)
        x = rng.normal(size=(8, 8))+1j*rng.normal(size=(8, 8))
        even, _ = f.half_masks(8)
        for independent in (True, False):
            maps = f.coil_maps(8, independent)
            operator = f.coil_operator(8, maps, even)
            data = f.measure_coils(x, maps, even)
            by_blocks = f.unfold_twofold(data, maps, even)
            by_global = (np.linalg.pinv(operator)@np.concatenate(data)).reshape(x.shape)
            np.testing.assert_allclose(by_blocks, by_global, atol=1e-13)

    def test_rank_spectra_and_noise_covariance(self):
        even, _ = f.half_masks(8)
        for independent, rank, trace_inverse in ((True, 64, 128), (False, 32, 32)):
            operator = f.coil_operator(8, f.coil_maps(8, independent), even)
            normal = operator.conj().T@operator
            summary = m.spectral_summary(np.linalg.eigvalsh(normal))
            self.assertEqual(summary["zeta_at_0"], rank)
            self.assertAlmostEqual(summary["zeta_at_1"], trace_inverse, places=9)
            self.assertEqual(summary["nullity"], 64-rank)
            if independent:
                np.testing.assert_allclose(normal, np.eye(64)/2, atol=1e-14)
                decoder = np.linalg.pinv(operator)
                np.testing.assert_allclose(decoder@decoder.conj().T, 2*np.eye(64), atol=1e-13)

    def test_noise_is_not_repaired_and_bad_calibration_matters(self):
        result = f.coil_checks(m.phantom(32))
        self.assertLess(result["independent_coils_noiseless_nrmse"], 1e-13)
        self.assertGreater(result["noisy_nrmse"], 0)
        self.assertGreater(result["wrong_phase_calibration_0_15_rad_nrmse"], .05)
        self.assertAlmostEqual(result["noise_retained_norm"], result["noise_norm_predicted_for_EstarE_half_identity"], places=11)

    def test_full_rank_does_not_mean_well_conditioned(self):
        result = f.coil_checks(m.phantom(16))["local_matrix_conditioning"]
        self.assertEqual(result["orthogonal"]["zeta_at_0"], 2)
        self.assertEqual(result["almost_duplicate"]["zeta_at_0"], 2)
        self.assertGreater(result["almost_duplicate"]["condition_number"], 4000)
        self.assertGreater(result["almost_duplicate"]["zeta_at_1"], 8e6)


class HeatAndFiniteField(unittest.TestCase):
    def test_heat_preserves_channels_but_inverse_amplifies(self):
        result = f.heat_checks()
        self.assertLess(result["commutator_norm"], 1e-12)
        self.assertLess(result["minus_to_plus_leakage_norm"], 1e-12)
        self.assertAlmostEqual(result["heat_matrix_condition_number"], np.exp(8), places=7)

    def test_goldilocks_roundtrip_and_limits(self):
        result = f.goldilocks_checks()
        self.assertTrue(result["lucas_prime_certificate_base7"])
        self.assertEqual(result["exact_sum_difference_roundtrips"], 1000)
        self.assertTrue(result["same_sum"])
        self.assertTrue(result["modular_wrap_collision"])

    def test_characteristic_two_sign_channel_collapses_but_rs_does_not(self):
        self.assertEqual((1+1) % 2, (1-1) % 2)
        data = b"Two locators need not be plus and minus one"
        encoded = bytearray(rs.encode(data, 2))
        encoded[2] ^= 128
        self.assertEqual(rs.decode(encoded, 2), data)


class Reframing(unittest.TestCase):
    def test_one_error_per_old_frame_can_be_two_in_a_new_codeword(self):
        payload = bytes(range(256))*3
        for nsym in (2, 4):
            blocks = [bytearray(word) for word in rs.encode_packet(payload, nsym)]
            chunk = 255-nsym
            for position, error in ((255, 1), (256, 3)):
                word, index = divmod(position, chunk)
                blocks[word][index] ^= error
            recovered = rs.decode_packet(blocks, len(payload), nsym)
            if nsym == 2:
                self.assertIsNone(recovered)
            else:
                self.assertEqual(recovered, payload)


class SavedImages(unittest.TestCase):
    def test_saved_pngs_and_montage_are_not_added_or_blended(self):
        try:
            from PIL import Image
        except ImportError as exc:
            raise unittest.SkipTest("Saved preview audit requires Pillow") from exc
        directory = Path(__file__).with_name("mri_benchmark")
        if not (directory/"primary_arrays.npz").is_file():
            self.skipTest("Generate the original benchmark fixtures first")
        with np.load(directory/"primary_arrays.npz") as arrays:
            names = ("truth", "sender_baseline", "damaged_transport", "recovered_transport",
                     "half_sampling", "complementary_acquisition")
            self.assertEqual(arrays["truth"].shape, (64, 64))
            peak = np.abs(arrays["truth"]).max()
            with Image.open(directory/"reconstructions.png") as montage:
                for index, name in enumerate(names):
                    expected = np.rint(255*np.clip(np.abs(arrays[name])/peak, 0, 1)).astype(np.uint8)
                    with Image.open(directory/f"{name}.png") as panel:
                        np.testing.assert_array_equal(np.asarray(panel), expected)
                    x, y = 24+(index % 3)*320, 82+(index//3)*340+26
                    actual = np.asarray(montage.crop((x, y, x+256, y+256)))
                    expanded = np.repeat(np.repeat(expected, 4, axis=0), 4, axis=1)
                    np.testing.assert_array_equal(actual, np.repeat(expanded[..., None], 3, axis=2))


if __name__ == "__main__":
    unittest.main()
