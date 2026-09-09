"""Reference-beat and two-projection checks for the affine-flow example.
Run: python3 NS/check_reference_beat.py
Standard library, finite float64 checks in a noiseless model, not sensor validation.
"""
import cmath
import math
import unittest

from check_phase_clock import phase, zeta_clock


def beat(t, a, omega0, reference_rate):
    q = cmath.exp(1j * phase(t, a, omega0))
    r = cmath.exp(1j * reference_rate * t)
    return q * r.conjugate()


def projections(z, beta):
    return ((z * cmath.exp(-1j * beta)).real,
            (z * cmath.exp(1j * beta)).real)


def recover_projections(m_plus, m_minus, beta):
    # This API chooses the branch 0 < beta < pi/2; endpoints are singular.
    if not 0 < beta < math.pi / 2:
        raise ValueError("choose two non-collinear axes: 0 < beta < pi/2")
    return complex((m_plus + m_minus) / (2 * math.cos(beta)),
                   (m_plus - m_minus) / (2 * math.sin(beta)))


class ReferenceBeatChecks(unittest.TestCase):
    def test_phase_sensitive_beat_separates_equal_metric_readouts(self):
        t, a, reference_rate = math.log(2), 1., 1.
        self.assertAlmostEqual(zeta_clock(t, a), 17 / 4, places=14)
        h = 1e-5
        for omega0, expected_rate in ((1., 1.), (2., 3.)):
            b = beat(t, a, omega0, reference_rate)
            # Derivative estimated from independent neighboring phase samples.
            db = (beat(t + h, a, omega0, reference_rate)
                  - beat(t - h, a, omega0, reference_rate)) / (2 * h)
            rate = (b.conjugate() * db).imag
            self.assertAlmostEqual(rate, expected_rate, places=8)
            recovered = math.exp(-a * t) * (rate + reference_rate)
            self.assertAlmostEqual(recovered, omega0, places=8)

    def test_reference_without_phase_measurement_adds_no_spin_information(self):
        for t in (.1, .5, 1.):
            channels = []
            for omega0 in (1., 2.):
                channels.append((zeta_clock(t, 1.), cmath.exp(1j * t)))
                self.assertAlmostEqual(abs(beat(t, 1., omega0, 1.)), 1., places=14)
            self.assertEqual(channels[0], channels[1])

    def test_virtual_phase_origin_cancels(self):
        q, r = cmath.exp(1.3j), cmath.exp(-.7j)
        for alpha in (-2., .1, 1.7):
            shift = cmath.exp(1j * alpha)
            self.assertLess(abs((shift * q) * (shift * r).conjugate()
                                - q * r.conjugate()), 1e-14)

    def test_two_projections_recover_complex_readout(self):
        for theta in (-2.1, .2, 1.3, math.pi):
            for amplitude in (.3, 2.):
                z = amplitude * cmath.exp(1j * theta)
                for beta in (math.pi / 6, math.pi / 4, math.pi / 3):
                    self.assertLess(abs(recover_projections(*projections(z, beta), beta)
                                        - z), 1e-14)

    def test_collinear_axes_do_not_recover_second_component(self):
        z1, z2 = cmath.exp(.7j), cmath.exp(-.7j)
        self.assertNotEqual(z1, z2)
        self.assertEqual(projections(z1, 0.), projections(z2, 0.))
        for beta in (0., math.pi / 2):
            with self.assertRaises(ValueError):
                recover_projections(1., 1., beta)

    def test_intensity_alone_does_not_supply_signed_phase(self):
        b1, b2 = cmath.exp(.7j), cmath.exp(-.7j)
        self.assertAlmostEqual(abs(1 + b1)**2, abs(1 + b2)**2, places=14)
        self.assertNotEqual(b1.imag, b2.imag)

    def test_reference_does_not_prevent_sampling_alias(self):
        # Distinct smooth flows, same C(t), same measured beat at t=0 and t=1.
        omega1 = 1.
        omega2 = omega1 + 2 * math.pi / math.expm1(1.)
        self.assertNotEqual(omega1, omega2)
        for t in (0., 1.):
            self.assertLess(abs(beat(t, 1., omega1, .4)
                                - beat(t, 1., omega2, .4)), 1e-14)
        self.assertGreater(abs(beat(.5, 1., omega1, .4)
                               - beat(.5, 1., omega2, .4)), 1.)


if __name__ == "__main__":
    unittest.main(verbosity=2)
