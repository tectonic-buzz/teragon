"""Exact rational checks for an affine stretching/rotating fluid.
Run: python3 NS/check_stretching_envelope.py
The cases test the displayed algebra; they do not certify global NS regularity.
"""
from fractions import Fraction as Q
import unittest

def matrix(rows): return tuple(tuple(Q(x) for x in row) for row in rows)
def transpose(A): return tuple(zip(*A))
def add(A,B): return tuple(tuple(x+y for x,y in zip(a,b)) for a,b in zip(A,B))
def multiply(A,B):
    return tuple(tuple(sum(x*y for x,y in zip(a,b)) for b in transpose(B)) for a in A)
def act(A,v): return tuple(sum(x*y for x,y in zip(row,v)) for row in A)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def diagonal(values): return tuple(tuple(v if i==j else Q(0) for j in range(3)) for i,v in enumerate(values))
def trace(A): return sum(A[i][i] for i in range(3))
def det(A):
    return (A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])
            -A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])
            +A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]))
def gradient(a,omega):
    return matrix(((-a/2,-omega,0),(omega,-a/2,0),(0,0,a)))
def time_gradient(a,omega):
    return matrix(((0,-a*omega,0),(a*omega,0,0),(0,0,0)))
def curl(A):
    return (A[2][1]-A[1][2],A[0][2]-A[2][0],A[1][0]-A[0][1])
def metric(s): return diagonal((1/s,1/s,s*s))
def zeta_metric(s,q):
    return sum(value**(-q) for value in (1/s,1/s,s*s))
CASES=tuple((Q(a),Q(o)) for a in (1,2,3) for o in (-2,0,1,3))

class StretchingEnvelopeChecks(unittest.TestCase):
    def test_incompressibility(self):
        for a,o in CASES:
            self.assertEqual(trace(gradient(a,o)),0)

    def test_acceleration_matches_pressure_gradient(self):
        for a,o in CASES:
            A=gradient(a,o)
            acceleration=add(time_gradient(a,o),multiply(A,A))
            # This is - Hessian(p)/rho for the pressure written in the note.
            expected=diagonal((a*a/4-o*o,a*a/4-o*o,a*a))
            self.assertEqual(acceleration,expected)

    def test_vorticity_stretching(self):
        for a,o in CASES:
            A=gradient(a,o)
            self.assertEqual(curl(A),(0,0,2*o))
            self.assertEqual(curl(time_gradient(a,o)),act(A,curl(A)))

    def test_material_enstrophy_growth(self):
        for a,o in CASES:
            w=curl(gradient(a,o))
            wdot=curl(time_gradient(a,o))
            # e=|w|^2/2; for a material parcel, volume is constant.
            self.assertEqual(dot(w,wdot),2*a*(dot(w,w)/2))

    def test_viscous_dissipation_is_nonzero(self):
        mu=Q(5)
        for a,o in CASES:
            A=gradient(a,o)
            symmetric=add(A,transpose(A))
            D=tuple(tuple(x/2 for x in row) for row in symmetric)
            dissipation=2*mu*sum(x*x for row in D for x in row)
            self.assertEqual(dissipation,3*mu*a*a)
            self.assertGreater(dissipation,0)

    def test_volume_vs_spectral_deformation_readout(self):
        for s in (Q(1),Q(2),Q(4),Q(1,2)):
            self.assertEqual(det(metric(s)),1)
            self.assertEqual(zeta_metric(s,0),3)
            self.assertEqual(zeta_metric(s,1),2*s+s**(-2))
            self.assertGreaterEqual(zeta_metric(s,1),3)
        self.assertEqual(zeta_metric(Q(2),1),Q(17,4))
        self.assertEqual(zeta_metric(Q(2),-1),Q(5))

    def test_metric_loses_rotation_and_vorticity(self):
        # At s=4, transverse lengths 1/2, axial length 4.
        D=diagonal((Q(1,2),Q(1,2),Q(4)))
        R=matrix(((Q(3,5),Q(-4,5),0),(Q(4,5),Q(3,5),0),(0,0,1)))
        F=multiply(R,D)
        self.assertEqual(det(F),1)
        self.assertEqual(multiply(transpose(F),F),metric(Q(4)))
        self.assertEqual(multiply(transpose(D),D),metric(Q(4)))
        # The family C(t) has no Omega0 parameter; different spins remain distinct.
        self.assertNotEqual(curl(gradient(Q(1),Q(0))),curl(gradient(Q(1),Q(4))))

    def test_freezing_spin_breaks_pressure_compatibility(self):
        A=gradient(Q(1),Q(2))
        wrong=multiply(A,A)  # Omits A', as if Omega were time-independent.
        self.assertNotEqual(wrong,transpose(wrong))
        # A pressure Hessian must be symmetric: the omitted spin evolution matters.

if __name__=='__main__':
    unittest.main(verbosity=2)
