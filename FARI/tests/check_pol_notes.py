"""Finite checks for the review comments in PÓŁ; not a proof of Firoozbakht.
Run from repository root: python3 FARI/tests/check_pol_notes.py
Requires NumPy through check_rh_formulas; float64 checks are not intervals.
"""
import math
import unittest
import numpy as np
from check_rh_formulas import euler_maclaurin

LIMIT = 2**20

def primes_up_to(limit):
    sieve = bytearray(b'\1') * (limit + 1)
    sieve[:2] = b'\0\0'
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p*p::p] = bytes((limit-p*p)//p+1)
    return [p for p in range(limit+1) if sieve[p]]

class NotesChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.primes = primes_up_to(LIMIT)

    def test_prime_count(self):
        self.assertEqual(len(self.primes), 82025)

    def test_sum_two_evaluations(self):
        scalar = math.fsum(math.expm1(math.log(p)/m)/math.sqrt(m)
                           for m,p in enumerate(self.primes,1))
        m = np.arange(1,len(self.primes)+1,dtype=float)
        vector = float(np.sum(np.expm1(np.log(self.primes)/m)/np.sqrt(m)))
        self.assertLess(abs(scalar-vector), 1e-12)
        self.assertAlmostEqual(scalar, 7.069617410744346, places=11)

    def test_zeta_derivative_at_three_halves(self):
        # Complex-step differentiation of Euler–Maclaurin; two truncations.
        for N in (32,64):
            value = -euler_maclaurin(1.5+1e-7j,N,8).imag/1e-7
            self.assertAlmostEqual(value, 3.932239737430942, places=10)

    def test_zeta_derivative_at_minus_two(self):
        rhs = -float(euler_maclaurin(3,32,8))/(4*math.pi**2)
        for N in (16,32):
            lhs = euler_maclaurin(-2+1e-7j,N,8).imag/1e-7
            self.assertLess(abs(lhs-rhs), 1e-9)

if __name__ == '__main__':
    unittest.main(verbosity=2)
