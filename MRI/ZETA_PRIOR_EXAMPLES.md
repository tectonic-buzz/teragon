# ζ — wcześniejsze przykłady, zachowane wyniki i granice

Stan: 2026-09-09. Zapis wcześniejszych sprawdzeń rozmowy, nie nowy wspólny dowód wszystkich korespondencji. Przykład Smith–Cauchy–MRI oraz nowy rachunek Fourier–Möbius są w osobnym dokumencie [MRI_MOBIUS_FOURIER_AUDIT.md](MRI_MOBIUS_FOURIER_AUDIT.md).

Każdy wpis określa obiekt, odczyt i to, czego odczyt nie odzyskuje. Numeryczne sprawdzenia historyczne nie są tu przedstawiane jako ponownie uruchomione.

## 1. Biegun → delta; pełny Laurent → pochodne delty

Dla funkcji meromorficznej w otoczeniu pionowego odcinka definiujemy lokalnie, w sensie dystrybucji,

\[
J_\sigma[f](t)=\lim_{\varepsilon\downarrow0}
\frac{f(\sigma+\varepsilon+it)-f(\sigma-\varepsilon+it)}{2\pi}.
\]

Przy prostym biegunie o residuum \(r\), w \(\sigma\), mamy \(J_\sigma[f]=r\delta_0\). W kanale rzeczywistym odczytujemy \(\Re(r)\delta_0\). Część holomorficzna znika w tej lokalnej różnicy. Dla ζ Riemanna residuum w 1 jest równe 1.

Dokładniej:

\[
\frac{(\varepsilon+it)^{-m-1}-(-\varepsilon+it)^{-m-1}}{2\pi}
\longrightarrow \frac{i^m}{m!}\delta_0^{(m)}.
\]

Stąd

\[
J_1[\zeta^2]=i\delta'_0+2\gamma\delta_0,
\qquad \Re J_1[\zeta^2]=2\gamma\delta_0.
\]

Usunięcie `Re` przywraca dipol, ale nie usuwa atomu z kolejnego współczynnika Laurenta. Wyższy biegun daje cały odpowiedni jet, nie tylko najwyższą pochodną.

