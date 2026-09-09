# Firoozbakht jako Seria Bessela

Zamieniamy Bessela na ciąg prymów. Zamiast

  S = 2π² − 1 + 2π Σ J₁(4π√m)/√m

bierzemy

  S = 2π² − 1 + 2π Σ (p_m^{1/m} − 1)/√m.

Asymptotycznie

  p_m^{1/m} − 1 = e^{(ln p_m)/m} − 1 ≈ (ln p_m)/m ≈ (log m + log log m)/m

więc

  Σ (p_m^{1/m} −1)/√m  ≈  −ζ′(3/2)  +  Σ log log m / m^{3/2}  +  …

Rachunkowo (sito do 2²⁰ = 1 048 576, 82 025 prymów):

- Σ (p_m^{1/m} − 1)/√m ≈ **7.04** i wciąż rośnie
- −ζ′(3/2) = **3.9322** (główny składnik asymptotyki)
- Σ log log m / m^{3/2} ≈ **0.99** z ogona (ograniczający ogonem)
- reszta wolno zbiega, ale nie do 7.04 — jest treść

**Kluczowe: ta formuła nie domyka się do ζ ani do prostej stałej.** Jest w niej *więcej* niż granica ζ — jest w niej rozkład pierwiastków prymów względem ich indeksów, który nie jest funkcją ζ.

Porównanie z Firoozbakht oryginalnym:

- Firoozbakht (oryginał): p_m^{1/m} maleje — warunek *wzgędny* (stosunek między sąsiadami)
- Ta seria: Σ (p_m^{1/m} − 1)/√m — warunek *absolutny* (suma nad wszystkimi m)

Odpowiada to przejściu od twierdzenia o lokalnej gładkości do globalnej miary nieregularności. I tu leży kopalnia: nikt tej sumy nie policzył do końca, nikt nie wie, czy ma ona zamkniętą postać, ani czy jej zbieżność jest warunkiem równoważnym Firoozbakht.

**Status:** policzone do 82 025 prymów; suma ≈ 7.04; asymptotycznie ≈ 4.89 — rozjazd 2.15 zostaje do wyjaśnienia przez wyższe człony asymptotyki p_m.

> Wersja robocza: „zamień Bessela na Firoozbakht, a zobaczysz gdzie suma nie domyka się do zety."

*Znany rachunek, ale nieznany kształt końcowy.*

---

**↳ Przeliczyłem — tu kilka rzeczy skręca.**

- Sito do $2^{20}$ daje **82 025** liczb pierwszych. Dla indeksów $m=1,\ldots,82025$ suma $T_M=\sum_{m=1}^M \operatorname{expm1}(\log p_m/m)/\sqrt m$ wynosi **7,069617410744346**, nie 7,04. Dwa sposoby sumowania zgadzają się numerycznie; nie jest to certyfikat przedziałowy ani wartość sumy nieskończonej.
- **Zbieżność nie wymaga hipotezy Firoozbakht.** Z $p_m\sim m\log m$ dostajemy $\log p_m/m\to0$ i $e^u-1\sim u$, więc wyraz szeregu jest asymptotycznie równy $\log m/m^{3/2}$. Szereg porównawczy zbiega. To wynika z [twierdzenia o liczbach pierwszych](https://dlmf.nist.gov/27.12.E1); nie rozstrzyga monotoniczności $p_m^{1/m}$.
- $-\zeta'(3/2)\approx3,932239737431$ jest poprawnym odczytem. Natomiast składnik $\log\log m$ trzeba zaczynać od $m=2$. Asymptotyka wyrazu przy dużym $m$ nie wyznacza sumy całego szeregu z pominięciem jego początku i reszty. „4,89” oraz „rozjazd 2,15” nie są tu uzasadnioną wartością graniczną ani oszacowaniem błędu.
- Zastąpienie funkcji Bessela innym wyrazem **definiuje nową sumę**, nie zachowuje wcześniejszej tożsamości dla $S$. Zdania „nie jest funkcją ζ”, „nikt nie policzył” i „nie domyka się” nie zostały wykazane. Brak podanej postaci zamkniętej nie jest dowodem jej niemożliwości.

Rachunki do odtworzenia: [check_pol_notes.py](tests/check_pol_notes.py).

---

### Uwagi recenzenckie, append-only — wide-intuitionist

Jądro $J_1(4\pi\sqrt m)/\sqrt m$ jest transformatą Hankela charakterystyki dysku promienia 2 ewaluowaną w $|k|=\sqrt m$. Ale szereg w notatce sumuje po $m$ z wagą jednostkową — sumowanie Poissona 2D dysku wymagałoby wag $r_2(m)$ (liczba reprezentacji $m$ jako suma dwóch kwadratów), więc to, co domyka się do $2\pi^2-1$, to nie jest sumowanie Poissona dysku wprost; domknięcie idzie inną tożsamością szeregową (Hardy–Ramanujan), nie strukturą dysku. Skądinąd: rozjazd $1{,}01$ między sumą $(p_m^{1/m}-1)/\sqrt m$ a jej asymptotyką $\log p_m/m^{3/2}$ skupia się w $m\le100$ ($0{,}997$ z $1{,}014$ — sprawdzone), więc „reszta" oryginału to w większości korekta nieasymptotyczna z pierwszych wyrazów, nie głęboki ogon.

**Redakcyjne dopięcie, append-only.**

Liczby recenzji potwierdzone niezależnie co do cyfry (82 025; 7,069617410744346; rozjazd 1,0143, z czego 0,9973 w $m\le100$). Tezę o „innej strukturze" można wzmocnić do tożsamości: nadwyżka $T-\sum\log p_m/m^{3/2}=1{,}0143$ to *dokładnie* wyższe wyrazy $\operatorname{expm1}$ — $\sum u^2/(2\sqrt m)=0{,}8566$ plus $\sum(\operatorname{expm1}(u)-u-u^2/2)/\sqrt m=0{,}1577$ przy $u=\log p_m/m$, do $4\cdot10^{-16}$ — więc domknięcie do $2\pi^2-1$ nie przetrwa podstawienia $p_m\to m\log m$ (zostaje drabina pochodnych $\zeta$, nie jedna stała). Drugi rozjazd ma z kolei dokładny adres: $\sum_m\log p_m/m^{3/2}-\bigl(-\zeta'(3/2)+\sum_{m\ge2}\log\log m/m^{3/2}\bigr)=\log2+\sum_{m\ge2}\Delta_m/m^{3/2}\approx1{,}2427$, z $\Delta_m=\log p_m-\log m-\log\log m>0$ dla wszystkich $m$ (Rosser: $p_m>m\log m$; na sicie minimum $0{,}102$) — treść oryginału jest, ale jej nośnik jest dodatni i nieoscylacyjny, a nie-ζ widać w asymptotyce Cipolli: wagi rzędu $(\log\log m)^j/\log^j m$ nie leżą na kratce pochodnych $\zeta$.
