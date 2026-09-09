# Smith → Cauchy → MRI: cztery sprawdzenia Möbiusa, Fouriera i ζ

Stan: 2026-09-09. Audyt wklejonej rozmowy, z własnymi rachunkami i kontrolami. To notatka matematyczno-inżynierska, **nie walidacja skanera, danych pacjenta ani nowej metody klinicznej**.

**Wynik:** Fourier rzeczywiście rozdziela sektory skręcenia. Można też skonstruować dokładny most od nawinięcia fazy do wiązki Möbiusa — przez lokalną połowę fazy. Most zachowuje jednak tylko parzystość nawinięcia. Zwykłe zawinięcie fazy MRI nie jest przepełnieniem arytmetycznym ani automatycznie wstęgą Möbiusa. ζ odpowiednio wybranego operatora jest dodatkowym odczytem, a nie uniwersalnym dekoderem obrazu.

**Po dopiskach o ι, wielomianach i Babbage'u:** pełna DFT jest obliczaniem wielomianu w pierwiastkach z jedności, ale nie dodaje redundancji. Różnice skończone są anihilatorem dla zadanej klasy wielomianów, lecz nie odróżnią dwóch różnych poprawnych elementów tej klasy. Transport, test zgodności i korekcja to trzy różne gwarancje. Cała wklejona interpretacja wymaga istotnych poprawek; poniższe ograniczone wyniki nadają się do dalszych badań z podanymi założeniami.

Wcześniejsze przykłady: [ZETA_PRIOR_EXAMPLES.md](ZETA_PRIOR_EXAMPLES.md). Nowe kontrole: [test_mobius_fourier_readout.py](test_mobius_fourier_readout.py).

## Sprawdzenie 1 — co jest przestrzenią, nakryciem i dodatkowym wymiarem?

| Obiekt | Wymiar wewnętrzny / rodzaj danych | Istotna własność |
| --- | --- | --- |
| Wstęga Möbiusa | powierzchnia 2D z brzegiem | osadza się bez samoprzecięć w \(\mathbb R^3\) |
| Butelka Kleina | zamknięta powierzchnia 2D | osadza się w \(\mathbb R^4\), nie w \(\mathbb R^3\) |
| Nakrycie orientacyjne | dwie karty nad tym samym lokalnym obszarem | nie zwiększa lokalnego wymiaru |
| Zespolony obraz MRI | amplituda i faza / dwie składowe rzeczywiste | dodatkowe dane nie są automatycznie dodatkowym wymiarem przestrzennym |

