# Ramifik(s)acja Funkcji Zeta Riemanna

W jednym uderzeniu, i najpierw słowo „ramifikacja" ustawione tak, żeby uderzenie było w cel.

**Definicja.** Równanie funkcyjne to inwolucja J(s) = 1 − s̄, odbicie płaszczyzny względem prostej Re s = ½; ξ jest J-symetryczna, więc jej zera układają się w J-orbity. Zero *ramifikowane* to zero będące punktem stałym J — leży na prostej. Zero *rozłożone* to para {ρ, 1−ρ̄} dwóch różnych zer po obu stronach. **RH to zdanie: każde zero jest ramifikowane; żadne się nie rozkłada.** Dokładnie jak (x−5)³ mod 7 kontra trzy osobne pierwiastki — ten sam słownik, tydzień temu.

**Twierdzenie (placek).** Dla krzywej eliptycznej E nad F_q każda wartość własna Frobeniusa jest ramifikowana względem inwolucji α ↦ q/ᾱ, tzn. |α| = √q; zera Z(E,t) leżą na Re s = ½.

**Dowód, jedno uderzenie.** Stopień endomorfizmu jest formą kwadratową dodatnio określoną na End(E): dla m, n ∈ ℤ,
 deg(m − nφ) = m² − a·mn + q·n² ≥ 0,
gdzie φ = Frobenius, a = trace(φ), deg(1−φ) = #E(F_q). Forma dodatnio określona ma wyróżnik ujemny: a² − 4q ≤ 0. Więc T² − aT + q ma pierwiastki sprzężone zespolone o iloczynie q: αᾱ = q, czyli ᾱ = q/α — α jest punktem stałym inwolucji, ramifikowane. ∎

Cały dowód to jedno zdanie: **dodatniość formy stopnia zmusza wartości własne na okrąg stały inwolucji.** Dla y² = x³+x+1 nad F₇: a = 3, wyróżnik −19, α = 1,5 + 2,18i, αᾱ = 7 — policzone. To Hasse 1933 (Weil dla dowolnego rodzaju, Deligne dla wszystkiego); placek ma RH jako twierdzenie, bo ma *geometrię*, która czyni formę dodatnią.

**Nad ℚ — uczciwa część uderzenia.** ξ(½ + z) jest funkcją parzystą z (sprawdzone: ξ(½+z) = ξ(½−z) co do 10⁻¹²) i rzeczywistą na osi urojonej (w pierwszym zerze: 1,96·10⁻¹⁰ + 0i). Czyli ξ *schodzi* przez rozgałęzione nakrycie z ↦ z², ramifikowane w s = ½, do funkcji całkowitej G((s−½)²). Prosta krytyczna to **locus rozgałęzienia** tego nakrycia — ramifikacja zety w sensie dosłownym, i to jest dowiedzione: fałd, zgięcie, parzystość. Ale to mówi, *gdzie jest zgięcie*, nie że *zera na nim leżą*. Krok, którego brakuje, ma ten sam kształt co u placka: **Weil 1952 — RH ⟺ dodatniość pewnej formy kwadratowej** (funkcjonału Weila ze wzoru jawnego, na przestrzeni funkcji próbnych). Dokładnie ta sama logika: forma dodatnia ⇒ wartości własne na okręgu stałym. Różnica jest jedna i cała: **placek ma krzywą, której stopniem jest ta forma — ℚ nie ma krzywej.** Nikt nie widzi geometrii, która zrobiłaby z funkcjonału Weila stopień czegoś. Program Connesa to próba zbudowania tej geometrii (przestrzeń klas adeli); Deninger to próba zbudowania jej jako dynamiki. To jest to samo, co ci powiedziałem wczoraj — „kula nad ℚ jeszcze nie" — tylko teraz z podaną *dokładną brakującą przesłanką*: dodatniość.

Więc jedno uderzenie brzmi tak: **ramifikacja = bycie stałym pod inwolucją; na placku dodatniość stopnia to wymusza w jednej linijce; nad ℚ ta sama linijka nazywa się kryterium Weila i jest równoważna RH — i to, czego brakuje, to nie dowód, tylko placek.** 🥞🗡️🦧
