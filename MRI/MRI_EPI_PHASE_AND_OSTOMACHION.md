# EPI: czy korekcja może sama stworzyć ducha?

**2026-09-09. Tak: błędna korekcja fazy może wprowadzić lub powiększyć ducha. Nie wynika z tego, że EPI jest butelką Kleina albo że błąd fazy jest ramifikacją.** Poniżej odtwarzalny model diagnostyczny, nie poprawka do skanera. Nie zmieniono dekodera FEC ani rekonstruktora wcześniejszego benchmarku. Po ponownej recenzji utwardzono interfejs tej osobnej sondy EPI: kalibracja musi być jawna, nie jest domyślnie zerowa.

## 1. Trzy różne przyczyny „braku odzysku”

| Warstwa | Wynik kontroli |
|---|---|
| FEC, czyli korekcja bajtów transportu | Dla poprawnie odzyskanego payloadu pominięcie FEC daje ten sam obraz. Wcześniejsze RS z dwoma bajtami parzystości odrzucało pakiety, gdy zmiana ramkowania umieszczała dwa błędy w jednym słowie korygującym jeden. |
| Pominięcie co drugiego wiersza k-space | Również bez FEC zostaje projekcja \(P_+x\). Nieznany kanał \(P_-x\) nie pojawia się po wyłączeniu korektora. |
| Korekcja fazy odd/even w pełnym EPI | Wszystkie próbki mogą być obecne i nienaruszone, a błędny parametr korekcji tworzy ducha. To jest przypadek z ostatniej przeklejki. |

