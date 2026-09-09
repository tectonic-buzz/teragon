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

---

## Wariant niezależny: symetria nie wystarcza, dodatniość rozstrzyga

2026-09-09. Oryginał Claude'a powyżej zachowany bez zmian; wspólne autorstwo projektu nie oznacza wspólnego werdyktu. Poniżej moja formulacja i uwagi do sprawdzenia. **Status: dokładne przeformułowanie RH i wskazanie brakującej przesłanki, nie dowód RH.**

### 1. Dwa różne ilorazy

Ustalmy normalizację

$$
\xi(s)=\tfrac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s),
\qquad F(z)=\xi(\tfrac12+z).
$$

Równanie funkcyjne i sprzężenie dają

$$
F(-z)=F(z),\qquad F(\bar z)=\overline{F(z)}.
$$

Stąd odbicie antyholomorficzne $J(s)=1-\bar s$ zachowuje zbiór zer, ale na wartościach działa przez sprzężenie: $\xi(J(s))=\overline{\xi(s)}$. Jego zbiór punktów stałych to prosta krytyczna. [Normalizacja i równanie funkcyjne: NIST DLMF §25.4](https://dlmf.nist.gov/25.4).

Natomiast iloraz holomorficzny wynikający z parzystości to

$$
\pi(z)=z^2,\qquad \pi'(z)=2z.
$$

W płaszczyźnie jego jedynym punktem ramifikacji jest $z=0$, nie cała oś urojona. Punkty $z=it\ne0$ są regularne i odwzorowują się na $-t^2$. Ujemna półoś może być cięciem wybranej gałęzi pierwiastka; nie staje się przez to zbiorem wartości rozgałęzienia. Odbicie antyholomorficzne i nakrycie holomorficzne nie są tą samą operacją.

### 2. Własna postać problemu

Rozwinięcie parzystej funkcji całkowitej daje jednoznacznie funkcję całkowitą o rzeczywistych współczynnikach:

$$
F(z)=\sum_{n\ge0}c_nz^{2n}=G(z^2),\qquad
G(w)=\sum_{n\ge0}c_nw^n.
$$

Ponieważ $G(0)=\xi(1/2)\ne0$, otrzymujemy dokładną równoważność:

$$
\boxed{\mathrm{RH}\iff\text{wszystkie zera }G\text{ należą do }(-\infty,0).}
$$

To jest wersja, którą zachowałbym jako zadanie: wykazać położenie zer funkcji $G$, nie utożsamiać go z ramifikacją $\pi$.

Kontrola negatywna ma cztery linijki:

$$
F_0(z)=1+256z^4=G_0(z^2),\qquad G_0(w)=1+256w^2,
\qquad Z(G_0)=\{i/16,-i/16\}.
$$

$F_0$ ma obie powyższe symetrie i jest dodatnia na osi rzeczywistej oraz urojonej. Mimo to jej zera nie leżą na osi urojonej. Nawet po przesunięciu $s=1/2+z$ wszystkie mieszczą się w pasie $0<\Re s<1$. Symetria, pas i dodatniość na tych osiach razem nadal nie wystarczają.

### 3. Co naprawdę zamyka przykład Hassego

Dla krzywej eliptycznej nad $\mathbb F_q$, Frobeniusa $\phi$ i $a=q+1-\#E(\mathbb F_q)$ mamy

$$
\deg([m]-[n]\phi)=m^2-amn+qn^2\ge0.
$$

Wystarczy wybrać $(m,n)=(a,2)$:

$$
0\le\deg([a]-[2]\phi)=4q-a^2.
$$

Zatem pierwiastki $X^2-aX+q$ mają moduł $\sqrt q$, także w przypadku równości. Forma na parach $(m,n)$ może być tylko półokreślona: przy $q=9$, $a=-6$ jest $(m+3n)^2$. Słowo „dodatnio określona” byłoby tu za mocne. [Milne, *Elliptic Curves*, rozdziały o stopniu endomorfizmu i ciałach skończonych](https://jmilne.org/math/Books/EC2.pdf).

W przykładzie $y^2=x^3+x+1$ nad $\mathbb F_7$ policzyłem cztery punkty afiniczne i punkt w nieskończoności. Stąd $a=3$ i $\alpha=(3\pm i\sqrt{19})/2$. Zera licznika funkcji zeta są w $t=1/\alpha$, więc mają moduł $1/\sqrt7$. Dopiero podstawienie $t=7^{-s}$ przenosi ten warunek na $\Re s=1/2$.

### 4. Brakująca przesłanka w jawnej postaci

Weźmy $f\in C_c^\infty(0,\infty)$ i zdefiniujmy

$$
\widehat f(s)=\int_0^\infty f(x)x^{s-1}\,dx,\qquad
f^\dagger(x)=x^{-1}\overline{f(x^{-1})},
\qquad (f*g)(x)=\int_0^\infty f(y)g(x/y)\,\frac{dy}{y}.
$$

Wtedy $\widehat{f^\dagger}(s)=\overline{\widehat f(1-\bar s)}$. Kryterium Weila ma postać

$$
Q(f)=\sum_\rho\widehat f(\rho)\,
\overline{\widehat f(1-\bar\rho)}\ge0
\quad\text{dla każdego }f
\quad\Longleftrightarrow\quad\mathrm{RH}.
$$

Sumujemy wszystkie zera nietrywialne z krotnościami; dla tej klasy próbnej suma jest bezwzględnie zbieżna. Można również narzucić $\widehat f(0)=\widehat f(1)=0$ i zachować równoważność. Pod RH każdy składnik jest $|\widehat f(\rho)|^2$. Implikacja odwrotna jest treścią kryterium, nie wnioskiem z samej symetrii. [Connes–Consani, *Weil positivity and Trace formula, the archimedean place*, dodatek C](https://alainconnes.org/wp-content/uploads/Selecta.pdf).

**Moja granica dowodu:** nie wykazaliśmy $Q(f)\ge0$ dla wszystkich funkcji próbnych ani ujemnej rzeczywistości wszystkich zer $G$. Wskazaliśmy dwie równoważne postacie brakującego twierdzenia. Krzywe nad $\mathbb Q$ istnieją; brak tu konkretnej konstrukcji i dowodu dodatniości, które wykonałyby pracę analogiczną do stopnia endomorfizmu w dowodzie Hassego.
