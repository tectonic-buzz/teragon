"""Causal phase-correction probes; all inputs and assumptions are synthetic."""

import unittest

try:
    import numpy as np
except ImportError as exc:
    raise unittest.SkipTest("EPI probe requires NumPy") from exc

if __package__:
    from . import mri_epi_phase_probe as p
else:
    import mri_epi_phase_probe as p


class EpiPhaseProbe(unittest.TestCase):
    def test_missing_calibration_is_not_silently_zero(self):
        raw = p.acquire(p.m.phantom(16))
        with self.assertRaises(TypeError):
            p.reconstruct(raw)
        for invalid in (None, np.nan, np.inf, -np.inf, .05j, [.05], "0.05", True):
            with self.subTest(phase=invalid), self.assertRaises(ValueError):
                p.reconstruct(raw, invalid)
        np.testing.assert_allclose(p.reconstruct(raw, 0), p.m.phantom(16), atol=1e-13)

    def test_boustrophedon_is_bijective_reindexing(self):
        data = np.arange(64).reshape(8, 8).astype(complex)
        np.testing.assert_array_equal(p.reverse_odd_rows(p.reverse_odd_rows(data)), data)
        self.assertEqual(set(p.reverse_odd_rows(data).ravel()), set(data.ravel()))

    def test_proposed_glide_is_not_a_generic_double_cover_involution(self):
        def glide(point):
            x, y = point
            return (-x) % 8, (y+1) % 8
        self.assertEqual(glide(glide((2, 3))), (2, 5))
        self.assertNotEqual(glide(glide((2, 3))), (2, 3))

    def test_free_glide_requires_the_stated_periods(self):
        # Discretize x mod 1 with eight samples. A y period of 2 makes +1
        # a half-period shift; a y period of 1 makes +1 the identity.
        doubled = [(x, y) for x in range(8) for y in range(16)]
        glide = lambda point: ((-point[0]) % 8, (point[1]+8) % 16)
        self.assertTrue(all(glide(glide(point)) == point for point in doubled))
        self.assertTrue(all(glide(point) != point for point in doubled))
        unit = [(x, y) for x in range(8) for y in range(8)]
        flip = lambda point: ((-point[0]) % 8, (point[1]+8) % 8)
        self.assertEqual(sum(flip(point) == point for point in unit), 16)

    def test_parity_cosets_each_have_two_fourier_spikes(self):
        n = 16
        ky = np.arange(n)
        direct_inverse = np.exp(2j*np.pi*np.outer(ky, ky)/n)/n
        for parity, sign in ((0, 1), (1, -1)):
            expected = np.zeros(n, dtype=complex)
            expected[0], expected[n//2] = .5, .5*sign
            np.testing.assert_allclose(direct_inverse@(ky % 2 == parity), expected, atol=1e-14)

    def test_complete_half_angle_operator_is_two_pi_periodic(self):
        image = p.m.phantom(16)
        for phi in (-3.1, -.05, 0, .6, np.pi):
            np.testing.assert_allclose(p.mix_pair(image, phi+2*np.pi), p.mix_pair(image, phi), atol=1e-13)

    def test_known_phase_reconstructs_without_ground_truth_input(self):
        rng = np.random.default_rng(20260909)
        for _ in range(20):
            image = rng.normal(size=(16, 16))+1j*rng.normal(size=(16, 16))
            phi = rng.uniform(-np.pi, np.pi)
            np.testing.assert_allclose(p.reconstruct(p.acquire(image, phi), phi), image, atol=1e-13)

    def test_pair_formula_against_fft_pipeline_all_phases(self):
        image = p.m.phantom(32)
        for phi in np.linspace(-2*np.pi, 2*np.pi, 51):
            output = p.reconstruct(p.acquire(image, phi), 0)
            np.testing.assert_allclose(output, p.mix_pair(image, phi), atol=1e-13)
            np.testing.assert_allclose(p.mix_pair(output, -phi), image, atol=1e-13)
            self.assertAlmostEqual(np.linalg.norm(output), np.linalg.norm(image), places=11)

    def test_wrong_correction_creates_ghost_on_clean_input(self):
        impulse = np.zeros((16, 16), dtype=complex)
        impulse[1, 3] = 1
        baseline = p.reconstruct(p.acquire(impulse), 0)
        wrong = p.reconstruct(p.acquire(impulse), .05)
        self.assertLess(abs(baseline[9, 3]), 1e-14)
        self.assertAlmostEqual(abs(wrong[9, 3]/wrong[1, 3]), abs(np.tan(.025)), places=13)

    def test_half_angle_ratio_is_not_percent_image_error(self):
        impulse = np.zeros((16, 16), dtype=complex)
        impulse[1, 3] = 1
        output = p.reconstruct(p.acquire(impulse, .6), 0)
        self.assertAlmostEqual(abs(output[9, 3]/output[1, 3]), np.tan(.3), places=13)
        self.assertAlmostEqual(abs(output[9, 3]), np.sin(.3), places=13)
        self.assertNotAlmostEqual(p.m.nrmse(output, impulse), np.tan(.3), places=3)

    def test_pi_phase_swaps_instead_of_losing_information(self):
        image = p.m.phantom(32)
        np.testing.assert_allclose(p.reconstruct(p.acquire(image, np.pi), 0), np.roll(image, 16, axis=0), atol=1e-13)

    def test_unknown_phase_can_be_absorbed_into_different_image(self):
        image = p.m.phantom(32)
        raw = p.acquire(image, .6)
        alternative = p.reconstruct(raw, .2)
        self.assertGreater(p.m.nrmse(alternative, image), .1)
        np.testing.assert_allclose(p.acquire(alternative, .2), raw, atol=1e-13)

    def test_entropy_cannot_distinguish_shifted_solution(self):
        image = p.m.phantom(32)
        swapped = np.roll(image, 16, axis=0)
        np.testing.assert_allclose(p.acquire(image, .6), p.acquire(swapped, .6+np.pi), atol=1e-13)
        self.assertAlmostEqual(p.entropy(image), p.entropy(swapped), places=13)

    def test_reference_free_one_correlation_is_conditional(self):
        result = p.run_probe()["conditional_one_correlation_estimator"]
        self.assertAlmostEqual(result["estimated_phase"], .6, places=13)
        self.assertLess(result["reconstruction_nrmse"], 1e-13)
        self.assertIsNone(result["all_image_estimate"])
        self.assertAlmostEqual(result["violated_support_coherence"], 1, places=13)
        self.assertAlmostEqual(result["violated_support_estimated_phase"], .6-np.pi/2, places=13)
        self.assertGreater(result["violated_support_reconstruction_nrmse"], .9)

    def test_zeta_and_repacking_do_not_supply_phase_or_missing_dimensions(self):
        result = p.run_probe()
        self.assertEqual(result["tile_permutation"]["before"]["nullity"], 32)
        self.assertEqual(result["tile_permutation"]["after"]["nullity"], 32)
        self.assertLess(result["tile_permutation"]["max_normal_spectral_change"], 1e-12)
        self.assertLess(max(result["full_acquisition_zeta"]["normal_identity_errors"]), 1e-12)


if __name__ == "__main__":
    unittest.main()