Źródło: [Sochocki–Plemelj, notatki Habera](https://scipp.ucsc.edu/~haber/archives/physics215_17/Plemelj17.pdf). Pełny lokalny dowód i warunki: [DIRAC_DELTA_FROM_ZETA.md](DIRAC_DELTA_FROM_ZETA.md).

**Nie mylić:** jednostronny odczyt \(\Re(\zeta'/\zeta)\) zawiera gładkie tło. Dwustronny skok usuwa lokalną część holomorficzną; zamknięty kontur nie jest konieczny do samego liczenia atomów na zadanej prostej. Kontur liczy zera minus bieguny w obszarze. Liczenie wszystkich nietrywialnych zer wyłącznie na prostej krytycznej wymaga RH.

## 2. Ramanujan τ i zmiana pola bazowego

\(L(\Delta,s)\), dla formy parabolicznej wagi 12, jest całkowita. Detektor biegunów zastosowany do samej funkcji daje lokalnie zero — to nie znaczy, że funkcja nie niesie informacji.

Seria

\[
F(s)=\sum_{n\ge1}\tau(n)^2n^{-s}
\]

nie jest kwadratem \(L(\Delta,s)\). Ma prosty biegun w 12. Natomiast \(-L'/L\) ma przy zerze residuum równe minus krotność. Linie zer całej funkcji nie wynikają z detektora; dla Δ położenie wszystkich nietrywialnych zer na \(\Re s=6\) pozostaje hipotezą. Normalizacja: [LMFDB — funkcja L formy Δ](https://www.lmfdb.org/L/2/1/1.1/c11/0/0).

Dla ciała liczbowego \(K\):

\[
J_1[\zeta_K]=r_K\delta_0,\qquad
r_K=\frac{2^{r_1}(2\pi)^{r_2}h_KR_K}{w_K\sqrt{|D_K|}}.
\]

Jedna masa koduje tę kombinację niezmienników, nie każdy z nich oddzielnie. [Milne, Class Field Theory](https://www.jmilne.org/math/CourseNotes/CFTc.pdf).

Dla gładkiej, projektowej, geometrycznie spójnej krzywej \(C/\mathbb F_q\), rodzaju \(g\), z licznikiem \(P\):

\[
\zeta_C(s)=\frac{P(q^{-s})}{(1-q^{-s})(1-q^{1-s})},
\]
\[
J_1[\zeta_C]=r_C\sum_{k\in\mathbb Z}\delta_{2\pi k/\log q},
\quad
r_C=\frac{P(1/q)}{(1-1/q)\log q}
=\frac{q^{1-g}\#\operatorname{Jac}(C)(\mathbb F_q)}{(q-1)\log q}.
\]

Okres w kierunku urojonym i czynnik \(\log q\) należą do normalizacji. [MIT — definicje funkcji ζ nad ciałami skończonymi](https://math.mit.edu/~drew/Definitions.html).

## 3. Punkt jako delta; punkt jako adres Mortona

\[
\delta_u(\varphi)=\varphi(u),\qquad F_*\delta_u=\delta_{F(u)}.
\]

Przeplot pięciu nieujemnych współrzędnych całkowitych:

\[
M(u_0,\ldots,u_4)=\sum_{b\ge0}\sum_{a=0}^{4}u_{a,b}2^{5b+a}.
\]

Przykład: \((19,30,5,2,1)\leftrightarrow3217781\).

\[
M(u)\bmod 2^{5k}=M(u\bmod2^k),\qquad
\left\lfloor\frac{M(u)}{2^{5k}}\right\rfloor
=M\!\left(\left\lfloor\frac{u}{2^k}\right\rfloor\right).
\]

Pierwsze zachowuje młodsze bity i kongruencje 2-adyczne; drugie zgrubia położenie przez starsze bity. To różne operacje. Sąsiedztwo przestrzenne nie gwarantuje długiego wspólnego prefiksu przy przeniesieniach bitowych. Sam adres Mortona nie dodaje redundancji ani korekcji błędów. [Morton, oryginalny raport IBM](https://dominoweb.draco.res.ibm.com/0dabf9473b9c86d48525779800566a39.html).

## 4. ζ dynamiczna: punkty okresowe i krotności

\[
\zeta_f(u)=\exp\left(\sum_{n\ge1}\frac{N_n}{n}u^n\right),
\quad N_n=\#\operatorname{Fix}(f^n).
\]

W zwykłej ζ Artina–Mazura liczymy różne punkty. Stopień równania \(f^n(z)=z\) liczy pierwiastki z krotnościami. Dla \(f(z)=z^2+c\) liczba \(2^n\) nie jest zatem automatycznie liczbą różnych punktów dla każdego \(c\).

Kontrola historyczna: przy \(c=-5/4\), \(N_2=4\), \(N_4=12\), a więc są \((12-4)/4=2\) pierwotne czterocykle, nie 3. Dla \(c=-2\) jest ich 3. [Hinkkanen, Zeta functions of rational functions](https://www.acadsci.fi/mathematica/Vol19/hinkkan1.pdf).

Mapa \(g(x)=x^2-2\) jest półsprzężona z podwajaniem kąta przez \(x=2\cos\theta\); utożsamienie \(\theta\sim-\theta\) ma znaczenie. Warunek czwartej iteracji daje zarówno mianowniki 15, jak i 17. Nie jest to ta sama dynamika co samo podwajanie na okręgu. [Milnor, On Lattès Maps](https://people.math.harvard.edu/~demarco/Math295/Milnor_Lattes.pdf).

Dokładny most do pierwiastków lokalnego czynnika Hecke'a:

\[
g^{\circ2}\left(\frac{\tau(p)}{p^{11/2}}\right)
=\frac{\alpha_p^4+\beta_p^4}{p^{22}},
\quad \alpha_p+\beta_p=\tau(p),\quad\alpha_p\beta_p=p^{11}.
\]

Dwie iteracje \(g\) dają czwartą potęgę parametrów widmowych; nie oznacza to orbity o okresie 4. Dla \(1/(1-2u)\) biegun w \(u=1/2\) ma residuum \(-1/2\). Położenie bieguna może kodować tempo wzrostu; jego residuum nie jest tym samym co entropia.

## 5. Ciepło, rachunek funkcyjny, ζ i determinant

Dla odpowiedniego dodatniego operatora \(A\), po odjęciu jądra:

\[
\zeta_A(s)=\frac1{\Gamma(s)}\int_0^\infty t^{s-1}
\operatorname{Tr}'e^{-tA}\,dt,\qquad
\det{}'A=e^{-\zeta'_A(0)}.
\]

Pierwszy wzór zaczyna obowiązywać w półpłaszczyźnie zbieżności; drugi wymaga regularności przedłużenia w zerze. Całka \(\int_0^\infty e^{-tA}dt=A^{-1}\) wymaga odpowiedniej dodatniości. Nie ustanawia uniwersalnego kombinatora punktu stałego Y ani bezkosztowej eliminacji obliczeń.

Dla \(A=-\Delta_{S^2}\), poza modą stałą:

\[
A^{\pi/2+i}=A^{\pi/2}A^i.
\]

\(A^i\) jest unitarne; \(A^{\pi/2}\) wzmacnia wysokie częstotliwości i jest nieograniczone na całym \(L^2\), a nie wygładzające. \(\zeta_A(\pi+2i)\) jest śladem **ujemnej** potęgi \(A^{-(\pi+2i)}\), nie tego dodatniego operatora. [De Nápoli–Stinga, Fractional Laplacians on the sphere](https://arxiv.org/abs/1709.00448).

## 6. Torus, drzewo wolnej grupy i „drukarka kul”

Dla prostego spaceru na \(F_2\), drzewie stopnia 4,

\[
\rho=\frac{\sqrt3}{2},\qquad
G(z)=\sum_{n\ge0}p_{2n}(e,e)z^n
=\frac3{1+2\sqrt{1-3z/4}}.
\]

Promień zbieżności jest \(\rho^{-2}=4/3\). W punkcie granicznym \(G(4/3)=3\): jest rozgałęzienie pierwiastkowe, nie biegun ani nieskończona wartość. Detektor prostego bieguna nie stosuje się do niego bez zmian.

Spacer na nieskończonym \(\mathbb Z^2\) ma \(\rho=1\). Z kolei zwarty płaski torus ma dodatnią pierwszą niezerową wartość własną Laplasjanu. Brak szczeliny spaceru na grupie nakrywającej nie znaczy braku szczeliny zwartego ilorazu. Kryterium Kestena wymaga wskazania grupy, miary i reprezentacji. [Dougall–Sharp, kontekst twierdzenia Kestena](https://arxiv.org/abs/2309.01766).

Banach–Tarski nie daje podwojenia skończonej objętości za pomocą kawałków mierzalnych w sensie Lebesgue'a i izometrii. Wersje mierzalnej równoważności zachowują objętość; własność Baire'a to inna regularność. [Grabowski–Máthé–Pikhurko](https://arxiv.org/abs/1601.02958), [Marks–Unger](https://arxiv.org/abs/1501.01690).

## 7. Möbius, modularność i wspólny transport danych

Dla \(\gamma=\begin{pmatrix}a&b\\c&d\end{pmatrix}\in SL_2(\mathbb Z)\):

\[
\tau'=\frac{a\tau+b}{c\tau+d},\qquad
(n_e',n_m')=(a n_e-b n_m,-c n_e+d n_m).
\]
\[
\frac{|n_e'+\tau'n_m'|^2}{\Im\tau'}
=\frac{|n_e+\tau n_m|^2}{\Im\tau}.
\]

Transport obejmuje zarówno parametr, jak i współrzędne ładunku. Sama zmiana \(\tau\) nie zachowuje ogólnie odczytu. Ta tożsamość nie jest dowodem pełnej dualności Montonen–Olive. [Vafa–Witten](https://arxiv.org/abs/hep-th/9408074).

Pojedyncza transformacja Möbiusa stopnia 1 jest nierozgałęziona. Rozgałęzienie pojawia się natomiast w ilorazie modularnym: \(j\) ma lokalne stopnie 3 przy \(e^{2\pi i/3}\) i 2 przy \(i\). Nie są to osobliwości samej \(\gamma\). [Milne, Modular Functions and Modular Forms](https://www.jmilne.org/math/CourseNotes/MF.pdf).

\[
j=\frac{E_4^3}{\Delta},\qquad
\Delta(\gamma\tau)=(c\tau+d)^{12}\Delta(\tau).
\]

Δ jest formą wagi 12, nie funkcją niezmienniczą. \((\Im\tau)^{12}|\Delta(\tau)|^2\) jest niezmiennikiem. Związek z moonshine jest realny; nie dowodzi wszystkich interpretacji fizycznych. [Borcherds, Problems in Moonshine](https://math.berkeley.edu/~reb/papers/iccm/iccm.pdf).

## 8. Notka o rolach danych

ζ nie ustala znaczenia kodowania. Matematyczna jednostka, tag `01`, historyczne słowo `NUM(0)` i współczynnik wielomianu to różne role. Elementy pola bazowego można reprezentować wielomianami stałymi.

W starym `Tale/dude/iota.c`: `NUM(n)=(n<<2)|1`, więc słowo `01` dekoduje się jako liczba zero, `05` jako jeden, a `09` jako dwa. To nie identyfikacja matematycznego zera z jedynką. W odzyskanym `Tale/ik` census, payload i adres są osobnymi odczytami. Ten historyczny wariant nie jest automatycznie aktualnym systemem.

Podobnie w \(\mathbb Q[C_8]\), przy \(u=1+x+\cdots+x^7\),

\[
\Lambda\Delta=1+u,\quad (1+u)u=9u,\quad
\Delta^{-1}=\Lambda-\tfrac13u.
\]

Ślepota projekcji na mody pierwotne względem DC nie oznacza nieodwracalności całego operatora. Identyczny census lub identyczny odczyt ζ nie gwarantuje identyczności danych.

## 9. Galois, Artin i rozkład widma — wspólny mechanizm, różne operacje

Dla skończonego rozszerzenia Galois \(K/k\), grupy \(G\) i jej nieredukowalnych reprezentacji zespolonych:

\[
\mathbb C[G]\simeq\bigoplus_{\rho\in\widehat G}V_\rho^{\oplus\dim\rho},
\qquad
\zeta_K(s)=\prod_{\rho\in\widehat G}L(s,\rho,K/k)^{\dim\rho}.
\]

W czynnikach Artina przy pierwszych ramifikowanych należy używać podprzestrzeni niezmienniczych inercji. Nie usuwa się tych czynników bez odpowiedniej zmiany równania. Dla dowolnej podgrupy \(H\le G\) poprawny wzór na ciało pośrednie to

\[
\zeta_{K^H}(s)=\prod_{\rho\in\widehat G}
L(s,\rho,K/k)^{\dim V_\rho^H},
\qquad
\dim V_\rho^H=\frac1{|H|}\sum_{h\in H}\chi_\rho(h).
\]

To indukcja reprezentacji trywialnej z H oraz wzajemność Frobeniusa. Warunek \(\chi|_H=1\) wystarcza dopiero dla jednowymiarowych charakterów, w szczególności gdy G jest abelowa. Źródła: [Artin 1924, §4, tłumaczenie z komentarzem](https://public.csusm.edu/aitken_html/Translations/Artin1924.pdf), [Knapp — formalizm indukcji funkcji L](https://www.math.stonybrook.edu/~aknapp/pdf-files/notices2.pdf).

**Kontrola nieabelowa.** Dla \(G=S_3\), \(H=\langle(12)\rangle\), wymiary przestrzeni H-niezmienniczych w reprezentacjach trywialnej, znaku i standardowej wynoszą odpowiednio **1, 0, 1**. Dlatego stopień pola pośredniego wynosi \(1+0+2=3\), a \(\zeta_{K^H}=\zeta_k L(s,\rho_{\mathrm{std}})\). Sama lista jednowymiarowych charakterów zgubiłaby składnik stopnia 2.

Dla skończonego regularnego nakrycia riemannowskiego \(\widetilde M\to M\), z podniesioną metryką i zgodnymi warunkami brzegowymi, ten sam rozkład reprezentacji daje natomiast **sumę**:

\[
\zeta^{\mathrm{spec}}_{\widetilde M}(s)
=\sum_{\rho\in\widehat G}(\dim\rho)\,
\zeta^{\mathrm{spec}}_{\Delta_\rho}(s).
\]

\(\Delta_\rho\) jest Laplasjanem na skręconej wiązce nad M. Niezerowe wartości własne i krotności muszą być liczone konsekwentnie. Iloczyn odzyskujemy dla wyznaczników, gdy odpowiednie ζ są regularne w zerze:

\[
\det{}'\Delta_{\widetilde M}
=\prod_{\rho\in\widehat G}
(\det{}'\Delta_\rho)^{\dim\rho}.
\]

[Spectra, Group Representations and Twisted Laplacians, równanie (3.6)](https://link.springer.com/chapter/10.1007/978-3-031-27704-7_3).

Dla cylindra nakrywającego wstęgę: \(P_\pm=(I\pm U_\tau)/2\). Zwykłe funkcje na wstędze odpowiadają sektorowi **+**, a sektor − to sekcje skręcone. Ich zety spektralne się dodają. Odczyt tylko sektora + nie rekonstruuje automatycznie sektora −: np. macierze o sektorowych wartościach własnych \((2,3)\) i \((2,5)\) mają identyczny sektor +, ale inne pokrycie widmowe.

Galois dostarcza odpowiedniości podgrup i pól; w przypadku ogólnym nie jest to krata „podgrup charakterów”. Historia determinanty grupowej rzeczywiście prowadzi przez Dedekinda i Frobeniusa, lecz nie wynika stąd meta-twierdzenie „każda przeszkoda jest grupą, a każda korekta teorią reprezentacji”. [Frobenius i determinanta grupowa — Conrad](https://kconrad.math.uconn.edu/articles/groupdet.pdf). Nie przypisujemy też całej teorii jednej nocy: zachował się tekst Galois datowany na wrzesień 1831, opisujący już jego wcześniejsze badania nad równaniami. [Rękopis Galois, wydanie Tannery, s. 24](https://fr.wikisource.org/wiki/Page:Galois_-_Manuscrits,_%C3%A9dition_Tannery,_1908.djvu/24).

## 10. Topologia Krulla: adres jako zgodna rodzina odczytów

Niech \(\Omega/k\) będzie algebraicznym rozszerzeniem Galois, być może nieskończonym. Dla skończonych podrozszerzeń Galois \(E/k\) połóżmy

\[
G=\operatorname{Gal}(\Omega/k),\quad
U_E=\operatorname{Gal}(\Omega/E),\quad
\pi_E:G\to\operatorname{Gal}(E/k).
\]

Topologia Krulla ma bazę otoczeń automorfizmu σ złożoną z klas \(\sigma U_E\):

\[
\tau\in\sigma U_E\iff\tau|_E=\sigma|_E,
\qquad
G\simeq\varprojlim_{E/k\ \mathrm{fin.\ Galois}}\operatorname{Gal}(E/k).
\]

Skończony odczyt określa klasę automorfizmów; wszystkie zgodne restrykcje określają jeden automorfizm. Grupa jest zwarta, Hausdorffa i całkowicie niespójna. Otoczenia te są zarazem otwarte i domknięte. Nie jest to zwykła gładka rozmaitość ani metryka odczytana z wartości ζ. W nieskończonej odpowiedniości Galois polom pośrednim odpowiadają **domknięte** podgrupy; otwarte odpowiadają skończonym rozszerzeniom. [Milne, Fields and Galois Theory, §7, twierdzenie 7.13](https://www.jmilne.org/math/CourseNotes/FT.pdf).

### Delta z ograniczania adresu — jawny rachunek

Niech m będzie znormalizowaną miarą Haara na G, a a ustalonym automorfizmem. Dla otwartej normalnej podgrupy U definiujemy

\[
K_{U,a}(g)=\frac{\mathbf1_{aU}(g)}{m(U)},\qquad
\int_GK_{U,a}\,dm=1.
\]

Gdy U przebiega bazę coraz mniejszych otoczeń jedności:

\[
K_{U,a}\,dm\ \xrightarrow{\mathrm{weak}}\ \delta_a.
\]

Dowód nie wymaga regulatora: dla ciągłej f błąd średniej po aU jest najwyżej \(\sup_{g\in aU}|f(g)-f(a)|\), który dąży do zera. To granica po bazie otoczeń (sieć); ciąg wystarcza, gdy jest przeliczalna baza, np. dla \(\operatorname{Gal}(\overline{\mathbb Q}/\mathbb Q)\).

Na skończonym ilorazie \(Q=G/U\) ortogonalność charakterów daje drugi, dokładny zapis tego samego jądra:

\[
K_{U,a}(g)=\sum_{\rho\in\widehat Q}
(\dim\rho)\,\chi_\rho\!\left(\pi_U(ga^{-1})\right).
\]

Suma jest charakterem reprezentacji regularnej: ma wartość |Q| na tożsamości i 0 poza nią. W przypadku abelowym redukuje się do skończonej sumy Fouriera. Współczynnik \(1/|Q|\) pojawiłby się dla delty Kroneckera względem miary zliczającej; tutaj jądro jest gęstością względem miary Haara o masie 1.

To wyprowadzenie łączy **Krull → skończony iloraz → charaktery → adres/delta**. Nie wymaga ζ Riemanna. Funkcje Artina mogą następnie rejestrować te reprezentacje, ale sam ich skalarny odczyt nie zastępuje kompletu restrykcji. Zgodność adresów nie jest ponadto redundancją kodu ani dowodem bezpieczeństwa kryptograficznego.

Kontrole skończone: [test_galois_krull_readout.py](test_galois_krull_readout.py). Testy obejmują reprezentacje S₃, utratę sektora, sumę ζ kontra iloczyn wyznaczników oraz zgodność skończonych adresów i jądra charakterowego. Nie są numerycznym dowodem twierdzeń o wszystkich nieskończonych rozszerzeniach.

## 11. Feit–Thompson, Burnside i p-grupy: certyfikaty rozwiązalności

| Warunek dla skończonej G | Wniosek |
| --- | --- |
| \(|G|\) nieparzyste | G rozwiązalna — Feit–Thompson |
| \(|G|=p^a q^b\), p,q pierwsze, a,b≥0 | G rozwiązalna — Burnside |
| \(|G|=p^a\) | G nilpotentna, więc rozwiązalna |

Źródła: [formalny dowód twierdzenia o nieparzystym rzędzie](https://github.com/math-comp/odd-order/blob/master/README.md), [Burnside_p_a_q_b w Mathematical Components](https://coq.kwarc.info/mathcomp.character.integral_char.html), [Milne, Group Theory, wniosek 6.17](https://www.jmilne.org/math/CourseNotes/GT.pdf). Nie uruchamialiśmy tu Rocq/Coq; wskazujemy istniejący dowód formalny.

Rozwiązalność oznacza, że ciąg \(G^{(0)}=G\), \(G^{(i+1)}=[G^{(i)},G^{(i)}]\) kończy się grupą trywialną. Daje serię z abelowymi ilorazami; dla skończonej grupy można ją uszczegółowić do czynników cyklicznych rzędu pierwszego. Dla p-grup czynniki takiej serii mają rząd p. Nie oznacza to, że sama grupa jest abelowa albo że rozszerzenia rozszczepiają się na iloczyny proste.

W zastosowaniu do Galois, dla wielomianu nad ciałem charakterystyki zero, rozwiązalność grupy ciała rozkładu odpowiada rozwiązywalności równania przez pierwiastniki. Nie jest to obietnica taniego obliczenia ani twierdzenie o odzyskiwaniu zaszumionych danych. [Milne, Fields and Galois Theory](https://www.jmilne.org/math/CourseNotes/FT.pdf).

**Ważne obok Aₙ:** A₄ jest rozwiązalna, A₅ już nie: \(|A_5|=60=2^2\cdot3\cdot5\). Aₙ dla n≥5 są nieabelowe proste. Istnienie rozwiązalnych podgrup Sylowa lub C₅ wewnątrz A₅ nie czyni A₅ rozwiązalną. Kontrola permutacyjna daje rzędy kolejnych grup pochodnych:

\[
C_3:\ 3\to1,\quad
D_8:\ 8\to2\to1,\quad
S_4:\ 24\to12\to4\to1,\quad
A_5:\ 60\to60.
\]

**Ważne dla korekcji:** w regularnym kodzie permutacyjnym C₃ minimum odległości transpozycji wynosi 2, a w C₅ wynosi 4. Obie grupy są cykliczne rzędu pierwszego, lecz tylko druga z tych konstrukcji poprawia każdą jedną zamianę. O zdolności korekcyjnej decyduje więc także działanie, wybrany codebook i metryka, nie rozwiązalność.

Każda permutacyjna reprezentacja grupy nieparzystego rzędu ma parzysty obraz: homomorfizm znaku do C₂ musi być trywialny. To daje też ślepą plamkę — przestawienie należące do takiej grupy nie zmieni samego bitu parzystości.

**Ważne dla Krulla:** granica odwrotna skończonych p-grup jest pro-p, a skończonych grup rozwiązalnych — pro-rozwiązalna. Nie wolno z tego wywnioskować wspólnej skończonej długości szeregu pochodnego w granicy. Jeżeli wszystkie ilorazy mają długość ≤d dla tego samego d, wówczas odpowiednie słowo komutatorowe znika we wszystkich ilorazach, więc i w granicy. Bez tego ograniczenia krok do rozwiązalności całej granicy nie jest uzasadniony.

Podział pracy: **Galois — symetrie i pola; Krull — zgodność odczytów; rozwiązalność — seria redukcji grupy; FEC — rozróżnialność dopuszczonych uszkodzeń.** Te warunki mogą współpracować, ale nie zastępują się nawzajem.
