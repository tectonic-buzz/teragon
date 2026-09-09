"""Reproducible finite checks for the appended independent RH notes.

Run: python3 FARI/tests/check_rh_formulas.py
Requires NumPy (the same dependency as MRI); no network at runtime.
Exact Fraction checks and float64 spot checks are distinguished below.
These checks do not establish RH or certify all zeta zeros.
"""

import cmath
from fractions import Fraction as Q
import json
import math
import unittest

import numpy as np


def bernoulli_numbers(n):
    result = [Q(1)]
    for m in range(1, n + 1):
        result.append(-sum(Q(math.comb(m + 1, k)) * result[k]
                           for k in range(m)) / (m + 1))
    return result


B = bernoulli_numbers(16)


def bernoulli_polynomial(n, x):
    return sum(Q(math.comb(n, k)) * B[k] * x ** (n - k)
               for k in range(n + 1))


def rising(s, n):
    result = 1
    for k in range(n):
        result *= s + k
    return result


def euler_maclaurin(s, N, m):
    """Terms 1..N-1; even Bernoulli corrections 2..2m; remainder omitted."""
    return (sum(Q(n) ** (-s) for n in range(1, N))
            + Q(N) ** (1 - s) / (s - 1) + Q(1, 2) * Q(N) ** (-s)
            + sum(B[2*k] * rising(s, 2*k - 1) * Q(N) ** (1 - s - 2*k)
                  / math.factorial(2*k) for k in range(1, m + 1)))


def apery_reference(terms=150):
    """Exact rational truncation of the alternating Apéry series.

    Error is bounded by 5/(2*(terms+1)^3*binom(2*(terms+1),terms+1)).
    Source: https://dlmf.nist.gov/25.6.E9
    """
    return Q(5, 2) * sum(Q((-1)**(n-1), n**3 * math.comb(2*n, n))
                         for n in range(1, terms + 1))


def theta(t):
    return float(np.exp(-math.pi * t * np.arange(-32, 33)**2).sum())


def xi_split(s, order=256):
    """Float64 quadrature on [1,32], theta terms n=1..9; not interval proof."""
    nodes, weights = np.polynomial.legendre.leggauss(order)
    t = 1 + (nodes + 1) * 31 / 2
    omega = np.exp(-math.pi * t[:, None] * np.arange(1, 10)[None, :]**2).sum(axis=1)
    integral = 31 / 2 * np.dot(weights, omega * (t**(s/2) + t**((1-s)/2)) / t)
    return float(.5 + .5 * s * (s - 1) * integral)


# First 60 positive ordinates, exactly as displayed in Odlyzko's table.
# https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1
# Index states accuracy within 3e-9:
# https://www-users.cse.umn.edu/~odlyzko/zeta_tables/
# This is input data, NOT independent zero certification by this script.
ZERO_HEIGHTS = tuple(map(float, """
14.134725142 21.022039639 25.010857580 30.424876126 32.935061588
37.586178159 40.918719012 43.327073281 48.005150881 49.773832478
52.970321478 56.446247697 59.347044003 60.831778525 65.112544048
67.079810529 69.546401711 72.067157674 75.704690699 77.144840069
79.337375020 82.910380854 84.735492981 87.425274613 88.809111208
92.491899271 94.651344041 95.870634228 98.831194218 101.317851006
103.725538040 105.446623052 107.168611184 111.029535543 111.874659177
114.320220915 116.226680321 118.790782866 121.370125002 122.946829294
124.256818554 127.516683880 129.578704200 131.087688531 133.497737203
134.756509753 138.116042055 139.736208952 141.123707404 143.111845808
146.000982487 147.422765343 150.053520421 150.925257612 153.024693811
156.112909294 157.597591818 158.849988171 161.188964138 163.030709687
""".split()))


def psi_direct(x):
    terms = []
    for p in range(2, math.floor(x) + 1):
        if any(p % d == 0 for d in range(2, math.isqrt(p) + 1)):
            continue
        power = p
        while power <= x:
            terms.append(math.log(p))
            power *= p
    return math.fsum(terms)


def psi_from_pairs(x, pairs=60):
    """Truncated formula, each stored height supplies BOTH conjugate zeros."""
    terms = [(x**complex(.5, t) / complex(.5, t)).real
             for t in ZERO_HEIGHTS[:pairs]]
    return x - 2 * math.fsum(terms) - math.log(2*math.pi) - .5*math.log1p(-x**-2)


