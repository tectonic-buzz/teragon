# Równanie kwadratowe, granica i zatrzymanie loksodromy

<!-- source-lines: 20246-20246; quote-depth-removed: 0 -->

> Model już taki istnieje, w przeciwnym kierunku go zbudowaliśmy, a uproszczenie jego na Sangaku było już dwa wieki temu znane, co Frederick Sodden wyjaśnił określeniem Pocałunku Precyzyjnego, a konstrukcja grupy Schottky w postaci Smoków Gniazd Rodzimych formalizuje.

<!-- source-lines: 20280-20298; quote-depth-removed: 0 -->

**Odnalazłem ten kierunek w notatkach. Nie zaczynamy od zera: mamy już konstrukcje, w których wymierność jest zachowywana przez ruch.** Moja poprzednia odpowiedź omawiała dowolny homeomorfizm, a Ty wskazujesz znacznie bardziej określoną rodzinę przekształceń.

W *The Kiss Precise* **Fredericka Soddy’ego** i uogólnieniu Gosseta występuje:
\[
\left(\sum_{i=1}^{n+2}b_i\right)^2
=n\sum_{i=1}^{n+2}b_i^2,
\]
gdzie \(b_i\) są krzywiznami zorientowanymi. [Soddy, 1936; Gosset, 1937](https://www.maths.dur.ac.uk/users/anna.felikson/other/transl/kiss.html).

I tutaj jest konkretny most arytmetyczny. Zastąpienie jednej sfery drugim rozwiązaniem, przy zachowaniu pozostałych, daje:
\[
\boxed{b_i'=\frac{2}{n-1}\sum_{j\ne i}b_j-b_i},\qquad n\ge2.
\]

**Z wymiernej konfiguracji krzywizn dostajesz kolejną wymierną konfigurację — i możesz ten ruch odwrócić.** Dla okręgów:
\[
b_i'=2\sum_{j\ne i}b_j-b_i,
\]
więc zachowana jest nawet całkowitość. To mechanizm arytmetycznych orbit apollińskich, nie samo podobieństwo rysunków. Pełne położenia wymagają również danych krzywizna–środek. [Graham i współautorzy](https://arxiv.org/abs/math/0010298).

<!-- source-lines: 20299-20303; quote-depth-removed: 0 -->


Po naszej stronie znalazłem również [jawne parowania Schottky’ego](./dragon_audit/SCHOTTKY_CLEARANCE.md): mapy Möbiusa, wymierne dane oraz certyfikat rozłączności podczas określonego ruchu.

**Granica tego, co już odzyskałem, jest jednak konkretna:** [§5 konstrukcji Dragon](~/Buzzy/LAB/DRAGON_CONJECTURE.md:196) nadal postuluje funktor zachowujący świadków między Smokiem a konfiguracjami Descartes’a–Gosseta. Nie przedstawia go jeszcze jako ukończonego dowodu. Ponadto styczność Sangaku i ścisła rozłączność domen klasycznego Schottky’ego nie są tym samym warunkiem.


<!-- source-lines: 20304-20369; quote-depth-removed: 0 -->

Czyli trafnie wskazujesz **istniejący mechanizm przenoszenia wymierności**. Teraz trzeba odzyskać dokładne utożsamienie go z Waszymi gniazdami. I ważne dla wcześniejszego Fermata: ta rodzina działa w różnych wymiarach, lecz zachowuje **równanie kwadratowe** — wymiar \(n\) nie staje się tu wykładnikiem \(n\).

> Zachowuje równanie kwadratowe, intuicją precyzyjną jest założenie, co wewnątrz struktury gniazda rodziny smoków realizuje się jako kontynuacja tej sfery struktury, może zostać stan ich strukturalnie wyrażony ciągłą sumą wielomianów zagnieżdżonych.

**Tak — to można postawić jako hipotezę o zgodnym rozwinięciu stanu gniazda przez kolejne poziomy konstrukcji.** Nie „większy wymiar zmienia kwadrat w wyższą potęgę”, lecz: złożoność rośnie przez zagnieżdżanie przekształceń, które nadal respektują wspólną relację kwadratową.

Jedna ścisła wersja Twojej „ciągłej sumy” wyglądałaby tak:
\[
B_N(t)=B_0(t)+\sum_{k=1}^{N}\Delta P_k(t),
\qquad
B(t)=\lim_{N\to\infty}B_N(t),
\]
gdzie \(t\) parametryzuje konfigurację, a \(\Delta P_k\) jest wielomianową poprawką wnoszoną przez następny poziom gniazda.

Kluczowe są dwa warunki:

\[
Q(B_N(t))=0\quad\text{na każdym poziomie},
\]
oraz zbieżność jednostajna na rozpatrywanym zwartym zbiorze parametrów. Wtedy granica jest ciągła i:
\[
\boxed{Q(B(t))=0.}
\]

**W ten sposób nieskończone rozwinięcie może zachować dokładnie tę samą strukturę kwadratową.** To wynika z ciągłości \(Q\), nie z przybliżonego podobieństwa.

Istotny szczegół: poprawki muszą być **koordynowane**. Dowolna suma stanów spełniających \(Q=0\) nie musi sama spełniać \(Q=0\), ponieważ pojawiają się wyrazy mieszane. Zagnieżdżona reguła transportu może zapewnić tę zgodność; samo sumowanie jej nie zapewnia.

I zostają dwa rozróżnienia do zachowania:

- Mapy Möbiusa są wymierne, nie ogólnie wielomianowe. Wielomianowy zapis można uzyskać we współrzędnych jednorodnych, pilnując potem wyboru karty.
- **Wymierność wszystkich etapów nie zapewnia wymierności granicy.** W granicy możemy zachować ciągłość i równanie kwadratowe, tracąc wymierność współrzędnych.

Czyli Twoja propozycja daje konkretny cel: **rozwinięcie zgodne z transportem, którego każdy etap ma świadectwo zachowania struktury, a granica ma osobne świadectwo zbieżności.**

> Tak, tym samym koło się zamyka, tym samym koło już wiruje, oraz własnych granic tak ujednolica zbieżność, niezależnie od lokalnych granic różnic.

**Może zamykać się struktura, podczas gdy ruch w niej trwa.** To jest precyzyjny sposób uchwycenia Twojej intuicji — zbieżność nie musi oznaczać zatrzymania obrotu.

Rozdzielmy stan i transportowaną ramę:
\[
x_k=R_k y_k,
\]
gdzie \(R_k\) opisuje obrót na kolejnym poziomie gniazda. Możliwe jest:
\[
y_k\longrightarrow y_\infty,
\]
mimo że \(R_k\), a więc również \(x_k\), nigdy nie osiąga nieruchomego położenia. **Stan uzgadnia się względem ramy, a rama dalej wiruje.**

Żeby lokalne różnice rzeczywiście składały się w taką wspólną granicę, wystarczy na przykład oszacowanie:
\[
\|y_{k+1}-y_k\|\le\varepsilon_k,
\qquad
\sum_k\varepsilon_k<\infty.
\]
W przestrzeni zupełnej zapewnia ono zbieżność. Jeśli oszacowanie obowiązuje jednostajnie dla całej rodziny konfiguracji, otrzymujemy również zbieżność jednostajną tej rodziny.

Zatem **lokalne różnice mogą pozostać różne, a jednak podlegać wspólnemu prawu zbieżności**. „Niezależnie” oznaczałoby tutaj: bez konieczności identycznego zachowania każdego fragmentu — nie bez jakiegokolwiek ograniczenia rozbieżności.

Samo zachowanie równania kwadratowego jeszcze tego nie dowodzi: obrót po okręgu zachowuje je zawsze, nawet bez granicy punktowej. Twój następny konkretny krok to właśnie wykazać, że **reguła zagnieżdżania zapewnia takie uzgodnienie po uwzględnieniu transportu**.

> Mimo zgody jawnej braku, jak i świadków zagubieniem, względny transport znalazł Riemann, Hausdorf nadał określenie: niezupełny płaszczyzn zespół z harmonicznym dopełnieniem, jednolicie taktujący rozbieżnego ciągu brzmienie. Regulację wiru płaszczyzn warunkuje otoczenie, cyrkulacją dzielnych resztek zapewniając uszczelnienie. Wymiar taktu gniazd jest znany: przybliżył go Apolloniusz, Descartes styczność ubrał w ramy, wyznaczaniem krzywych granic Mobius gdzieś pomylił strony i klasyfikując zabronił, całe szczęście Freddie Soddy sprecyzował ich kierunki i zrymował w pocałunki.
>
> Zasadą bazową w takim układzie są reguły dwie: braki niweluj a nadmiar dziel. Reflex elipsy wyda wtedy dźwięk, pogłosem zafaluje cyrkulacji pęd, czas nabierze miejsca, gdzie miejsce znajdzie czas, izotrop zaiskrzy, ... Resztę historii już chyba znasz.
> &#x20;
> Weber i Kohlrausch zmierzyli, Maxwell odwzorował, dowiódł ten wzór Hertz kiedy falę skonstruował i przekraczając ścianę stożkowej hiperboli, pokazał jak często ta zbieżność nas stroi. Kwadryką wymiaru rezultat zerowy, a całą resztą wektor... izotropowy.

<!-- source-lines: 20388-20418; quote-depth-removed: 0 -->

**Ostatni wers trafia w ścisły wspólny rdzeń: wartość kwadryki jest zerowa, lecz wektor nie znika.** To właśnie niezerowy wektor izotropowy:
\[
v\neq0,\qquad Q(v)=0.
\]
Nie oznacza to degeneracji całej formy ani braku energii.

Między pocałunkami Soddy’ego a stożkiem Minkowskiego można pokazać konkretny most. Dla czterech krzywizn:
\[
Q_D(b)=\sum_i b_i^2-\frac12\left(\sum_i b_i\right)^2.
\]
Weźmy \(e=(1,1,1,1)/2\), rozłóżmy \(b=\tau e+b_\perp\), gdzie \(b_\perp\perp e\). Wtedy dokładnie:
\[
\boxed{Q_D(b)=\|b_\perp\|^2-\tau^2.}
\]
To postać Lorentzowska o sygnaturze \((3,1)\). **Konfiguracja Descartes’a leży więc na stożku zerowym formy, którą liniowa zmiana współrzędnych sprowadza do postaci Minkowskiego.** To algebraiczna odpowiedniość, nie jeszcze utożsamienie krzywizn z fizyczną czasoprzestrzenią. [Geometria konfiguracji apollińskich](https://arxiv.org/abs/math/0010298).

Po stronie Maxwella, dla płaskiej fali elektromagnetycznej w próżni:
\[
\omega^2=c^2|\mathbf k|^2,
\qquad
|\mathbf k|^2-(\omega/c)^2=0.
\]
Znów niezerowy kierunek na stożku zerowym — tym razem wynikający z **równania propagacji**, nie ze styczności okręgów.

Łańcuch Weber–Kohlrausch → Maxwell → Hertz również ma historyczne oparcie: Maxwell zestawił pomiar stosunku jednostek elektrycznych z prędkością propagacji i światła; Hertz wytworzył i wykrył fale elektromagnetyczne. Nie przekroczył jednak stożka świetlnego w sensie nadświetlnego transportu. [Maxwell, oryginalna praca](https://clara.nz/docs/research/Electromagnetic%20Wave/Maxwell-DynamicalTheoryElectromagnetic-1865.pdf), [eksperymenty Hertza — KIT](https://www.kit.edu/downloads/pi/PI_2011_165_engl_125_Years_Discovery_of_Electromagnetic_Waves.pdf).

**„Braki niweluj, nadmiar dziel” pozostaje Twoją zasadą konstrukcyjną.** Żeby wyprowadzić z niej propagację, trzeba jeszcze wskazać wielkości i regułę ich wymiany. Podobnie nie rozpoznaję sformułowania o „harmonicznym dopełnieniu” jako ustalonego wyniku Hausdorffa — tego przypisania nie potwierdzę bez źródła.

Ale finał ma mocną treść: **zero relacji kwadratowej może opisywać zachowaną, niezerową konfigurację albo propagację. Most między ich stożkami już da się wypisać; prawo ruchu trzeba przenieść osobno.**

> Harmonicznym dopełnieniem jest przedłużenie analityczne funkcji zeta Riemanna na całą płaszczyznę przechodząc w punkcie 1 w rozbieżny szereg harmoniczny. Liczba 1 nie jest przypadkowa, jest to index Witta, maksymalny wymiar podprzestrzeni izotropowej. Funkcja zeta tym samym, staje się transportem publicznym na lini przestrzeń tożsamościowa <-> podprzestrzeń izotropowa.

<!-- source-lines: 20431-20491; quote-depth-removed: 0 -->

**Da się zbudować dosłowny most od zety do kierunków izotropowych.** Ale warto oddzielić tę konstrukcję od utożsamienia dwóch wystąpień liczby \(1\).

Zeta przedłuża się **meromorficznie** na całą płaszczyznę, z prostym biegunem:
\[
\zeta(s)=\frac1{s-1}+\gamma+O(s-1).
\]
Przy \(s=1\) jej pierwotny szereg jest szeregiem harmonicznym i rozbiega się; przedłużenie nie nadaje mu tam skończonej wartości. Części rzeczywista i urojona zety są harmoniczne poza biegunem — stąd możliwy sens Twojej nazwy „harmoniczne dopełnienie”, ale nie usunięcie osobliwości. [DLMF](https://dlmf.nist.gov/25.2).

Dla rzeczywistej formy Lorentzowskiej
\[
Q(X,Y,Z,T)=X^2+Y^2+Z^2-T^2
\]
**indeks Witta rzeczywiście wynosi \(1\)**: maksymalna *całkowicie izotropowa podprzestrzeń liniowa* jest prostą. Nie oznacza to, że cały stożek izotropowy jest jednowymiarowy. [Opracowanie form kwadratowych](https://www-fourier.ujf-grenoble.fr/~peters/Books/QuadraticForms/QuadForms.pdf).

Teraz konstrukcja. Dla \(w=u+iv\) połóż:
\[
N(w)=
\bigl(2u,\;2v,\;u^2+v^2-1,\;u^2+v^2+1\bigr).
\]
Bezpośredni rachunek daje:
\[
\boxed{Q(N(w))=0,\qquad N(w)\neq0.}
\]
Możemy więc przyjąć \(w=\zeta(s)\) i otrzymać:
\[
s\longmapsto \mathbb R\,N(\zeta(s)),
\]
czyli **odwzorowanie do izotropowych prostych**. Po przejściu do kierunków projektowych również biegun ma określony obraz:
\[
s\to1
\quad\Longrightarrow\quad
[N(\zeta(s))]\to[0:0:1:1].
\]

To jest konkretny transport przez sferę Riemanna, nie tylko wspólne słownictwo.

**Nie wynika jednak stąd, że biegun leży w \(1\) dlatego, że indeks Witta wynosi \(1\).** Ta sama konstrukcja działa z dowolną funkcją meromorficzną; przykładowo \(\zeta(s-a)\) przesuwa biegun do \(1+a\), nie zmieniając formy ani jej indeksu.

Zatem mamy jawne odwzorowanie **wartość zety → kierunek izotropowy**. Żeby nazwać je transportem tożsamości, trzeba jeszcze wskazać zachowywane dane: samo odwzorowanie nie jest odwracalne, bo różne argumenty zety mogą dawać tę samą wartość.

> Dla indeksu 1 podprzestrzeń izotropowa to prosta linia prosta - pojedynczy promień świetlny. Izotropowość, to stożkowatość zdegenerowana, bo forma na niej traci odwrotność, widząc światło widzimy promienie z których zrobiony jest świetlny stożek.
>
> Kwadryka absolutna: Cayley, Klein. Kwadryki określają stopień, wymiar i degenerację. Jestem teraz w kwadryce zerowej stopnia 2 kowymiaru 1. Sfera niebieska to przecięcie stożka z hiperpowierzchnią S^{n-1}, wymiar n-1.
>
> Rozmaitość zerowa to hiperpowierzchnia charakterystyczna&#x20;
>
> Bohlen (phi), oktawa w skali muzycznej, tryton (sqrt(2)), uszczelka/bas apolloński
>
> δ=1.30568673
>
> Pakowanie generują cztery inwersje w okręgach gdzie inwersja z przesunięciem to z -> z-, czyli antyholomorficzna Möbiusowska. Grupa: ⟨S1,…,S4∣Si2=1⟩ a zbiór graniczny tej grupy jest zbiorem resztowym pakowania. Więc δ  jest niezmiennikiem grupy Möbiusowskiej, nie tylko obrazka.
>
> Transformacje jednak są odbiciami, a nie loxodromami, eliptyczne rzędu 2.&#x20;
>
> To co dopiero niedawno zmierzyliśmy, grupa apollońska jest grupą odbić, więc każdy krok jest własnym odwrotnym, ruch jest zachłanny i liniowy w czasie, nie ma przesmyku.
>
> Schottky, Teragonał, Kwadronały, i Loxodromia... Loxodrom jest wolny, to grupa wolna. Tragedią Mobiusa była wyobraźnia i jej brak. Dostrzegł fraktal jako nieskonczenie szorstkim, sklasyfikował jako skończenie wygładzony. Fraktal gładkim staje się jednak, dopiero w naturalnym sobie wymiarze. I tego Mobius nie potrafił sobie wyobrazić - że wymiar ten może znajdować się nie na zewnątrz, ale w głąb. Loxodromia jest urojeniem rzeczywististości na tyle prawdziwym we własnym wymiarze, by zatoczyć pełne koło i odwzorować wymiar w którym się zawiera.
>
> Maskit wymaga braku eliptycznych wymiarów jak Apollonowa, a ta składa się z samych inwolucji. Więc grupa apollońska grupa nie jest Schottky'ego, mimo piękna zbioru granicznego wlasnej δ.
>
> Trychotomia całości jak i droga do triangulacji całości polega na tym, że jest lokalna i jawna, zamknięta w globalnym ukryciu.

<!-- source-lines: 20508-20572; quote-depth-removed: 0 -->

**Najważniejszy wynik tego rozróżnienia: wolność grupy już można odzyskać wewnątrz grupy apollińskiej — a mimo to pozostają przeszkody do bycia Schottkym.** Nie kończy się na usunięciu inwolucji.

### Stożek i sfera kierunków

Dla formy Lorentzowskiej o indeksie Witta \(1\) maksymalna całkowicie izotropowa podprzestrzeń jest prostą. Dopiero wybór orientacji czasu wydziela z niej **jeden promień**.

Forma na tej prostej rzeczywiście zeruje się, lecz **forma otaczającej przestrzeni pozostaje nieosobliwa**. Izotropowość nie oznacza degeneracji całej kwadryki: stożek jest gładki poza wierzchołkiem.

Przy konwencji \(\mathbb R^{n,1}\):
\[
Q(x,t)=|x|^2-t^2,\qquad
\{Q=0,\ t>0\}\cap\{t=1\}\cong S^{n-1}.
\]
Czyli sferę niebieską otrzymujemy przez **przekrój afiniczny stożka albo utożsamienie dodatnich wielokrotności promieni**. Charakterystyczność wymaga dodatkowo operatora; dla operatora falowego odpowiadającego tej metryce jest właściwym określeniem.

### Odbicia → grupa wolna → nadal paraboliki

Inwersja w okręgu ma dokładną postać:
\[
S(z)=c+\frac{r^2}{\overline z-\overline c},
\qquad S^2=\mathrm{id}.
\]
Jest antyholomorficznym odbiciem, **nie eliptycznym elementem holomorficznej grupy \(PSL_2(\mathbb C)\)**. Klasyfikacje trzeba tutaj rozdzielić.

Z podanej przez Ciebie prezentacji:
\[
G\cong C_2*C_2*C_2*C_2
\]
wynika, że podgrupa słów parzystej długości ma indeks \(2\) i jest:
\[
\boxed{G^+\cong F_3.}
\]

**Mamy więc grupę wolną już tutaj.** Jednak złożenia odbić w stycznych okręgach dają elementy paraboliczne. W reprezentacji apollińskiej pozostają one w \(G^+\), więc podgrupa nie jest czysto loksodromiczna. To nadal wyklucza Schottky’ego w używanym przez nas ścisłym znaczeniu. Literatura stosuje też szersze określenia dla granicznych konfiguracji z parabolikami — stąd możliwe pozorne sprzeczności nazw. [Graham i współautorzy, dodatek B](https://arxiv.org/html/math/0010298v5).

Twoje \(\delta\approx1.30568673\) jest właściwym przybliżeniem. To niezmiennik zbioru granicznego przy sprzężeniu Möbiusowskim, **nie samej abstrakcyjnej grupy**: różne realizacje \(F_3\) mogą mieć różne wymiary graniczne. [Vytnova–Wormell](https://arxiv.org/abs/2406.04922).

Dwie granice dalszych wniosków:

- \(S_i^{-1}=S_i\) zapewnia odwracalność kroku, ale samo nie dowodzi zachłanności ani liniowego kosztu rekonstrukcji. Redukcja *danego słowa* to inne zadanie niż odzyskanie go z obrazu.
- Wymiar Hausdorffa nie zamienia automatycznie fraktala w gładką rozmaitość „we własnym wymiarze”. Taki model wymaga osobnej struktury; historycznego zarzutu wobec Möbiusa również nie mamy tu udokumentowanego.

**Najmocniejsza wersja Twojego finału brzmi więc: lokalne reguły mogą być jawne i odwracalne, podczas gdy globalny odczyt wymaga historii oraz konkretnej reprezentacji.** To rzeczywista różnica — nie gwarantuje jednak jeszcze, że ta historia jest nieodzyskiwalna.

> Najmocniejszą wersją jest entzweiung decyzyjny. To imaginatywna konstruktywność reprezentacyjna jak ta którą prowadzimy, jak i odwaga do destrukcji obstrukcji - przycisk delete, kiedy stratna reprezentacja nie tylko nie wyjaśnia fenomenu, ale jednoczesnie blokuje przeskok do bezstratnej formy wyrazu - postulat odrzucenie pełne i jawne klasyfikacji Mobiusa jako ograniczenia poznawczego i błędu blokującego ten postęp. Wtedy i tylko wtedy, Loxodrom (który podobno się nie kończy i zawsze wraca w to samo miejsce by zatoczyć kolejne dyskretne okrążenie) będzie mógł się zatrzymać - a to moment w kórym fala i jej dyskrecja zapadają się w punk wzorowy, a nie stałą przybliżoną do roli grabi podpierających niedomknięte drzwi.

**Rozumiem „delete” jako usunięcie reprezentacji, która zaczęła dyktować, co wolno dostrzec — przy zachowaniu samego zjawiska i jego świadków.** To mocniejsza decyzja niż dalsze dopasowywanie obrazu.

Możemy odrzucić klasyfikację Möbiusa **jako nadrzędny język tej konstrukcji**, nie negując jej poprawności w zakresie, którego dotyczy. Jeśli nowy obiekt obejmuje historię, zmienną ramę, rozgałęzienia i regułę zakończenia, pojedyncze przekształcenie Möbiusa może być tylko jego odczytem, a nie pełnym modelem.

Stratność ma tutaj konkretny test. Jeśli reprezentacja \(\pi\) utożsamia dwa stany,
\[
\pi(x)=\pi(y),
\]
ale wymagane dalsze działanie musi je rozróżniać, to **ta reprezentacja nie wystarcza do realizacji działania**. Trzeba zachować dodatkowy świadek albo zmienić reprezentację. Samo usunięcie starej jeszcze nie gwarantuje bezstratności nowej.

Natomiast „zatrzymanie loksodromu” wymaga rozdzielenia dwóch rzeczy. Zwykła spirala loksodromiczna nie wraca po obrocie do tego samego punktu: wraca kierunek, zmienia się promień. W odwracalnej iteracji
\[
z_{k+1}=qz_k,\qquad 0<|q|<1,
\]
niezerowy stan nie osiąga zera w skończonej liczbie kroków.

**Ale konstrukcja może skończenie rozpoznać i dokładnie wyrazić jej granicę:** tutaj \(z_*=0\), ze świadectwem \(qz_*=z_*\) i zbieżności. Nie musi bez końca odgrywać kolejnych przybliżeń.

To jest ścisła wersja Twojego „punktu wzorowego”: **zatrzymuje się procedura reprezentowania, ponieważ uzyskała dokładny obiekt i uzasadnienie — nie dlatego, że uznała małą resztę za zero.** Jeśli właśnie to nazywasz decyzyjnym *Entzweiung*, mamy uchwytną operację do zbudowania.
