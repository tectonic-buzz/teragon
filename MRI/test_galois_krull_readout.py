"""Finite controls for Galois sectors and Krull-style address refinement.

Standard library only. No claim to reconstruct an infinite Galois group from
finitely many observations, or to decode data using scalar zeta alone.
"""

import cmath
import itertools
import math
import unittest
from fractions import Fraction as Q


S3 = list(itertools.permutations(range(3)))
IDENTITY = (0, 1, 2)


def characters(p):
    inversions = sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3))
    return (1, (-1)**inversions, sum(p[i] == i for i in range(3))-1)


def permutation_sign(p):
    return (-1)**sum(p[i] > p[j] for i in range(len(p))
                    for j in range(i+1, len(p)))


def cycle_lengths(p):
    unseen, lengths = set(range(len(p))), []
    while unseen:
        start = next(iter(unseen))
        current, length = start, 0
        while current in unseen:
            unseen.remove(current)
            length += 1
            current = p[current]
        lengths.append(length)
    return sorted(lengths)


def swap_positions(p, i, j):
    result = list(p)
    result[i], result[j] = result[j], result[i]
    return tuple(result)


def transposition_distance(p, q):
    """Minimum number of arbitrary swaps, not adjacent swaps or Hamming."""
    inverse = [0]*len(p)
    for i, value in enumerate(p):
        inverse[value] = i
    relative = tuple(inverse[value] for value in q)
    return len(p)-len(cycle_lengths(relative))


def compose(p, q):
    return tuple(p[value] for value in q)


def inverse_permutation(p):
    inverse = [0]*len(p)
    for i, value in enumerate(p):
        inverse[value] = i
    return tuple(inverse)


