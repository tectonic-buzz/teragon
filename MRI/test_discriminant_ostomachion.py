"""Exact finite checks for DISCRIMINANT_AND_OSTOMACHION.md.

No enumeration of the 268 STOMACH tilings is claimed here. The independent
graph calculation is the 64-vertex symmetry factor specified by Chung/Graham.
Python standard library only. Sources and mathematical domains are in the note.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import product
from math import comb, exp, isqrt
import unittest


PRIMES = (2, 3, 5, 7, 11, 13, 17)
ROWS = ((0, 1), (1, 1), (2, 1), (3, 1), (1, -1), (2, -1))


def factors(n):
    if not isinstance(n, int) or n == 0:
        raise ValueError("Factorization requires a nonzero integer")
    n = abs(n)
    result = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            result[p] = result.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        result[n] = result.get(n, 0) + 1
    return result


def legendre(d, p):
    if p <= 2 or factors(p) != {p: 1}:
        raise ValueError("Legendre symbol requires an odd prime")
    value = pow(d % p, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def root_count(v, w, p):
    return sum((x*x - v*x + w) % p == 0 for x in range(p))


def field_discriminant(d):
    """Discriminant of Q(sqrt(d)); reject the split and nonreduced cases."""
    primes = factors(d)
    squarefree = -1 if d < 0 else 1
    for p, exponent in primes.items():
        if exponent % 2:
            squarefree *= p
    if squarefree == 1:
        raise ValueError("A nonzero square does not define a quadratic field")
    return squarefree if squarefree % 4 == 1 else 4 * squarefree


def field_character(dk, p):
    if p != 2:
        return legendre(dk, p)
    if dk % 2 == 0:
        return 0
    return 1 if dk % 8 == 1 else -1


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def mobius_regime(matrix):
    a, b = matrix[0]
    c, d = matrix[1]
    determinant = a*d - b*c
    if determinant == 0:
        return "not_mobius"
    if determinant < 0:
        return "orientation_reversing"
    if b == c == 0 and a == d:
        return "identity"
    disc = (a+d)**2 - 4*determinant
    return "elliptic" if disc < 0 else "hyperbolic" if disc > 0 else "parabolic"


def padic_abs(x, p):
    x = Q(x)
    if not x:
        return Q(0)
    power = factors(x.denominator).get(p, 0) - factors(x.numerator).get(p, 0)
    return Q(p) ** power


class QuadraticChecks(unittest.TestCase):
    def test_all_six_rows_by_direct_roots(self):
        expected = (
            (1, 0, 2, 0, 0, 2, 2),
            (0, 1, 0, 2, 0, 2, 0),
            (1, 1, 1, 1, 1, 1, 1),
            (0, 0, 1, 0, 2, 0, 0),
            (0, 0, 1, 0, 2, 0, 0),
            (1, 0, 0, 2, 0, 0, 2),
        )
        self.assertEqual(tuple(tuple(root_count(v, w, p) for p in PRIMES)
                               for v, w in ROWS), expected)

    def test_root_formula_over_odd_primes(self):
        for v, w, p in product(range(-8, 9), range(-8, 9), PRIMES[1:]):
            self.assertEqual(root_count(v, w, p), 1 + legendre(v*v - 4*w, p))

    def test_two_requires_more_than_discriminant_mod_two(self):
        self.assertEqual(1 % 2, 5 % 2)
        self.assertEqual(root_count(1, 0, 2), 2)
        self.assertEqual(root_count(1, -1, 2), 0)
        with self.assertRaises(ValueError):
            legendre(5, 2)

    def test_kronecker_at_two_against_integral_basis(self):
        for dk in (-4, -3, 5, 8, 12, 13, 17, 21):
            if dk % 4 == 1:
                v, w = 1, (1 - dk) // 4
            else:
                v, w = 0, -dk // 4
            self.assertEqual(root_count(v, w, 2), 1 + field_character(dk, 2))

    def test_order_index_changes_bad_prime_list(self):
        for v, w, dk, index in ((7, 1, 5, 3), (0, -5, 5, 2),
                                (3, 1, 5, 1), (2, -1, 8, 1)):
            d = v*v - 4*w
            self.assertEqual(field_discriminant(d), dk)
            self.assertEqual(d, index*index*dk)
            self.assertEqual(isqrt(d // dk), index)

    def test_three_is_inert_despite_repeated_polynomial_root(self):
        self.assertEqual(root_count(7, 1, 3), 1)
        self.assertEqual(legendre(45, 3), 0)
        self.assertEqual(field_character(field_discriminant(45), 3), -1)
        self.assertEqual(root_count(1, -1, 3), 0)

    def test_two_is_inert_despite_repeated_polynomial_root(self):
        self.assertEqual(root_count(0, -5, 2), 1)
        self.assertEqual(field_character(field_discriminant(20), 2), -1)

    def test_zero_discriminant_is_not_a_number_field(self):
        with self.assertRaises(ValueError):
            field_discriminant(0)
        with self.assertRaises(ValueError):
            factors(0)
        for p in PRIMES:
            self.assertEqual(root_count(2, 1, p), 1)
            # (x-1)^2 = 0 in F_p[x]/((x-1)^2), but x-1 is not zero.
            self.assertNotEqual(((-1) % p, 1), (0, 0))

    def test_positive_square_discriminant_is_not_a_quadratic_field(self):
        with self.assertRaises(ValueError):
            field_discriminant(9)

    def test_trace_norm_companion_and_orientation(self):
        for v, w in ROWS:
            a = ((v, -w), (1, 0))
            expected = ("orientation_reversing" if w < 0 else
                        "elliptic" if v*v - 4*w < 0 else
                        "hyperbolic" if v*v - 4*w > 0 else "parabolic")
            self.assertEqual(mobius_regime(a), expected)
        self.assertEqual(mobius_regime(((1, 0), (0, 1))), "identity")
        self.assertEqual(mobius_regime(((1, 0), (1, 0))), "not_mobius")

    def test_golden_square_is_cat_with_positive_determinant(self):
        golden = ((1, 1), (1, 0))
        cat = mm(golden, golden)
        self.assertEqual(cat, ((2, 1), (1, 1)))
        self.assertEqual(mobius_regime(cat), "hyperbolic")

    def test_count_ramified_places_not_one_plus_polynomial_omega(self):
        def count(d):
            dk = field_discriminant(d)
            return len(factors(dk)) + int(dk < 0)
        self.assertEqual(count(45), 1)   # Only 5; real infinity splits.
        self.assertEqual(1 + len(factors(45)), 3)
        self.assertEqual(count(-4), 2)   # 2 and real-to-complex infinity.
        self.assertEqual(count(12), 2)
        self.assertEqual(count(21), 2)

    def test_product_formula_exactly_for_rationals(self):
        for numerator, denominator in product(range(-25, 26), range(1, 26)):
            if numerator == 0:
                continue
            x = Q(numerator, denominator)
            primes = set(factors(x.numerator)) | set(factors(x.denominator))
            result = abs(x)
            for p in primes:
                result *= padic_abs(x, p)
            self.assertEqual(result, 1)
        self.assertEqual(Q(1729, 7*13*19), 1)

    def test_product_without_infinity_can_equal_one(self):
        for x in (1, -1):
            self.assertTrue(all(padic_abs(x, p) == 1 for p in PRIMES))

    def test_zeta_local_factor_exposes_wrong_order_readout(self):
        p, s = 3, 2
        q = Q(1, p**s)
        correct = 1 / ((1-q) * (1+q))  # Inert prime: norm p^2.
        wrong = 1 / (1-q)              # Mistakenly called ramified.
        self.assertEqual(correct, Q(81, 80))
        self.assertEqual(wrong, Q(9, 8))
        self.assertNotEqual(correct, wrong)


# B = K_2 box K_2 box K_2 box K_8. Labels of K_8 are arbitrary bit strings;
# Walsh vectors below diagonalize the complete graph, not a claim that D_4
# is an abelian group. All seven nonconstant K_8 modes have eigenvalue 8.
BLOCK_VERTICES = tuple(product(range(8), range(8)))


def parity(n):
    return bin(n).count("1") % 2


def neighbors(vertex):
    a, b = vertex
    return tuple((a ^ (1 << i), b) for i in range(3)) + tuple(
        (a, j) for j in range(8) if j != b)


def mode(a, b, vertex):
    x, y = vertex
    return (-1) ** (parity(a & x) + parity(b & y))


def eigenvalue(a, b):
    return 2 * bin(a).count("1") + (8 if b else 0)


class OstomachionFactorChecks(unittest.TestCase):
    def test_binary_fourier_projectors_over_rationals(self):
        plus = ((Q(1, 2), Q(1, 2)), (Q(1, 2), Q(1, 2)))
        minus = ((Q(1, 2), Q(-1, 2)), (Q(-1, 2), Q(1, 2)))
        self.assertEqual(mm(plus, plus), plus)
        self.assertEqual(mm(minus, minus), minus)
        self.assertEqual(mm(plus, minus), ((0, 0), (0, 0)))
        self.assertEqual(tuple(tuple(plus[i][j] + minus[i][j] for j in range(2))
                               for i in range(2)), ((1, 0), (0, 1)))

    def test_binary_fourier_basis_collapses_in_characteristic_two(self):
        first, second = (1, 1), (1, -1)
        self.assertEqual(first[0]*second[1] - first[1]*second[0], -2)
        self.assertEqual(tuple(x % 2 for x in first), tuple(x % 2 for x in second))

    def test_nonzero_nilpotent_survives_the_collapsed_readout(self):
        nilpotent = ((1, 1), (1, 1))  # S-I modulo 2.
        self.assertNotEqual(nilpotent, ((0, 0), (0, 0)))
        self.assertEqual(tuple(tuple(x % 2 for x in row) for row in mm(nilpotent, nilpotent)),
                         ((0, 0), (0, 0)))

    def test_determinant_zeta_loses_jordan_information_mod_two(self):
        swap_denominator = (1, 0, -1)    # det(I-tS)
        identity_denominator = (1, -2, 1)  # det(I-tI_2)
        self.assertNotEqual(swap_denominator, identity_denominator)
        self.assertEqual(tuple(x % 2 for x in swap_denominator),
                         tuple(x % 2 for x in identity_denominator))

    def test_independent_symmetry_factor_has_64_vertices_and_degree_ten(self):
        self.assertEqual(len(BLOCK_VERTICES), 64)
        self.assertTrue(all(len(set(neighbors(v))) == 10 for v in BLOCK_VERTICES))

    def test_all_64_modes_by_direct_laplacian_action(self):
        for a, b in BLOCK_VERTICES:
            lam = eigenvalue(a, b)
            for v in BLOCK_VERTICES:
                lv = sum(mode(a, b, v) - mode(a, b, u) for u in neighbors(v))
                self.assertEqual(lv, lam * mode(a, b, v))

    def test_mode_basis_is_complete_by_orthogonality(self):
        for a, b in BLOCK_VERTICES:
            for c, d in BLOCK_VERTICES:
                inner = sum(mode(a, b, v) * mode(c, d, v) for v in BLOCK_VERTICES)
                self.assertEqual(inner, 64 if (a, b) == (c, d) else 0)

    def test_heat_factorization_and_zero_mode(self):
        spectrum = Counter(eigenvalue(a, b) for a, b in BLOCK_VERTICES)
        self.assertEqual(spectrum, {0: 1, 2: 3, 4: 3, 6: 1,
                                    8: 7, 10: 21, 12: 21, 14: 7})
        for t in (0, 0.1, 0.7, 2):
            direct = sum(m * exp(-t*lam) for lam, m in spectrum.items())
            factored = (1 + exp(-2*t))**3 * (1 + 7*exp(-8*t))
            self.assertAlmostEqual(direct, factored, places=12)

    def test_spectral_zeta_additional_readout_two_routes(self):
        for s in (1, 2, 3):
            direct = sum(Q(1, eigenvalue(a, b)**s)
                         for a, b in BLOCK_VERTICES if (a, b) != (0, 0))
            factored = sum(comb(3, j) * Q(1, (2*j)**s) for j in range(1, 4))
            factored += sum(7*comb(3, j) * Q(1, (2*j+8)**s) for j in range(4))
            self.assertEqual(direct, factored)

    def test_reported_component_sizes_match_product_not_reenumeration(self):
        self.assertEqual(268*64, 17152)
        self.assertEqual((266*64, 2*64), (17024, 128))
        # Two zero modes belong to G. Multiplying by connected B preserves two.
        self.assertEqual(2 * sum(eigenvalue(a, b) == 0 for a, b in BLOCK_VERTICES), 2)


if __name__ == "__main__":
    unittest.main()