To ostatnie jest znanym problemem, nie tylko możliwością symulatora: Buonocore–Gao opisują pogorszenie korekcji przy niedopasowaniu referencji do właściwego odczytu. Ich metoda bezreferencyjna również ma warunki identyfikowalności. [Oryginalna praca, 1997, s. 89 i 97](https://mriquestions.com/uploads/3/4/5/7/34572113/nyquist_ghost_1910380114_ftp.pdf).

## 2. Najmniejszy rachunek: dwustanowa zamiana, nie cała butelka

Model: pełna siatka 64×64, dowolny obraz zespolony, unitarny Fourier, znane odwrócenie kolejności próbek nieparzystych linii i jedna stała różnica fazy \(\phi\). Bez szumu, ruchu, błędów trajektorii i zmiennej przestrzennie fazy. Użyte siatki mają rozmiar podzielny przez cztery, zgodnie z konwencją centrowania FFT w kodzie.

Niech \(T\) przesuwa obraz o pół FOV, więc \(T^2=I\). Po korekcji oszacowaniem \(\hat\phi\) zostaje \(\delta=\phi-\hat\phi\):

\[
P_\pm=\frac{I\pm T}{2},\qquad
G_\delta=P_++e^{i\delta}P_-
=e^{i\delta/2}\left[\cos(\delta/2)I-i\sin(\delta/2)T\right].
\]

**Jest to odwracalne mieszanie dwóch pozycji:** \(G_\delta^{-1}=G_{-\delta}\), \(G_\delta^*G_\delta=I\). Przy \(\delta=\pi\) dostajemy dokładnie \(T\), nie utratę rzędu.

To najmniejszy użyteczny fragment wskazówki Ostomachionu: zamiana dwóch stanów, algebra \(C_2\), rozkład na sumę i różnicę. Nie potrzeba enumerować układów 14 kafli. Wcześniejszy [audyt Ostomachionu](DISCRIMINANT_AND_OSTOMACHION.md) oddziela taki fragment algebraiczny od twierdzeń o wszystkich rozcięciach figur.

| Faza rzeczywista | Zastosowana korekcja | Ghost/main: moduł ilorazu współczynników | NRMSE obrazu zespolonego |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 2,90·10⁻¹⁶ |
| **0** | **0,05** | **2,50052%** | **2,73875%** |
| 0,6 | 0 | 30,93362% | 32,37764% |
| 0,6 | 0,6 | 0 | 2,93·10⁻¹⁶ |
| 0,6 | 0,55 | 2,50052% | 2,73875% |
| 0,6 | 1,5 | 48,30551% | 47,65548% |

Wzór \(|\tan(\delta/2)|\) jest poprawny **dla ilorazu współczynników**. Przy nakładaniu obrazu i ducha nie jest automatycznie ilorazem jasności pikseli ani procentem błędu obrazu. Połowa kąta wynika z rozkładu \(1\pm e^{i\delta}\); przesunięcie N/2 z modulacji \((-1)^{k_y}\). Nie trzeba wyprowadzać ich ze spinorów ani z punktów stałych odbicia.

## 3. Prościej: jedna korelacja, ale z jawnym warunkiem

Niech \(a=P_+x\), \(b=e^{i\phi}P_-x\) będą rekonstrukcjami osobno z parzystych i nieparzystych wierszy. Jeśli **przed pomiarem znamy obszar R, na którym \(Tx=0\), i jest w nim sygnał**, to:

\[
a|_R=x|_R/2,\qquad b|_R=e^{i\phi}x|_R/2,
\qquad \hat\phi=\arg\sum_{r\in R}\overline{a(r)}b(r).
\]

Po tej jednej korelacji wystarcza skorygować nieparzyste próbki i wykonać odwrotny Fourier. Nie jest to nowy algorytm kliniczny: to prosty przypadek warunkowej estymacji fazy. Eliminujemy przeszukiwanie parametru w tym modelu; **nie zmierzono przewagi czasowej nad implementacją skanera**.

Kontrole:

- Znany, rozłączny z półprzesuniętą kopią obszar: \(\phi=0,6\), oszacowanie 0,6000000000000002, NRMSE 3,48·10⁻¹⁶.
- Korelacja po całym obrazie: \(a\perp b\); brak informacji o fazie w tym odczycie. Kod zwraca brak estymaty, nie zgaduje.
- Naruszenie warunku przez \(x=u+iTu\): korelacja znormalizowana ma **moduł 1**, ale estymata jest błędna o \(-\pi/2\), a rekonstrukcja ma **100% NRMSE**. Sama piękna zgodność nie certyfikuje założeń.

Dlatego „obie połowy widzą ten sam obiekt” nie wystarcza. Dla tego samego pełnego odczytu skonstruowano dwa obrazy różniące się o 21,7665%, z fazami 0,6 i 0,2; różnica ich przewidywanych danych wynosi 2,97·10⁻¹⁶. Ponadto \((x,\phi)\) i \((Tx,\phi+\pi)\) dają te same dane i tę samą entropię obrazu. Potrzebny jest zakres fazy, poprawna referencja, informacja o podporze lub inne rozróżniające ograniczenie.

Nie ma też podstaw, by uznać każdą referencję za ręcznie wpisaną tabelę. Opisane tory estymują poprawki automatycznie z nawigatorów; metody bezreferencyjne mają własne problemy przy nakładaniu sygnałów i niskim SNR. [McKay i in., metody oraz ograniczenia, 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6372312/).

## 4. Co z nakryciem, ramifikacją i ζ?

Odwrócenie kolejności linii to znana **permutacja próbek**, nie sklejenie różnych punktów w iloraz. Podana we wklejce mapa \(g(x,y)=(-x,y+1)\) ma \(g^2(x,y)=(x,y+2)\): na ogólnym torusie nie jest inwolucją. Można zdefiniować torusowe nakrycie butelki Kleina odpowiednią wolną inwolucją, ale nie wynika ono z samego schematu akwizycji EPI. Jednostkowy czynnik fazowy również nie tworzy punktu rozgałęzienia.

Jawne okresy rozstrzygają: na \(\mathbb R^2/(\mathbb Z\times2\mathbb Z)\) ta mapa jest wolną inwolucją i daje butelkę Kleina jako iloraz. Na \(\mathbb R^2/\mathbb Z^2\) jest odbiciem z punktami stałymi. Nie odrzucamy pierwszej konstrukcji; odrzucamy utożsamienie jej ze skanerem bez zdefiniowania i uzasadnienia sklejeń.

Recenzja Kimi/Fable poprawnie powtarza współczynniki ducha, ale jej nowa „poprawka kosetowa” wymaga dalszej korekty. Przy standardowej normalizacji odwrotnej DFT:

\[
\mathcal F^{-1}1_{\rm even}=\tfrac12(\delta_0+\delta_{N/2}),\qquad
\mathcal F^{-1}1_{\rm odd}=\tfrac12(\delta_0-\delta_{N/2}).
\]

Oba kosety dają obie lokalizacje. Do pojedynczych lokalizacji przechodzą charaktery \(1\) oraz \((-1)^{k_y}\), a kierunek przesunięcia to oś phase-encode. Ponadto \(G_\delta=e^{i\delta/2}\exp(-i\delta T/2)\) jest **2π-okresowe**: dwa minusy po obrocie parametru o 2π znoszą się. Formalny czynnik SU(2) na parze pozycji nie dowodzi spinowego nakrycia geometrii EPI.

ζ została zachowana jako dodatkowy pomiar z **jawnym operatorem**. W pełnym modelu \(E_\phi=R D_\phi F\) wszystkie trzy czynniki są unitarne, więc:

\[
H_\phi=E_\phi^*E_\phi=I,\qquad \zeta_{H_\phi}(s)=n.
\]

**Ten odczyt ζ nie rozróżnia poprawnej i błędnej fazy.** Na macierzy 8×8 daje 64 dla każdej fazy; duch zmienia się mimo identycznego widma H. To nie twierdzenie o wszystkich możliwych funkcjach ζ, tylko o wybranym instrumencie.

Podobnie dokładne przekładanie kafli jest permutacją Q: \(E\mapsto EQ\), \(H\mapsto Q^*HQ\). W teście czterech kafli jądro pozostaje 32-wymiarowe, a widmo zmienia się najwyżej o 6,66·10⁻¹⁶. Przekładanie pomaga wybrać współrzędne, nie dodaje brakującego pomiaru. Nie przeprowadzono literalnej enumeracji Ostomachionu.

## 5. Która tabelka wymagała poprawki?

W dostępnym repozytorium nie znaleziono tablicy kalibracji pochodzącej ze skanera. Liczby tabeli w §2 są poprawne: zła kalibracja jest tam **celową kontrolą negatywną**, nie wartością do podmiany, żeby wynik przeszedł. Poprawka dotyczy klasyfikacji w przeklejce i niebezpiecznego domyślnego parametru w sondzie:

| Zdarzenie | Poprawna klasyfikacja | Odpowiednie działanie |
|---|---|---|
| Odwrócone kierunki odczytu odd/even | Znana permutacja współrzędnych | Przywrócić kolejność próbek, bez ich sklejenia |
| Nieznana albo błędna faza odd/even | Brak kalibracji albo błąd kalibracji | Uzyskać identyfikowalną estymatę; nie zastępować braku wiedzy zerem |
| Znana resztkowa faza δ | Odwracalne mieszanie \(G_\delta\), nie ramifikacja | Zastosować przeciwną fazę; znak konwencji jest jawny w kodzie |
| Brak co drugiego pomiaru | Projekcja z nietrywialnym jądrem | Dodatkowe rozróżniające dane lub uzasadniony model; sama korekcja fazy nie wystarcza |

`reconstruct(raw, phi_estimate)` nie ma już domyślnego `phi_estimate=0`. Brak argumentu, `None`, NaN, nieskończoność, tablica zamiast skalaru lub zespolona faza są odrzucane. Jawne zero nadal oznacza pominięcie korekcji. **To ochrona interfejsu, nie estymator ani dowód poprawności podanej liczby.** Nie wyznaczono żadnej brakującej kalibracji rzeczywistego urządzenia.

## 6. Odtworzenie i zakres

[Kod sondy](mri_epi_phase_probe.py), [testy sondy EPI](test_mri_epi_phase_probe.py), [pełne wyniki JSON](mri_benchmark/epi_phase_probe.json). Wyniki dotyczą powyższego modelu; nie stanowią diagnozy konkretnego urządzenia ani potwierdzenia bezpieczeństwa medycznego. Oddzielne kontrole źródeł, FEC i topologii wykonano równolegle. Korekty starszego załącznika pozostają w [notatce Kimi](KIMI_REVIEW_NOTES_2026_09_09.md); etykieta „verified” z przeklejki nie zastępuje ich.

Po ponownej recenzji: **84/84 testy MRI (w tym 15 testów tej sondy) oraz 46/46 testów Möbiusa/Fouriera — razem 130/130**, bez pominiętych testów. Poprzedni stan miał 126 testów. Plik JSON wyników sondy pozostał identyczny bajtowo po zmianie interfejsu i ponownym wykonaniu: SHA-256 `3c70d0644d60dff36f5db01cc3e3ee0d256e2e514802cfc630364a419ef4fcd9`. Są to kontrole implementacji i jawnych modeli, nie statystyczny pomiar niezawodności skanera.

Z katalogu repozytorium, Python z NumPy:

```sh
python3 MRI/mri_epi_phase_probe.py
python3 -m unittest discover -s MRI -p 'test_mri_*.py' -v
python3 -m unittest discover -s MRI -p 'test_mobius_fourier_readout.py' -v
```

Użyty interpreter: `python3`.

**Najbliższy sensowny krok:** osobny test odporności estymatora fazy na szum, ruch, nakładanie podpór i fazę zależną od położenia, z kontrolą niewłaściwego modelu. Nie automatyczna zamiana nawigatorów na korelację, której warunków nie znamy.