def generated_group(generators, degree):
    identity = tuple(range(degree))
    known, frontier = {identity}, [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            candidate = compose(generator, current)
            if candidate not in known:
                known.add(candidate)
                frontier.append(candidate)
    return known


def derived_orders(group):
    group = set(group)
    orders = [len(group)]
    while len(group) > 1:
        inverses = {p: inverse_permutation(p) for p in group}
        commutators = {compose(compose(p, q), compose(inverses[p], inverses[q]))
                       for p in group for q in group}
        derived = generated_group(commutators, len(next(iter(group))))
        orders.append(len(derived))
        if derived == group:
            break
        group = derived
    return orders


class GaloisSectors(unittest.TestCase):
    def test_s3_character_orthogonality_and_regular_multiplicities(self):
        for i, j in itertools.product(range(3), repeat=2):
            inner = sum(Q(characters(p)[i]*characters(p)[j], 6) for p in S3)
            self.assertEqual(inner, int(i == j))
        for p in S3:
            regular = sum(d*c for d, c in zip((1, 1, 2), characters(p)))
            self.assertEqual(regular, 6 if p == IDENTITY else 0)

    def test_intermediate_field_requires_standard_representation(self):
        subgroup = [IDENTITY, (1, 0, 2)]
        multiplicities = [sum(Q(characters(h)[i], 2) for h in subgroup)
                          for i in range(3)]
        self.assertEqual(multiplicities, [1, 0, 1])
        self.assertEqual(sum(d*m for d, m in zip((1, 1, 2), multiplicities)), 3)
        # G/H is the three-point permutation action, computed independently.
        for p in S3:
            cosets_fixed = sum(p[i] == i for i in range(3))
            self.assertEqual(sum(m*c for m, c in zip(multiplicities, characters(p))),
                             cosets_fixed)

    def test_plus_sector_alone_does_not_determine_cover_spectrum(self):
        plus, minus = [Q(1), Q(1)], [Q(1), Q(-1)]
        for odd_eigenvalue in (3, 5):
            matrix = [[Q(2+odd_eigenvalue, 2), Q(2-odd_eigenvalue, 2)],
                      [Q(2-odd_eigenvalue, 2), Q(2+odd_eigenvalue, 2)]]
            apply = lambda vector: [sum(a*b for a, b in zip(row, vector))
                                    for row in matrix]
            self.assertEqual(apply(plus), [2*v for v in plus])
            self.assertEqual(apply(minus), [odd_eigenvalue*v for v in minus])
        self.assertNotEqual(Q(1, 2)+Q(1, 3), Q(1, 2)+Q(1, 5))

    def test_spectral_zeta_adds_while_determinant_multiplies(self):
        matrix = [[Q(7, 2), Q(-3, 2)], [Q(-3, 2), Q(7, 2)]]
        determinant = matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
        self.assertEqual(determinant, 2*5)
        inverse = [[matrix[1][1]/determinant, -matrix[0][1]/determinant],
                   [-matrix[1][0]/determinant, matrix[0][0]/determinant]]
        trace_inverse_squared = sum(inverse[i][j]*inverse[j][i]
                                    for i in range(2) for j in range(2))
        self.assertEqual(trace_inverse_squared, Q(1, 2**2)+Q(1, 5**2))
        self.assertNotEqual(trace_inverse_squared, Q(1, 2**2)*Q(1, 5**2))


class FiniteAddressRefinement(unittest.TestCase):
    def test_character_kernel_is_normalized_coset_indicator(self):
        size, address = 64, 19
        for depth in range(1, 7):
            quotient = 2**depth
            kernels = []
            for g in range(size):
                character_sum = sum(cmath.exp(2j*math.pi*k*(g-address)/quotient)
                                    for k in range(quotient))
                expected = quotient if (g-address) % quotient == 0 else 0
                self.assertLess(abs(character_sum-expected), 2e-11)
                kernels.append(expected)
            self.assertEqual(sum(Q(value, size) for value in kernels), 1)

    def test_compatible_observations_refine_without_inventing_bits(self):
        size, address = 64, 19
        for depth in range(1, 7):
            quotient = 2**depth
            candidates = [g for g in range(size) if g % quotient == address % quotient]
            self.assertEqual(len(candidates), size//quotient)
            for observed_depth in range(depth+1):
                # An arbitrary nonlinear observable on a coarser quotient.
                observable = lambda g: (g % 2**observed_depth)**2+3
                mean = sum(Q(observable(g), len(candidates)) for g in candidates)
                self.assertEqual(mean, observable(address))
            if depth < 6:
                self.assertGreater(len(candidates), 1)
                self.assertTrue(any(g != address for g in candidates))
            else:
                self.assertEqual(candidates, [address])


class AlternatingOrderChecks(unittest.TestCase):
    def test_parity_detects_one_swap_but_leaves_ten_candidates(self):
        permutations = list(itertools.permutations(range(5)))
        alternating = [p for p in permutations if permutation_sign(p) == 1]
        self.assertEqual(len(alternating), 60)
        for p in alternating:
            for i, j in itertools.combinations(range(5), 2):
                self.assertEqual(permutation_sign(swap_positions(p, i, j)), -1)
        received = swap_positions(tuple(range(5)), 0, 1)
        candidates = [p for p in alternating if transposition_distance(p, received) == 1]
        self.assertEqual(len(candidates), 10)

    def test_alternating_minimum_distance_depends_on_error_metric(self):
        identity = tuple(range(5))
        alternating = [p for p in itertools.permutations(range(5))
                       if permutation_sign(p) == 1 and p != identity]
        self.assertEqual(min(transposition_distance(identity, p) for p in alternating), 2)
        self.assertEqual(min(sum(a != b for a, b in zip(identity, p))
                             for p in alternating), 3)

    def test_cyclic_subcode_in_a_five_corrects_all_single_swaps(self):
        code = [tuple((i+r) % 5 for i in range(5)) for r in range(5)]
        self.assertTrue(all(permutation_sign(p) == 1 for p in code))
        self.assertEqual(min(transposition_distance(p, q)
                             for p, q in itertools.combinations(code, 2)), 4)
        trials = 0
        for source in code:
            for i, j in itertools.combinations(range(5), 2):
                received = swap_positions(source, i, j)
                candidates = [p for p in code if transposition_distance(p, received) <= 1]
                self.assertEqual(candidates, [source])
                trials += 1
        self.assertEqual(trials, 50)

    def test_permutation_zeta_cycle_poles_recover_parity(self):
        # zeta_p(t) = product_cycles (1-t^length)^(-1).
        # Its pole order at t=1 is the number of cycles, including fixed points.
        for p in itertools.permutations(range(5)):
            pole_order = len(cycle_lengths(p))
            self.assertEqual((-1)**(len(p)-pole_order), permutation_sign(p))

    def test_permutation_zeta_does_not_identify_rotation_address(self):
        rotations = [tuple((i+r) % 5 for i in range(5)) for r in range(1, 5)]
        self.assertEqual(len(set(rotations)), 4)
        for p in rotations:
            self.assertEqual(cycle_lengths(p), [5])  # Same zeta: 1/(1-t^5).
            for n in range(1, 16):
                fixed = 0
                for start in range(5):
                    point = start
                    for _ in range(n):
                        point = p[point]
                    fixed += point == start
                self.assertEqual(fixed, 5 if n % 5 == 0 else 0)


class SolvabilityControls(unittest.TestCase):
    def test_derived_series_on_four_finite_examples(self):
        cyclic_three = [tuple((i+r) % 3 for i in range(3)) for r in range(3)]
        dihedral_eight = generated_group([(1, 2, 3, 0), (0, 3, 2, 1)], 4)
        symmetric_four = list(itertools.permutations(range(4)))
        alternating_five = [p for p in itertools.permutations(range(5))
                            if permutation_sign(p) == 1]
        for group, expected in ((cyclic_three, [3, 1]),
                                (dihedral_eight, [8, 2, 1]),
                                (symmetric_four, [24, 12, 4, 1]),
                                (alternating_five, [60, 60])):
            self.assertEqual(derived_orders(group), expected)

    def test_prime_order_and_solvability_do_not_fix_correction_radius(self):
        for n, expected_minimum in ((3, 2), (5, 4)):
            code = [tuple((i+r) % n for i in range(n)) for r in range(n)]
            self.assertEqual(derived_orders(code), [n, 1])
            self.assertTrue(all(permutation_sign(p) == 1 for p in code))
            minimum = min(transposition_distance(p, q)
                          for p, q in itertools.combinations(code, 2))
            self.assertEqual(minimum, expected_minimum)
            received = swap_positions(code[0], 0, 1)
            candidates = [p for p in code if transposition_distance(p, received) <= 1]
            self.assertEqual(len(candidates), 3 if n == 3 else 1)


if __name__ == "__main__":
    unittest.main()
