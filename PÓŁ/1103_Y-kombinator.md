# Y-kombinator

Czy ζ można używać jak Y-kombinatora — złożyć iterację w jeden obiekt bez pętli?

Tak, i to cała branża. Zeta jest **transformatą Mellina jądra iteracji** — Y-kombinator buduje się przez zintegrowanie półgrupy cieplnej raz.

### 1. Iterowana całka, rozwinięta

Cauchy: n-krotna całka spleciona to jedno jądro:

  ∫∫…∫ f = 1/(n−1)! ∫ (x−t)^{n−1} f(t) dt

I ruch ζ-type: Γ przyjmuje argumenty zespolone, więc *liczba iteracji staje się parametrem zespolonym* — Riemann–Liouville J^α f = 1/Γ(α) ∫ (x−t)^{α−1} f dt. Pętla stała się analityczna.

### 2. Resolwenta: zeta, którą jest samo-aplikacja

  (λI − A)^{-1} = Σ λ^{−k−1} A^k

a potem wydobyć dowolną potęgę przez kontur zamiast pętlę:

  e^{tA} = (1/2πi) ∮ e^{λt} (λ−A)^{-1} dλ

Dunford–Riesz functional calculus. Szereg Taylora z jego "stop gdy wyraz < ε" zastąpiony konturem. **Kontur jest pętlą.**

### 3. Suma widma bez liczenia wartości własnych

ζ_O(s) = Σ λ_n^{−s} = (1/2πi) ∮ λ^{−s} (d/dλ) log u_λ(1) dλ

— bieguny pochodnej logarytmicznej są wartościami własnymi. Kirsten–Loya determinują det funckjonalne "bez użycia choćby jednego eigenvalue explicite".

### 4. Pętla po eigenvalues → jedna pochodna w zerze

det A = e^{−ζ′_A(0)}, z ζ_A(s) = 1/Γ(s) ∫ t^{s−1} Tr e^{−tA} dt. Na torusie ℂ/(ℤ+τℤ), det Δ_τ = τ₂² |η(τ)|⁴ — η^6 = Δ Ramanujana.

> Czasem pętla i całka są *dowodliwie tym samym obiektem z dwóch stron* — to każda formuła śladowa. Selberg: pętla-sumowanie po geodezyjnych zamkniętych = widmowa całka Laplasjanu. Poisson summation to sygnatura typu.
