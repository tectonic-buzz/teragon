# Uwagi Kimi: zakres przyjętych sprawdzeń

Materiały otrzymane 2026-09-09: załącznik zaczynający się od „Three verifications…” oraz wklejony „Verification pass over the pancake”. **Poniżej kontrola wybranych twierdzeń, nie akceptacja całych tekstów jako certyfikatu. MRI pozostaje odrębnym eksperymentem.**

## Przyjęte: dokładny przykład nad F₇

Dla E: y²=x³+x+1 wyliczenie wszystkich par daje punkty afiniczne:

\[
(0,1),\ (0,6),\ (2,2),\ (2,5).
\]

Z punktem w nieskończoności #E(F₇)=5, a₇=3. Wyróżnik krzywej jest niezerowy modulo 7. Zatem:

\[
Z(E,t)=\frac{1-3t+7t^2}{(1-t)(1-7t)},\qquad
t_\pm=\frac{3\pm i\sqrt{19}}{14},\qquad |t_\pm|^2=\frac17.
\]

Po t=7⁻ˢ zera leżą na Re(s)=1/2, okresowo w kierunku urojonym. Twierdzenie dotyczy zety krzywej nad ciałem skończonym, nie odtworzenia danych MRI ani zety Riemanna. W konwencji det(I−tFrob) zera t są **odwrotnościami** wartości własnych Frobeniusa. Tło: [Milne, *Elliptic Curves*, IV §9](https://www.jmilne.org/math/Books/EC2.pdf).

## Nieprzyjęte: zastąpienie ciała cyklotomicznego kwadratowym

W załączniku napisano, że nieregularność p jest równoważna podzielności liczby klas podciała kwadratowego przez p. To nie jest kryterium Kummera. Właściwe ciało to **Q(ζ_p)**. [Milne, *Algebraic Number Theory*, „Class numbers of cyclotomic fields”, s. 101](https://www.jmilne.org/math/CourseNotes/ANTc.pdf).

Kontrprzykład: 37 dzieli licznik B₃₂=−7709321041217/510, ale h(Q(√37))=1. To ostatnie można sprawdzić krótko: granica Minkowskiego wynosi √37/2<4, więc wystarczą ideały normy 2 i 3; 2 jest inertna, zaś rozszczepione ideały nad 3 są główne, bo norma (5+√37)/2 wynosi −3. Kryterium nieregularności nie przenosi się więc na podciało kwadratowe.

Nieregularność nie znaczy też „więcej rozgałęzionych miejsc”: w Q(ζ_p)/Q ramifikuje wyłącznie p, zarówno dla pierwszych regularnych, jak i nieregularnych. Kwestia grupy klas jest innym odczytem.

## Nieprzyjęte: wzór na wyróżnik bez usunięcia kwadratów

Formuła D_K=d dla d≡1 mod 4 i D_K=4d w przeciwnym razie wymaga **bezkwadratowego d**, nie dowolnego wyróżnika wielomianu D. Przykład: X²−5 ma D=20, a ciało Q(√5) ma D_K=5, nie 80. Ta korekta już obowiązuje w [audycie wyróżnika, §3](DISCRIMINANT_AND_OSTOMACHION.md#3-wielomian-rząd-i-ciało--trzy-różne-obiekty); nie cofamy jej na podstawie ogólnego „verified”.

## Znaczenie dla MRI

Żadna z tych tożsamości nie dostarcza brakujących próbek ani nie stanowi testu rekonstrukcji. W [osobnym eksperymencie obrazowania](MRI_END_TO_END.md) ζ jest jawnie zdefiniowanym odczytem danych albo operatora pomiaru. O powodzeniu rozstrzygają tam odzysk bajtów, błąd obrazu, negatywne kontrole i rzeczywisty koszt redundancji.

Pozostałych historycznych, topologicznych i asymptotycznych zdań w obu materiałach nie oznaczamy tym wpisem jako w pełni zweryfikowanych.

## Kolejna recenzja: EPI, „sześć świateł” i Heine–Borel

Źródło: załącznik `f4e303b3-0499-4ec4-8032-d25e5ba658d2/pasted-text.txt`, zaczynający się od „Uściślone. Przeszedłem wszystkie trzy dokumenty…”. Sprawdzono wskazówki mające wpływ na dalszą metodę; nie odtworzono niezałączonych oryginałów dokumentów 2 i 3 ani wewnętrznych wyników membrany. Ogólne „wszystko czyste” nie jest potwierdzone.

### EPI: współczynniki poprawne, uzasadnienie topologiczne nadal nie

Rachunek \((1\pm e^{i\phi})/2\) powtarza wynik naszych testów. Nie dowodzi utożsamienia akwizycji z ilorazem torusa. Okresy decydują, czy podana mapa jest wolną inwolucją; sam półkąt nie dowodzi spinowej monodromii, bo pełny operator jest 2π-okresowy. Oba kosety parzystości dają w odwrotnej DFT dwie lokalizacje, nie po jednej. Poprawiony opis i zabezpieczenie jawnej kalibracji są w [raporcie EPI, §4–5](MRI_EPI_PHASE_AND_OSTOMACHION.md).

### Lapidus–Maier: dobry trop, węższe twierdzenie

Równoważność z niezerowaniem ζ na Re(s)=D dotyczy określonego problemu odwrotnego: czy zadany drugi człon asymptotyki zliczania częstości wymusza mierzalność Minkowskiego struny. Nie jest ogólnym jednoznacznym odtworzeniem całej geometrii ze „spektrum”. Wyjątek D=1/2 wynika z istnienia zer ζ na tej prostej, nie z wykazania, że wszystkie takie struny są samodualne. [Lapidus, §6, tw. 6.2–6.3 i wniosek 6.4](https://arxiv.org/html/1505.01548).

Dla standardowej struny Cantora wymiary zespolone to \(\log 2/\log 3+2\pi i k/\log 3\). Zapis „log₂2/log₃3” w załączniku dawałby 1, a nie wymiar Cantora. Pionowe arytmetyczne szeregi biegunów wymagają też odpowiedniej struktury kratowej; nie wszystkie samopodobne struny mają identyczną okresowość.

### Status 78557: aktualizacja z załącznika jest fałszywa

Nie dowiedziono w 2016, że 78557 jest najmniejszą liczbą Sierpińskiego. Wyeliminowano wtedy k=10223. Komunikat PrimeGrid z marca 2026 nadal podaje pięciu mniejszych nierozstrzygniętych kandydatów: 21181, 22699, 24737, 55459 i 67607. [PrimeGrid — aktualizacja projektu](https://www.primegrid.com/forum_thread.php?id=13913), [ogłoszenie wyniku z 2016](https://www.primegrid.com/download/SOB-31172165.pdf).

### Siatka konturu: użyteczna, ale ograniczenie pochodnej musi obejmować właściwy obszar

Z samych \(|f|\ge m\), \(|f'|\le M\) na konturze nie wynika dwustronna rurka bezzerowa o promieniu m/(2M). Kontrprzykład całkowity:

\[
f(z)=1+z^{16}/16,\quad |z|=1,\quad m=15/16,\quad M=1.
\]

Zero \(2^{1/4}e^{i\pi/16}\) leży w odległości około 0,1892 od konturu, mniejszej niż proponowane 15/32. Poprawne założenie: f jest holomorficzna w otoczeniu rurki o promieniu ρ, a **w całej rurce** \(|f'|\le M\). Wtedy

\[
\delta=\min\{\rho,m/(2M)\}\quad\Longrightarrow\quad |f|\ge m/2
\]

w rurce δ, przez scałkowanie pochodnej od najbliższego punktu konturu. Zakładamy M>0; stałą funkcję rozpatruje się oddzielnie.

Dla parametru długości łuku trzeba liczyć \(\operatorname{Im}(f'(\gamma(s))\gamma'(s)/f(\gamma(s)))\). Na pierwotnym konturze ograniczenie prędkości argumentu wynosi M/m, w powyższej rurce 2M/m. Bezpieczny krok z zapasem w drugim przypadku to \(h\le\pi m/(4M)\). Geometryczny krok nie certyfikuje jeszcze dostatecznej szerokości obliczonych przedziałów ani wymaganej precyzji: [FLINT — poprawność a jakość otoczeń](https://flintlib.org/doc/using.html). Nie zmieniono limitu `max_depth` w certyfikatorze konturów na podstawie tej podpowiedzi.

Niezwartość oznacza, że skończenie wiele ograniczonych pudełek nie pokryje nieograniczonego pasa. **Nie wyklucza skończonego dowodu symbolicznego obejmującego cały pas**, np. z osobnym oszacowaniem ogona. To ograniczenie konkretnego pokrycia, nie zakaz globalnego twierdzenia.

## Feedback GLM: przyjęte ulepszenia i odrzucone wzmocnienia

Źródło: załącznik `e5454f4f-0e20-4c1f-b9a3-7f93057554a1/pasted-text.txt`. Opis dotyczy głównie starszej wersji z sześcioma bajtami sum i SHA na każdą ramkę. Nowszy prototyp RS z hashem pakietu i narzutem 1,80664% już istnieje; nie cofamy go do starszego budżetu na potrzeby porównania.

**Przyjęte:** rozróżnienie trójpozycyjnej kolizji zerowego syndromu od dwóch zmian imitujących jedną; doprecyzowanie e=0; usunięcie dwuznacznego określenia 38 B jako „dolnej granicy”; wspólna definicja skończonej ζ. Poprawiono [raport benchmarku](MRI_END_TO_END.md). Wielomianowy zapis jest trafny: dla \(f(t)=\sum_{i=1}^n(x_i+1)t^i\) obecne odczyty to \(f(1),f'(1)\); błąd jest jednomianem \(et^j\). Przesunięcie +1 można usunąć po zmianie formatu referencji, bo znane stałe znikają w różnicach, ale **nie zmieniono w tej recenzji protokołu ani referencji**. Dwa odczyty wystarczają; argument „dwie niewiadome, więc dwa konieczne” nie jest ogólną dolną granicą liczby odczytów bez ograniczenia ich pojemności.

### Nowy użyteczny wskaźnik bezwymiarowy

Dla dodatniej części widma H i r>0:

\[
\kappa_\zeta=\frac{\zeta_H(-1)\zeta_H(1)}{r^2}
=\frac{\mathrm{AM}(\lambda_+)}{\mathrm{HM}(\lambda_+)}\ge1.
\]

Dowód to Cauchy–Schwarz. Równość zachodzi, gdy wszystkie dodatnie wartości własne są równe, także dla skalowanej projekcji cP. Dla diag(1,1,10⁻⁴) dokładny wynik to **11113889/5000 = 2222,7778**, sprawdzony na ułamkach; nie zmienia się po jednolitym przeskalowaniu. Nie jest to zwykłe uwarunkowanie: κ₂(H)=10000, κ₂(E)=100. Nie uwzględnia jądra, dla r=0 jest niezdefiniowany, a identyczny wskaźnik nie zapewnia jednakowej rozróżnialności fazy. Przy odczycie „ile brakuje” potrzebujemy także n, bo brak to n−r.

To zweryfikowana propozycja dodatkowej miary, **nie zmiana produkowanego JSON ani wdrożony wybór progu**. Obecny próg 10⁻¹⁰ jest jawnie bezwzględny. Względny próg usuwa wpływ jednostajnej zmiany jednostek na rząd numeryczny, ale nie dowodzi dokładnego zera. Wszystkie sumy wskaźnika muszą używać tego samego wybranego widma.

### Czego nie wolno wzmocnić

- **Różny kandydat nie oznacza różnego SHA.** Dekoder jest deterministyczny, ale nie wynika stąd bezkolizyjność jego kontroli. Nie przyjęto postulatu „każda wielobajtowa pomyłka zostanie na pewno odrzucona”. Odporność na kolizje i drugie przeciwobrazy jest własnością obliczeniową. [NIST — własności i rozróżnienie sił bezpieczeństwa](https://csrc.nist.gov/Projects/hash-functions).
- Około 2⁻ᵇ dla b-bitowego skrótu wymaga odpowiedniego modelu błędów/haszowania; nie jest uniwersalną gwarancją dla dowolnego kandydata. SHA-256 ma ogólną siłę kolizyjną 128 bitów, nie 256. Sam wybór 32 B nie dowodzi ochrony przed przeciwnikiem ani nie wymusza zmiany modelu zagrożeń; bez uwierzytelnienia spójna podmiana nadal może przejść.
- **Kierunki jądra są dostępne ze znanego E.** Nieznane są współczynniki obrazu w jądrze; sam odczyt ζ nie zawiera orientacji jądra. Kontrola negatywna w kodzie właśnie konstruuje taki kierunek, więc nie dowodzi jego niewyznaczalności.

### Budżety: zachować kanał i długość słowa

Dwie sumy modulo 65536 rzeczywiście wystarczają do korekcji jednej zmiany przy chronionych referencjach: e w [−255,255] jest jednoznaczne z pierwszej reszty, a \(|e(j-j')|\le255^2<65536\) wyklucza kolizję pozycji. Sprawdzono wszystkie **130560** niezerowe pary (j,e) z j=1…256 oraz e=−255…255; wszystkie dały różne pary syndromów. To arytmetyka lokalizatora, nie test nowego kompletnego łącza.

Nie oznacza to dzielenia przez e w pierścieniu modulo 65536: parzyste e nie ma tam odwrotności. Dekoder musi rozwiązać kongruencję z ograniczeniem j=1…256. Po usunięciu +1 również zwykłe sumy całkowite zajmowałyby **5 B (2+3)** zamiast 6 B; wariant modularny zajmuje 4 B. Każdy kandydat nadal wymaga sprawdzenia, czy poprawiony bajt mieści się w 0…255 — samo całkowite j w zakresie nie wystarcza. Obecny dekoder już sprawdza ten warunek.

Dwa chronione bajty bocznego syndromu nad GF(256) również wystarczają — taki wariant już sprawdzono w referencji RS. Jednak kod Hamminga nad GF(256) długości 257 z dwoma symbolami parzystości niesie **255**, nie 256 symboli danych. Dla 256 danych + 2 parzystości w paśmie granica kul daje \(1+258\cdot255=65791>65536\), więc taka jednobłędowa gwarancja nie jest możliwa. Trzy parzystości w paśmie mogą wystarczyć, np. przez skrócenie odpowiedniego kodu Hamminga do [259,256,≥3]; nie zaimplementowano tego dekodera.

Dwa RS(130,128) chronią dwie połowy po 128 B czterema bajtami parzystości. Nie gwarantują korekcji dwóch zmian w tej samej połowie. „Zero logiki odrzuceń” oraz „lepszy na każdej osi” nie zostały wykazane: poza promieniem dekoder może odrzucić lub źle poprawić, a integralność, ramkowanie, opóźnienie i koszt muszą być porównywane osobno. Dodatkowy FEC nadal nie odzyskuje danych, których akwizycja nie zmierzyła.
