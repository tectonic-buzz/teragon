"""End-to-end synthetic imaging checks. NumPy required, no scanner access."""

from dataclasses import replace
import unittest

try:
    import numpy as np
except ImportError as exc:
    raise unittest.SkipTest("MRI benchmark requires NumPy; use the bundled Python runtime") from exc

if __package__:
    from . import mri_transport_benchmark as m
else:
    import mri_transport_benchmark as m


class ComplexAcquisition(unittest.TestCase):
    def test_unitary_roundtrip_and_parseval(self):
        image = m.phantom(32)
        self.assertLess(m.nrmse(m.ifft2c(m.fft2c(image)), image), 1e-14)
        self.assertAlmostEqual(np.linalg.norm(image), np.linalg.norm(m.fft2c(image)), places=12)

    def test_quantization_bound_and_phase_components(self):
        values = m.fft2c(m.phantom(32))
        payload, layout = m.quantize_complex(values)
        restored = m.unpack_complex(payload, layout)
        self.assertEqual(len(payload), values.size*4)
        self.assertLessEqual(np.max(np.abs(values.real-restored.real)), layout.scale*.500001)
        self.assertLessEqual(np.max(np.abs(values.imag-restored.imag)), layout.scale*.500001)
        self.assertGreater(np.linalg.norm(restored.imag), 0)

    def test_endianness_is_explicit(self):
        layout = m.ComplexLayout((1, 1), 1)
        self.assertEqual(m.unpack_complex(b"\x01\x00\xfe\xff", layout)[0, 0], 1-2j)

    def test_reject_bad_header_or_payload_length(self):
        layout = m.ComplexLayout((1, 1), 1)
        with self.assertRaises(ValueError):
            m.unpack_complex(b"\x00", layout)
        with self.assertRaises(ValueError):
            m.unpack_complex(b"\x00"*4, replace(layout, scale=float("nan")))
        with self.assertRaises(ValueError):
            m.unpack_complex(b"\x00"*4, replace(layout, dtype=">i2"))

    def test_magnitude_is_not_a_phase_preserving_transport(self):
        image = m.phantom(32)
        self.assertEqual(m.nrmse(np.abs(image), np.abs(image)), 0)
        self.assertGreater(m.nrmse(np.abs(image), image), .1)


