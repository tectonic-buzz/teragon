# Loksodroma, kwadronał i równanie Fermata

<!-- source-lines: 19758-19758; quote-depth-removed: 0 -->

> Heh, a zastanawiam sie jesli chodzi o loxodrom, jaki jest wzor dokladnie?

<!-- source-lines: 19779-19822; quote-depth-removed: 0 -->

**W naszej karcie zespolonej najprostszy dokładny wzór to:**

\[
\boxed{z(t)=z_0\,e^{(a+i\omega)t}}
\qquad z_0\neq0,\quad a\neq0.
\]

Rozdziela się na:

\[
|z(t)|=|z_0|e^{at},
\qquad
\arg z(t)=\arg z_0+\omega t.
\]

Czyli **wykładnicza zmiana skali i jednostajny obrót**. W płaszczyźnie jest to spirala logarytmiczna; odwrotna projekcja stereograficzna przenosi ją na loksodromę sferyczną względem wybranych biegunów.

Na sferze, przy szerokości geograficznej \(\varphi\), rozwiniętej długości \(\lambda\) i stałym kącie \(\beta\) względem południka:

\[
\boxed{
\lambda-\lambda_0
=
\tan\beta\,
\log\!\left(
\frac{\tan(\pi/4+\varphi/2)}
     {\tan(\pi/4+\varphi_0/2)}
\right)
}
\]

Dla powyższej parametryzacji, z \(a>0\):

\[
\boxed{\tan\beta=\frac{\omega}{a}}.
\]

