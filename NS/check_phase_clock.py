"""Finite numerical checks for two clocks of the affine-flow example.
Run: python3 NS/check_phase_clock.py
Standard library only. Float64 checks, not interval certificates.
"""
import cmath
import math
import unittest

def phase(t,a,omega0):
    if a<=0 or t<0 or omega0==0: raise ValueError("a>0, t>=0, omega0!=0")
    return omega0/a*math.expm1(a*t)

def time_from_phase(theta,a,omega0):
    if a<=0 or omega0==0: raise ValueError("a>0 and omega0!=0")
    r=a*theta/omega0
    if r<0: raise ValueError("phase must be reachable from t=0 in this model")
    return math.log1p(r)/a

def zeta_clock(t,a):
    if a<=0 or t<0: raise ValueError("a>0 and t>=0")
    return 2*math.exp(a*t)+math.exp(-2*a*t)

def time_from_zeta(z,a):
    """Unique branch t>=0 for known a; bisection, not a validated inverse."""
    if a<=0 or z<3 or not math.isfinite(z):
        raise ValueError("a>0 and finite z>=3")
    if z==3: return 0.0
    lo,hi=1.0,z/2
    # Solve 2s+s^-2=z, s>=1; t=log(s)/a.
    for _ in range(100):
        mid=(lo+hi)/2
        if 2*mid+1/(mid*mid)<z: lo=mid
        else: hi=mid
    return math.log((lo+hi)/2)/a

class PhaseClockChecks(unittest.TestCase):
    def test_unwrapped_phase_roundtrip(self):
        for a in (.5,1.,3.):
            for omega in (-2.,.7,2.):
                for t in (0.,.01,.5,2.):
                    self.assertAlmostEqual(time_from_phase(phase(t,a,omega),a,omega),t,places=12)

    def test_same_wrapped_phase_different_times(self):
        a,omega=1.,2.
        phases=[.3+2*math.pi*k for k in range(4)]
        times=[time_from_phase(th,a,omega) for th in phases]
        self.assertTrue(all(y>x for x,y in zip(times,times[1:])))
        for th in phases:
            self.assertLess(abs(cmath.exp(1j*th)-cmath.exp(.3j)),2e-14)

    def test_full_turn_between_samples_can_be_invisible(self):
        t1=time_from_phase(2*math.pi,1.,1.)
        self.assertGreater(t1,0)
        principal_increment=cmath.phase(cmath.exp(1j*phase(t1,1.,1.)))
        self.assertAlmostEqual(principal_increment,0.,places=13)
        # No algorithm seeing just these endpoint phasors can choose 0 vs 2pi.

    def test_known_strain_rate_allows_spectral_clock(self):
        for a in (.5,1.,3.):
            for t in (0.,.01,.5,2.):
                self.assertAlmostEqual(time_from_zeta(zeta_clock(t,a),a),t,places=11)
        self.assertAlmostEqual(time_from_zeta(17/4,1.),math.log(2),places=13)

    def test_unknown_rate_prevents_absolute_time(self):
        # Same product a*t, hence same full C spectrum, different elapsed time.
        self.assertEqual(zeta_clock(1.,1.),zeta_clock(.5,2.))
        self.assertNotEqual(1.,.5)

    def test_clock_starts_quadratically(self):
        # Z(t)=3+3(a*t)^2+O((a*t)^3), so inverse sensitivity is singular at start.
        errors=[]
        for t in (.01,.005,.0025):
            errors.append(abs((zeta_clock(t,1.)-3)/t**2-3))
        self.assertTrue(all(y<x for x,y in zip(errors,errors[1:])))
        self.assertLess(errors[-1],.008)

    def test_wrong_branch_rejected(self):
        for z,a in ((2.9,1.),(4.,0.),(math.inf,1.)):
            with self.assertRaises(ValueError): time_from_zeta(z,a)
        with self.assertRaises(ValueError): time_from_phase(-1.,1.,1.)

if __name__=='__main__':
    unittest.main(verbosity=2)