Dwie wstęgi sklejone po brzegu tworzą butelkę Kleina. Nie wynika stąd, że sama wstęga jest czterowymiarowa lub musi powstać przez przekrój projekcji butelki. Rozklejenie powierzchni wzdłuż krzywej i przekrój hiperpłaszczyzną to inne operacje. [Banchoff — butelka Kleina w czterech wymiarach](https://www.math.brown.edu/tbanchof/gc/Klein4D/Klein4D.html).

Jawna parametryzacja wstęgi w \(\mathbb R^3\), przy dostatecznie małej szerokości:

\[
F(\theta,v)=\big((R+v\cos(\theta/2))\cos\theta,
(R+v\cos(\theta/2))\sin\theta,v\sin(\theta/2)\big),
\]
\[
F(2\pi,v)=F(0,-v).
\]

Metryka indukowana przez tę konkretną parametryzację nie jest automatycznie płaską metryką prostokąta używaną w następnym rachunku.

Płaska wstęga o długości podstawowego obiegu \(L\) i szerokości \(W\):

\[
M=([0,L]\times[0,W])/((0,y)\sim(L,W-y)).
\]

Jej nakrycie orientacyjne jest cylindrem **o obwodzie \(2L\)**:

\[
\widetilde M=(\mathbb R/2L\mathbb Z)\times[0,W],\qquad
\tau(x,y)=(x+L,W-y).
\]

\(\tau^2=I\), a \(\tau\) nie ma punktów stałych. Iloraz jest nierozgałęzionym nakryciem dwukrotnym. Skręcenie globalne nie oznacza lokalnej ramifikacji. Analogicznie torus jest nakryciem orientacyjnym butelki Kleina. Dodatkowa karta przechowuje znak, nie dodatkową lokalną współrzędną przestrzenną.

## Sprawdzenie 2 — Fourier na nakryciu i właściwy znak sektora

Niech \(A=-\Delta\), z warunkiem Dirichleta na \(y=0,W\). Na cylindrze \(\widetilde M\) mamy bazę

\[
u_{mn}(x,y)=e^{i\pi mx/L}\sin(\pi ny/W),\qquad
m\in\mathbb Z,\ n\ge1,
\]
\[
\lambda_{mn}=\left(\frac{\pi m}{L}\right)^2+
\left(\frac{\pi n}{W}\right)^2.
\]

Bezpośrednie podstawienie daje

\[
u_{mn}\circ\tau=(-1)^{m+n+1}u_{mn}.
\]

Zatem funkcje skalarne na wstędze to sektor **\(\tau=+1\)**, czyli \(m+n\) nieparzyste. To potwierdza filtr parzystości z wklejki, ale przeczy jej późniejszemu zdaniu, że sama wstęga jest sektorem minus. Sektor minus opisuje zamiast tego sekcje odpowiedniej skręconej wiązki na ilorazie. Ten model płaski i jego mody podaje także [Bérard–Helffer–Kiwan, Lemma 2.2](https://arxiv.org/pdf/2005.01175).

Projektory to dwupunktowy Fourier po grupie \(\mathbb Z/2\):

\[
P_+=\tfrac12(I+\tau^*),\qquad P_-=\tfrac12(I-\tau^*).
\]

Ponieważ \(A\) komutuje z \(\tau^*\), rozkład jest zachowany przez ewolucję \(e^{-tA}\). Dla \(\Re s>1\):

\[
Z(s)=\sum_{m\in\mathbb Z,n\ge1}\lambda_{mn}^{-s},\qquad
Z_{\rm alt}(s)=\sum_{m,n}(-1)^{m+n}\lambda_{mn}^{-s},
\]
\[
\boxed{\zeta_M(s)=\tfrac12[Z(s)-Z_{\rm alt}(s)]},\qquad
\zeta_-(s)=\tfrac12[Z(s)+Z_{\rm alt}(s)],
\]
\[
Z=\zeta_M+\zeta_-.
\]

W porównaniu z nieskręconym cylindrem **tej samej długości \(L\)** zmienia się warunek na sklejeniu. Dla \(L=W=1\), pierwsze wartości \(\lambda/\pi^2\), z krotnościami, to:

| cylinder | wstęga |
| --- | --- |
| \(1,4,5,5,8,8,9,13,13,16,\ldots\) | \(1,5,5,5,5,9,13,13,13,13,\ldots\) |

To rozróżnienie dwóch zadanych modeli. Nie jest twierdzeniem o jednoznacznej rekonstrukcji dowolnej powierzchni z ζ. Równość zet spektralnych nakrycia jest tutaj **sumą sektorów**; iloczyn funkcji Dedekinda w rozszerzeniu kwadratowym jest analogią reprezentacyjną, nie tą samą operacją. Iloczyn uzyskuje się odpowiednio dla determinantów.

### Niezależna kontrola dyskretna

Zbudowano macierz Laplasjanu bez korzystania z listy wartości własnych: 4 miejsca wzdłuż obiegu, 4 wewnętrzne poziomy poprzeczne, jednostkowy krok; brzeg Dirichleta w \(y=0,5\). Porównano dokładny ślad odwrotności macierzy, liczony na ułamkach, z sumą odwrotności analitycznych wartości własnych.

| Model | \(\operatorname{tr}A^{-1}=\zeta_A(1)\) dokładnie | Przybliżenie |
| --- | --- | --- |
| cylinder | \(1718752/248501\) | 6.916479209339198 |
| wstęga | \(67696/9889\) | 6.845586004651633 |

To skończona dyskretyzacja, nie numeryczne wartości ζ powyższych powierzchni ciągłych. Wszystkie dozwolone mody sprawdzono też bezpośrednio przeciw macierzy, a rozkład na sektory sprawdzono dla rzeczywistego i zespolonego \(s\).

## Sprawdzenie 3 — wir fazy, połowa fazy i rzeczywisty most do Möbiusa

Dla niezerowego sygnału zespolonego \(z=Ae^{i\phi}\), jego znormalizowana faza \(q=z/|z|\) jest mapą do \(S^1\). Odczyt opakowanej fazy to wybór argumentu, a nie zmiana samego \(q\):

\[
e^{i(\phi+2\pi k)}=e^{i\phi}.
\]

Zwykłe odwinięcie szuka podniesienia do nakrycia \(\mathbb R\to S^1\), o grupie \(\mathbb Z\). Dla regularnej fazy na obszarze bez zer sygnału globalny ciągły argument istnieje wtedy, gdy wszystkie okresy wzdłuż pętli są zerowe. W szczególności niezerowe nawinięcie wokół usuniętego zera blokuje jedno globalne odwinięcie na tym samym obszarze. Można wybrać cięcie lub pracować na nakryciu. Po przecięciu pierścienia radialnie otrzymujemy obszar typu prostokąta, nie wstęgę Möbiusa. [Hatcher, kryterium podnoszenia, Proposition 1.33](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf).

### Konstrukcja, która naprawia most

Na pętli o nawinięciu \(k\), lokalny pierwiastek fazy

\[
h(\theta)=e^{i\phi(\theta)/2}
\]

po obiegu spełnia

\[
h(2\pi)=(-1)^k h(0).
\]

Można zdefiniować nad pętlą rzeczywistą linię \(\ell_\theta=\mathbb R h(\theta)\). Znak lokalnie wybranego \(h\) nie zmienia tej linii. Dla nieparzystego \(k\) otrzymujemy wiązkę Möbiusa; dla parzystego — trywialną. To dokładna konstrukcja, a nie utożsamienie każdego wiru z wstęgą. Ogólna operacja to pullback wiązki Möbiusa; [Hatcher, Vector Bundles & K-Theory, przykład 4 na s. 19–20](https://pi.math.cornell.edu/~hatcher/VBKT/VB.pdf) podaje dokładnie zależność od parzystości stopnia.

\[
\mathbb Z\longrightarrow\mathbb Z/2,\qquad k\longmapsto k\bmod2.
\]

**Cena tego mostu:** \(k=1\) i \(k=3\) dają ten sam typ wiązki. Wiązka nie pamięta całego numeru obiegu. Sam pierwiastek jest dodatkową wybraną reprezentacją; nie dowodzi, że faza odczytywana w MRI jest fizycznie półfazą.

### Fourier + ζ Riemanna, bez zgadywania

Dla zespolonych sekcji na okręgu długości \(L\), z ustaloną płaską koneksją zapisaną warunkiem

\[
f(x+L)=e^{2\pi i\alpha}f(x),
\]

Fourier ma mody \(e^{2\pi i(n+\alpha)x/L}\). Dla \(0<\alpha<1\):

\[
\lambda_n=\left(\frac{2\pi}{L}\right)^2(n+\alpha)^2,
\]
\[
\zeta_\alpha(s)=\left(\frac{L}{2\pi}\right)^{2s}
\big[\zeta_H(2s,\alpha)+\zeta_H(2s,1-\alpha)\big],\qquad\Re s>\tfrac12.
\]

Rozdzielenie liczb parzystych i nieparzystych w szeregu daje

\[
\zeta_H(u,\tfrac12)=(2^u-1)\zeta_R(u).
\]

Zatem

\[
\boxed{\zeta_{1/2}(s)=2\left(\frac{L}{2\pi}\right)^{2s}
(2^{2s}-1)\zeta_R(2s)},
\]
\[
\zeta_0(s)=2\left(\frac{L}{2\pi}\right)^{2s}\zeta_R(2s)
\quad\text{(mod zerowy pominięty)}.
\]

\(\alpha=1/2\) to znak minus po obiegu: mody półcałkowite, czyli konkretny Fourierowski odczyt skręcenia. Definicja i przedłużenie: [DLMF, funkcja ζ Hurwitza](https://dlmf.nist.gov/25.11).

Dla \(L=1,s=1\):

\[
\zeta_0(1)=\tfrac1{12},\qquad \zeta_{1/2}(1)=\tfrac14.
\]

To ζ operatora jednowymiarowego z warunkiem sklejenia, nie ζ całej dwuwymiarowej wstęgi z poprzedniej sekcji. Tam trzeba zachować także mody poprzeczne. Rozkład na dwa sektory, przesunięcie częstotliwości i dodatkowy kanał fazy są realne; żaden z tych faktów sam nie wyznacza czwartego wymiaru przestrzennego.

### Dlaczego nawet „ζ z fazą” może niczego nowego nie rozróżnić

Na grafie niech \(D_q=\operatorname{diag}(q_i)\), \(|q_i|=1\). Operator

\[
L_q=D_q L D_q^*
\]

zawiera lokalne fazy, lecz jest unitarnie podobny do \(L\). Wszystkie jego wartości własne, a więc i ζ, pozostają takie same. To kontrola negatywna dla pomysłu „dodaj fazę do Laplasjanu, a ζ od razu zobaczy wszystkie wiry”. Należy wskazać nieusuwalny warunek brzegowy, holonomię lub dodatkowe dane — nie tylko zmianę cechowania.

## Sprawdzenie 4 — co MRI mierzy, gubi i może odzyskać?

### Aliasing nie jest dowodem przepełnienia typu integer

W phase-contrast MRI, w podstawowym modelu:

\[
\phi=\pi v/v_{\rm enc}\pmod{2\pi}.
\]

Przy \(v_{\rm enc}=100\), wartości \(120\) i \(-80\) mają tę samą fazę. To niejednoznaczność pomiaru okresowego, obecna nawet w arytmetyce dokładnej. Nie potrzeba przepełnionego rejestru, zgubionego bitu ani dodatkowej ramifikacji. Nie oznacza to braku znaczenia klinicznego aliasingu; oznacza inną przyczynę i inną metodę korekcji. [ISMRM — model fazy i VENC](https://cds.ismrm.org/protected/18MProceedings/PDFfiles/E3135.html).

Podobnie:

- ograniczony zakres k-space daje odpowiedź punktową z oscylacjami i ringing;
- zbyt rzadkie próbkowanie daje aliasing;
- niezgodność fazy parzystych i nieparzystych linii EPI może dawać przesuniętą kopię obrazu;
- rzeczywisty overflow, saturacja ADC czy utrata bitów to osobne defekty, których ta rozmowa nie wykazała.

Żadne z pierwszych trzech zjawisk nie wymaga wiru fazy ani wstęgi Möbiusa. Nie każde próbkowanie MRI jest też kartezjańską kratą: istnieją trajektorie spiralne i radialne; [SPIRiT](https://pmc.ncbi.nlm.nih.gov/articles/PMC2925465/) rozpatruje również rekonstrukcję dla niekartezjańskich trajektorii.

### Tak dla Fouriera — z kompletem danych

Pełna zespolona DFT jest odwracalną zmianą reprezentacji skończonego wektora. Nie ma w niej obowiązkowej utraty fazy. Przejście \(z\mapsto|z|\) jest natomiast wiele-do-jednego. Tak samo wycięcie próbek przed transformacją może usunąć rozróżnienia.

Jawna kontrola: przy 16 punktach \(\theta_j=2\pi j/16\), sygnały

\[
e^{i\theta_j}=e^{17i\theta_j}
\]

są nierozróżnialne. DFT też ich nie rozróżnia. Drugie próbkowanie przesunięte o pół kroku rozdziela tę parę, lecz połączone próbkowanie nadal nie rozróżnia częstości 1 i 33. **Dodatkowy kanał zwiększa rozróżnialność, o ile wnosi niezależny pomiar; nie daje nieograniczonego horyzontu.**

Kontrola roundtrip DFT/IDFT dla zadanego wektora dała maksymalny błąd \(2.75\cdot10^{-14}\); sprawdzono też Parsevala. To błąd zmiennoprzecinkowy tej implementacji testowej, nie degradacja wymuszona matematycznie przez Fouriera.

### Model rekonstrukcji i „pakowanie zamiast przelewania”

W uproszczonej dyskretyzacji wielocewkowej:

\[
y=Ex+\eta,\qquad E=\begin{bmatrix}P_1FS_1\\\vdots\\P_cFS_c\end{bmatrix}.
\]

\(S_c\) są czułościami cewek, \(F\) transformatą Fouriera, \(P_c\) wyborem próbek. Jednoznaczność bez dodatkowych ograniczeń wymaga \(\ker E=0\); stabilność zależy także od małych wartości singularnych i poziomu szumu. Dla klasy dopuszczalnych obrazów \(\mathcal C\) warunek jest słabszy: \(\ker E\cap(\mathcal C-\mathcal C)=\{0\}\).

LORAKS podnosi próbki do większej, strukturalnej macierzy i wykorzystuje jej niski rząd, wynikający z ograniczonego supportu i/lub odpowiednich własności fazy. To rzeczywiste zastosowanie „dodatkowego wymiaru reprezentacji”. Nie tworzy nowych pomiarów: skuteczność wymaga poprawności modelu i dostatecznych ograniczeń. [Haldar — LORAKS](https://pmc.ncbi.nlm.nih.gov/articles/PMC4122573/).

SPIRiT wymaga zgodności danych z operatorem kalibracyjnym oraz pomiarem, np.

\[
\min_x\|(G-I)x\|^2\quad\text{przy}\quad\|Dx-y\|\le\varepsilon.
\]

GRAPPA/SPIRiT nie dają ogólnej gwarancji poprawienia dowolnej uszkodzonej przez ruch linii. Trzeba wykryć uszkodzenie, opisać ruch lub uznać próbkę za brakującą; nadal pozostają warunki odzyskiwalności. Gładkość czułości nie oznacza ściśle skończonego supportu jej transformaty — małe jądra są modelem/przybliżeniem. [Lustig–Pauly — SPIRiT](https://pmc.ncbi.nlm.nih.gov/articles/PMC2925465/).

Najbliższy praktyczny odpowiednik dodatkowego kanału rozstrzygającego obrót to **dual-/multi-VENC**: różne kodowania prędkości dostarczają dodatkowych równań dla nieznanych wielokrotności \(2\pi\). Takie metody rzeczywiście istnieją; ograniczają je szum, zakres prędkości i projekt akwizycji. [Dual velocity encoding](https://pmc.ncbi.nlm.nih.gov/articles/PMC3343178/), [Venc Design and Velocity Estimation](https://pmc.ncbi.nlm.nih.gov/articles/PMC9837712/).

### Reed–Solomon: dobra inspiracja, inne gwarancje

Dla \(n\) różnych punktów pola skończonego i \(\deg p<k\), kod ma odległość \(n-k+1\). Gwarancja jednoznacznej korekcji obejmuje \(2e+r\le n-k\), gdzie \(e\) to błędy o nieznanej pozycji, a \(r\) znane wymazania. Przy stopniu **co najwyżej \(k\)** liczba współczynników wynosi \(k+1\): trzeba przesunąć formułę o jeden. [Guruswami — Error Correction Up to the Information-Theoretic Limit](https://www.cs.cmu.edu/~venkatg/cacm09.html).

Próbki zaszumionego sygnału analogowego i uszkodzone symbole skończonego kodu to różne modele. Redundancja cewek może pełnić pokrewną rolę identyfikacyjną, lecz nie dziedziczy automatycznie dystansu ani gwarancji RS. Wzory recytacji mogą inspirować organizację redundancji, ale bez jawnego kanału, kodu i dekodera nie stanowią metody korekcji MRI. Sam adres Mortona również nie jest kodem korekcyjnym.

## Dodatkowy odczyt ζ: model pomiarowy musi się zmieniać wraz z testem

Dla skończonej kraty toroidalnej \(C_m\square C_n\):

\[
\lambda_{jk}=4\sin^2(\pi j/m)+4\sin^2(\pi k/n),\qquad
\zeta_L(s)=\sum_{(j,k)\ne(0,0)}e^{-s\log\lambda_{jk}}.
\]

To **skończona suma funkcji całkowitych**: nie ma bieguna w \(s=1\). Krata ma też dodatnią szczelinę nad modą stałą. Biegun Epsteinowskiej ζ ciągłego torusa w \(s=d/2\) dotyczy innego, nieskończenie wymiarowego operatora, a brak szczeliny na \(\mathbb Z^2\) — innego, nieskończonego grafu.

Dla cyklu \(C_{16}\) kontrola daje

\[
\zeta_L(1)=\frac{16^2-1}{12}=21.25,\qquad
\lambda_1=4\sin^2(\pi/16)\simeq0.15224093498.
\]

ζ niezmienionej siatki ma taki sam wynik dla każdego obrazu na tej siatce. Jeśli celem jest pomiar odzyskiwalności, sensowniejszym kandydatem jest np. operator \(E^*\Sigma^{-1}E\), przy znanym modelu szumu. Jego zero i małe wartości własne opisują nieobserwowalne lub słabo obserwowalne kierunki. To propozycja odczytu badanego operatora, nie wynik testu klinicznego. Pominięcie zera w ζ nie może usuwać informacji o wymiarze jądra z raportu.

## Korekty wstępu Smith–Cauchy–Gauss

### Smith i Tustin

Dla rzeczywistej dodatniej impedancji odniesienia \(Z_0\):

\[
\Gamma=\frac{Z_L-Z_0}{Z_L+Z_0},\qquad
1-|\Gamma|^2=\frac{4Z_0\Re Z_L}{|Z_L+Z_0|^2}.
\]

To nierozgałęziony biholomorfizm prawej półpłaszczyzny na dysk. \(|\Gamma|^2\) jest stosunkiem mocy odbitej do padającej w tym modelu. Samo \(|\Gamma|=1\) nie dowodzi uszkodzenia wzmacniacza, a \(|\Gamma|>1\) nie dowodzi samowzbudzenia: potrzebny jest model mocy, obciążenia i stabilności układu. Wykres opisuje układ, nie wytwarza energii. [Rohde & Schwarz — Smith chart](https://www.rohde-schwarz.com/us/products/test-and-measurement/essentials-test-equipment/spectrum-analyzers/understanding-the-smith-chart_257989.html).

\(-d\arg\Gamma/d\omega\) opisuje opóźnienie grupowe odbicia tam, gdzie \(\Gamma\ne0\); nie jest automatycznie opóźnieniem sygnału transmitowanego. Sam współczynnik jako funkcja impedancji nie określa też dyspersji bez zależności impedancji od częstości.

Tustin:

\[
s=\frac2T\frac{z-1}{z+1},\qquad
\Omega=\frac2T\tan(\omega T/2).
\]

Stabilna lewa półpłaszczyzna przechodzi do wnętrza dysku. Warping jest znaną zmianą współrzędnej częstości; prewarping dostraja wybrane częstotliwości. Brak prewarpingu nie jest dowodem ramifikacji. [SciPy — bilinear](https://docs.scipy.org/doc/scipy-1.17.0/reference/generated/scipy.signal.bilinear.html).

### Cauchy z ilorazu i granice wniosków o czasie

Dla niezależnych standardowych, wycentrowanych Gaussów \(Z_1,Z_2\), iloraz jest Cauchy'ego. Po odwracalnym przekształceniu rzeczywistym:

\[
\frac{aZ_1+bZ_2}{cZ_1+dZ_2}\sim\operatorname{Cauchy}\left(
\frac{ac+bd}{c^2+d^2},\frac{|ad-bc|}{c^2+d^2}\right).
\]

Mianownik jest niemal na pewno niezerowy, lecz może być dowolnie mały. Nie ma klasycznej średniej ani wariancji; średnia arytmetyczna niezależnych próbek Cauchy'ego zachowuje ten sam rozkład, zamiast skupiać się w punkcie. To nie wyklucza estymacji, np. przez medianę. Ilorazy Gaussów o niezerowych średnich nie są ogólnie rozkładem Cauchy'ego. [McCullagh — własności rodziny Cauchy'ego](https://www.stat.uchicago.edu/~pmcc/pubs/paper28.pdf).

Gęstość czasu pierwszego dojścia standardowego jednowymiarowego ruchu Browna bez dryfu do poziomu \(a>0\) wynosi

\[
f_T(t)=\frac{a}{\sqrt{2\pi t^3}}e^{-a^2/(2t)}.
\]

Średnia jest nieskończona, choć \(T<\infty\) prawie na pewno. Potęga \(t^{-3/2}\) dotyczy **gęstości**; funkcja przeżycia ma rząd \(t^{-1/2}\). Ograniczony obszar, dryf, reset i timeout zmieniają problem. Nie wynika z tego, że dowolna pętla sterowania ma nieskończony oczekiwany czas. [Notatki Rahmana — zasada odbicia i czas dojścia](https://www.maths.dur.ac.uk/users/mustazee.rahman/brownian.html).

Dla Browna na \(\mathbb H^2\), z generatorem \(\Delta/2\), odległość od punktu startu rośnie asymptotycznie jak \(t/2\). Brzeg idealny jest osiągany jako granica przy nieskończonym czasie, nie jako skończony wybuch. Transjencja nie oznacza zakazu wszystkich wcześniejszych powrotów. [Shiozawa — escape rate](https://arxiv.org/abs/1609.06814).

### Szum MRI i water-filling

Wycentrowany izotropowy szum zespolony pozostaje Gaussowski po unitarnej DFT. W idealnym pojedynczym kanale moduł \(|A+X+iY|\) ma rozkład Rice'a; przy \(A=0\) — Rayleigha. Przy wielu cewkach i nieliniowej rekonstrukcji model może być inny, np. niecentralny χ dla odpowiedniego sum-of-squares. Nie wolno narzucać Rice'a każdemu finalnemu obrazowi. [Gudbjartsson–Patz, 1995](https://pmc.ncbi.nlm.nih.gov/articles/PMC2254141/).

W prostym estymatorze dyfuzji \(\mathrm{ADC}=-\log(S_b/S_0)/b\), podniesienie małego \(S_b\) przez noise floor **obniża**, a nie podnosi estymowane ADC, przy ustalonym \(S_0\). To bezpośredni znak pochodnej; bardziej złożone estymatory trzeba sprawdzić osobno.

Water-filling optymalizuje rozdział mocy między zadanymi kanałami Gaussowskimi, \(P_i=(\nu-N_i/|h_i|^2)_+\). Nie jest zasadą „więcej parzystości w ciemnym pikselu” ani sposobem pakowania nadmiarowego szumu. [Tse–Viswanath, rozdział 5](https://stanford.edu/~dntse/Chapters_PDF/Fundamentals_Wireless_Communication_chapter5.pdf).

## Dopisek do czterech sprawdzeń — sampling, ι i wielomianowy transport

### Nie każda wieloznaczność jest ramifikacją

Nakrycie

\[
\mathbb R^d\longrightarrow\mathbb R^d/\Lambda
\]

jest lokalnie odwracalne wszędzie. To, że różne punkty mają ten sam obraz, jest zwykłą własnością wielokrotnego nakrycia, a nie punktem rozgałęzienia. Jeszcze prostszy kontrprzykład: \(z\mapsto z^2\) na \(\mathbb C^\times\) ma dwa przeciwne preobrazy każdego punktu i nigdzie zerowej pochodnej. Ramifikacja w \(z=0\) pojawia się dopiero po dołączeniu tego punktu. [Hatcher — nakrycia](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf).

Warunek Nyquista ogranicza klasę sygnałów tak, aby próbkowanie było na niej jednoznaczne. Zbyt rzadkie próbkowanie nie zamienia zwykłego nakrycia w rozgałęzione. Przy konwencji

\[
S(k)=\int\rho(x)e^{-2\pi ikx}\,dx
\]

próbkowanie **k-space** z krokiem \(\Delta k\) daje, w idealnym nieskończonym modelu, periodyzację **obrazu** z okresem \(1/\Delta k\):

\[
\Delta k\sum_{j\in\mathbb Z}S(j\Delta k)e^{2\pi ij\Delta kx}
=\sum_{m\in\mathbb Z}\rho(x-m/\Delta k).
\]

To własny zapis wzoru Poissona; wymaga odpowiedniej regularności albo interpretacji dystrybucyjnej. Próbkowanie obrazu daje analogicznie periodyzację jego widma. Skończone okno w k-space dodatkowo zmienia odpowiedź punktową — stąd ringing, odrębny od nakładania się kopii.

W języku klinicznych artefaktów trzeba zachować rozdzielenie: aliasing, truncation ringing, błędy fazy EPI, wiry fazy i kwantyzacja nie są jedną listą punktów ramifikacji.

### Half-Fourier: dodatkowy warunek, nie własność każdego MRI

\[
S(-k)=\overline{S(k)}
\]

jest symetrią transformaty **rzeczywistego** obrazu. Obraz zespolony MRI nie musi jej spełniać. Przykład kontrolny: obraz stały \(i\) na \(N\) punktach ma \(S(0)=Ni\), a nie rzeczywiste DC. Partial Fourier korzysta z oszacowania i korekcji fazy, żeby wykorzystać odpowiednią symetrię; niedokładne oszacowanie może powodować błędy. [Koopmans — Enhanced POCS, 2021](https://onlinelibrary.wiley.com/doi/abs/10.1002/mrm.28417).

Na skończonej siatce o parzystych \(N_x,N_y\), inwolucja \(k\mapsto-k\) ma **cztery** punkty stałe:

\[
(0,0),\ (N_x/2,0),\ (0,N_y/2),\ (N_x/2,N_y/2).
\]

DC jest jedynym punktem stałym w ciągłym \(\mathbb R^d\), nie w każdej dyskretnej reprezentacji. Sprzężenie zespolone jest też antyliniowe nad \(\mathbb C\); warunek Hermitowski trzeba traktować odpowiednio jako warunek rzeczywiście liniowy.

Rozkład \(P_\pm=(I\pm T)/2\) działa dla liniowego \(T^2=I\) również wtedy, gdy akcja geometryczna ma punkty stałe. Wolność akcji jest warunkiem zwykłego nakrycia ilorazowego, **nie warunkiem istnienia rozkładu na charaktery**. Orbifoldowy iloraz można skonstruować osobno; nie wynika stąd, że FFT wykonuje taki iloraz.

### Co rzeczywiście daje „carry complex across”?

W tej sekcji \(\iota\) oznacza jawnie włączenie \(S^1\hookrightarrow\mathbb C\), nie zweryfikowaną implementację wcześniejszego adresu Fable'a.

Zachowanie zespolonego sygnału przed modułem, argumentem i stratną kwantyzacją zachowuje więcej dostępnych danych. Ma to rzeczywiste zastosowania. Nie odzyskuje jednak informacji już utraconej:

\[
\phi,\ \phi+2\pi k\quad\longmapsto\quad e^{i\phi}
\quad\longmapsto\quad\iota(e^{i\phi})
\]

dają nadal ten sam punkt dla każdego \(k\). Jeśli zadaniem jest estymacja pełnej prędkości lub pełnego numeru obiegu, nie wystarcza przesunięcie operacji argumentu na koniec. Dla zadania niewymagającego pełnego argumentu można w ogóle go nie wyznaczać.

\(\mathbb C\) jest ściągalna, ale faza istnieje tylko tam, gdzie sygnał jest niezerowy, czyli w \(\mathbb C^\times\), którego grupa podstawowa to \(\mathbb Z\). Skurczenie pętli przez zero przechodzi przez stan bez określonej fazy. Nie jest darmowym usunięciem obstrukcji odwinięcia.

Filtr liniowy \(K*z\) może być użyteczny, lecz:

- dla faz \(179^\circ\) i \(-179^\circ\), średnia wektorów poprawnie wskazuje okolice \(180^\circ\), podczas gdy średnia tych dwóch reprezentantów kątowych daje \(0^\circ\);
- dla \(z_1=1,z_2=-1\), średnia zespolona jest zerem, chociaż oba moduły wynoszą 1;
- surowy sygnał \(Ae^{i\phi}\) i znormalizowany fazor \(e^{i\phi}\) to inne dane: normalizacja usuwa amplitudę i zmienia model szumu;
- liniowe filtrowanie ustalonym filtrem zachowuje zerową średnią szumu zespolonego, ale późniejszy moduł nadal może mieć dodatnie obciążenie estymacji;
- do koherentnego uśredniania sygnałów o zmiennych fazach może być potrzebna ich wcześniejsza korekcja.

Ostatni warunek jest wyraźnie opisany w badaniach [Adaptive phase correction of diffusion-weighted images](https://pmc.ncbi.nlm.nih.gov/articles/PMC7355239/). Gdy prawdziwa faza jest znana, obrócenie sygnału i odczyt jego części rzeczywistej może uniknąć obciążenia modułu; estymowana faza wprowadza własny błąd.

Nie ma więc ogólnego wyniku „ściśle dokładniej i taniej”. Realny koszt zależy od reprezentacji bazowej, filtrów i celu odczytu: amplituda+faza to już dwie liczby rzeczywiste, tak samo jak real+imag. Filtr o rzeczywistych współczynnikach działa osobno na dwóch składowych; nie każda operacja potrzebuje pełnego mnożenia zespolonego. Nie przeprowadzono benchmarku porównywalnych pipeline'ów. Zachowanie liczb zespolonych nie usuwa też wcześniejszej kwantyzacji akwizycji.

Nie wszystkie ilorazy się rozgałęziają, a „nierozgałęzienie” nie jest automatycznie właściwą kategorią dla dowolnego włączenia między przestrzeniami różnych wymiarów. Odłożenie stratnego odczytu jest zasadą inżynierską, nie ogólnym twierdzeniem „quotients ramify, inclusions don't”.

### Zera i kontury: co właściwie liczy całka?

Dla gładkiego pola \(f:\mathbb R^2\to\mathbb C\), niezerowego na konturze, całka

\[
\frac{1}{2\pi i}\oint\frac{df}{f}
\]

mierzy nawinięcie obrazu konturu wokół zera. Przy izolowanych regularnych zerach wewnątrz jest sumą ich **znakowanych indeksów**. Równość z liczbą zer minus bieguny, liczonych dodatnimi krotnościami, wymaga dodatkowo struktury meromorficznej. Obraz MRI nie jest ogólnie funkcją holomorficzną współrzędnych przestrzennych.

Kontrprzykład: \(f(z)=\bar z\) ma jedno zero, lecz indeks \(-1\), a nie \(+1\). Z kolei \(f(z)=z\) ma wir fazy o nawinięciu 1, choć sama mapa ma wszędzie niezerową pochodną — wir fazy nie wymusza ramifikacji mapy zespolonej. Zera poprzeczne pola zespolonego w 2D są izolowane, ale w 3D są jednowymiarowe. Stabilność wymaga regularności i kontroli zakłóceń; nie każde zero jest stabilne.

### Wielomianowy transport: trzy różne konstrukcje

**1. DFT jako ewaluacja — dokładnie, w modelu dyskretnym.**

\[
P(w)=\sum_{j=0}^{N-1}x_jw^j,\qquad
y_k=P(\omega^k),\quad\omega=e^{-2\pi i/N}.
\]

To \(N\) współczynników i \(N\) wartości. Dwuwymiarowy odpowiednik ma \(N_xN_y\) współczynników i tyle samo próbek na pełnej kracie. Macierz jest odwracalna, lecz **nie ma nadmiarowych równań**. Dowolnie zmieniony wektor \(y'\) jest DFT innego dopuszczalnego, nieograniczonego obrazu zespolonego \(x'=F^{-1}y'\). Nie da się wykryć takiego uszkodzenia bez dodatkowej wiedzy.

Jedna zmiana próbki \(y_{k_0}\) o \(\epsilon\) daje

\[
x'_j-x_j=\frac{\epsilon}{N}e^{2\pi ik_0j/N}.
\]

To zespolony mod na całym obrazie, nie lokalny uszkodzony piksel. Dla danych o odpowiedniej symetrii rzeczywistej pary modów składają się na sinusoidę. Po modułowaniu obraz wygląda jeszcze inaczej.

Jeżeli z góry wiadomo, że wielomian ma mniej niezależnych współczynników niż liczba ewaluacji, pojawia się redundancja. Wtedy algebra kodów ewaluacyjnych rzeczywiście ma zastosowanie — także nad polami nieskończonymi w modelu dokładnych błędów symboli. Szum mały, ale obecny w każdej próbce, wymaga jednak analizy stabilności numerycznej, a nie tylko odległości Hamminga.

Kontrola dodatnia: dla stopnia co najwyżej 2, siedem ewaluacji nad \(\mathbb Q\) pozwoliło jednoznacznie odtworzyć wielomian mimo dwóch dowolnie zmienionych próbek. Kontrola ujemna: zmiana jednej z ośmiu próbek pełnej DFT nadal dała w pełni spójny transformat innego obrazu.

**2. SLR — rzeczywiste wielomiany, ale w projektowaniu impulsu.**

W modelu Shinnara–Le Roux parametry Cayleya–Kleina są opisywane przez wielomiany \(A(z),B(z)\), z warunkiem

\[
|A(e^{i\theta})|^2+|B(e^{i\theta})|^2=1.
\]

Dobór impulsu można sprowadzić do projektowania tych wielomianów. Jest to poprawny i ważny fragment wklejki. Klasyczny model używa dyskretyzacji impulsów/precesji i pomija relaksację; nie wszystkie etapy fizycznego MRI są automorfizmami sfery spinorowej. Ten opis nie jest kodem korekcyjnym pomiarów obrazu. [Pauly–Le Roux–Nishimura–Macovski, 1991](https://mriquestions.com/uploads/3/4/5/7/34572113/pauly-slr.pdf), [SLfRank — założenia i wielomiany CK](https://pmc.ncbi.nlm.nih.gov/articles/PMC10234625/).

Jednorodne przesunięcie obrazu \(x(r-a)\) daje mnożnik \(e^{-2\pi ik\cdot a}\) w k-space. Dla przesunięć całkowitych na siatce jest to odpowiedni jednomian w zmiennych pierwiastków z jedności. Nie obejmuje to dowolnego ruchu, obrotu, deformacji ani ruchu zmieniającego się w trakcie zbierania linii.

Zwarte wsparcie ciągłego obrazu zapewnia, przy standardowych założeniach całkowalności, całkowite przedłużenie jego transformaty Fouriera. Nie zamienia jej w skończony wielomian; nieskończony szereg Taylora nie jest skończonym kodem RS. Jakość przybliżenia wymaga osobnego oszacowania.

**3. Residuum rekonstrukcji — test modelu, nie oryginalności danych.**

\[
r=(G-I)d
\]

jest odczytem zgodności z zadanym operatorem kalibracyjnym. Jeśli \(e\in\ker(G-I)\), to

\[
r(d+e)=r(d).
\]

Zmiana danych może więc przejść niezauważona. Z kolei szum lub niedokładna kalibracja może dać niezerowy residual bez uszkodzenia transportu. Jądro filtra może roznieść pojedyncze zaburzenie na sąsiednie pozycje — residual nie musi być deltą w miejscu pierwotnego błędu. Panel k-space z residuami jest sensownym narzędziem QC, lecz nie certyfikatem „zero wtedy i tylko wtedy, gdy wszystko było poprawne”.

Sama transformacja Fouriera, polynomiczny model impulsu i anihilujące ograniczenie rekonstrukcji są powiązane algebrą, lecz nie stanowią jednego twierdzenia o korekcji. Stan wiedzy o tych ostatnich ograniczeniach opisuje [Linear Predictability in MRI Reconstruction](https://pmc.ncbi.nlm.nih.gov/articles/PMC7971148/).

### Konduktor: zachować precyzyjny zakres

Dla skończonego abelowego rozszerzenia \(K/\mathbb Q\), przy właściwych pierwotnych charakterach Dirichleta:

\[
\zeta_K(s)=\prod_\chi L(s,\chi),\qquad |D_K|=\prod_\chi f_\chi.
\]

Konduktor jest globalnym obiektem z lokalnymi wykładnikami ramifikacji; „pierwsza nierozgałęziona” oznacza odpowiedni lokalny wykładnik zero, a nie że każdy globalny konduktor wynosi 1. Przy ramifikowanym \(p\) nie wszystkie czynniki Eulera muszą zniknąć: dla \(\mathbb Q(i)\), \(p=2\), czynnik \(L(s,\chi_{-4})\) jest równy 1, ale czynnik \(\zeta(s)\) nadal wynosi \((1-2^{-s})^{-1}\).

Ogólny lokalny czynnik Artina zależy od działania Frobeniusa na podprzestrzeni niezmienniczej względem inercji; w nieabelowym przypadku dochodzą wymiary reprezentacji. Nie jest to uniwersalna zasada „każdy stabilizator w dowolnym systemie płaci konduktor”. [Milne — Class Field Theory, conductor–discriminant formula](https://www.jmilne.org/math/CourseNotes/CFT.pdf).

Także modularny przykład wymaga efektywnej grupy \(PSL_2(\mathbb Z)\) przy mówieniu o stabilizatorach rzędu 2 i 3. Cusp nie jest kolejnym punktem wnętrza \(\mathbb H\) tego samego typu: dochodzi przy kompaktyfikacji. Nie należy używać go jako wspólnej definicji każdego artefaktu próbkowania.

## Babbage: dokładny most przez różnice, z jawną ślepą plamką

Historycznie trafna jest intencja usunięcia ręcznego przepisywania między obliczeniem a drukiem. Nieprawdziwe jest jednak „Babbage zbudował kompletną maszynę w 1822”. W 1822 ogłosił projekt; w 1832 powstał działający fragment Difference Engine No. 1. Realizacja z 1991 dotyczy części obliczeniowej **No. 2**, zaprojektowanej w latach 1847–1849; mechanizm drukujący dołączono później. Muzeum podaje ukończenie całości w 2002. [Science Museum — historia obu maszyn](https://www.sciencemuseum.org.uk/objects-and-stories/charles-babbages-difference-engines-and-science-museum).

Automatyczny druk i stereotypia miały zapobiegać klasom błędów kopiowania. Zapobieganie przepisywaniu nie oznacza uniwersalnego dekodera błędów ani gwarancji poprawności początkowych danych. Projekt i zakres drukarki opisuje [Computer History Museum — The Engines](https://www.computerhistory.org/babbage/engines).

### Anihilator i syndrom

Dla próbek wielomianu stopnia co najwyżej \(d\), na równomiernej, nieperiodycznej siatce:

\[
\Delta p(j)=p(j+1)-p(j),\qquad \Delta^{d+1}p=0.
\]

Jeśli \(y=p+e\) oraz \(H=\Delta^{d+1}\), to

\[
\boxed{s=Hy=He.}
\]

To dokładny odpowiednik anihilującego testu zgodności. Ale kolumny różnic wyliczone z tych samych danych nie są niezależnym pomiarem. Redundancja wynika z **wcześniejszego ograniczenia stopnia** przy liczbie próbek większej niż liczba współczynników.

Kontrprzykład dla \(d=2\):

\[
p(j)=j^2,\qquad \widetilde p(j)=j^2+3j+7,
\qquad \Delta^3p=\Delta^3\widetilde p=0.
\]

Druga tabela może być błędna względem zamówienia, lecz poprawna względem badanego modelu. Zera syndromu nie zapewniają tożsamości z oczekiwanym wielomianem. Potrzebne są warunki początkowe, znane wartości kontrolne lub odpowiednio ograniczony model błędów.

Dla błędu pojedynczej próbki \(e(k)=\epsilon\,\delta_{k,j}\), poprawny indeksowo wzór to

\[
(\Delta^r e)(k)=
\begin{cases}
\epsilon(-1)^{r-(j-k)}\binom r{j-k},&0\le j-k\le r,\\
0,&\text{inaczej}.
\end{cases}
\]

Stąd wachlarz współczynników Pascala rzeczywiście występuje. Dla ustalonego \(r\) zajmuje najwyżej \(r+1\) pozycji. Wiele błędów może się jednak kompensować, a błąd będący wielomianem stopnia co najwyżej \(d\) znika całkowicie w \(\Delta^{d+1}\).

Te same różnice wzmacniają szum. Dla niezależnego szumu o wariancji \(\sigma^2\) w próbkach:

\[
\operatorname{Var}[(\Delta^r\eta)(k)]
=\sigma^2\sum_{\ell=0}^r\binom r\ell^2
=\sigma^2\binom{2r}{r}.
\]

Większy residual nie oznacza zatem sam z siebie lepszego detektora: potrzebny jest próg uwzględniający szum i błąd przybliżenia. Dla tablic funkcji niewielomianowej dochodzi rzeczywista, niezerowa różnica wyższego rzędu.

### Fourier i ζ tego samego operatora różnic

Na **periodycznej** siatce \(C_N\) wprowadzamy osobno operator \(D=T-I\), gdzie \((Ty)_j=y_{j+1}\). Z przyjętą konwencją DFT:

\[
\widehat{Dy}_k=(e^{2\pi ik/N}-1)\widehat y_k,
\]
\[
L=D^*D,\qquad
\lambda_k=|e^{2\pi ik/N}-1|^2=4\sin^2(\pi k/N).
\]

W dwóch wymiarach \(L=D_x^*D_x+D_y^*D_y\). To dokładny most do użytego wcześniej Laplasjanu i ζ:

\[
\zeta_L(s)=\sum_{k=1}^{N-1}\lambda_k^{-s},
\qquad
\|Dy\|^2=\frac1N\sum_k\lambda_k|\widehat y_k|^2.
\]

Pierwszy odczyt opisuje **operator**, drugi zależy od **danych**. Dla dwóch różnych tabel na tej samej siatce ζ pozostaje identyczna. Ponadto nieperiodyczna tabela wielomianu i periodyczna siatka mają inne warunki brzegowe: \(\Delta^{d+1}\) nie anihiluje na torusie dowolnego nieperiodycznego wielomianu bez artefaktu sklejenia. Tego warunku nie wolno zgubić przy przenoszeniu rachunku.

Najkrótsza poprawna wersja wspólnej zasady:

> Zachowuj dostępny sygnał. Zadeklaruj model i jego anihilator. Residuum mierzy niezgodność z modelem; korekcja wymaga dodatkowo identyfikowalności błędu. ζ opisuje wybrany operator, nie poświadcza oryginalności danych.

## Bilans i możliwość dalszego testu

**Potwierdzone:** rozkład Fouriera po nakryciu; filtr parzystości widma; wzór ζ wstęgi; jawna wiązka Möbiusa z połowy fazy; półcałkowite mody i powyższy wzór z ζ Riemanna; odwracalność pełnej DFT; możliwość rozdzielenia aliasów dodatkowym niezależnym pomiarem; ewaluacyjny zapis DFT; polynomiczny model SLR; anihilacja wielomianów przez różnice i jej Fourierowski symbol.

**Nie potwierdzone / błędne jako ogólne zdania:** „wstęga jest 4D”, „wir MRI jest blizną Kleina”, „wrapping to integer overflow”, „ζ stałej siatki diagnozuje obraz”, „Fourier odtwarza utracone dowolne próbki”, „RS/GRAPPA gwarantują naprawę każdego uszkodzenia”, „aliasing jest ramifikacją nakrycia”, „włączenie w C usuwa brak pełnej fazy”, „pełna DFT sama jest redundantnym RS”, „zerowy residual gwarantuje brak błędu”.

Sprawdzenia są czterema perspektywami, nie czterema niezależnymi zespołami. Kod zawiera **46 testów**, w tym przypadki pozytywne i kontrolne przypadki nierozróżnialności. Rachunek na ułamkach, sumowanie modów, transformacja sygnału i anihilatory są sprawdzane osobnymi drogami. Dodatkowe 10 testów redundancji i 4 testy korektora ζ, oraz porównanie recytacji, Xiping i profili FEC opisuje [MRI_REDUNDANCY_PROFILES.md](MRI_REDUNDANCY_PROFILES.md). Wynik testów nie waliduje wszystkich historycznych i klinicznych twierdzeń w przytoczonych rozmowach.

Ocena walidacji: **wklejona całość wymaga rewizji**; ograniczone twierdzenia w tej notatce są udokumentowane wraz z założeniami. Nie ma danych skanera, ustalonego zadania klinicznego ani benchmarku, więc przewagi w dokładności, czasie i koszcie nie zostały wykazane. Audyt rozdziela źródłowe wyniki, własne rachunki i propozycje dalszych pomiarów.

Uruchomienie:

```sh
python3 -m unittest discover -s MRI -p test_mobius_fourier_readout.py -v
```

Następny uzasadniony eksperyment, jeśli ma wejść do MRI: jawny fantom zespolony, operator akwizycji i szumu, zadana mapa fazy, kontrolowane podpróbkowanie; porównanie pełnego zespolonego odczytu, odczytu modułu, podniesienia z dodatkowym kodowaniem i odczytu spektralnego właściwego operatora. Raportować błąd fazy, amplitudy, wrap count oraz niepewność — nie sam wygląd obrazu. Tego eksperymentu klinicznego ani rekonstrukcji danych skanera w tym audycie nie wykonano.