Stały kierunek względem południków jest właśnie definicją loksodromy. Przypadek kierunku równoleżnikowego wymaga osobnego zapisu. [GeographicLib — rhumb lines](https://geographiclib.sourceforge.io/html/RhumbSolve.1.html).

**Najkrótsze równanie ruchu:**

\[
\boxed{\dot z=(a+i\omega)z}.
\]

<!-- source-lines: 19831-19893; quote-depth-removed: 0 -->

Ważne: **\(t\) jest tu parametrem przebiegu**. Sam kształt loksodromy nie narzuca jeszcze fizycznego zegara ani szybkości jej przemierzania.

> a udalo by Ci sie na loksodromie opisac albo wpisac w niego trojkat z katem prostym tak, by pasowal co twierdzenia pitagorasa?

**Tak — i bardzo naturalnie: przyprostokątne to zmiana logarytmu skali oraz zmiana kąta.**

Mamy:
\[
z(t)=z_0e^{(a+i\omega)t}.
\]

Przechodzimy na **rozwinięte współrzędne logarytmiczne**:
\[
u=\log|z|,\qquad v=\arg z,
\]
gdzie kąta nie obcinamy po pełnym obrocie. Wtedy loksodroma staje się prostą:
\[
(u(t),v(t))=(u_0+at,\;v_0+\omega t).
\]

Dla odcinka parametru \(0\le t\le T\) wybieramy trzy wierzchołki:
\[
A=(u_0,v_0),\quad
B=(u_0+aT,v_0),\quad
C=(u_0+aT,v_0+\omega T).
\]

**Kąt przy \(B\) jest prosty, a loksodroma w tym rozwinięciu jest przeciwprostokątną \(AC\):**

\[
\boxed{
\underbrace{|AC|^2}_{\text{przebieg w karcie}}
=
\underbrace{(aT)^2}_{\text{zmiana logarytmu skali}}
+
\underbrace{(\omega T)^2}_{\text{obrót}}
}
\]

To dokładne twierdzenie Pitagorasa — nie przybliżenie.

### A na samej sferze?

Tam również mamy prostopadłe kierunki: południkowy i równoleżnikowy. Dla promienia \(R\):
\[
ds^2=(R\,d\varphi)^2+(R\cos\varphi\,d\lambda)^2.
\]

To **lokalny Pitagoras**. Co ciekawe, stały kurs loksodromy pozwala również zbudować dokładny, skończony trójkąt **składowych przebytej drogi**:
\[
N=R(\varphi_1-\varphi_0),\qquad
E=R\int_{\lambda_0}^{\lambda_1}\cos\varphi\,d\lambda
=N\tan\beta,
\]
\[
\boxed{L_{\mathrm{loksodromy}}^2=N^2+E^2}.
\]

Przy stałym kursie nierównoleżnikowym. **\(E\) jest zsumowaną składową drogi na wschód, nie odległością między końcami po jednym równoleżniku.**

Czyli możemy wpisać Pitagorasa zarówno w jej logarytmiczne rozwinięcie, jak i w bilans drogi. Trzeba tylko zachować, **co mierzą boki**.

> i co jesli kwadrat zamienic na dowolny wymiar? czy nie była by nagle dziedzina fermata w całości?

<!-- source-lines: 19911-19945; quote-depth-removed: 0 -->

**Tak — jeśli „kwadrat” zamieniamy na dowolną potęgę, trafiamy dokładnie w rodzinę równań Fermata.** Tylko rozdzielmy wymiar przestrzeni, potęgę i rodzaj dopuszczalnych liczb.

Dla naszej loksodromy w rozwiniętych współrzędnych logarytmicznych przyprostokątne były:
\[
A=aT,\qquad B=\omega T.
\]

Pitagoras daje:
\[
C^2=A^2+B^2.
\]

Możemy zastąpić go całą rodziną:
\[
\boxed{C_n^n=|A|^n+|B|^n},
\qquad
C_n=T\bigl(|a|^n+|\omega|^n\bigr)^{1/n},\quad T>0.
\]

**To jest poprawna geometria norm \(\ell^n\)** — zmieniamy sposób mierzenia długości. Dla \(n\ne2\) nie jest to już zwykła euklidesowa długość przeciwprostokątnej ani automatycznie długość na sferze.

I teraz wchodzi arytmetyka:

- **Długości rzeczywiste:** rozwiązania istnieją dla każdego \(n\), choćby \(1^n+1^n=(2^{1/n})^n\).
- **Dodatnie liczby całkowite lub wymierne:** dla całkowitego \(n>2\) takich rozwiązań nie ma — to właśnie wielkie twierdzenie Fermata. [Wiles, 1995](https://annals.math.princeton.edu/1995/141-3/p01).

Natomiast zwiększenie **liczby wymiarów** samo nie zmienia potęgi:
\[
C^2=x_1^2+\cdots+x_d^2.
\]
Możemy też zmienić oba parametry: \(C^n=\sum_{j=1}^{d}|x_j|^n\), ale przy więcej niż dwóch składnikach mamy już inne pytanie diofantyczne.

Czyli **loksodroma daje nam ciągłą rodzinę konfiguracji; Fermat pyta, czy konkretna konfiguracja może mieć wszystkie trzy długości wymierne.** Most jest konkretny — warunku wymierności sama konstrukcja geometryczna jeszcze nie dostarcza.

> Ale jest taka, ktora tak, Quadronał?

<!-- source-lines: 19957-19976; quote-depth-removed: 1 -->

**Dla potęgi drugiej — tak: można wbudować wymierność w samą konstrukcję**, zamiast sprawdzać ją dopiero na końcu.

W naszej loksodromie
\[
z(t)=z_0e^{(a+i\omega)t}
\]
wybierz:
\[
a=u^2-v^2,\qquad \omega=2uv,\qquad u>v>0.
\]
Wtedy dokładnie:
\[
a^2+\omega^2=(u^2+v^2)^2.
\]

Jeżeli \(u,v\) są wymierne, wszystkie trzy boki trójkąta **w rozwiniętej płaszczyźnie logarytmicznej**, dla \(T=1\), są wymierne. Na przykład \(u=2,v=1\) daje \(3,4,5\). To już **parametryzacja niosąca gwarancję arytmetyczną**, nie przypadkowe trafienie.

Dla wyższych potęg ta konstrukcja nie przenosi się automatycznie — właśnie warunek drugiej potęgi umożliwia powyższą tożsamość.

Natomiast **„Quadronał” nie znalazłem w przeszukanych notatkach**. To Twoja nazwa tej konstrukcji, czy konkretnego innego obiektu? Chcę uchwycić wskazany przez Ciebie mechanizm, nie przypisać mu swojego.

<!-- source-lines: 19978-19980; quote-depth-removed: 0 -->

> nie mamy
>
> kwadronał to uproszczenie najsilniejsze koła

<!-- source-lines: 19982-20003; quote-depth-removed: 1 -->

Aha — **„kwadronał” jako Twoja nazwa uproszczenia koła**, nie obiekt, którego mam szukać w notatkach.

Jest tu bardzo konkretna konstrukcja: **całe koło można opisać jednym parametrem wymiernym**:
\[
x(t)=\frac{1-t^2}{1+t^2},\qquad
y(t)=\frac{2t}{1+t^2}.
\]
Wtedy identycznie:
\[
x(t)^2+y(t)^2=1.
\]

Dla wymiernego \(t\) dostajesz wymierne współrzędne — **bez pierwiastków, bez aproksymacji, z zachowanym równaniem koła**. Każdy punkt wymierny koła poza \((-1,0)\) otrzymujesz tak; brakujący punkt odpowiada \(t=\infty\). Geometrycznie to parametryzacja przez nachylenie prostej przechodzącej przez \((-1,0)\).

Po usunięciu mianowników wraca:
\[
(u^2-v^2)^2+(2uv)^2=(u^2+v^2)^2.
\]

**To byłby precyzyjny sens bardzo mocnego uproszczenia: warunek geometryczny zostaje spełniony przez konstrukcję, a wymierność przechodzi razem z parametrem.**

Nie przypisuję jeszcze temu słowa „najsilniejsze” bez określenia, co porównujemy — ale ten mechanizm rzeczywiście dostarcza tego, czego brakowało samej loksodromie: gwarancji wymierności boków.

<!-- source-lines: 20005-20005; quote-depth-removed: 0 -->

> ograniczenie okregu loxodromii w kwadracie

<!-- source-lines: 20008-20124; quote-depth-removed: 0 -->

Aha — **kwadrat jako rama ograniczająca okrąg i przebieg loksodromii**, nie parametryzacja koła. Wcześniej poszedłem w inną konstrukcję.

W płaskiej karcie można to zapisać:
\[
\underbrace{x^2+y^2\le R^2}_{\text{dysk}}
\quad\subset\quad
\underbrace{|x|\le R,\ |y|\le R}_{\text{kwadrat}}.
\]

Dla obrazu loksodromy
\[
z(t)=Re^{(-a+i\omega)t},\qquad a>0,\ t\ge0,
\]
cały przebieg mieści się w tym dysku, a więc również w kwadracie: obrót trwa, promień maleje.

**Kwadrat daje wtedy dwa niezależne ograniczenia współrzędnych; okrąg wiąże je jednym warunkiem kwadratowym.**
\[
|x|\le R,\quad |y|\le R
\qquad\text{wobec}\qquad
x^2+y^2\le R^2.
\]

To jednak dwa różne zakresy: narożniki kwadratu leżą poza dyskiem. Zastąpienie dysku kwadratem upraszcza ograniczenie, ale dopuszcza dodatkowe punkty.

Jeżeli to nazywasz **kwadronałem**, mamy już konkretną konstrukcję. Sama rama nie wymusza jeszcze wymierności długości — określa, **gdzie przebieg może się mieścić**, nie z jakich liczb musi być zbudowany.

> bo trzeba kwadronał wpisać w loxodrom, a jesli zaszła by taka potrzeba loxodrom wpisać w kwadronał, wtedy coś bardzo ciekawego się dzieje, prawda?

**Może — szczególnie jeśli oba wpisania mają się składać w ruch.** Wcześniej potraktowałem kwadronał jako nieruchome ogrodzenie, a Ty mówisz o wzajemnym dopasowaniu.

Jeden konkretny mechanizm widać już dla
\[
z(t)=r(t)e^{i\theta(t)}.
\]
Odczyt „okrągły” daje promień \(r(t)\), natomiast odczyt kwadratowy:
\[
\boxed{\|z(t)\|_\infty
=r(t)\max\bigl(|\cos\theta(t)|,|\sin\theta(t)|\bigr).}
\]

**Jednostajny obrót loksodromii staje się w kwadratowym odczycie czterokrotnie powtarzającą się modulacją.** Czynnik zmienia się między \(1/\sqrt2\) a \(1\). Nawet przy stałym promieniu kwadratowy odczyt „oddycha”; przy spirali nakłada to oddychanie na wzrost lub kurczenie.

Możesz również przenieść kierunek na brzeg kwadratu:
\[
q(t)=
\frac{R\,e^{i\theta(t)}}
{\max(|\cos\theta(t)|,|\sin\theta(t)|)}.
\]
Wtedy ciągły obrót obiega cztery boki, przechodząc przez narożniki.

**A przy powrocie pojawia się istotna różnica:** sam punkt \(q(t)\) zachował kierunek, ale zgubił \(r(t)\). Jeżeli zachowasz również promień, odzyskasz pierwotną loksodromię dokładnie. Bez niego wiele różnych spiral daje ten sam obieg kwadratu.

To jest konkretny efekt wzajemnego przekładania reprezentacji: **modulacja odczytu oraz pytanie, co trzeba zachować, żeby powrót był pełny**. Nie utożsamiam jeszcze tego z Twoim wpisaniem kwadronału — ale tutaj rzeczywiście zaczyna się ciekawa konstrukcja, nie samo ograniczanie zasięgu.

> wiele dróg jest tutaj metodą, kwadronał zaczyna undulować, a drogi takiej wspólą naturę, różnicowaniem, do dróg wszystkich wspólnych zniwelujesz... jest to loxodesia - geodesji teragonalny przodek

**Wielość dróg jest tu częścią konstrukcji, a nie przeszkodą do usunięcia.** Tak rozumiem Twoją *loksodezję*: kwadronał dostosowuje się podczas przejścia, a porównywanie dróg pozwala uzgadniać to, co wspólnie przenoszą.

Można temu nadać konkretny zapis. Niech \(T_\gamma\) oznacza transport wzdłuż drogi \(\gamma\). Dla dwóch dróg między tymi samymi punktami, przy odwracalnych transportach:
\[
H_{\gamma_1,\gamma_2}
=T_{\gamma_2}^{-1}T_{\gamma_1}.
\]

To jest **reszta po przejściu jedną drogą i powrocie drugą**:

- jeśli \(H=\mathrm{id}\), obie drogi uzgadniają pełny transport;
- jeśli \(H\neq\mathrm{id}\), pozostaje obrót, przesunięcie fazy albo inna zmiana, którą trzeba zachować w opisie;
- mogą też uzgadniać tylko wybrany odczyt, mimo różnicy stanów wewnętrznych.

Tu „undulowanie kwadronału” może dostać rolę **zmiennej ramy odczytu**. Ale potrzebujemy jej prawa zmiany: inaczej dałoby się dopasować ramę do każdego wyniku już po fakcie.

Najważniejsze pytanie w Twoim „zniwelowaniu do wszystkich wspólnych dróg” brzmi więc: **czy lokalne uzgodnienia składają się zgodnie także po zamknięciu pętli?** Różnicowanie wzdłuż dróg daje dane lokalne; obieg sprawdza ich wspólną zgodność.

„Teragonalny przodek geodezji” zachowałbym jako Twoją nazwę kierunku: najpierw konstruujemy rodzinę dopuszczalnych transportów i ich uzgodnienia, a dopiero po określeniu metryki możemy pytać o geodezyjne.

> dałoby się dopasować ramę do każdego wyniku już po fakcie - i to jest to prawo - prawo derywacji wirowej

Rozumiem — **dopasowanie ramy jest u Ciebie operacją konstrukcyjną**, a nie czymś, co należy wykluczyć. Moje „po fakcie” mieszało dwie sytuacje: zmianę reprezentacji oraz niezależne sprawdzenie przewidywania. Do pierwszej masz pełne prawo; drugiej samo dopasowanie nie zastępuje.

Dla obracającej się ramy można zapisać konkretną wersję Twojej **derywacji wirowej**. Niech
\[
x(t)=R(t)y(t),\qquad R(t)\in SO(d),
\]
gdzie \(x\) opisuje przebieg w ramie wyjściowej, a \(y\) — w obracającej się. Wówczas:
\[
\boxed{D_t y:=\dot y+\Omega y=R^{-1}\dot x},
\qquad
\Omega=R^{-1}\dot R.
\]

Masz tutaj dwie części jednego odczytu:

- \(\dot y\): zmianę widoczną w ruchomej ramie;
- \(\Omega y\): poprawkę wynikającą z wirowania samej ramy.

**Rama może nadążać za przebiegiem, ale jej ruch pozostaje zapisany w pochodnej.** Przykładowo: obracający się wektor może w dopasowanej ramie wyglądać na nieruchomy, \(\dot y=0\), a mimo to \(D_t y=\Omega y\neq0\). Ruch nie zniknął — przeszedł do opisu transportu.

To daje ścisłą realizację części Twojego pomysłu. Sam obrót zachowuje jednak długości; jeśli kwadronał również rozciąga się i unduluje, trzeba dopuścić bardziej ogólną ramę, a jej zmianę rozdzielić na obrót i deformację.

**Dopasowywać wolno; derywacja przechowuje, jakim dopasowaniem to osiągnęliśmy.**

> I jest to model sokratejski, gdzie apagogiczność rozmaitości ad absurdum reductios reductio, w świetle prawdy jako powszechnie obowiązującej wartości poznawczej, wyznacza kierunki pierwotne i naczelne dróg wartości poznania.

**Sokratejski w sensie metody: droga poznania powstaje przez pytanie, odpowiedź i sprawdzenie konsekwencji — również konsekwencji zmiany własnej perspektywy.** Tak odczytuję Twoje zdanie.

W tym ujęciu derywacja wirowa pilnuje, żeby dostosowanie ramy nie wymazało historii rozumowania. Możesz zmienić punkt odniesienia, ale zachowujesz transport: *co zmieniłeś, co pozostało wspólne i co dzięki temu zobaczyłeś*.

Apagogia byłaby wtedy próbą obciążeniową drogi. Doprowadzasz przyjęte założenia do konsekwencji; jeśli otrzymujesz sprzeczność, masz świadectwo, że **nie mogą wszystkie obowiązywać razem**. To jeszcze nie wskazuje automatycznie, które odrzucić ani którą drogę obrać — tutaj potrzebne jest następne pytanie lub konstrukcja.

Ująłbym Twój postulat tak:

> **Drogi poznania wolno przekształcać wraz z ramą odniesienia, lecz trzeba zachować rozliczalność tych przekształceń. Sprzeczność ujawnia niezgodność założeń; prawda jest normą ich uzgadniania, nie wynikiem samego dopasowania.**

To spójny kierunek metodologiczny. Żeby wyznaczał również konkretne „kierunki naczelne”, pozostaje określić, co rozstrzyga między kilkoma drogami, które przeszły dotychczasowe próby bez sprzeczności.

> Jest to zarazem prawo ramifikacji przekształceń kontynuowanych, lub mówiąc wprost prawo spójności gradientu - w rozumieniu Poincare i Sobolewa

<!-- source-lines: 20139-20170; quote-depth-removed: 0 -->

**To wskazuje na konkretny most: lokalna zgodność różniczkowania → uzgadnianie potencjałów → kontrola rozbieżności.** „Prawo spójności gradientu” może być Twoją nazwą tej konstrukcji; nie utożsamiałbym go jeszcze z jednym gotowym twierdzeniem Poincarégo–Sobolewa.

**Po stronie Poincarégo:** dla gładkiej formy \(\alpha\), opisującej przyrosty wzdłuż dróg,
\[
d\alpha=0\quad\Longrightarrow\quad \alpha=du\ \text{lokalnie}.
\]
Na odpowiedniej dziedzinie, np. kuli, przyrosty pochodzą więc od wspólnego potencjału. To ma dowód konstrukcyjny przez całkowanie. [Lemat Poincarégo — wykład Vincenta Boucharda](https://sites.ualberta.ca/~vbouchar/MATH315/section_poincare_one.html).

Ale **lokalna zgodność może współistnieć z różnicą po pełnym obiegu**. Dokładnie przy naszym kącie:
\[
\alpha=\frac{-y\,dx+x\,dy}{x^2+y^2}
\]
jest lokalnie \(d\theta\), lecz wokół początku:
\[
\oint\alpha=2\pi.
\]
Kontynuowany kąt zachowuje nawinięcie. To przykład monodromii — nie automatycznie ramifikacji każdego przekształcenia.

**Po stronie Sobolewa:** nie musimy wymagać klasycznej gładkości; pracujemy ze słabymi pochodnymi. Na kuli \(\Omega\), dla \(u\in W^{1,p}(\Omega)\), nierówność Poincarégo daje
\[
\|u-u_\Omega\|_{L^p}
\le C_{\Omega,p}\|\nabla u\|_{L^p}.
\]
Gradient kontroluje odchylenie od wspólnego poziomu. Zastosowane do \(u-v\), oszacowanie mówi, jak bliskie są dwa potencjały po uzgodnieniu ich średnich. **Nie oznacza przy tym, że gradient musi być ciągły punktowo.** [Notatki Johna Huntera](https://www.math.ucdavis.edu/~hunter/prelim_workshop/analysis_sobolev_th.pdf).

Najściślej ująłbym więc Twój kierunek: **uzgadniaj lokalne przyrosty, zachowuj informację o obiegach, a pozostałą różnicę kontroluj normą.** Tutaj „niwelacja” dostaje zarówno konstrukcję, jak i oszacowanie.

> Z hipotezy Poincara, dowiedzionej w 2006 roku przez Grigorija Perelmana, wiemy że:
>
> > Każda n-wymiarowa rozmaitość bez brzegu, zwarta i mająca typ homotopijny n-wymiarowej hipersfery jest homeomorficzna z n-wymiarową hipersferą.
>
> A to oznacza...

<!-- source-lines: 20185-20244; quote-depth-removed: 0 -->

**…że po spełnieniu tych założeń istnieje globalny, odwracalny transport topologiczny do sfery — nie tylko lokalne podobieństwo.**

Drobne uporządkowanie: cytujesz **uogólnioną hipotezę Poincarégo**. Perelman rozwiązał przypadek \(n=3\), publikując prace w latach 2002–2003; pozostałe wymiary obejmują wcześniejsze wyniki, m.in. Smale’a i Freedmana. [Clay — historia](https://www.claymath.org/millennium/poincare-conjecture/), [opracowanie Milnora](https://www.claymath.org/library/monographs/MPPc.pdf).

Dla naszego pytania wynika z tego coś konkretnego. Jeżeli **dwie rozmaitości \(M,N\) tego samego wymiaru** spełniają te założenia, możemy wybrać:
\[
h_M:M\longrightarrow S^n,\qquad h_N:N\longrightarrow S^n
\]
i złożyć:
\[
\boxed{H=h_N^{-1}\circ h_M:M\longrightarrow N.}
\]

Wtedy **jedno odwzorowanie przenosi wszystkie drogi naraz**:
\[
\gamma\longmapsto H\circ\gamma.
\]
Zachowuje ich łączenie, odwracanie i homotopie. Nie trzeba dopasowywać każdej drogi osobno.

Można również przenieść cały ciągły potok:
\[
\boxed{\widetilde F_t=H\circ F_t\circ H^{-1}.}
\]
Prawo składania czasu zostaje zachowane. To już ścisła realizacja Twojego motywu wspólnego transportu.

**Natomiast homeomorfizm nie gwarantuje zachowania gradientów, kątów, długości ani kosztów.** Do transportu tych struktur potrzebujemy dodatkowej regularności i odpowiednio przeniesionej metryki; samo twierdzenie nie dostarcza też wyróżnionego, kanonicznego \(H\).

Czyli: **w tej klasie rozmaitości sfera może być wspólnym globalnym modelem dróg i przenoszonej dynamiki.** Pozostaje wykazać, że nasz obiekt rzeczywiście spełnia założenia — zwłaszcza ma typ homotopijny \(S^n\).

> Dokładnie, jednak definiować ich a priori nie trzeba, gdy mosty teraz dostrzegamy o których mowa była wcześniej, w kontekście Fermata, znając teraz kształt ciągłości rodzin konfiguracji, po drodze dostarczając tej wymierności warunek.
>
> Intuicyjnie, mostów takich jest nieskończenie wiele dla każdej nieskoczonej rozmaitości, droga jednak w każdej z nich kierunku, również się nie kończy, każda będąc nieskończoną częścią wspólną nieskończenie wielu rozmaitości.

**Tak — nie trzeba z góry wybierać wszystkich mostów ani metryk. Można je konstruować po drodze, razem ze świadectwem tego, co zachowują.** Wymierność może być właśnie takim dostarczanym warunkiem. Musi jednak przejść przez konstrukcję, nie tylko przez jej ciągłość.

Tutaj mamy wyjątkowo czytelny przykład. Dodatni łuk koła
\[
x^2+y^2=1
\]
możemy homeomorficznie przenieść na
\[
u^n+v^n=1
\]
przez
\[
\boxed{u=x^{2/n},\qquad v=y^{2/n}.}
\]

**Most istnieje dla każdego \(n>0\)**: ciągły, odwracalny, obejmujący cały dodatni łuk. Ale nie zachowuje automatycznie wymierności. Dla \(n=4\):
\[
(3/5,4/5)\longmapsto
\left(\sqrt{3/5},\sqrt{4/5}\right).
\]
Geometria przeszła dokładnie; współrzędne wymierne — nie. Co więcej, dla całkowitego \(n>2\) na docelowym łuku nie ma punktów o obu współrzędnych wymiernych, właśnie na mocy Fermata. [Wiles](https://annals.math.princeton.edu/1995/141-3/p01).

To precyzuje zadanie: **jakie dane arytmetyczne niesie most i w jakiej reprezentacji je zachowuje?** Możesz przenieść oznaczenia wymiernych punktów razem z nimi, ale „punkt pochodzący od wymiernego” nie oznacza jeszcze „punkt o wymiernych współrzędnych docelowych”.

Natomiast Twoją intuicję nieskończonej wspólnoty rozmaitości zostawiłbym jako hipotezę wymagającą modelu. Nieskończenie wiele punktów nie oznacza niekończącego się zasięgu drogi: okrąg jest nieskończony jako zbiór, lecz zwarty i ma skończony obwód. „Część wspólna rozmaitości” wymaga też wskazania, **jak są osadzone lub identyfikowane**.

Najmocniejszy uchwycony tutaj kierunek brzmi więc: **budować most wraz z zachowywaną strukturą — dopuszczając, że jej właściwa reprezentacja ujawni się podczas konstrukcji.**
