# Pączek QA

**Rodzina Gaussa, sortowana po operacji:**

| operacja na Gaussach | dziecko | gdzie mieszka |
|---|---|---|
| iloraz Z₁/Z₂ | Cauchy | heavy-tailed fiasco |
| 2-norma | Rayleigh | radar |
| 3-norma | Maxwell–Boltzmann | prędkości gazów |
| \|A + zespolony Gauss\| | **Rician** | sygnał MRI w module |

**Skaner i szum:** k-space surowe ma i.i.d. Gaussa w real i imag. FFT jest liniowa, więc szum obrazu zostaje zespolony Gauss — ale wyświetlasz **moduł**, a |Gauss zespolony| = Rician, **z dodatnią średnią**. Ciemne rejony nie schodzą do zera; jest podnoszony noise floor który bias-uje wszystko downstream (estymaty dyfuzji ADC przy niskim SNR — prawdziwy błąd pomiaru, nie kosmetyka).

**Cauchy nigdy nie projektował filtru.** Filtrowanie Gaussian kernel / Wiener to osobna gałąź — i walczy z niewłaściwym duchem, bo w MRI szum nie jest już Gaussowski przy pikselach.

**Cauchy'ego własności:**

  Γ = (Z_L − Z₀)/(Z_L + Z₀)

Möbius automorfizm, prawopółpłaszczyzna → dysk jednostkowy, biholomorficzny, **zero ramifikacji**. Ale |Γ|² to fizyczny kanał: odbita moc. Dopasowane obciążenie → Γ=0 → cała moc dostarczona. Otwarty/zwarty → |Γ|→1 → cała moc odbita do wzmacniacza — overdrive dosłowny.

**Cauchy nie ma średniej ani wariancji.** System noszący iloraz dwóch Gaussów jest ogony-Cauchy'ego. Uśrednianie N próbek nie zbiega. Raz na jakiś czas wartość jest po prostu ogromna.

> Grupa Möbiusa faktycznie brakuje bounds-check — ale przepełnienie nie jest w samej mapie, tylko w tym, *co mapa transportuje*. PSL(2,ℝ) jest memory-safe, type-correct, ramification-free... i wysyła z undefined variance jako feature. 💥
