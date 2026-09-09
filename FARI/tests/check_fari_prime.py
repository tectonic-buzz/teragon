"""Exact Lucas certificate for the existing palindromic address.

Run: python3 FARI/tests/check_fari_prime.py
Criterion: full factorization of n-1 into certified primes, a^(n-1)=1
mod n, and gcd(a^((n-1)/q)-1,n)=1 for every prime q dividing n-1.
https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/LucasPrimality.html
"""

from math import gcd, prod
import unittest

PRIME = 9999987899999
CERTIFICATE = {
    3: (2, (2,)),
    5: (2, (2, 2)),
    7: (3, (2, 3)),
    11: (2, (2, 5)),
    19: (2, (2, 3, 3)),
    23: (5, (2, 11)),
    41: (6, (2, 2, 2, 5)),
    43: (3, (2, 3, 7)),
    173: (2, (2, 2, 43)),
    5659: (2, (2, 3, 23, 41)),
    552217: (10, (2, 2, 2, 3, 7, 19, 173)),
    22088681: (3, (2, 2, 2, 5, 552217)),
    44177363: (2, (2, 22088681)),
    883547261: (2, (2, 2, 5, 44177363)),
    PRIME: (11, (2, 5659, 883547261)),
}


def verify(n, certificate):
    if n == 2:
        return True
    if n < 2 or n not in certificate:
        return False
    a, factors = certificate[n]
    if not factors or prod(factors) != n - 1:
        return False
    if any(q < 2 or q >= n or not verify(q, certificate)
           for q in set(factors)):
        return False
    return (pow(a, n - 1, n) == 1
            and all(gcd(pow(a, (n - 1)//q, n) - 1, n) == 1
                    for q in set(factors)))


class CertificateChecks(unittest.TestCase):
    def test_palindrome(self):
        self.assertEqual(str(PRIME), str(PRIME)[::-1])
        self.assertEqual(len(str(PRIME)), 13)

    def test_exact_prime_certificate(self):
        self.assertTrue(verify(PRIME, CERTIFICATE))

    def test_bad_witness_rejected(self):
        changed = dict(CERTIFICATE)
        changed[PRIME] = (1, CERTIFICATE[PRIME][1])
        self.assertFalse(verify(PRIME, changed))

    def test_missing_factor_certificate_rejected(self):
        changed = dict(CERTIFICATE)
        del changed[5659]
        self.assertFalse(verify(PRIME, changed))

    def test_composite_rejected(self):
        self.assertFalse(verify(9, {3: (2, (2,)), 9: (2, (2, 2, 2))}))


if __name__ == '__main__':
    unittest.main(verbosity=2)
