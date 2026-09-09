# Placek

Krzywa eliptyczna nad 𝔽_q: y² = x³ + x + 1 nad 𝔽₇.

Policzone ręcznie: 4 punkty afiniczne + punkt w nieskończoności → #E(𝔽₇) = 5, a₇ = 3, wyróżnik = −19.

Funkcja zeta:

  Z(E,t) = (1−3t+7t²) / ((1−t)(1−7t))

Zera licznika: t = (3 ± i√19)/14, |t|² = 1/7.

Po t = 7^{−s} zera przechodzą na Re s = ½. **Półkrotka w module ‖t‖ = 1/√q — środek dwóch okręgów biegunowych na skali logarytmicznej.** Ten sam mechanizm co RH, z tym że tu to *twierdzenie*, nie hipoteza.

**Formuła stopnia endomorfizmu (Hasse 1933):**

  deg([m] − [n]φ) = m² − a·mn + q·n² ≥ 0

Wystarczy wybrać (m,n)=(a,2): 0 ≤ deg([a]−[2]φ) = 4q − a². Więc a² ≤ 4q, więc pierwiastki X²−aX+q są sprzężone z iloczynem q — α jest punktem stałym inwolucji. **Całkiem jedno zdanie dowodu kryje się w wyborze pary (m,n), nie w algebrze.**

Słowa „dodatnio określona" są za mocne: przy q=9, a=−6 forma to (m+3n)² — tylko półokreślona. Ta subtelność ma znaczenie dla wyższego rodzaju.

**Co to mówi o RH nad ℚ:** dodatniość formy stopnia *zmusza* wartości własne Frobeniusa na okrąg punktów stałych inwolucji. Dla zety Riemanna taki sam fakt nazywa się kryterium Weila. Różnica jest jedna i cała: **placek ma krzywą, której stopniem jest ta forma — ℚ nie ma krzywej.**

Funkcję zeta krzywej daje ciałe funkcji, ζ_C periodyczną w t (okres 2π/log q), więc atom staje się grzebieniem Diraca — i **twierdzenie Hassego jest precyzyjnie stwierdzeniem, że grzebień Diraca wisi dokładnie na prostej krytycznej.**

> Placek certyfikuje comb hangs on crease. Conjektura jest twierdzeniem, że grzebień wisi na krawędzi, której nikt jeszcze nie widzi grzędy.