class ExactChecks(unittest.TestCase):
    def test_hasse_example(self):
        affine = [(x, y) for x in range(7) for y in range(7)
                  if (y*y - x**3 - x - 1) % 7 == 0]
        self.assertEqual(affine, [(0, 1), (0, 6), (2, 2), (2, 5)])
        a = 8 - (len(affine) + 1)
        self.assertEqual((a, 4*7 - a*a), (3, 19))

    def test_degree_pullback_may_be_semidefinite(self):
        a, q, m, n = -6, 9, -3, 1
        self.assertEqual(m*m - a*m*n + q*n*n, 0)
        self.assertNotEqual((m, n), (0, 0))

    def test_even_factorization_does_not_force_negative_zeros(self):
        w = complex(0, 1/16)
        self.assertEqual(1 + 256*w*w, 0)
        self.assertNotEqual(w.imag, 0)
        # Every nonzero point on the critical-axis preimage is unramified.
        z = 1j
        self.assertEqual(z*z, -1)
        self.assertNotEqual(2*z, 0)

    def test_bernoulli_normalization(self):
        self.assertEqual(B[:7], list(map(Q, ['1', '-1/2', '1/6', '0', '-1/30', '0', '1/42'])))

    def test_polynomial_antidifference(self):
        for n in range(9):
            for x in map(Q, ['-3', '-1/2', '0', '1/3', '2', '5']):
                delta = (bernoulli_polynomial(n+1, x+1) - bernoulli_polynomial(n+1, x))/(n+1)
                self.assertEqual(delta, x**n)

    def test_finite_step_is_not_delta(self):
        # On phi(x)=1+x+x², average over [-h,0] is 1-h/2+h²/3.
        for h in [Q(1), Q(1, 10), Q(1, 100)]:
            action = 1 - h/2 + h*h/3
            self.assertNotEqual(action, 1)
            self.assertLess(abs(action - 1), h)

    def test_zeta3_euler_maclaurin_error_is_not_zero(self):
        error = euler_maclaurin(3, 9, 4) - apery_reference()
        self.assertLess(error, 0)
        self.assertGreater(abs(error), Q(1, 10**12))
        self.assertLess(abs(error), Q(2, 10**12))


class NumericalChecks(unittest.TestCase):
    def test_theta_inversion(self):
        for t in [.3, 2.0]:
            self.assertAlmostEqual(theta(1/t), math.sqrt(t)*theta(t), places=13)

    def test_xi_by_two_routes(self):
        s = 2.7
        direct = .5*s*(s-1)*math.pi**(-s/2)*math.gamma(s/2)*float(euler_maclaurin(s, 32, 8))
        for order in [128, 256]:
            self.assertLess(abs(xi_split(s, order)-direct), 5e-13)
        self.assertAlmostEqual(direct, .555701423555263, places=13)

    def test_xi_symmetry_and_endpoints(self):
        self.assertEqual(xi_split(0), .5)
        self.assertEqual(xi_split(1), .5)
        self.assertAlmostEqual(xi_split(2.7), xi_split(-1.7), places=14)

    def test_positive_fourier_measure_does_not_force_real_zeros(self):
        z = complex(math.pi, math.acosh(2))
        self.assertLess(abs(2 + cmath.cos(z)), 1e-14)
        self.assertNotEqual(z.imag, 0)
        # 2+cos(t) is Fourier transform of 2δ0+(δ1+δ−1)/2, a positive measure.

    def test_prime_power_count_and_truncation(self):
        self.assertEqual(len(ZERO_HEIGHTS), 60)
        self.assertAlmostEqual(psi_direct(50.5), 49.48538079241837, places=12)
        self.assertAlmostEqual(psi_from_pairs(50.5), 49.55827796617394, places=11)
        self.assertAlmostEqual(psi_from_pairs(50.5, 30), 49.48827965921462, places=11)
        self.assertGreater(abs(psi_from_pairs(50.5)-psi_direct(50.5)), .07)

    def test_fourier_comb_normalizations(self):
        N = 8
        delta = np.eye(1, N).ravel()
        np.testing.assert_allclose(np.fft.fft(delta), np.ones(N), atol=1e-14)
        np.testing.assert_allclose(np.fft.fft(np.ones(N)), N*delta, atol=1e-14)
        x = np.arange(N) + 1j*np.arange(N)[::-1]
        even = np.arange(N) % 2 == 0
        np.testing.assert_allclose(np.fft.ifft(even*np.fft.fft(x)),
                                   (x+np.roll(x, N//2))/2, atol=1e-14)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print(json.dumps({'arithmetic': 'exact rational where marked; otherwise float64, not interval-certified',
                          'xi_2_7': xi_split(2.7),
                          'zeta3_EM_N9_m4_error': float(euler_maclaurin(3, 9, 4)-apery_reference()),
                          'psi_50_5_direct': psi_direct(50.5),
                          'psi_50_5_60_pairs': psi_from_pairs(50.5),
                          'RH_proved': False}, indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)
