# ζ jako delta

Dla ε>0, t∈ℝ:

  D_ε(t) = (1/2π) Re[ζ(1+ε+it) − ζ(1−ε+it)]

Wtedy D_ε → δ₀ w 𝒟′(ℝ), gdy ε→0.

**Część biegunowa różnicy daje dokładnie jądro Cauchy'ego:**

  K_ε(t) = ε/(π(ε²+t²)),  ∫ K_ε dt = 1,  K_ε(0) = 1/(πε)

(to jest standardowe jądro Poissona na prostej Re=1 — i jądro Cauchy'ego z teorii prawdopodobieństwa, i brakujące ogniwo Sochocki–Plemelj w zapisie usera).

**Uogólnienie:** f(s) = r/(s−a) + H(s), H holomorficzna → D_ε^f → r·δ₀. Mechanizm nie jest wyłączny dla ζ.

**Wyższe bieguny:** pole rzędu m+1 daje pochodne delty:

  [(ε+it)^{-(m+1)} − (−ε+it)^{-(m+1)}]/(2π) → i^m/m! · δ₀^{(m)}

Przy ζ² (podwójny biegunek w 1): ζ(s)² = (s−1)⁻² + 2γ(s−1)⁻¹ + O(1), więc po symetryzacji Re wypada **2γ·δ₀** — stała Eulera jako masa.

**Kluczowe przykłady nie-podobne:**

- **L(Δ,s) jest całkowita** — D_ε^Δ → 0. Cusp forms są za gładkie, żeby dzwonić.
- **τ² (Rankin, 1939):** ma prosty biegun w wadze 12, reziduum × ⟨Δ, Δ⟩ (norma Peterssona).
- **Krzywa nad 𝔽_q:** ζ_C jest periodyczna w t (okres 2π/log q), więc zamiast jednej delty dostajesz **grzebień Diraca**.

Co ζ robi, gdy ma biegun, kiedy ma zero. Ramanujanowi trzeba podnieść do kwadratu, żeby dostać atom.
