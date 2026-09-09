"""Exact finite checks: a rotating control volume inside solid-body rotation.
Run: python3 NS/check_moving_volume.py
Only standard-library Fractions; polynomial face integrals use exact Simpson.
This is a local finite example, not a global finite-energy solution on R^3.
"""
from fractions import Fraction as Q
import unittest

ZERO = (Q(0), Q(0))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(k,a): return tuple(k*x for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def turn(a): return (-a[1],a[0])
def rotate(a,c,s): return (c*a[0]-s*a[1],s*a[0]+c*a[1])

RHO, OMEGA = Q(3), Q(2)
# Counterclockwise rectangle [1,3] x [-1,1], per unit axial length.
VERTICES = ((Q(1),Q(-1)),(Q(3),Q(-1)),(Q(3),Q(1)),(Q(1),Q(1)))
AREA, CENTER = Q(4), (Q(2),Q(0))

def velocity(x): return scale(OMEGA,turn(x))
def pressure(x): return RHO*OMEGA**2*dot(x,x)/2

def boundary_integral(fn,c=Q(1),s=Q(0)):
    """fn(x, outward_normal_times_edge_length); cubic-exact in edge parameter."""
    vertices = [rotate(v,c,s) for v in VERTICES]
    total = None
    for i,a in enumerate(vertices):
        b = vertices[(i+1)%4]
        edge = add(b,scale(-1,a))
        nds = (edge[1],-edge[0])
        for t,weight in ((Q(0),Q(1,6)),(Q(1,2),Q(4,6)),(Q(1),Q(1,6))):
            val = fn(add(a,scale(t,edge)),nds)
            if total is None: total=[Q(0)]*len(val)
            total=[v+weight*w for v,w in zip(total,val)]
    return tuple(total)

def flux(alpha,c=Q(1),s=Q(0)):
    return boundary_integral(
        lambda x,n: scale(RHO*(1-alpha)*dot(velocity(x),n),velocity(x)),c,s)

def force(c=Q(1),s=Q(0)):
    return boundary_integral(lambda x,n: scale(-pressure(x),n),c,s)

def storage(alpha,c=Q(1),s=Q(0)):
    # P(t)=rho*area*Omega*J*c(t), c'=alpha*Omega*J*c, J^2=-I.
    return scale(-alpha*RHO*AREA*OMEGA**2,rotate(CENTER,c,s))

class MovingVolumeChecks(unittest.TestCase):
    def test_pressure_force_and_fixed_window(self):
        self.assertEqual(force(),(Q(-96),Q(0)))
        self.assertEqual(storage(Q(0)),ZERO)
        self.assertEqual(flux(Q(0)),force())

    def test_material_boundary_no_crossing_but_force_remains(self):
        self.assertEqual(flux(Q(1)),ZERO)
        for x in VERTICES:
            self.assertEqual(add(velocity(x),scale(-1,velocity(x))),ZERO)
        self.assertEqual(storage(Q(1)),force())
        self.assertNotEqual(force(),ZERO)

    def test_same_balance_in_rotating_windows(self):
        for c,s in ((Q(1),Q(0)),(Q(3,5),Q(4,5)),(Q(0),Q(1))):
            self.assertEqual(c*c+s*s,1)
            for alpha in (Q(-1),Q(0),Q(1,2),Q(1),Q(2)):
                with self.subTest(c=c,s=s,alpha=alpha):
                    self.assertEqual(add(storage(alpha,c,s),flux(alpha,c,s)),force(c,s))

    def test_zero_net_mass_flux_is_not_zero_local_crossing(self):
        mass=boundary_integral(lambda x,n:(RHO*dot(velocity(x),n),))
        self.assertEqual(mass,(Q(0),))
        self.assertNotEqual(dot(velocity((Q(3),Q(1))), (Q(1),Q(0))),0)

    def test_omitting_relative_velocity_breaks_material_balance(self):
        # Deliberate wrong formula: use fixed-window flux for a material parcel.
        self.assertNotEqual(add(storage(Q(1)),flux(Q(0))),force())

    def test_angular_momentum_flux_and_torque(self):
        # About a fixed origin; the local pressure torque need not vanish.
        torque=boundary_integral(lambda x,n:(cross(x,scale(-pressure(x),n)),))
        self.assertEqual(torque,(Q(0),))
        self.assertNotEqual(cross((Q(3),Q(1)),scale(-pressure((Q(3),Q(1))),(Q(1),Q(0)))),0)
        for alpha in (Q(0),Q(1,2),Q(1)):
            angular_flux=boundary_integral(
                lambda x,n:(RHO*cross(x,velocity(x))*(1-alpha)*dot(velocity(x),n),))
            self.assertEqual(angular_flux,(Q(0),))
        # Every material particle keeps |x|, so rho*Omega*integral |x|^2 is constant.

    def test_rotation_is_not_shear(self):
        def dissipation(A,mu):
            D=[[Q(A[i][j]+A[j][i],2) for j in range(2)] for i in range(2)]
            return 2*mu*sum(v*v for row in D for v in row)
        self.assertEqual(dissipation(((0,-2),(2,0)),Q(5)),0)
        # Following the flow does not cancel strain or viscous dissipation.
        self.assertEqual(dissipation(((0,2),(0,0)),Q(5)),20)

if __name__=='__main__':
    unittest.main(verbosity=2)
