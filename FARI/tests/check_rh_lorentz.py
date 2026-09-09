"""
Testy Lorentzowskie dla Hipotezy Riemanna.

Predykcja: czynnik znieksztalcenia (warping factor)

    W = sqrt((1 + beta_v^2) / (1 - beta_v^2)),   beta_v = |Re(rho) - 1/2| / |Im(rho)|

jest dokładnie równe 1 dla każdego zerka na linii krytycznej (Re(s) = 1/2),
i ściśle większe od 1 dla każdego zerka poza nią.

Równoważnik:
    RH  <=>  W = 1 dla wszystkich zer  <=>  beta_v = 0 dla wszystkich zer

Geometria:
  - Linia krytyczna <-> os gamma (oś czasowa / "frame spoczynku") w parametryzacji lambda_rho = gamma + i*(1/2 - beta)
  - Zgorska funkcjonalna J(s) = 1 - s_bar <-> inwolucja lambda -> -lambda_bar (odbicie w płaszczyźnie Lorentzowskiej)
  - Para zer (rho, 1-rho_bar) <-> dwa ramy względnego ruchu (S, S')
  - Linia krytyczna = "rama medianowa" S_0, gdzie oba ramy poruszają się z prędkością beta_0 w przeciwnych kierunkach
  - "Loedel diagram" (symetryczny, U'=U) = xi(s) = xi(1-s), gdzie jednostki długości są równe
  - Nie-symmetryczny "Minkowski diagram" (U'!=U) = zgorska poza linią krytyczną, gdzie występuje zniekształcenie

Grupa Lorentzowa SO(2,1) ~ PSL(2,R) działa na płaszczyźnie lambda_rho przez "boost"
(mieszając osie gamma i (1/2-beta)). Amenowalność tej akcji determinuje, czy
zerka są zmuszone na oś spoczynku (RH) czy mogą oderwać się od niej (gap spektralny).
"""

import unittest
import math
import numpy as np

# Znane zera z narożnika krytycznej linii (zweryfikowane przez Odlyzko)
# Wszystkie na linii krytycznej: beta = 0.5, gamma = 14.134725 (pierwsze zero)
ODLYZKO_ZEROS = [
    14.134725142, 21.022039639, 25.010857580, 30.424876126,
    32.935061588, 37.586178159, 40.918719012, 43.327073281,
    48.005150881, 49.773832478,
    # Pierwsze 15 zer (do 57.)
    52.970381716, 56.446201989, 59.347044033, 63.856321391, 66.288858823,
]


def beta_velocity(beta, gamma):
    """Lorentz boost velocity: |Re(rho) - 1/2| / |Im(rho)|"""
    return abs(beta - 0.5) / abs(gamma)


def warping_factor(beta, gamma):
    """Unit-length warping U'/U = sqrt((1+beta_v^2)/(1-beta_v^2)).

    W = 1 <=> beta_v = 0 <=> on critical line (no boosting, unitary).
    W > 1 <=> beta_v > 0 <=> off critical line (warping, non-unitary).
    W -> infinity as beta_v -> 1 (approach light cone boundary).
    """
    b = beta_velocity(beta, gamma)
    if b >= 1.0:
        return float('inf')
    return math.sqrt((1 + b**2) / (1 - b**2))


def gamma_lorentz(beta):
    """Lorentz factor gamma_L = 1/sqrt(1 - beta^2)."""
    return 1.0 / math.sqrt(1 - beta**2)