class DigitalRecovery(unittest.TestCase):
    def test_no_error_and_partial_last_frame(self):
        original = bytes(i % 256 for i in range(259))
        recovered = m.recover_payload(original, m.protect_payload(original))
        self.assertEqual(recovered.payload, original)
        self.assertEqual(recovered.statuses, ("unchanged", "unchanged"))

    def test_every_location_and_every_nonzero_byte_change(self):
        # 256 positions x 255 possible changed values: 65,280 deterministic cases.
        original = bytes((i*37+11) % 256 for i in range(256))
        refs = m.protect_payload(original)
        for i in range(256):
            for offset in range(1, 256):
                damaged = bytearray(original)
                damaged[i] = (damaged[i]+offset) % 256
                recovered = m.recover_payload(bytes(damaged), refs)
                self.assertEqual(recovered.payload, original, (i, offset))

    def test_syndrome_collision_is_rejected_by_separate_digest(self):
        original, collision = bytes((2, 2, 2, 2)), bytes((3, 0, 3, 2))
        self.assertEqual(m.zeta_check_channels(original), m.zeta_check_channels(collision))
        recovered = m.recover_payload(collision, m.protect_payload(original))
        self.assertIsNone(recovered.payload)
        self.assertEqual(recovered.statuses, ("rejected",))

    def test_two_errors_must_not_release_wrong_correction(self):
        original, damaged = bytes((2, 2, 2)), bytes((3, 2, 3))
        refs = m.protect_payload(original)
        self.assertEqual(m.decode_one_error_from_zeta_channels(damaged, refs[0].moments), (3, 0, 3))
        self.assertIsNone(m.recover_payload(damaged, refs).payload)

    def test_kimi_two_errors_mimic_error_at_third_position(self):
        original, damaged = bytes((10, 10, 10, 10)), bytes((10, 12, 10, 12))
        refs = m.protect_payload(original)
        delta = tuple(a-b for a, b in zip(m.zeta_check_channels(damaged), refs[0].moments))
        self.assertEqual(delta, (4, 12))
        self.assertEqual(m.decode_one_error_from_zeta_channels(damaged, refs[0].moments), (10, 12, 6, 12))
        self.assertIsNone(m.recover_payload(damaged, refs).payload)

    def test_every_single_reference_byte_change_is_rejected_not_repaired(self):
        # Explicit byte-aligned reference layout: 3B c0 + 3B c1 + 32B digest.
        # Length/order remain trusted. 38*255=9,690 single-byte fault cases.
        original = bytes(range(256))
        ref, = m.protect_payload(original)
        packed = ref.moments[0].to_bytes(3, "little")+ref.moments[1].to_bytes(3, "little")+ref.digest
        self.assertEqual(len(packed), 38)
        for position in range(len(packed)):
            for step in range(1, 256):
                damaged = bytearray(packed)
                damaged[position] = (damaged[position]+step) % 256
                bad_ref = replace(ref, moments=(int.from_bytes(damaged[:3], "little"),
                                               int.from_bytes(damaged[3:6], "little")),
                                  digest=bytes(damaged[6:]))
                recovered = m.recover_payload(original, (bad_ref,))
                self.assertIsNone(recovered.payload, (position, step))
                self.assertEqual(recovered.statuses, ("rejected",))

    def test_corrupted_moments_can_suggest_wrong_data_but_intact_digest_rejects(self):
        original = bytes((10, 10, 10, 10))
        ref, = m.protect_payload(original)
        bad_ref = replace(ref, moments=(ref.moments[0]-1, ref.moments[1]-3))
        self.assertEqual(m.decode_one_error_from_zeta_channels(original, bad_ref.moments), (10, 10, 9, 10))
        self.assertIsNone(m.recover_payload(original, (bad_ref,)).payload)

    def test_consistently_replaced_data_and_reference_can_pass(self):
        original, substituted = bytes((10, 10, 10, 10)), bytes((10, 10, 9, 10))
        # Deliberately violate the trusted-reference assumption. No secret or
        # authenticated original is supplied, so a valid new packet can pass.
        recovered = m.recover_payload(substituted, m.protect_payload(substituted))
        self.assertEqual(recovered.payload, substituted)
        self.assertNotEqual(recovered.payload, original)
        self.assertEqual(recovered.statuses, ("unchanged",))

    def test_burst_rejection_and_no_partial_image_release(self):
        original = bytes((i*19+8) % 256 for i in range(768))
        damaged = bytearray(original)
        damaged[260:320] = bytes([255])*60
        recovered = m.recover_payload(bytes(damaged), m.protect_payload(original))
        self.assertIsNone(recovered.payload)
        self.assertEqual(recovered.statuses, ("unchanged", "rejected", "unchanged"))

    def test_frame_swap_rejected_by_context_bound_digest(self):
        original = bytes(range(256))+bytes(reversed(range(256)))
        damaged = original[256:]+original[:256]
        recovered = m.recover_payload(damaged, m.protect_payload(original))
        self.assertIsNone(recovered.payload)

    def test_truncation_is_rejected(self):
        original = bytes(range(256))
        with self.assertRaises(m.FrameRejected):
            m.recover_payload(original[:-1], m.protect_payload(original))

    def test_wrong_reference_is_not_success(self):
        original = bytes(range(256))
        ref, = m.protect_payload(original)
        self.assertIsNone(m.recover_payload(original, (replace(ref, digest=b"\0"*32),)).payload)

    def test_noise_before_reference_is_preserved_not_removed(self):
        already_bad = bytes((21, 10, 3))
        refs = m.protect_payload(already_bad)
        recovered = m.recover_payload(already_bad, refs)
        self.assertEqual(recovered.payload, already_bad)
        self.assertEqual(recovered.statuses, ("unchanged",))

    def test_reference_budget_covers_maxima(self):
        self.assertEqual(m.reference_storage_bytes(256), 38)
        maxima = m.zeta_check_channels(bytes([255])*256)
        self.assertEqual(maxima, (65536, 8421376))
        self.assertTrue(all(maxima[i] < 2**24 for i in range(2)))


