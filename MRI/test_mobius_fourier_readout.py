"""Four audit passes: covers, spectra, Fourier data, recovery limits.

Self-contained mathematical toy models, NOT scanner software or clinical tests.
All floating comparisons have explicit tolerances; inverse matrices use Fraction.
Run: python3 -m unittest discover -s MRI -p test_mobius_fourier_readout.py -v
"""

import cmath
import math
import unittest
from fractions import Fraction as Q
from itertools import combinations, product


def dft(values, inverse=False):
    n = len(values)
    sign = 1 if inverse else -1
    scale = n if inverse else 1
    return [sum(z * cmath.exp(sign * 2j * math.pi * k * j / n)
                for j, z in enumerate(values)) / scale for k in range(n)]


def differences(values, order=1, periodic=False):
    result = list(values)
    for _ in range(order):
        if periodic:
            result = [result[(j+1) % len(result)]-result[j] for j in range(len(result))]
        else:
            result = [b-a for a, b in zip(result, result[1:])]
    return result


def zeta_check_channels(values):
    """Exact zeta_A(-1)=tr(A) for A0=diag(x_i+1), A1=diag(i*(x_i+1)).

    Byte data, positive integer spectra; this is spectral zeta, not Riemann zeta.
    The pair of reference values must be independently preserved before damage.
    """
    return (sum(x+1 for x in values),
            sum(i*(x+1) for i, x in enumerate(values, 1)))


def decode_one_error_from_zeta_channels(received, reference):
    current = zeta_check_channels(received)
    change, weighted_change = (a-b for a, b in zip(current, reference))
    if change == weighted_change == 0:
        return tuple(received)  # Passed checks, NOT proof of original identity.
    if change == 0 or weighted_change % change:
        raise ValueError("Not consistent with the declared one-symbol error model")
    index = weighted_change // change - 1
    if not 0 <= index < len(received):
        raise ValueError("Error location outside this frame")
    candidate = list(received)
    candidate[index] -= change
    if not 0 <= candidate[index] <= 255:
        raise ValueError("Corrected value outside byte alphabet")
    if zeta_check_channels(candidate) != reference:
        raise ValueError("Checks do not close")
    return tuple(candidate)


def grid_matrix(nx, ny, twisted=False):
    """Unit-step -Laplacian: periodic x, Dirichlet y=0,ny.

    twisted=True identifies (nx,y) with (0,ny-y).
    Matrix entries are integers. Interior sites: x=0..nx-1, y=1..ny-1.
    """
    sites = [(x, y) for x in range(nx) for y in range(1, ny)]
    index = {site: i for i, site in enumerate(sites)}
    matrix = [[0] * len(sites) for _ in sites]
    for i, (x, y) in enumerate(sites):
        matrix[i][i] = 4
        for xx, yy in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            if yy in (0, ny):
                continue
            if xx in (-1, nx):
                xx %= nx
                if twisted:
                    yy = ny - yy
            matrix[i][index[xx, yy]] -= 1
    return sites, matrix


def matvec(matrix, vector):
    return [sum(a*b for a, b in zip(row, vector)) for row in matrix]


