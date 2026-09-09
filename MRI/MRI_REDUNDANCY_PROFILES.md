# Redundancja: recytacja, Xiping i wymienny profil FEC

Stan: 2026-09-09. Uzupełnienie [audytu MRI–Fourier–Möbius](MRI_MOBIUS_FOURIER_AUDIT.md).

**Wniosek:** wzorzec recytacyjny może organizować redundantny zapis danych; wzorzec typu Xiping kontroluje zgodność z wcześniej ustaloną referencją. To różne mechanizmy. Samo dołączenie tekstu mantry nie koduje danych MRI ani nie usuwa ich niejednoznaczności.

**Zakres:** obliczenia offline na syntetycznych symbolach i propozycja interfejsu FEC. Nie wybrano częstotliwości mantry, nie wygenerowano RF ani audio, nie zmieniono sekwencji skanera. Nie zweryfikowano odporności konkretnego urządzenia na sprzężenie fazowe.

## 1. Co porównujemy?

Tradycja recytacji wedyjskiej wykorzystuje m.in. powtarzanie i określone porządki słów do zachowania tekstu i wymowy. [UNESCO — Tradition of Vedic chanting](https://ich.unesco.org/en/RL/tradition-of-vedic-chanting-00062). Układ par jaṭā-pāṭha \(ab,\ ba,\ ab\) jest opisany także w materiale [IGNCA — Rigvedic Education](https://ignca.gov.in/Asi_data/47848.pdf). W teście używamy tylko tego wzorca kolejności, nie pełnej tradycji fonetycznej i nie konkretnej mantry.

Xiping Stone Classics powstawały w latach 175–183 jako publiczny, utrwalony wzorzec tekstów do porównywania. Potwierdza to [Library of Congress, materiał National Library of China](https://www.loc.gov/item/2021667417/). Techniczny odpowiednik to chroniona referencja, nie drugi rodzaj rezonującej fali.

| Wariant | Mechanizm w naszym modelu | Co może wykryć / naprawić | Ślepa plamka |
| --- | --- | --- | --- |
| Jaṭā-inspired | powtórzenia i przeplot danych | większość poprawia pojedynczą błędną kopię symbolu | skorelowane uszkodzenie większości kopii |
| Xiping-inspired | niezależnie chroniony wzorzec | zmianę względem wcześniej ustalonej referencji | błędna lub wspólnie uszkodzona referencja |
| Kod ewaluacyjny | parytety zależne od danych | błędy w granicach odległości kodu | błędy spoza gwarancji; zły model kanału |
| Wariant łączony | FEC i osobna kontrola integralności | uzupełniające się rodzaje awarii | nie zapewnia prawdziwości pierwotnego pomiaru |

Niezależność wzorca jest **założeniem o domenie awarii**, nie skutkiem nazwania go kamieniem.

## 2. Test przy tym samym budżecie symboli

Dwie dane \(a,b\in\mathbb F_7\), sześć transmitowanych symboli.

### A. Powtórzenia

\[
C_J(a,b)=(a,b,b,a,a,b).
\]

Każdy symbol występuje trzy razy. Kod ma 49 słów i minimalną odległość Hamminga 3. Dekoder większościowy poprawia każdy pojedynczy błąd symbolu w całym bloku. Może poprawić też dwa błędy dotyczące po jednej kopii różnych danych, ale nie dowolną parę błędów.

**Kontrola okresowa:** dla \((a,b)=(2,5)\), zakłócenie zwiększające symbol o 1 modulo 7 w chwilach \(t=0,3\) uszkadza dwie kopie \(a\). Dekoder zwraca **\((3,5)\)**. Rytm sam nie chroni przed korelacją. Jednostka czasu jest umowna; nie jest to pomiar zakłóceń MRI.

### B. Kontrolny kod wielomianowy

\[
C_E(a,b)=\big(a+bt\pmod7\big)_{t=0}^{5}.
\]

To kod ewaluacyjny \([6,2,5]_7\): te same 49 wiadomości, sześć symboli tego samego alfabetu, ale minimalna odległość wynosi 5. Różnica dwóch różnych wielomianów liniowych ma najwyżej jeden pierwiastek, więc słowa różnią się na co najmniej pięciu pozycjach.

Dekodowanie do odległości 2 poprawia **dowolne dwa błędy symboli**, także poprzedni przykład okresowy. Gwarancja nie obejmuje dowolnie silnego zakłócenia okresowego: jeśli zmieni więcej symboli, może przestać obowiązywać.

Sprawdzono wyczerpująco:

- 49 wiadomości i wszystkie 1764 pojedyncze zmiany symbolu dla powtórzeń;
- wszystkie \(49\cdot\binom62\cdot6^2=26\,460\) przypadków dokładnie dwóch błędów dla kodu ewaluacyjnego;
- odległości między wszystkimi parami słów obu kodów.

Kontrole przeszły. Nie mierzono wydajności produkcyjnego dekodera ani jakości rekonstrukcji MRI. \(\mathbb F_7\) jest małym przykładem do wyczerpującego testu, nie wybranym formatem skanera.

### C. Co wnosi „kamień”?

Gdy wszystkie kopie zawierają \((3,5)\), większość nie zauważa błędu. Niezależnie zachowany wzorzec \((2,5)\) wykrywa rozjazd. Ale jeśli już pomiar dał błędne \((3,5)\), a dopiero potem zapisano wzorzec, oba kanały będą zgodnie błędne.

W MRI trzeba rozdzielić:

- **wzorzec cyfrowy po akwizycji:** kontroluje późniejsze zmiany zapisanych danych;
- **kalibrację / znany fantom:** sprawdza określone własności toru pomiarowego;
- **nieznaną anatomię pacjenta:** nie mamy jej pełnego, niezależnego wzorca.

Pełna kopia referencyjna może przywrócić dane. Sam skrót kontrolny zwykle tylko pomaga wykryć zmianę; nie odtwarza danych ani nie dowodzi poprawności pomiaru. Uwierzytelnienie i FEC również rozwiązują osobne problemy.

## 3. Jak sprawdzać „złapanie fazy”?

Błędy cyfrowego transportu i zakłócenia pierwotnego pomiaru zespolonego to różne kanały. Test jednego nie waliduje automatycznie drugiego.

Dla pomocniczego modelu uśredniania trzech kopii z zakłóceniem \(A\cos(\omega t+\phi)\):

\[
H(\omega)=\frac13\sum_{\ell=1}^3e^{i\omega t_\ell},\qquad
\max_\phi\left|\frac A3\sum_\ell\cos(\omega t_\ell+\phi)\right|
=A|H(\omega)|.
\]

To jawny test najgorszej fazy, nie jedna dogodna faza losowa. Dla kopii \(a\) w bloku jaṭā, \(t_\ell=(0,3,4)\):

\[
|H(0)|=1,\qquad |H(2\pi)|=1,\qquad
|H(2\pi/3)|=1/\sqrt3.
\]

Wspólne przesunięcie i zakłócenie zsynchronizowane z próbkowaniem nie są tłumione. Przeplot lub randomizacja mogą ograniczać wybrane korelacje, ale wymagają synchronizacji, budżetu opóźnienia i osobnego sprawdzenia.

Dla konkretnej maszyny profil walidacji musi określić:

1. Zegary próbkowania i ramkowania, sekwencję akwizycji, trajektorię k-space, cewki, model szumu i jego zmienność.
2. Tony i harmoniczne, chirpy, zakłócenia impulsowe i paczkowe, błędy wspólne kanałów, dryf zegara, utratę i przestawianie pakietów.
3. Przemiatanie fazy i częstości względem symboli, granic bloków i przeplotu — również przypadki współmierne.
4. Błędy ramek, niewykryte błędy, najgorsze opóźnienie i pamięć oraz poprawne przypisanie próbki do czasu, cewki i współrzędnej.

Nie ma tu jeszcze tych danych. Nie wybieramy rzekomo bezpiecznego tonu ani nie deklarujemy braku sprzężenia z MRI. Wariant offline nie wprowadza żadnej emisji RF/audio do skanera.

## 4. Abstrakcyjny korektor: wymienny profil FEC

Profil \(\theta\) określa rodzinę kodu, alfabet, długość bloku, redundancję, przeplot, model kanału i budżet dekodowania:

\[
C_\theta:\mathcal M_\theta\hookrightarrow\mathcal X_\theta^{n_\theta},
\qquad
D_\theta:\mathcal Y_\theta\to
(\widehat m,\ \mathrm{status},\ \mathrm{diagnostics}).
\]

Dla danych bez uszkodzeń: odzyskana wiadomość z \(D_\theta(C_\theta(m))\) ma być równa \(m\).
Dla kodu o odległości \(d_{\min}\), z dekoderem realizującym odpowiednią gwarancję:

\[
2e+r<d_{\min}\ \Longrightarrow\ \text{jednoznaczne odzyskanie},
\]

gdzie \(e\) oznacza błędy o nieznanej pozycji, a \(r\) znane wymazania. To nie gwarantuje rozpoznania każdej awarii spoza tej klasy.

**Interfejs nie wymaga macierzy \(H\).** Może udostępniać test przynależności do kodu, metrykę i dekoder, dzięki czemu obejmuje także kody nieliniowe.

| Profil | Parametry / mechanizm | Gwarancja lub wymaganie | Kiedy rozważać |
| --- | --- | --- | --- |
| Rozszerzony Golay | binarny \([24,12,8]\), 12 bitów → 24 | dowolne 3 błędy bitowe | krótkie bloki i ograniczona praca dekodera |
| Nordstrom–Robinson | nieliniowy \((16,256,6)\), 8 bitów → 16 | dowolne 2 błędy bitowe | bardzo krótkie bloki, dekoder nieliniowy |
| Turbo | składowe kody splotowe, przeplot, miękkie dekodowanie iteracyjne | konkretna stopa, długość, LLR, zakończenie i limit iteracji | wiarygodne miękkie odczyty i budżet opóźnienia |
| Reed–Solomon / ewaluacyjny | pole i \([n,k,n-k+1]\) | \(2e+r\le n-k\) w symbolach | wymazania lub błędy symboli/pakietów |

Źródła: [JPL — Golay](https://ntrs.nasa.gov/citations/19890018520), [GAP/GUAVA — NordstromRobinsonCode](https://www.math.rwth-aachen.de/~GAP/WWW2/Gap3/Manual3/C065S055.htm), [JPL — porównanie rodzin, w tym turbo](https://ipnpr.jpl.nasa.gov/1990-1999/progress_report/42-133/133K.pdf), [Guruswami — kody ewaluacyjne](https://www.cs.cmu.edu/~venkatg/cacm09.html).

To nie ranking „który najlepszy”. Binarny codebook NR nie jest jądrem zwykłej binarnej macierzy kontrolnej, choć ma opisy strukturalne nad innymi alfabetami. Turbo nie otrzymuje gwarancji krótkiego kodu blokowego przez samo wybranie nazwy.

### Pola profilu

~~~text
codec               rodzina + komplet parametrów + wersja implementacji
frame               serializacja, długości, numer i identyfikator bloku
channel             błędy bitów/symboli, wymazania, LLR i ich kalibracja
interleaver         permutacja, głębokość i synchronizacja
decoder_budget      maks. iteracje/czas/pamięć; polityka niepowodzenia
integrity           zewnętrzna kontrola; chroniony punkt odniesienia
acquisition_context cewka, czas, trajektoria, jednostki, wersja kalibracji
validation          modele awarii, zakres testów, wyniki i ograniczenia
~~~

Nie ustawiono domyślnego profilu dla skanera. Golay, turbo i NR są **kandydatami**, nie zaimplementowanymi i zwalidowanymi sterownikami.

### Umiejscowienie

~~~text
zespolone próbki po akwizycji + metadane
    → bezstratna serializacja / utworzenie chronionej referencji
    → kodowanie FEC + przeplot
    → zawodny transport lub zapis
    → dekodowanie + kontrola integralności
    → dokładne odtworzenie bajtów i kontekstu
    → rekonstrukcja zespolona
~~~

Kodowanie musi poprzedzać odcinek, przed którego błędami chroni. FEC na bajtach **nie wymaga zaokrąglania wartości zespolonej do liczby całkowitej**: symbole pola kodowego oznaczają fragmenty bezstratnej serializacji. Po dekodowaniu można odzyskać dokładnie te same bity części rzeczywistej i urojonej. Wcześniejsza kwantyzacja ADC i szum analogowy pozostają osobnym problemem.

Status dekodera oznacza „zaakceptowano według tych kontroli”, nie „na pewno odzyskano prawdę”. Poza promieniem gwarancji możliwa jest zamiana na inne poprawne słowo kodowe. Potrzebne są osobne kontrole integralności i polityka odrzucenia niepewnych danych.

### Dodatkowy profil: grupa alternująca i błędy kolejności

Grupa alternująca (naprzemienna) to \(A_n=\ker(\mathrm{sgn}:S_n\to\{\pm1\})\). Jeżeli dopuszczamy tylko parzyste permutacje jednoznacznie oznaczonych pozycji, każda pojedyncza transpozycja zmienia znak i zostaje wykryta. Nie ustala to jednak jej położenia: każda nieparzysta permutacja ma \(\binom n2\) parzystych sąsiadów w odległości jednej dowolnej transpozycji.

Trzeba ustalić metrykę błędu. Dla n≥3 minimum odległości **dowolnych transpozycji** w Aₙ wynosi 2, a minimum **Hamminga** wynosi 3. Zamiana dwóch pozycji jest jednym błędem w pierwszej metryce i dwoma w drugiej. Nie wolno przenosić gwarancji między nimi. Teoria kodów permutacyjnych: [Cameron — Permutation codes](https://maths.qmul.ac.uk/~pjc/preprints/permcode.pdf).

**Mały pozytywny korektor:** wybierzmy podkod

\[
C=\langle(12345)\rangle\subset A_5.
\]

Ma 5 słów, a każda nietrywialna różnica dwóch słów jest 5-cyklem, więc wymaga czterech dowolnych transpozycji. Zatem \(d_{\min}=4\) i najbliższe słowo jednoznacznie poprawia jedną zamianę. Wyczerpujący test **5 słów × 10 zamian = 50 przypadków** przechodzi. Redundancja jest jawna: zamiast 60 dowolnych elementów A₅ dopuszczamy tylko 5. To demonstrator kodu kolejności, nie gotowy profil transmisji próbek MRI.

**Dodatkowy pomiar ζ jest tu dokładny:** dla permutacji p o c cyklach długości \(\ell_1,\ldots,\ell_c\), z uwzględnieniem punktów stałych,

\[
\zeta_p(t)=\prod_{j=1}^c(1-t^{\ell_j})^{-1},
\qquad \mathrm{sgn}(p)=(-1)^{n-c}.
\]

Rząd bieguna ζ w t=1 wynosi c, więc przy znanym n odczytujemy parzystość. Ale cztery nietrywialne obroty kodu C mają **identyczną** \(\zeta_p(t)=1/(1-t^5)\). ζ wykrywa ten aspekt struktury cykli; sam skalarny odczyt nie wskazuje, który obrót wysłano, ani którą parę zamieniono. Dekoder korzysta z oznaczonych pozycji i odległości do całego codebooka.

W profilu zapisujemy osobno `order_code`, metrykę, referencyjną kolejność i ochronę indeksów. Sama lista powtarzających się wartości nie określa permutacji jednoznacznie. Błędy fazy i amplitudy nie są ogólnie błędami permutacji; ten profil nie zastępuje ich modelu ani FEC bitów/symboli.

Nie mylić Aₙ z **kodami alternantowymi**, opartymi na macierzach ewaluacyjnych nad rozszerzeniem ciała i ograniczeniu alfabetu do podciała. To inna rodzina FEC, do której należą ważne konstrukcje BCH/Goppa; sama zbieżność nazwy nie daje związku z Aₙ. [Magma — AlternantCode](https://magma.maths.usyd.edu.au/magma/handbook/linear_codes_over_finite_fields).

Testy: [test_galois_krull_readout.py](test_galois_krull_readout.py), 5 nowych kontroli kolejności, metryki, dekodera i ζ.

## 5. Korektor z dwoma odczytami ζ — konstrukcja i granica

Można zbudować kod używający odczytów ζ. Trzeba jednak zadeklarować operator zależny od danych, chronioną referencję i klasę błędów. Poniżej ζ oznacza **skończoną zetę spektralną**, nie funkcję Riemanna.

Dla bajtów \(x_i\in\{0,\ldots,255\}\), \(i=1,\ldots,N\), niech

\[
A_0(x)=\operatorname{diag}(x_i+1),\qquad
A_1(x)=\operatorname{diag}\big(i(x_i+1)\big),\qquad
\zeta_A(s)=\operatorname{tr}A^{-s}.
\]

Wszystkie wartości własne są dodatnie. W \(s=-1\) otrzymujemy dokładnie:

\[
c_0(x)=\zeta_{A_0(x)}(-1)=\sum_i(x_i+1),\qquad
c_1(x)=\zeta_{A_1(x)}(-1)=\sum_i i(x_i+1).
\]

Zachowujemy oba odczyty **przed uszkodzeniem**, razem z chronioną długością i kolejnością ramki. Jeśli później zmienił się dokładnie jeden symbol,

\[
y=x+\varepsilon e_j,\qquad\varepsilon\ne0,
\]

to różnice odczytów dają

\[
r_0=c_0(y)-c_0(x)=\varepsilon,\qquad
r_1=c_1(y)-c_1(x)=j\varepsilon.
\]

Zatem **\(j=r_1/r_0\)** lokalizuje błąd, a **\(y_j-r_0\)** przywraca wartość. To dowód dla dowolnej długości ramki i pojedynczej zmiany bajtu, przy dokładnej arytmetyce i nieuszkodzonych kontrolach. Dodatkowo sprawdzono wszystkie **3072** pojedyncze zmiany czteroelementowych wiadomości nad alfabetem \(\{0,1,2,3\}\), oraz wiadomości bez błędu.

Mechanizmem są tutaj **dwie sumy kontrolne momentów, zapisane jako odczyty ζ**. Nie potrzebujemy numerycznego przedłużenia analitycznego ani szukania zer. Ten zapis nie wykazuje przewagi nad zwykłym liczeniem obu sum. Wagi pozycyjne w drugim operatorze są dodatkową informacją konstrukcyjną: nieważona ζ sama nie odróżnia permutacji wartości własnych.

### Kontrole negatywne

- \((2,2,2,2)\) i \((3,0,3,2)\) mają jednakowe **oba** odczyty: błąd \((1,-2,1,0)\) jest niewidoczny.
- Dla oryginału \((2,2,2)\), dwie zmiany dające \((3,2,3)\) powodują, że dekoder jednobłędowy zwraca \((3,0,3)\): inny tekst przechodzący kontrole.
- Uszkodzona referencja, zamiana kolejności lub błędny pomiar przed zakodowaniem nie są objęte gwarancją.

Same sumy też kosztują miejsce: nie są dwoma bajtami niezależnie od długości ramki. W tym wariancie trzeba pomieścić odpowiednio do \(256N\) i \(128N(N+1)\), bez przepełnienia. Ich ochronę należy uwzględnić w profilu FEC. Nie wolno porównywać tego budżetu wprost z sześcioma symbolami \(\mathbb F_7\) z poprzedniego testu.

**Krótka notka:** ζ może być kanałem kontrolnym korektora. Korekcję zapewniają rozróżnialność dopuszczonych błędów, zachowana referencja i dekoder — nie sama nazwa ζ. Ten przykład nie naprawia niejednoznacznej akwizycji MRI.

## 6. Stan wykonania

W [skrypcie kontrolnym](test_mobius_fourier_readout.py) przechodzi **46 testów**, w tym 10 dotyczących redundancji i referencji oraz 4 dotyczące korektora ζ i jego ograniczeń. Jest to deterministyczny eksperyment bez zewnętrznych pakietów:

~~~sh
python3 -m unittest discover -s MRI -p test_mobius_fourier_readout.py -v
~~~

Zaimplementowano małe codebooki kontrolne — powtórzenia i ewaluacje nad \(\mathbb F_7\) — jednobłędowy dekoder dwóch odczytów ζ oraz wcześniejsze modele matematyczne. **Nie zaimplementowano Golaya, turbo ani NR; nie przeprowadzono testu na danych MRI.**

Uzasadniony kierunek: pełny sygnał zespolony, FEC dopasowany do cyfrowego kanału, niezależna referencja integralności i osobna walidacja akwizycji oraz rekonstrukcji. Powtarzanie, trwały wzorzec, korekcja i pomiar uzupełniają się, ale nie zastępują automatycznie.