class SamplingObservability(unittest.TestCase):
    def test_rank_identity_for_nonprojection_normal_operator(self):
        operator = np.array([[2, 0, 0], [0, .5j, 0]], dtype=complex)
        normal = operator.conj().T@operator
        self.assertFalse(np.allclose(normal@normal, normal))
        summary = m.spectral_summary(np.linalg.eigvalsh(normal))
        self.assertEqual(summary["zeta_at_0"], 2)
        self.assertEqual(summary["nullity"], 1)
        self.assertEqual(summary["zeta_at_1"], 4.25)
        witness = np.array([0, 0, 1])
        np.testing.assert_array_equal(operator@witness, [0, 0])
        np.testing.assert_array_equal(normal@witness, [0, 0, 0])

    def test_general_complex_rectangular_rank_against_singular_values(self):
        rng = np.random.default_rng(20260929)

        def matrix(rows, cols):
            return rng.normal(size=(rows, cols))+1j*rng.normal(size=(rows, cols))

        for operator in (matrix(3, 5), matrix(5, 3), matrix(3, 2)@matrix(2, 5)):
            with self.subTest(shape=operator.shape):
                normal = operator.conj().T@operator
                self.assertFalse(np.allclose(normal@normal, normal))
                summary = m.spectral_summary(np.linalg.eigvalsh(normal))
                singular_values = np.linalg.svd(operator, compute_uv=False)
                nonzero = singular_values[singular_values > 1e-5]  # sqrt(1e-10).
                self.assertEqual(summary["zeta_at_0"], len(nonzero))
                self.assertEqual(summary["nullity"], operator.shape[1]-len(nonzero))
                self.assertAlmostEqual(summary["zeta_at_1"], float(np.sum(nonzero**-2)), places=9)

    def test_tolerance_is_not_a_certificate_of_exact_zero(self):
        # Both eigenvalues are mathematically positive, but one is below the
        # default numerical cutoff. Do not label numerical rank as exact rank.
        coarse = m.spectral_summary([1, 1e-12])
        finer = m.spectral_summary([1, 1e-12], tolerance=1e-14)
        self.assertEqual(coarse["zeta_at_0"], 1)
        self.assertEqual(finer["zeta_at_0"], 2)

    def test_scaling_preserves_zeta_zero_not_zeta_one(self):
        values = np.array([4, .25, 0])
        original, scaled = m.spectral_summary(values), m.spectral_summary(9*values)
        self.assertEqual(original["zeta_at_0"], scaled["zeta_at_0"])
        self.assertAlmostEqual(scaled["zeta_at_1"], original["zeta_at_1"]/9)

    def test_rank_and_zeta_against_explicit_normal_matrix(self):
        for mode in ("full", "half", "none"):
            mask = np.ones((8, 8), dtype=bool)
            if mode == "half":
                mask[1::2] = False
            elif mode == "none":
                mask[:] = False
            operator = m.explicit_fourier_operator(8, mask)
            eigenvalues = np.linalg.eigvalsh(operator.conj().T@operator)
            actual = m.spectral_summary(eigenvalues)
            shortcut = m.sampling_summary(mask)
            self.assertEqual(actual["nullity"], shortcut["nullity"])
            self.assertEqual(actual["zeta_at_0"], shortcut["zeta_at_0"])
            self.assertAlmostEqual(actual["zeta_at_1"], shortcut["zeta_at_1"], places=9)

    def test_distinct_images_are_identical_under_half_sampling(self):
        image = m.phantom(32)
        mask = np.ones(image.shape, dtype=bool)
        mask[1::2] = False
        invisible_k = np.zeros_like(image)
        invisible_k[1, 3] = 10+3j
        alternative = image+m.ifft2c(invisible_k)
        self.assertGreater(m.nrmse(alternative, image), .1)
        self.assertLess(np.linalg.norm((m.fft2c(alternative)-m.fft2c(image))[mask]), 1e-12)

    def test_fec_of_missing_data_does_not_create_new_samples(self):
        mask = np.ones((32, 32), dtype=bool)
        mask[1::2] = False
        missing = np.where(mask, m.fft2c(m.phantom(32)), 0)
        payload, layout = m.quantize_complex(missing)
        received, _ = m.corrupt_one_byte_per_frame(payload, np.random.default_rng(1))
        recovered = m.recover_payload(received, m.protect_payload(payload))
        self.assertEqual(recovered.payload, payload)
        self.assertTrue(np.all(m.unpack_complex(recovered.payload, layout)[~mask] == 0))

    def test_rank_does_not_prove_stable_reconstruction(self):
        good, bad = m.spectral_summary([1, 1, 1]), m.spectral_summary([1, 1, .0001])
        self.assertEqual(good["nullity"], bad["nullity"])
        self.assertEqual(bad["zeta_at_1"], 10002)


class EndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result, cls.arrays = m.run_benchmark(runs=20)

    def test_all_twenty_seeds_recover_sender_bytes(self):
        self.assertEqual(self.result["summary"]["byte_identical_recoveries"], 20)
        self.assertEqual(self.result["summary"]["corrected_frames"], 1280)

    def test_recovery_exactly_matches_noisy_sender_not_truth(self):
        for trial in self.result["trials"]:
            restored = trial["metrics"]["recovered_transport"]
            self.assertEqual(restored["complex_nrmse_vs_sender"], 0)
            self.assertGreater(restored["complex_nrmse_vs_truth"], 0)
            self.assertEqual(restored["complex_nrmse_vs_truth"], trial["metrics"]["sender_baseline"]["complex_nrmse_vs_truth"])

    def test_corrected_injected_damage_improves_this_benchmark(self):
        for trial in self.result["trials"]:
            self.assertLess(trial["metrics"]["recovered_transport"]["complex_nrmse_vs_truth"],
                            trial["metrics"]["damaged_transport"]["complex_nrmse_vs_truth"])

    def test_extra_acquisition_is_required_and_clearly_counted(self):
        trial = self.result["primary"]
        self.assertEqual(trial["ambiguity_control"]["extra_complex_samples_needed_for_complement"], 2048)
        self.assertGreater(trial["metrics"]["half_sampling"]["complex_nrmse_vs_truth"], .1)
        self.assertEqual(trial["metrics"]["complementary_acquisition"]["complex_nrmse_vs_sender"], 0)

    def test_zeta_operator_cannot_see_arbitrary_value_corruption(self):
        reports = self.result["primary"]["operator_zeta"]
        self.assertEqual(reports["full_sampling"], reports["corrupted_full_sampling"])
        self.assertEqual(reports["half_sampling"]["nullity"], 2048)

    def test_primary_arrays_are_not_silently_magnitude_only(self):
        for name in ("truth", "sender_baseline", "recovered_transport"):
            self.assertTrue(np.iscomplexobj(self.arrays[name]))
        np.testing.assert_array_equal(self.arrays["sender_baseline"], self.arrays["recovered_transport"])

    def test_numerical_results_reproduce_with_same_seed(self):
        repeat, _ = m.scenario()
        primary = self.result["primary"]
        self.assertEqual(repeat["metrics"], primary["metrics"])
        self.assertEqual(repeat["digital_transport"]["payload_sha256"], primary["digital_transport"]["payload_sha256"])


if __name__ == "__main__":
    unittest.main()