def inverse_trace(matrix):
    n = len(matrix)
    a = [[Q(v) for v in row] + [Q(i == j) for j in range(n)]
         for i, row in enumerate(matrix)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        scale = a[k][k]
        a[k] = [v / scale for v in a[k]]
        for i in range(n):
            if i != k:
                c = a[i][k]
                a[i] = [v-c*w for v, w in zip(a[i], a[k])]
    return sum(a[i][n+i] for i in range(n))


def mobius_eigenvalues(nx, ny):
    return [4*math.sin(math.pi*m/(2*nx))**2
            + 4*math.sin(math.pi*n/(2*ny))**2
            for m in range(2*nx) for n in range(1, ny) if (m+n) % 2]


class CoversAndBoundary(unittest.TestCase):
    def test_embedded_strip_seam(self):
        def embedded(theta, v):
            r = 2 + v*math.cos(theta/2)
            return (r*math.cos(theta), r*math.sin(theta), v*math.sin(theta/2))
        for v in (-0.2, -0.1, 0, 0.1, 0.2):
            self.assertLess(max(abs(a-b) for a, b in
                                zip(embedded(2*math.pi, v), embedded(0, -v))), 1e-14)

    def test_deck_is_free_involution_and_commutes(self):
        nx, ny = 4, 5
        sites, matrix = grid_matrix(2*nx, ny)
        lookup = {site: i for i, site in enumerate(sites)}
        permutation = [lookup[((x+nx) % (2*nx), ny-y)] for x, y in sites]
        self.assertTrue(all(permutation[permutation[i]] == i for i in range(len(sites))))
        self.assertTrue(all(permutation[i] != i for i in range(len(sites))))
        v = [Q((i*i+3*i) % 13) for i in range(len(sites))]
        tau = lambda u: [u[i] for i in permutation]
        self.assertEqual(matvec(matrix, tau(v)), tau(matvec(matrix, v)))
        plus = [(a+b)/2 for a, b in zip(v, tau(v))]
        minus = [(a-b)/2 for a, b in zip(v, tau(v))]
        self.assertEqual(tau(plus), plus)
        self.assertEqual(tau(minus), [-a for a in minus])
        self.assertEqual([a+b for a, b in zip(plus, minus)], v)

    def test_continuum_parity_and_derivative_at_seam(self):
        length, width = 1.3, 0.9
        for m in range(-6, 7):
            for n in range(1, 8):
                for y in (0.13, 0.31, 0.67):
                    f = lambda x, yy: cmath.exp(1j*math.pi*m*x/length)*math.sin(math.pi*n*yy/width)
                    sign = (-1)**(m+n+1)
                    self.assertLess(abs(f(length, y)-sign*f(0, width-y)), 3e-14)
                    if (m+n) % 2:
                        factor = 1j*math.pi*m/length
                        self.assertLess(abs(factor*(f(length, y)-f(0, width-y))), 5e-13)


class SpectralAudit(unittest.TestCase):
    def test_discrete_modes_against_matrix(self):
        nx, ny = 4, 5
        sites, matrix = grid_matrix(nx, ny, twisted=True)
        count = 0
        for m in range(2*nx):
            for n in range(1, ny):
                if (m+n) % 2 == 0:
                    continue
                v = [cmath.exp(1j*math.pi*m*x/nx)*math.sin(math.pi*n*y/ny) for x, y in sites]
                lam = 4*math.sin(math.pi*m/(2*nx))**2+4*math.sin(math.pi*n/(2*ny))**2
                self.assertLess(max(abs(a-lam*b) for a, b in zip(matvec(matrix, v), v)), 2e-14)
                count += 1
        self.assertEqual(count, len(sites))

    def test_inverse_trace_independent_of_mode_sum(self):
        _, mob = grid_matrix(4, 5, twisted=True)
        _, cyl = grid_matrix(4, 5, twisted=False)
        self.assertAlmostEqual(float(inverse_trace(mob)), sum(1/v for v in mobius_eigenvalues(4, 5)), places=12)
        self.assertNotEqual(inverse_trace(mob), inverse_trace(cyl))

    def test_cover_zeta_splits_with_correct_sign(self):
        nx, ny = 4, 5
        for s in (1, 2, 0.8+0.4j):
            even_sector = odd_sector = alternating = full = 0j
            for m in range(2*nx):
                for n in range(1, ny):
                    lam = 4*math.sin(math.pi*m/(2*nx))**2+4*math.sin(math.pi*n/(2*ny))**2
                    term = lam**(-s)
                    full += term
                    alternating += (-1)**(m+n)*term
                    if (m+n) % 2:
                        even_sector += term  # tau=+1: scalar functions on strip
                    else:
                        odd_sector += term
            self.assertLess(abs(full-even_sector-odd_sector), 1e-13)
            self.assertLess(abs(even_sector-(full-alternating)/2), 1e-13)

    def test_riemann_half_integer_identity_with_tail_bounds(self):
        # Direct finite sums, with analytic integral upper bounds on omitted tails.
        cutoff = 2000
        for s in (1, 2):
            zeta = sum(n**(-2*s) for n in range(1, cutoff+1))
            half = 2*sum((n+0.5)**(-2*s) for n in range(cutoff))
            target = 2*(2**(2*s)-1)*zeta
            bound = (2*(cutoff-0.5)**(1-2*s)
                     + 2*(2**(2*s)-1)*cutoff**(1-2*s))/(2*s-1)
            self.assertLessEqual(abs(half-target), bound + 1e-10)
        # At length L=1: periodic zeta(1)=1/12, antiperiodic=1/4.
        periodic = 2*sum(n**-2 for n in range(1, cutoff+1))/(2*math.pi)**2
        anti = 2*sum((n+0.5)**-2 for n in range(cutoff))/(2*math.pi)**2
        self.assertLess(abs(periodic-1/12), 1e-4)
        self.assertLess(abs(anti-1/4), 1e-4)

    def test_finite_cycle_has_gap_and_finite_zeta(self):
        for n in (8, 16, 32):
            eigenvalues = [4*math.sin(math.pi*j/n)**2 for j in range(1, n)]
            self.assertGreater(min(eigenvalues), 0)
            self.assertAlmostEqual(sum(1/v for v in eigenvalues), (n*n-1)/12, places=10)
            self.assertTrue(math.isfinite(sum(v**(-1) for v in eigenvalues)))

    def test_pure_gauge_phase_does_not_change_spectrum(self):
        n = 16
        lap = lambda v: [2*v[j]-v[(j-1) % n]-v[(j+1) % n] for j in range(n)]
        for winding in (0, 1, 2, -1):
            z = [cmath.exp(2j*math.pi*winding*j/n) for j in range(n)]
            # L_z = D_z L D_z^*: same eigenvalues for every vertex phase.
            for m in range(n):
                f = [z[j]*cmath.exp(2j*math.pi*m*j/n) for j in range(n)]
                output = [z[j]*v for j, v in enumerate(lap([z[j].conjugate()*f[j] for j in range(n)]))]
                lam = 4*math.sin(math.pi*m/n)**2
                self.assertLess(max(abs(a-lam*b) for a, b in zip(output, f)), 3e-14)


class FourierAndPhase(unittest.TestCase):
    def test_full_complex_fourier_roundtrip_and_parseval(self):
        v = [complex((3*j) % 11, (j*j) % 7) for j in range(16)]
        spectrum = dft(v)
        recovered = dft(spectrum, inverse=True)
        self.assertLess(max(abs(a-b) for a, b in zip(v, recovered)), 1e-12)
        self.assertAlmostEqual(sum(abs(x)**2 for x in v), sum(abs(x)**2 for x in spectrum)/16, places=10)

    def test_integer_lift_does_not_change_complex_signal(self):
        for phase in (-2.3, 0.2, 1.4):
            for lift in range(-7, 8):
                self.assertLess(abs(cmath.exp(1j*phase)-cmath.exp(1j*(phase+2*math.pi*lift))), 2e-14)

    def test_half_phase_detects_parity_not_full_winding(self):
        for winding in range(-6, 7):
            endpoint = cmath.exp(1j*math.pi*winding)
            self.assertLess(abs(endpoint-(-1)**winding), 3e-15)
        self.assertEqual((-1)**1, (-1)**3)
        theta = 0.7
        self.assertGreater(abs(cmath.exp(1j*theta)-cmath.exp(3j*theta)), 1)

    def test_alias_survives_dft_but_extra_measurement_separates_pair(self):
        n = 16
        sample = lambda k, offset: [cmath.exp(2j*math.pi*k*(j+offset)/n) for j in range(n)]
        a, b = sample(1, 0), sample(17, 0)
        self.assertLess(max(abs(x-y) for x, y in zip(a, b)), 2e-14)
        self.assertLess(max(abs(x-y) for x, y in zip(dft(a), dft(b))), 2e-13)
        aa, bb = sample(1, 0.5), sample(17, 0.5)
        self.assertLess(max(abs(x+y) for x, y in zip(aa, bb)), 2e-14)
        # The larger acquisition also has a finite horizon: 1 and 33 still alias.
        for offset in (0, 0.5):
            self.assertLess(max(abs(x-y) for x, y in zip(sample(1, offset), sample(33, offset))), 4e-14)

    def test_magnitude_is_not_invertible(self):
        a = [1+0j, 0+1j, -1+0j, 0-1j]
        b = [1+0j]*4
        self.assertEqual([abs(x) for x in a], [abs(x) for x in b])
        self.assertGreater(max(abs(x-y) for x, y in zip(dft(a), dft(b))), 3)

    def test_dft_is_polynomial_evaluation_by_horner(self):
        coefficients = [complex(2*j-3, j % 3) for j in range(8)]
        for k, measured in enumerate(dft(coefficients)):
            w = cmath.exp(-2j*math.pi*k/len(coefficients))
            value = 0j
            for coefficient in reversed(coefficients):
                value = value*w+coefficient
            self.assertLess(abs(value-measured), 1e-12)

    def test_full_dft_has_no_redundancy_for_unknown_corruption(self):
        n, changed_bin, error = 8, 3, 1.2-0.5j
        original = [complex(j % 3, (j*j) % 5) for j in range(n)]
        measured = dft(original)
        measured[changed_bin] += error
        different_image = dft(measured, inverse=True)
        # The corrupted data are also a valid full DFT of another complex image.
        self.assertLess(max(abs(a-b) for a, b in zip(dft(different_image), measured)), 1e-12)
        for j, (a, b) in enumerate(zip(different_image, original)):
            predicted = error*cmath.exp(2j*math.pi*changed_bin*j/n)/n
            self.assertLess(abs(a-b-predicted), 1e-13)
            self.assertAlmostEqual(abs(a-b), abs(error)/n, places=12)

    def test_hermitian_symmetry_requires_real_image(self):
        real_image = [j*j-2*j for j in range(8)]
        spectrum = dft(real_image)
        for k, value in enumerate(spectrum):
            self.assertLess(abs(value.conjugate()-spectrum[-k % 8]), 1e-12)
        complex_spectrum = dft([1j]*8)
        self.assertEqual(complex_spectrum[0], 8j)  # DC is not generally real.

    def test_even_grid_involution_has_nyquist_fixed_points_too(self):
        nx, ny = 8, 10
        fixed = {(j, k) for j in range(nx) for k in range(ny)
                 if (j, k) == (-j % nx, -k % ny)}
        self.assertEqual(fixed, {(0, 0), (4, 0), (0, 5), (4, 5)})

    def test_phasor_average_respects_the_argument_cut(self):
        a, b = math.radians(179), math.radians(-179)
        naive = (a+b)/2
        coherent = (cmath.exp(1j*a)+cmath.exp(1j*b))/2
        self.assertEqual(naive, 0)
        self.assertLess(coherent.real, -0.999)
        self.assertAlmostEqual(abs(cmath.phase(coherent)), math.pi, places=14)

    def test_complex_average_can_cancel_and_normalization_loses_amplitude(self):
        samples = (1+0j, -1+0j)
        self.assertEqual(abs(sum(samples)/2), 0)
        self.assertEqual(sum(abs(z) for z in samples)/2, 1)
        self.assertLess(abs((2+2j)/abs(2+2j)-(7+7j)/abs(7+7j)), 1e-15)

    def test_smooth_complex_field_can_have_negative_zero_index(self):
        # On the unit circle, z has index +1 and conjugate(z) has index -1.
        # Both have one zero inside; only the first is holomorphic.
        for degree in (1, -1, 3):
            values = [cmath.exp(2j*math.pi*degree*j/256) for j in range(256)]
            winding = sum(cmath.phase(values[(j+1) % 256]/values[j]) for j in range(256))/(2*math.pi)
            self.assertAlmostEqual(winding, degree, places=12)

    def test_multiple_sheets_do_not_imply_ramification(self):
        # z -> z^2 is a covering on C*, locally invertible at both preimages.
        self.assertEqual((1+0j)**2, (-1+0j)**2)
        for z in (1+0j, -1+0j):
            self.assertNotEqual(2*z, 0)


class RecoveryLimits(unittest.TestCase):
    def test_redundant_linear_channel_can_restore_injectivity(self):
        # First measurement observes only a+b; independent second observes a-b.
        for a in range(-4, 5):
            for b in range(-4, 5):
                y1, y2 = a+b, a-b
                self.assertEqual((Q(y1+y2, 2), Q(y1-y2, 2)), (a, b))
        self.assertEqual(1+0, 0+1)  # first channel alone cannot distinguish

    def test_lift_does_not_recover_discarded_data(self):
        observation = lambda v: v[0]+v[1]
        lift = lambda y: (y, y*y, y*y*y, cmath.exp(1j*y))
        self.assertEqual(lift(observation((1, 0))), lift(observation((0, 1))))

    def test_venc_wrapping_is_not_integer_overflow(self):
        venc = 100
        wrapped_velocity = lambda v: math.atan2(math.sin(math.pi*v/venc), math.cos(math.pi*v/venc))*venc/math.pi
        self.assertAlmostEqual(wrapped_velocity(120), -80, places=12)
        self.assertAlmostEqual(wrapped_velocity(120), wrapped_velocity(-80), places=12)

    def test_zero_consistency_residual_does_not_certify_the_original_data(self):
        g = lambda v: [sum(v)/2]*2
        residual = lambda v: [a-b for a, b in zip(g(v), v)]
        self.assertEqual(residual([1, 1]), [0, 0])
        self.assertEqual(residual([2, 2]), [0, 0])
        # One changed datum affects two residual entries, not a single delta.
        self.assertEqual(residual([2, 1]), [-0.5, 0.5])

    def test_extra_polynomial_evaluations_correct_two_exact_symbol_errors(self):
        # Positive control: 7 evaluations of degree <=2, over Q. Distance 5.
        # This is an exact-symbol test, not a Gaussian-noise MRI decoder.
        original = tuple(3+2*x-x*x for x in range(7))
        received = list(original)
        received[1] += 7
        received[5] -= 9
        candidates = set()
        for indices in combinations(range(7), 3):
            def interpolate(t):
                return sum(Q(received[x])*math.prod(Q(t-a, x-a) for a in indices if a != x)
                           for x in indices)
            candidate = tuple(interpolate(t) for t in range(7))
            if sum(a == b for a, b in zip(candidate, received)) >= 5:
                candidates.add(candidate)
        self.assertEqual(candidates, {original})


class BabbageAndDifferences(unittest.TestCase):
    def test_polynomial_annihilation(self):
        for degree in range(7):
            coefficients = [(-1)**r*(r+1) for r in range(degree+1)]
            samples = [sum(c*j**r for r, c in enumerate(coefficients)) for j in range(-4, 16)]
            self.assertEqual(differences(samples, degree+1), [0]*(len(samples)-degree-1))

    def test_impulse_error_has_signed_binomial_stencil(self):
        length, error = 20, 7
        for order in range(1, 7):
            for location in (0, 9, length-1):
                impulse = [error*int(k == location) for k in range(length)]
                expected = [error*(-1)**(order-(location-k))*math.comb(order, location-k)
                            if 0 <= location-k <= order else 0
                            for k in range(length-order)]
                self.assertEqual(differences(impulse, order), expected)
                self.assertTrue(any(expected))

    def test_polynomial_drift_is_an_undetected_error(self):
        original = [j*j for j in range(12)]
        wrong = [j*j+3*j+7 for j in range(12)]
        self.assertNotEqual(original, wrong)
        self.assertEqual(differences(original, 3), [0]*9)
        self.assertEqual(differences(wrong, 3), [0]*9)

    def test_differences_amplify_white_noise_variance(self):
        # Variance gain = sum of squared filter coefficients (independent noise).
        for order in range(1, 9):
            gain = sum(math.comb(order, r)**2 for r in range(order+1))
            self.assertEqual(gain, math.comb(2*order, order))

    def test_periodic_difference_fourier_symbol_and_laplacian(self):
        n = 16
        values = [complex(j % 3, j*j % 5) for j in range(n)]
        spectrum = dft(values)
        derivative = differences(values, periodic=True)
        derivative_spectrum = dft(derivative)
        for k in range(n):
            multiplier = cmath.exp(2j*math.pi*k/n)-1
            self.assertLess(abs(derivative_spectrum[k]-multiplier*spectrum[k]), 1e-12)
        lap = [derivative[(j-1) % n]-derivative[j] for j in range(n)]
        self.assertEqual(lap, [2*values[j]-values[(j-1) % n]-values[(j+1) % n] for j in range(n)])
        # Nonconstant polynomial tables are not periodic: the seam matters.
        self.assertTrue(any(differences([j*j for j in range(n)], 3, periodic=True)))


class RecitationAndReference(unittest.TestCase):
    """Synthetic digital codes, not acoustic mantras or MRI pulse sequences."""

    repeat_order = (0, 1, 1, 0, 0, 1)  # ab, ba, ab: one jata-inspired block
    alphabet = range(7)

    @classmethod
    def repeat_encode(cls, message):
        return tuple(message[i] for i in cls.repeat_order)

    @classmethod
    def repeat_decode(cls, received):
        result = []
        for component in (0, 1):
            copies = [received[t] for t, label in enumerate(cls.repeat_order) if label == component]
            values = [value for value in set(copies) if copies.count(value) >= 2]
            if len(values) != 1:
                raise ValueError("No majority")
            result.append(values[0])
        return tuple(result)

    @staticmethod
    def hamming(a, b):
        return sum(x != y for x, y in zip(a, b))

    @classmethod
    def setUpClass(cls):
        cls.eval_codebook = {
            tuple((a+b*t) % 7 for t in range(6)): (a, b)
            for a, b in product(cls.alphabet, repeat=2)
        }

    @classmethod
    def eval_decode(cls, received):
        # Bounded-distance decoder for the tiny [6,2,5] evaluation code over F_7.
        candidates = [message for word, message in cls.eval_codebook.items()
                      if cls.hamming(word, received) <= 2]
        if len(candidates) != 1:
            raise ValueError("No unique candidate within the declared radius")
        return candidates[0]

    def test_repetition_minimum_distance_is_three(self):
        codewords = [self.repeat_encode(pair) for pair in product(self.alphabet, repeat=2)]
        self.assertEqual(min(self.hamming(a, b) for a, b in combinations(codewords, 2)), 3)

    def test_repetition_corrects_every_single_symbol_error(self):
        for message in product(self.alphabet, repeat=2):
            for position in range(6):
                for change in range(1, 7):
                    received = list(self.repeat_encode(message))
                    received[position] = (received[position]+change) % 7
                    self.assertEqual(self.repeat_decode(received), message)

    def test_periodic_interference_can_defeat_repetition(self):
        message = (2, 5)
        received = list(self.repeat_encode(message))
        for t in range(6):
            if t % 3 == 0:  # Hits positions 0 and 3: two copies of first symbol.
                received[t] = (received[t]+1) % 7
        self.assertEqual(self.repeat_decode(received), (3, 5))
        self.assertNotEqual(self.repeat_decode(received), message)

    def test_independent_reference_detects_shared_wrong_copies(self):
        reference = (2, 5)  # Assumed protected and fixed before transport.
        received = self.repeat_encode((3, 5))
        self.assertEqual(self.repeat_decode(received), (3, 5))
        self.assertNotEqual(self.repeat_decode(received), reference)

    def test_reference_does_not_correct_error_before_reference_creation(self):
        truth = (2, 5)
        measured = (3, 5)
        reference = tuple(measured)
        self.assertEqual(self.repeat_decode(self.repeat_encode(measured)), reference)
        self.assertNotEqual(reference, truth)

    def test_evaluation_code_has_distance_five_at_same_symbol_budget(self):
        self.assertEqual(len(self.eval_codebook), 49)
        self.assertEqual(min(self.hamming(a, b) for a, b in
                             combinations(self.eval_codebook, 2)), 5)

    def test_evaluation_code_corrects_all_two_symbol_errors(self):
        # 49 messages * 15 position pairs * 36 nonzero error pairs = 26,460 cases.
        cases = 0
        for word, message in self.eval_codebook.items():
            for left, right in combinations(range(6), 2):
                for a, b in product(range(1, 7), repeat=2):
                    received = list(word)
                    received[left] = (received[left]+a) % 7
                    received[right] = (received[right]+b) % 7
                    self.assertEqual(self.eval_decode(received), message)
                    cases += 1
        self.assertEqual(cases, 26460)

    def test_evaluation_code_corrects_the_periodic_example(self):
        message = (2, 5)
        received = [(message[0]+message[1]*t) % 7 for t in range(6)]
        for t in (0, 3):
            received[t] = (received[t]+1) % 7
        self.assertEqual(self.eval_decode(received), message)

    def test_unknown_interference_phase_needs_a_worst_phase_test(self):
        times = (0, 3, 4)
        for omega in (0, math.pi/2, 2*math.pi/3, math.pi, 2*math.pi):
            response = sum(cmath.exp(1j*omega*t) for t in times)/3
            worst_phase = -cmath.phase(response)
            observed = sum(math.cos(omega*t+worst_phase) for t in times)/3
            self.assertAlmostEqual(observed, abs(response), places=13)
        # Common-mode and sample-synchronous sinusoids pass with full gain.
        self.assertAlmostEqual(abs(sum(cmath.exp(2j*math.pi*t) for t in times)/3), 1)
        gain_period_three = abs(sum(cmath.exp(2j*math.pi*t/3) for t in times)/3)
        self.assertAlmostEqual(gain_period_three, 1/math.sqrt(3), places=13)

    def test_unrelated_fixed_text_does_not_separate_aliased_measurements(self):
        measure = lambda pair: sum(pair)
        attach_fixed_reference = lambda y: (y, "fixed recitation / fixed canonical text")
        self.assertEqual(attach_fixed_reference(measure((1, 0))),
                         attach_fixed_reference(measure((0, 1))))


class ZetaCheckChannels(unittest.TestCase):
    def test_two_protected_zeta_readouts_correct_one_symbol(self):
        cases = 0
        for message in product(range(4), repeat=4):
            reference = zeta_check_channels(message)
            self.assertEqual(decode_one_error_from_zeta_channels(message, reference), message)
            for position in range(4):
                for replacement in range(4):
                    if replacement == message[position]:
                        continue
                    received = list(message)
                    received[position] = replacement
                    self.assertEqual(decode_one_error_from_zeta_channels(received, reference), message)
                    cases += 1
        self.assertEqual(cases, 3072)

    def test_unweighted_spectral_zeta_cannot_locate_permutations(self):
        spectra = ([2, 3, 5], [5, 2, 3])
        for s in (-2, -1, 1, 2, 0.7+0.2j):
            self.assertLess(abs(sum(x**(-s) for x in spectra[0])
                                - sum(x**(-s) for x in spectra[1])), 1e-13)
        self.assertNotEqual(spectra[0], spectra[1])

    def test_two_zeta_checks_have_multisymbol_collisions(self):
        original, other = (2, 2, 2, 2), (3, 0, 3, 2)
        self.assertNotEqual(original, other)
        self.assertEqual(zeta_check_channels(original), zeta_check_channels(other))
        self.assertEqual(decode_one_error_from_zeta_channels(other, zeta_check_channels(original)), other)

    def test_outside_one_error_radius_can_miscorrect(self):
        original, two_errors = (2, 2, 2), (3, 2, 3)
        reference = zeta_check_channels(original)
        decoded = decode_one_error_from_zeta_channels(two_errors, reference)
        self.assertEqual(decoded, (3, 0, 3))
        self.assertNotEqual(decoded, original)
        self.assertEqual(zeta_check_channels(decoded), reference)


if __name__ == '__main__':
    unittest.main()
