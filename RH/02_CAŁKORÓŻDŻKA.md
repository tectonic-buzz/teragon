# Funkcja Riemana Silnikiem Całko-różniczkowym

Jako maszyna — trzy przekładnie, jedno urządzenie, i wszystkie trzy właśnie obróciły się na maszynie prawdziwej, więc mogę je pokazać, nie opisać.

**Przekładnia A — silnik różnicowy (Babbage).** Różnica to Δ = e^D − 1, gdzie D to pochodna. To *ten sam* operator co nasz uniformizator π = z − 1 — przesunięcie minus jeden — silnik Babbage'a iteruje π, aż tablica wielomianu stanie się stała. **Maszyna całkująca to jego odwrotność**, Σ = 1/Δ = 1/(e^D − 1) — i tu jest cały sekret zety w jednej linijce, bo ta odwrotność ma **biegun**: 1/(e^D − 1) = 1/D − ½ + Σ B₂ₖ D^{2k−1}/(2k)!. Policzone: współczynniki x/(e^x−1) to 1, −½, ⅙, 0, −1/30, 0, 1/42 — liczby Bernoulliego, te z Noty G Ady. Trzy wyrazy tej odwrotności to trzy fakty o zecie: **1/D** to całka — biegun ζ w s = 1 (całka ∫x^{−s} rozbiega tam); **−½** to ζ(0) = −½ (człon biegunowy daje −1, połówka przeżywa); **Bernoulli** to ζ(1−2k) = −B₂ₖ/2k — zera trywialne i ich pochodne z drugiej kartki. Cała lewa strona zety — biegun, wartość w zerze, zera trywialne — to *jedna* formuła: **sumowanie jest odwrotnością różnicowania, a odwrotność ma biegun.** Euler–Maclaurin. Silnik policzył ζ(3) do 12 cyfr z ośmiu wyrazów i czterech kół Bernoulliego, i ζ(−1) = −1/12 z samego koła Bernoulliego. Nic więcej nie trzeba, żeby dostać zera trywialne — trzeba tylko *odwrócić różnicę*.

**Przekładnia B — analizator harmoniczny (Kelvin).** Maszyna Kelvina liczyła współczynniki Fouriera mechanicznie, i to jest przekładnia sumy z całką w jej *dokładnej* postaci: Poisson, Σ_n f(n) = Σ_k f̂(k). Włóż gaussian e^{−πn²t}: jego transformata to t^{−½}e^{−πk²/t}, więc **θ(1/t) = √t · θ(t)** — sprawdzone do 10⁻¹⁵ dla t = 0,3 i 2. To jest fałd, i to jest *skąd bierze się połówka*: √t to waga modularna gaussianu, wymiar przez dwa, jeden wymiar. Kelvin obraca korbą i wypada ½.

**Przekładnia C — integrator z kołem odwracającym (Mellin, i inwersja t ↦ 1/t).** ξ(s) = ∫₀^∞ ψ(t) t^{s/2} dt/t, ψ = (θ−1)/2. Teraz jedyny ruch: **rozetnij całkę w t = 1** — punkt stały inwersji, zgięcie — i połowę poniżej zgięcia przepuść przez koło odwracające t ↦ 1/t. Przekładnia B mówi, że po odwróceniu wypada √t, więc t^{s/2} zamienia się w t^{(1−s)/2}: dolna połowa staje się górną z s ↦ 1−s. Dwie połowy zamieniają się rolami na zgięciu t = 1, więc ξ(s) = ξ(1−s), a zgięcie w t przechodzi w zgięcie w s: **t = 1 ↦ s = ½.** Policzone: maszyna dwupołówkowa oddaje ξ(2,7) = 0,555701423555, tyle samo co bezpośrednio. To jest cały dowód Riemanna, jako trzy koła: różnica (π), Fourier (Poisson), inwersja (σ). Zauważ, które to koła: **z − 1, transformata, x ↦ x⁻¹** — uniformizator, DFT, lustro. Trzy rzeczy, na których stoi cały ik.

I gdzie w tej maszynie jest placek: forma stopnia z poprzedniego uderzenia to *dodatniość* — a maszyna Kelvina liczy dokładnie to, przy czym dodatniość widać: współczynniki Fouriera funkcji dodatnio określonej. Kryterium Weila to zdanie „ta maszyna zwraca formę dodatnią" — dla placka koło jest widoczne (stopień endomorfizmu), dla ℚ koło jest zasłonięte. Silnik różnicowy daje biegun i zera trywialne, integrator z inwersją daje zgięcie w ½, analizator daje wagę ½ — i jedyne koło, którego nikt nie widzi, to to, które gwarantuje, że wszystkie zera siedzą na zgięciu. Trzy koła obracają się i drukują ξ do dwunastu cyfr; czwarte koło to RH. Babbage, Kelvin, Riemann — i jedno puste łożysko. ⚙️🦧

---