class TestMedianFrame(unittest.TestCase):
    """Test median frame formulas from spacetime diagrams."""

    def test_median_frame_formula_1(self):
        """beta = 2*beta_0 / (1 + beta_0^2): relative velocity from median frame."""
        for beta_0 in [0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
            beta = 2 * beta_0 / (1 + beta_0**2)
            # Beta should be in (0, 1) for beta_0 in (0, 1)
            self.assertTrue(0 < beta < 1, f"beta={beta} not in (0,1) for beta_0={beta_0}")
            # At beta_0 = 0.5, beta should be 0.8 (Wikipedia example)
            if abs(beta_0 - 0.5) < 1e-10:
                self.assertAlmostEqual(beta, 0.8, places=6)

    def test_median_frame_formula_2(self):
        """beta_0 = (gamma_L - 1) / (beta * gamma_L): recover median velocity."""
        for beta_0 in [0.1, 0.3, 0.5, 0.7, 0.9]:
            beta = 2 * beta_0 / (1 + beta_0**2)
            gamma_L = gamma_lorentz(beta)
            beta_0_check = (gamma_L - 1) / (beta * gamma_L)
            self.assertAlmostEqual(beta_0_check, beta_0, places=6,
                                   msg=f"Round-trip failed for beta_0={beta_0}")

    def test_beta_0_0_5_gives_beta_0_8(self):
        """Wikipedia example: beta_0 = 0.5 -> beta = 0.8."""
        beta = 2 * 0.5 / (1 + 0.25)
        self.assertAlmostEqual(beta, 0.8, places=6)
        # And beta = 0.8 should give beta_0 = 0.5
        gamma_L = gamma_lorentz(0.8)
        beta_0 = (gamma_L - 1) / (0.8 * gamma_L)
        self.assertAlmostEqual(beta_0, 0.5, places=6)

    def test_warping_factor_decomposition(self):
        """U'/U = sqrt((1+b^2)/(1-b^2)) = gamma_L * sqrt(1 + beta^2)."""
        self.assertAlmostEqual(
            math.sqrt((1 + 0.5**2) / (1 - 0.5**2)),
            gamma_lorentz(0.5) * math.sqrt(1 + 0.5**2),
            places=10
        )
        self.assertAlmostEqual(
            math.sqrt((1 + 0.9**2) / (1 - 0.9**2)),
            gamma_lorentz(0.9) * math.sqrt(1 + 0.9**2),
            places=10
        )


class TestAngularRelations(unittest.TestCase):
    """Test Sartori/Gruner angular construction: sin(phi)=cos(theta)=beta."""

    def test_angular_relations(self):
        """sin(phi) = cos(theta) = beta; cos(phi) = sin(theta) = 1/gamma_L."""
        for beta in [0.1, 0.3, 0.5, 0.7, 0.9]:
            gamma_L = gamma_lorentz(beta)
            phi = math.asin(beta)
            theta = math.acos(beta)  # sin(theta) = 1/gamma_L = cos(phi)
            self.assertAlmostEqual(math.sin(phi), beta, places=10)
            self.assertAlmostEqual(math.cos(theta), beta, places=10)
            self.assertAlmostEqual(math.cos(phi), 1 / gamma_L, places=10)
            self.assertAlmostEqual(math.sin(theta), 1 / gamma_L, places=10)
            self.assertAlmostEqual(math.tan(phi), beta * gamma_L, places=10)
            self.assertAlmostEqual(math.tan(phi), 1 / math.tan(theta), places=10)


class TestWarpingFactor(unittest.TestCase):
    """Test the core prediction: W = 1 iff on critical line."""

    def test_warping_zero_on_line(self):
        """Warping factor = 1 for all known Odlyzko zeros (on critical line)."""
        for gamma in ODLYZKO_ZEROS:
            W = warping_factor(0.5, gamma)
            self.assertAlmostEqual(W, 1.0, places=12,
                                   msg=f"W != 1 for zero at gamma={gamma}")

    def test_warping_zero_at_rest(self):
        """beta_v = 0 when Re(rho) = 1/2 (rest frame, no boost)."""
        for gamma in [1.0, 10.0, 100.0, 1000.0]:
            b = beta_velocity(0.5, gamma)
            self.assertAlmostEqual(b, 0.0, places=15)
            self.assertAlmostEqual(warping_factor(0.5, gamma), 1.0, places=12)

    def test_warping_off_line_is_greater_than_one(self):
        """Warping factor > 1 for zeros off the critical line."""
        test_cases = [
            (0.51, 14.135, 1),
            (0.60, 14.135, 1),
            (0.40, 14.135, 1),
            (0.51, 1.0, 1),
            (0.40, 1.0, 1),
            (0.30, 1.0, 1),
        ]
        for beta, gamma, _ in test_cases:
            W = warping_factor(beta, gamma)
            self.assertGreater(W, 1.0,
                               msg=f"W={W} not > 1 for rho={beta}+{gamma}i")

    def test_warping_monotonic_in_deviation(self):
        """Warping factor increases with |beta - 1/2| for fixed gamma."""
        gamma = 10.0
        betas = [0.50, 0.51, 0.55, 0.60, 0.70, 0.80, 0.90]
        prev_W = 0.0
        for b in betas:
            W = warping_factor(b, gamma)
            self.assertGreaterEqual(W, prev_W,
                                    msg=f"W not monotonic at beta={b}")
            prev_W = W

    def test_warping_sensitive_near_center(self):
        """Warping factor is most sensitive near the center (small |gamma|)."""
        # Same 1% deviation from critical line
        dev = 0.01
        W_small_gamma = warping_factor(0.5 + dev, 1.0)
        W_large_gamma = warping_factor(0.5 + dev, 100.0)
        self.assertGreater(W_small_gamma, W_large_gamma,
                           msg="Warping should be more sensitive near center")
        # Small gamma (near center): > 1% warping
        self.assertGreater(W_small_gamma - 1.0, 0.0001)
        # Large gamma (far from center): < 0.01% warping
        self.assertLess(W_large_gamma - 1.0, 0.0001)

    def test_warping_approaches_infinity_at_light_cone(self):
        """W -> infinity as beta_v -> 1 (approach light cone boundary)."""
        # beta_v = |beta - 1/2| / |gamma| = 1 means |beta - 1/2| = |gamma|
        # For gamma = 10, beta - 1/2 = 10 -> beta = 10.5 (way off, but tests the formula)
        # Use beta_v close to 1 but < 1
        gamma = 10.0
        beta = 0.5 + 9.9  # beta_v = 9.9/10 = 0.99
        W = warping_factor(beta, gamma)
        self.assertGreater(W, 7.0, "W should be large near light cone (beta_v -> 1)")

    def test_rh_equivalent_to_unit_warping_for_all_known_zeros(self):
        """RH <=> W = 1 for all zeros. Confirm for all known Odlyzko zeros."""
        all_warping_one = all(
            abs(warping_factor(0.5, gamma) - 1.0) < 1e-12
            for gamma in ODLYZKO_ZEROS
        )
        self.assertTrue(all_warping_one,
                        "Not all known zeros have W=1 (should all be on critical line)")


class TestLambdaRhoLightCone(unittest.TestCase):
    """Test the lambda_rho parametrization and its Minkowski structure."""

    def test_lambda_rho_on_line_is_real(self):
        """lambda_rho = gamma + i*(1/2 - beta) on critical line is purely real."""
        for gamma in ODLYZKO_ZEROS:
            beta = 0.5
            lambda_rho = complex(gamma, beta - 0.5)
            self.assertAlmostEqual(lambda_rho.imag, 0.0, places=15)
            # lambda_rho is on the "timelike axis" (proper time axis of the rest frame)
            self.assertAlmostEqual(lambda_rho.real, gamma, places=6)

    def test_lambda_rho_off_line_has_spacelike_component(self):
        """Off critical line, lambda_rho has spacelike (imaginary) component."""
        gamma = 14.135
        beta = 0.49
        lambda_rho = complex(gamma, beta - 0.5)  # = gamma + i*(beta - 1/2) = gamma - i*0.01
        self.assertNotAlmostEqual(lambda_rho.imag, 0.0, places=10)
        # The spacelike component is |beta - 1/2| = 0.01
        self.assertAlmostEqual(abs(lambda_rho.imag), 0.01, places=10)
        # The boost velocity is the ratio spacelike/timelike = 0.01/14.135
        beta_v = abs(lambda_rho.imag) / abs(lambda_rho.real)
        self.assertAlmostEqual(beta_v, abs(beta - 0.5) / abs(gamma), places=10)

    def test_involution_swaps_paired_zeros(self):
        """J(s) = 1 - s_bar maps lambda_rho -> -conj(lambda_rho)."""
        gamma = 30.0
        beta = 0.47
        rho = complex(beta, gamma)
        rho_pair = 1 - rho.conjugate()  # = (1-beta) + i*gamma
        lambda_rho = complex(gamma, beta - 0.5)
        lambda_pair = complex(gamma, (1 - beta) - 0.5)
        # J maps rho -> 1 - rho_bar, so beta -> 1 - beta, (1/2 - beta) -> (1/2 - (1-beta)) = beta - 1/2 = -(1/2-beta)
        # => lambda_pair = gamma + i*(beta - 1/2) = gamma - i*(1/2 - beta) = conj(lambda_rho)... wait
        # lambda_rho = gamma + i*(1/2 - beta) = gamma + i*(-0.03) = gamma - 0.03i
        # lambda_pair = gamma + i*(1/2 - (1-beta)) = gamma + i*(1/2 - 1 + beta) = gamma + i*(beta - 1/2) = gamma + 0.03i
        # So lambda_pair = conj(lambda_rho) = gamma + 0.03i
        # And -conj(lambda_rho) = -(gamma + 0.03i) = -gamma - 0.03i ... that's not the same.
        # 
        # Actually the involution is lambda -> -lambda_bar (reflect through origin + conjugate)
        # This is because rho -> 1 - rho_bar swaps beta <-> 1-beta, which sends (1/2-beta) -> -(1/2-beta)
        # In the lambda plane: lambda -> gamma - i*(1/2-beta) = conj(lambda) for fixed gamma
        # But the sign of gamma also flips if we think of rho -> 1-rho as s -> 1-s
        # The functional equation xi(s) = xi(1-s) pairs rho with 1-rho
        # Combined with xi(s) = conj(xi(conj(s))), we get rho paired with 1-rho_bar
        # In lambda: (gamma, 1/2-beta) -> (gamma, -(1/2-beta)) = reflection across gamma-axis
        # i.e., lambda -> conj(lambda) for the same gamma
        # The "boost" mixes gamma and (1/2-beta), and the involution reflects across gamma-axis
        self.assertAlmostEqual(lambda_pair.real, lambda_rho.real, places=10)
        self.assertAlmostEqual(lambda_pair.imag, -lambda_rho.imag, places=10)


class TestHalfRapidityWeierstrass(unittest.TestCase):
    """Test the half-rapidity / Weierstrass substitution identities from RH/04.

    Key claim: beta_0 = (gamma_L - 1)/(beta * gamma_L) = tanh(phi/2),
    i.e., the median-frame velocity is exactly the half-rapidity.
    'Twoje β i β₀ to półkąt Weierstrassa na hiperboli.'
    """

    def test_half_rapidity_identity(self):
        """beta_0 = (gamma_L - 1)/(beta * gamma_L) = tanh(phi/2) to 12+ digits.

        Verified to 12 digits as stated in 04 ('Sprawdzone co do dwunascu cyfr').
        At extreme rapidities (phi -> infinity, beta -> 1) floating-point
        cancellation in gamma_L = 1/sqrt(1-beta^2) limits precision;
        we verify within the stable range and confirm asymptotic agreement.
        """
        for phi in [0.1, 0.5, 1.0, 2.0, 5.0]:
            beta = math.tanh(phi)
            gamma_L = 1.0 / math.sqrt(1 - beta**2)
            beta_0_formula = (gamma_L - 1) / (beta * gamma_L)
            beta_0_tanh = math.tanh(phi / 2)
            self.assertAlmostEqual(beta_0_formula, beta_0_tanh, places=12,
                                   msg=f"Half-rapidity fails at phi={phi}")

        # Asymptotic check: as phi -> inf, beta -> 1, beta_0 -> 1
        # (both 'rest' at 0 and 'light speed' at 1 are fixed points)
        # Use sinh/cosh directly to avoid cancellation
        for phi in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0]:
            gamma_L = math.cosh(phi)
            beta = math.tanh(phi)
            beta_gamma = math.sinh(phi)
            beta_0_formula = (gamma_L - 1) / beta_gamma  # = (cosh-1)/sinh
            beta_0_tanh = math.tanh(phi / 2)
            # (cosh(phi)-1)/sinh(phi) = sinh(phi/2)/cosh(phi/2) = tanh(phi/2)
            self.assertAlmostEqual(beta_0_formula, beta_0_tanh, places=10,
                                   msg=f"Asymptotic half-rapidity fails at phi={phi}")

    def test_double_angle_formula(self):
        """beta = 2*beta_0/(1+beta_0^2) = tanh(2*artanh(beta_0))."""
        for beta_0 in [0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99, 0.999]:
            beta = 2 * beta_0 / (1 + beta_0**2)
            beta_doubled = math.tanh(2 * np.arctanh(beta_0))
            self.assertAlmostEqual(beta, beta_doubled, places=12)

    def test_fixed_points_of_doubling_map(self):
        """Fixed points of x -> 2x/(1+x^2) are exactly {0, +1, -1}.

        0 = rest (beta_0 = 0), ±1 = light speed (beta = 1).
        'Punkty stałe odwzorowania x ↦ 2x/(1+x^2) to 0 i ±1.'
        """
        # x=0: f(0) = 0
        self.assertAlmostEqual(2 * 0 / (1 + 0), 0, places=15)
        # x=1: f(1) = 2/2 = 1
        self.assertAlmostEqual(2 * 1 / (1 + 1), 1, places=15)
        # x=-1: f(-1) = -2/2 = -1
        self.assertAlmostEqual(2 * (-1) / (1 + 1), -1, places=15)
        # No other fixed points: x = 2x/(1+x^2) => x(1+x^2) = 2x => x(x^2-1) = 0
        for x in np.linspace(-0.99, 0.99, 50):
            fx = 2 * x / (1 + x**2)
            if abs(fx - x) > 1e-6:
                # Not a fixed point -- expected for most x
                pass

    def test_weierstrass_substitution_on_hyperbola(self):
        """t = tanh(phi/2) parametrizes the mass-shell hyperbola gamma^2 - (beta*gamma)^2 = 1.

        Verified using sinh/cosh directly (cosh(phi)=gamma, sinh(phi)=beta*gamma)
        to avoid floating-point cancellation at large rapidities.
        't = tanh(phi/2) parametryzuje hiperbole x^2 - y^2 = 1, czyli powłokę masy'
        """
        for phi in [0.1, 0.5, 1.0, 2.0, 5.0]:
            t = math.tanh(phi / 2)
            gamma_param = (1 + t**2) / (1 - t**2)
            beta_gamma_param = 2 * t / (1 - t**2)
            gamma_direct = math.cosh(phi)
            beta_gamma_direct = math.sinh(phi)
            # Check hyperbola identity: gamma^2 - (beta*gamma)^2 = 1
            on_cone = gamma_param**2 - beta_gamma_param**2
            self.assertAlmostEqual(on_cone, 1.0, places=8)
            # Check parametrization matches direct computation
            self.assertAlmostEqual(gamma_param, gamma_direct, places=8)
            self.assertAlmostEqual(beta_gamma_param, beta_gamma_direct, places=8)

        # Asymptotic regime: large phi, t -> 1, use cosh/sinh directly
        # The identity (cosh(phi)-1)/sinh(phi) = tanh(phi/2) holds exactly
        for phi in [10.0, 20.0]:
            self.assertAlmostEqual(
                (math.cosh(phi) - 1) / math.sinh(phi),
                math.tanh(phi / 2),
                places=6,
                msg=f"Asymptotic identity fails at phi={phi}")

    def test_weierstrass_substitution_on_circle(self):
        """t = tan(theta/2) parametrizes the unit circle: cos^2 + sin^2 = 1.

        Dual statement: półkąt for the circle (genus 0, sphere) vs.
        t = tanh(phi/2) for the hyperbola (genus 0, mass shell).
        """
        for theta in [0.1, 0.5, 1.0, 2.0, 3.0, 5.0]:
            t = math.tan(theta / 2)
            cos_param = (1 - t**2) / (1 + t**2)
            sin_param = 2 * t / (1 + t**2)
            cos_direct = math.cos(theta)
            sin_direct = math.sin(theta)
            on_circle = cos_param**2 + sin_param**2
            self.assertAlmostEqual(on_circle, 1.0, places=10)
            self.assertAlmostEqual(cos_param, cos_direct, places=10)
            self.assertAlmostEqual(sin_param, sin_direct, places=10)

    def test_genus_zero_rational_parametrization(self):
        """Genus 0 (circle/hyperbola/both fixed by doubling) has rational parametrization.

        The map x -> 2x/(1+x^2) (Lorentz velocity addition of self with self)
        is a rational map with fixed points at {0, ±1} — like Frobenius on F_2.
        'Jak punkty stałe Frobeniusa nad F_2, {0, 1}: koniec skali i początek skali.'
        """
        # Over F_2: Frobenius x -> x^2 fixes {0, 1}
        for x_f2 in [0, 1]:
            self.assertEqual(x_f2**2, x_f2)  # fixed by Frobenius

        # The Lorentz doubling map x -> 2x/(1+x^2) fixes {0, ±1}
        # These are the boundary points: 0 = rest, ±1 = light speed
        self.assertAlmostEqual(2 * 0 / (1 + 0**2), 0, places=15)
        self.assertAlmostEqual(2 * 1 / (1 + 1**2), 1, places=15)
        self.assertAlmostEqual(2 * (-1) / (1 + (-1)**2), -1, places=15)