**Status: konstrukcja i sprawdzalne tożsamości analityczne; bez dowodu RH.** Zacznijmy od tego, co każda operacja przyjmuje, co zwraca i czego nie odwraca.

### 1. Silnik różnicowy, z ustaloną stałą

Dla wielomianów $D=d/dx$ oraz $e^D f(x)=f(x+1)$, zatem

$$
\Delta_1=e^D-I,\qquad \Delta_1f(x)=f(x+1)-f(x).
$$

Nie jest to operator odwracalny na całej przestrzeni: usuwa stałe. Na większych klasach funkcji jego jądro zawiera wszystkie funkcje o okresie $1$. Symbol $1/D$ wymaga wyboru stałej całkowania; symbol $1/(e^D-1)$ również wymaga wyboru rozwiązania.

Na wielomianach dostajemy konkretne rozwiązanie bez niedopowiedzeń:

$$
A_m(x)=\frac{B_{m+1}(x)-B_{m+1}(0)}{m+1},\qquad
\Delta_1 A_m=x^m,\quad A_m(0)=0.
$$

To jedyna wielomianowa antyróżnica $x^m$ z taką normalizacją. [Równanie różnicowe wielomianów Bernoulliego: DLMF 24.4.1](https://dlmf.nist.gov/24.4.E1).

Zeta Hurwitza łączy tę konstrukcję z parametrem zespolonym wprost:

$$
\zeta(s,a+1)-\zeta(s,a)=-a^{-s},\qquad
-\zeta(-m,a)=\frac{B_{m+1}(a)}{m+1}.
$$

Tu $a>0$, pierwsza równość dla $s\ne1$ przez przedłużenie analityczne, druga dla $m=0,1,\ldots$. Jest to rodzina antyróżnic potęg, nie nieograniczony operator rozwiązujący każdą rekurencję. [DLMF §25.11, równania 3 i 14](https://dlmf.nist.gov/25.11).

Rozwinięcie

$$
\frac{1}{e^z-1}=\frac1z-\frac12+
\sum_{k\ge1}\frac{B_{2k}}{(2k)!}z^{2k-1},\qquad 0<|z|<2\pi,
$$

uzasadnia współczynniki. Podstawienie operatora $D$ pozostaje rachunkiem formalnym, dopóki nie określimy dziedziny i sensu zbieżności. [Funkcja tworząca: DLMF §24.2](https://dlmf.nist.gov/24.2).

### 2. Skończony rachunek potrzebuje reszty

Przy $s>1$ i naszej konwencji sumowania:

$$
\zeta(s)=\sum_{n=1}^{N-1}n^{-s}+\frac{N^{1-s}}{s-1}
+\frac12N^{-s}
+\sum_{k=1}^{m}\frac{B_{2k}}{(2k)!}(s)_{2k-1}N^{1-s-2k}
+R_{N,m}(s),
$$

gdzie $(s)_j=s(s+1)\cdots(s+j-1)$. $R$ jest resztą Eulera–Maclaurina, nie domyślnym zerem. [Reprezentacje z resztą: DLMF §25.2](https://dlmf.nist.gov/25.2).

Dla $s=3$, ośmiu składników, czyli $N=9$, oraz czterech poprawek Bernoulliego otrzymałem błąd około $-1.4077353453\cdot10^{-12}$ (przybliżenie minus $\zeta(3)$, czyli $-R_{9,4}(3)$). Porównanie jest niezależne od Eulera–Maclaurina: używa wymiernej sumy 150 wyrazów szeregu

$$
\zeta(3)=\frac52\sum_{n\ge1}\frac{(-1)^{n-1}}{n^3\binom{2n}{n}},
$$

z błędem ograniczonym następnym wyrazem. Wynik dobrze przybliża liczbę, ale nie uprawnia do pominięcia reszty. [Szereg odniesienia: DLMF 25.6.9](https://dlmf.nist.gov/25.6.E9).

### 3. Wersja Mellina, która rzeczywiście zwraca ξ

Niech

$$
\theta(t)=\sum_{n\in\mathbb Z}e^{-\pi n^2t},\qquad
\omega(t)=\tfrac12(\theta(t)-1),\qquad
\Lambda(s)=\pi^{-s/2}\Gamma(s/2)\zeta(s).
$$

Surowa całka zwraca $\Lambda$, nie $\xi$:

$$
\Lambda(s)=\int_0^\infty\omega(t)t^{s/2}\,\frac{dt}{t},
\qquad\Re s>1.
$$

Po użyciu $\theta(1/t)=\sqrt t\,\theta(t)$ i rozcięciu w $1$:

$$
I(s)=\int_1^\infty\omega(t)
\left(t^{s/2}+t^{(1-s)/2}\right)\frac{dt}{t},
\qquad
\Lambda(s)=\frac{1}{s(s-1)}+I(s),
$$

$$
\boxed{\xi(s)=\frac12+\frac12s(s-1)I(s).}
$$

$I$ jest całkowita dzięki wykładniczemu zanikowi $\omega$. Ostatnia formuła obowiązuje również w $s=0,1$ i daje tam $\xi=1/2$. Symetria $s\leftrightarrow1-s$ jest widoczna w całej formule. Tożsamość pochodzi z rozdzielenia całki, nie z punktowego odwzorowania $t=1\mapsto s=1/2$. Mellin przekształca funkcję, nie pojedynczy punkt osi. [Całka theta po rozcięciu: DLMF 25.5.13–14](https://dlmf.nist.gov/25.5.E13).

Sprawdzenie dwiema drogami: całka powyżej daje $\xi(2.7)\approx0.5557014235552705$; definicja przez $\Gamma$ i Euler–Maclaurin daje $0.555701423555263$. Różnica około $7.6\cdot10^{-15}$ jest kontrolą zmiennoprzecinkową, nie certyfikatem przedziałowym.

### 4. Dodatni sygnał nie zamyka lokalizacji zer

Kontrola przeciw nadmiernemu wnioskowi z Fouriera:

$$
h(z)=2+\cos z=\int_{\mathbb R}e^{izx}\,d\mu(x),\qquad
\mu=2\delta_0+\tfrac12\delta_1+\tfrac12\delta_{-1}\ge0.
$$

$h$ jest dodatnio określona na osi rzeczywistej, nawet $h(t)\ge1$, ale ma zera $z=\pi\pm i\operatorname{arcosh}2$. Sama dodatniość miary w reprezentacji Fouriera nie wymusza rzeczywistości wszystkich zer jej całkowitej transformaty. Nie jest tym samym co dodatniość konkretnego funkcjonału Weila.

**W skrócie:** antyróżnica z warunkiem normalizującym → transformacja theta z obszarem zbieżności → całkowita funkcja $\xi$ z jawnymi składnikami brzegowymi. Te kroki dają równanie funkcyjne i obliczenia. Dodatniość potrzebna do RH pozostaje osobnym twierdzeniem z dodatku do pierwszej notatki. Żaden z testów liczbowych nie zastępuje tego kroku.

---

### Uwagi recenzenckie, append-only

Narracja powyżej pozostaje niezmieniona.

**R1 (kolizja notacji).** Linia 5 używa π dla operatora przesunięcia $e^D-1$. W [notatce 01](01_RAMIFIKSACJA.md) $\pi$ oznaczało nakrycie $z\mapsto z^2$ (tu omawiane w Przekładni B jako fałd). To ten sam symbol, dwie różne role. Sekcje 1–3 tłumaczą każdą z osobna, więc błędu nie ma — ale czytelnik skaczący między plikami może się zatrzymać. Jedno zdanie klucza wystarczy.

**R2 (szczelina do pilnowania).** Linia 5: „silnik policzył $\zeta(-1)=-1/12$ z samego koła Bernoulliego". Koło (szereg $1/(e^D-1)$) ma zerowe współczynniki przy nieparzystych potęgach powyżej $D^1$ — daje tylko $\zeta(1-2k)$ dla $k\ge1$. Wartość przy $m=1$ (czyli $\zeta(-1)$) nie leży w tym kole; wymaga wzoru $\zeta(-m)=-B_{m+1}/(m+1)$, który formalne podstawienie operatora nie dowodzi. Sekcja §1 mówi o tym właściwie ("podstawienie operatora pozostaje rachunkiem formalnym"), ale sformułowanie narracyjne jest bliższe silnikowi, niż zasługuje. **Nie błąd matematyczny — ryzyko nadinterpretacji.**

**Co zweryfikowano poza plikiem.** Współczynniki szeregu $z/(e^z-1)$: $1,-1/2,1/6,0,-1/30,0,1/42$ dokładnie wymiernie; Euler–Maclaurin $\zeta(3)$ z $N=9,m=4$ daje błąd $-1{,}40773534529\cdot10^{-12}$ zgodny z plikiem do 10 cyfr; niezależna kontrola szeregiem Apéry'ego (150 wyrazów) $\zeta(3)$ = 1,2020569031595942854; $\theta(1/t)=\sqrt{t}\,\theta(t)$ do $10^{-60}$ dla $t=0{,}3$ i $t=2$; $\xi(2{,}7)$ dwiema drogami do $10^{-62}$; tożsamości Hurwitza i antyróżnicy wielomianów Bernoulliego potwierdzone wymiernie i numerycznie.

**Czego te uwagi nie mówią.** Nie dołączono dowodu RH; nie wykazano rozbieżności między ξ a Eulerem–Maclaurinem; nie wykazano, że trzy koła tworzą zamknięty system. Kontrola w §4 (funkcja $2+\cos z$ z dodatnią miarą i zerami poza osią) nadal zamyka pokusę przeniesienia dodatniości Fouriera na rzeczywistość zer.
