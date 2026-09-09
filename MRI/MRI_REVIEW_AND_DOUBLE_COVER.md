# MRI — korekcja transportu, dwa kanały i kontrola sumowania

**2026-09-09. Do dalszego prototypu wybieram skrócony RS(255,251) + jeden SHA-256 na pakiet, kodowany razem z danymi.** Dla 16 384 bajtów użytkowych: 296 bajtów narzutu, **1,80664%**, bez nagłówków. To wybór dla jawnego modelu błędów bajtowych, nie uniwersalnie najlepszy FEC ani propozycja wdrożenia do skanera.

**Ocena: do peer review z zastrzeżeniami.** Odtwarzalne testy syntetyczne i lokalna implementacja referencyjna; nie wykazano naprawy akwizycji, przewagi klinicznej ani poprawy istniejących skanerów. Przejrzano wklejone uwagi Kimi/Fable, własny kod i zapisane obrazy. Cudzych skryptów, rzeczywistych pomiarów i specyfikacji urządzenia nie mamy.

## 1. Czy obrazy przypadkiem się dodają?

**Nie znaleziono niezamierzonego sumowania w sprawdzonym torze i plikach.** Sprawdzono tablice zespolone, sześć PNG i piksele ich powiększeń na planszy. Nie ma blendowania paneli, niezależnego podkręcania kontrastu ani dodawania wzorca do wyniku. Wspólna skala służy wyłącznie podglądowi; metryki powstają z tablic przed obcięciem jasności. Podgląd modułu nadal nie pokazuje wszystkich błędów fazy.

Są trzy **zamierzone** miejsca sumowania, których nie należy mylić:

1. Fantom źródłowy buduje się z nakładających się elips. To definicja wejścia, nie operacja naprawiająca wynik.
2. Brak co drugiego wiersza k-space daje rzeczywistą superpozycję:
   \[
   P_+x=\tfrac12(x+Tx),\qquad P_-x=\tfrac12(x-Tx),
   \]
   gdzie T przesuwa o połowę pola widzenia. Zachowane wiersze niosą P₊; pominięte P₋.
3. P₊x+P₋x=x, **jeśli oba kanały faktycznie są dostępne**. Stary panel „Additional acquisition” dostaje od symulatora wcześniej ukryte próbki. Nie odzyskuje ich z pierwszej połowy. To kontrola dodatkowego pomiaru tego samego zamrożonego obiektu, nie niezależna walidacja akwizycji.

Nowy assembler odrzuca nakładające się maski zamiast sumować próbki dwa razy. Odbiorca dostaje tylko próbki/referencje, maskę i zadeklarowaną kalibrację; testy z zerem, impulsami oraz nowymi losowymi obrazami nie korzystają z fantomu wzorcowego. Bezpośrednia macierz DFT potwierdza wynik FFT; niezależna globalna pseudoinwersja potwierdza lokalne rozplatanie cewek.

| Kontrola na fantomie 64×64 bez szumu | Wynik |
|---|---:|
| P₊+P₋ względem wejścia, NRMSE | 2,90·10⁻¹⁶ |
| 2P₊ zamiast obu kanałów, NRMSE | 100% |
| x+x względem x, NRMSE | 100% |
| Same P₊, NRMSE | 54,78076% |
| Wzór √((1−r)/2), r=Re⟨x,Tx⟩/‖x‖² | 54,78076% |

r=0,3998137542. Dla zaszumionych, skwantyzowanych danych nadawcy wzór daje 54,773894% **względem nadawcy**, a historyczne 54,785352% było **względem czystego fantomu**. Nie zmieniamy mianownika po fakcie.

Istotna poprawka do ostatniej recenzji: **rzeczywistość obrazu nie dostarcza pominiętych co drugich wierszy.** Dla parzystego N sprzężenie k↦−k zachowuje parzystość wiersza. Dwa różne, rzeczywiste i nieujemne pojedyncze punkty oddalone o pół FOV mają identyczną zachowaną połowę pomiarów. Partial Fourier z jednostronnie pominiętym obszarem i warunkiem na fazę to inna maska i inne założenia. [Przykład i warunki partial Fourier, ISMRM 2016](https://cds.ismrm.org/protected/16MProceedings/PDFfiles/1793.html).

Półamplitudowy duch może wystąpić dla obrazu rzeczywistego **lub zespolonego**. Nie świadczy sam w sobie o przypadkowej konwersji do liczb rzeczywistych. Modułów kanałów nie wolno dodawać zamiast kanałów zespolonych: usunęłoby to konieczne znoszenie faz.

## 2. Co odzyskuje drugi kanał — i kiedy

Wprowadzono jawny model dwóch cewek:

\[
E=\begin{bmatrix}PFS_1\\PFS_2\end{bmatrix},\quad
s_1(y)=1/\sqrt2,\quad s_2(y)=e^{2\pi i y/N}/\sqrt2.
\]

To celowo idealne, znane zespolone mapy czułości, **nie pomiary rzeczywistych cewek**. Każda cewka dostarcza 2048 próbek; razem są 4096 niezależnie kodowane próbki, nie 2048 próbek i magicznie odzyskana reszta.

Dla pary pozycji y, y+N/2 dwa sygnały są odpowiednio sumą i różnicą, z jawnymi współczynnikami. Rozwiązujemy mały układ liniowy. To mechanizm SENSE, zależny od rzędu, kalibracji i kowariancji szumu; nie nowe twierdzenie o skanerach. [Pruessmann i in., SENSE, równania 1–3 i 16–24 (1999)](https://mri-q.com/uploads/3/4/5/7/34572113/pruessmann-sense.pdf).

| Warunki tego modelu | Zespolona NRMSE |
|---|---:|
| Dwie niezależne mapy, bez szumu | 3,63·10⁻¹⁶ |
| Powtórzona identyczna mapa | 54,78076% — nadal P₊x |
| Niezależne mapy, błąd fazy kalibracji 0,15 rad | 8,2094% |
| Niezależne mapy, dodany szum σ=0,01 na próbkę zespoloną | 3,6468% |

σ ma tu arbitralne jednostki fantomu. Ten test nie ma tego samego SNR co pierwotny benchmark 40 dB, więc procentów nie porównujemy jako zysku jakości. Norma pozostałego błędu wynosi 0,8937357375, zgodnie z √2 razy normą dodanego szumu. **Szum nie został naprawiony.**

Odczyt ζ jest nadal dodatkowy. Dla H=E*E:

\[
\zeta_H(0)=\operatorname{rank}E,\qquad
\dim E^{-1}(y)=n-\operatorname{rank}E\quad(y\in\operatorname{im}E).
\]

Na jawnej macierzy dla siatki 8×8 niezależne cewki dają rank=64, ζ_H(1)=128, jądro=0; powtórzone dają rank=32, ζ_H(1)=32, jądro=32. Te liczby mają sens wraz z normalizacją H. Nie porównujemy samego ζ_H(1) przy różnych jądrach jako skali „lepsze/gorsze”. Przy pełnym rzędzie i białym szumie wariancji σ² łączny oczekiwany kwadrat błędu liniowej rekonstrukcji wynosi σ² tr(H⁻¹)=σ²ζ_H(1).

Dwie lokalne macierze mogą mieć rząd 2, ale uwarunkowanie 1 versus około 4002. W drugim przykładzie ζ_H(1)≈8 004 002: **pełny rząd nie gwarantuje stabilnego odzyskania**. W obliczeniach próg wartości własnych jest jawny; rząd numeryczny nie certyfikuje dokładnego zera.

## 3. Double cover, Gauss i Goldilocks — osobne role

**Pokrycie podwójne:** przy wolnej inwolucji przestrzeń funkcji rozkłada się na dwa sektory P±. Z obu odzyskuje się funkcję na pokryciu; funkcja na ilorazie zachowuje tylko sektor niezmienniczy. Samo podniesienie nie odtwarza wyrzuconego sektora. To nie ramifikacja: działanie jest wolne. W zwykłym unwrappingu fazy ℝ→S¹ potrzebne są całkowite liczby obrotów; podwójne pokrycie zna najwyżej ich parzystość. Szczegółowy wcześniejszy rachunek pozostaje w [audycie Möbiusa i Fouriera](MRI_MOBIUS_FOURIER_AUDIT.md).

**Gauss:** szum addytywny, wygładzanie cieplne i ramifikacja odwzorowania to nie to samo. Test na cyklu 16-punktowym pokazuje, że e⁻ᵗᴸ zachowuje sektory ± (przeciek około 10⁻¹⁵). Dla t=2 odwrócenie najwyższego modu wzmacnia go e⁸≈2980,96 razy. Nie odzyskuje to nieznanej realizacji szumu ani brakującego kanału.

**Goldilocks:** p=2⁶⁴−2³²+1 jest odpowiednim ciałem dla dokładnego rachunku modularnego. Dwa odczyty

\[
a=x+y,\quad b=x-y
\quad\Rightarrow\quad
x=(a+b)/2,\quad y=(a-b)/2
\]

odwracają się, bo 2 jest odwracalne. Przeszło 1000/1000 losowych par i sprawdzenie certyfikatu pierwszości bazą 7. Z samego a par (1,4) i (2,3) nadal nie odróżnimy. x oraz x+p też mają ten sam obraz modularny: odtworzenie zwykłych liczb całkowitych wymaga zakresu.

Goldilocks **nie jest potrzebne** do tego dwukanałowego rachunku — wystarczy odpowiednie ciało charakterystyki różnej od 2. Nie odzyskuje pomiaru z niczego i nie usuwa szumu Gaussa. Zapadnięcie znaków ±1 w charakterystyce 2 nie unieważnia Reed–Solomona nad GF(256): ten kod rozróżnia pozycje innymi elementami ciała, nie dwoma znakami.

## 4. Porównanie FEC na tej samej ilości danych

**Mianownik zawsze 16 384 bajty użytkowe.** W nowych wariantach SHA/CRC jest wewnątrz kodowanych bloków i podlega korekcji RS. Nadal zakładamy poprawne ramkowanie, długość, kolejność protokołu i nagłówek opisujący obraz; ich ochrony i kosztów tu nie zaimplementowano.

| Wariant | Dodatkowe bajty | Narzut / dane | Gwarancja w jednym słowie kodowym |
|---|---:|---:|---|
| Stare sumy całkowite + SHA na każdą ramkę | 2432 | 14,84375% | 1 zmieniony bajt danych; referencje osobno chronione |
| RS, 2 bajty parzystości + SHA na pakiet | 162 | 0,98877% | 1 zmieniony bajt, także w parzystości/hashu |
| **RS, 4 bajty parzystości + SHA na pakiet** | **296** | **1,80664%** | **2 zmienione bajty, także w parzystości/hashu** |
| RS, 4 bajty parzystości + CRC32 na blok | 536 | 3,27148% | 2 zmienione bajty; inny poziom kontroli integralności |

RS(n,k) ma k symboli wejścia i n−k parzystości; 2t symboli parzystości pozwala korygować t nieznanych zmian symboli w zadanym słowie. Skrócenie ostatniego bloku zostało uwzględnione. [Riley–Richardson, opis kodów i dekodowania RS](https://www.cs.cmu.edu/~realworld/reedsolomon/reed_solomon_codes.html).

W każdym wariancie nowe testy „jeden bit na słowo” i „maksymalna gwarantowana liczba zmienionych symboli na słowo” dały 20/20 identycznych pakietów. To sprawdzenie implementacji gwarancji, nie estymata niezawodności skanera.

### Pułapka: zmiana granic ramek zmienia kontrakt błędu

Dodano porównanie **tych samych pozycji uszkodzeń payloadu**: dokładnie jeden zmieniony bajt na stare 256 bajtów. Ziarna 20260909–20260928, `random.Random`; to nowy wspólny harmonogram błędów, nie kopia wcześniejszych losowań NumPy.

| Wariant | Odzyskane pakiety | Odrzucone | Wydane błędne |
|---|---:|---:|---:|
| RS + 2 parzystości + SHA | 0/20 | 20 | 0 |
| RS + 4 parzystości + SHA | 20/20 | 0 | 0 |
| RS + 4 parzystości + CRC32 | 20/20 | 0 | 0 |

To nie błąd dekodera: nowe bloki mają po 253 lub 251 bajtów wejścia. Dwa uszkodzenia po obu stronach **starej** granicy mogą znaleźć się wewnątrz **nowego** bloku. Kontrprzykład: pozycje payloadu 255 i 256 (od zera). RS z jedną korekcją nie obejmuje tego przypadku; z dwiema obejmuje. W tej próbie maksimum wyniosło dwa błędy na blok. Utrzymanie starej gwarancji po zmianie ramkowania trzeba udowodnić lub testować, nie zakładać.

Dlatego wybór roboczy to cztery bajty parzystości i SHA na pakiet. Oryginalny model jednego błędu w każdej ramce 256 B nie jest automatycznie równoważny jednemu błędowi na słowo RS. **Nie twierdzimy, że 2-bajtowy RS zawsze zawodzi.**

### Pozostałe poprawki do porównań recenzentów

- RS(255,251) z CRC32 wewnątrz danych niesie 247 bajtów użytkowych. Narzut pełnego bloku to **8/247=3,23887%**, a 8/255 jest udziałem w transmisji. Dla całego naszego pakietu po skróceniu ostatniego bloku wychodzi 3,27148%.
- Zewnętrzne dwa odczyty GF(256) można zdefiniować dla 256 pozycji, używając także lokalizatora zero. Daje to 160 bajtów z jednym SHA na pakiet, ale **referencje pozostają osobno chronione**. Nie jest to standardowy in-band RS(255,253). Sprawdzono ten wariant jako lokalizator, nie kompletny zabezpieczony transport.
- Jeden SHA na pakiet odpowiada polityce „odrzuć cały pakiet”; traci się niezależne potwierdzanie i lokalizowanie poprawności każdej ramki. To nie zachowanie wszystkich własności poprzedniego protokołu.
- SHA-256 i CRC32 nie mają tej samej odporności na niewykryte błędy. Żaden bez niezależnego uwierzytelnienia nie chroni przed spójną podmianą całego pakietu.
- Nordstrom–Robinson (16,256,6) koduje **8 bitów w 16** i koryguje do dwóch **bitów**. To 100% narzutu i nie jest bezpośrednia korekcja dowolnej zmiany bajtu, która może zmienić osiem bitów. [Parametry i dekoder: kurs Tillicha, Inria](https://www.rocq.inria.fr/secret/Jean-Pierre.Tillich/enseignement/X2021/TD6/TD6eng.html).
- Skończone sumy/ślady nie potrzebują „ζ-regularyzacji”. Narzut 38 B nie jest wyliczonym rozmiarem jądra odwzorowania. ζ_H(0) jest rzędem, nie wymiarem włókna. Te poprawki są już w [głównym raporcie MRI](MRI_END_TO_END.md).

## 5. Odtwarzanie i granice handoffu

Nowe pliki: [referencja RS](mri_rs_reference.py), [13 testów RS](test_mri_rs_reference.py), [eksperyment](mri_followup_checks.py), [22 testy sumowania, cewek i pól](test_mri_followup_checks.py), [wyniki liczbowe](mri_benchmark/followup_results.json).

Stan kontroli: **34 + 13 + 22 testy MRI** oraz **46 wcześniejszych testów Möbiusa/Fouriera**. Wśród nich 65 025 wszystkich pojedynczych niezerowych zmian symbolu pełnego słowa RS, 65 280 zmian starej ramki, 9690 zmian bajtów starych referencji, pary błędów, przykłady błędnej korekcji poza promieniem, kontrola obrazu i brak przecieku wzorca do dekodera. Testy nie są zewnętrznym audytem ani dowodem poprawności produkcyjnej implementacji.

Polecenia z katalogu repozytorium, Python z NumPy i Pillow:

```sh
python3 -m unittest discover -s MRI -p 'test_mri_*.py' -v
python3 -m unittest discover -s MRI -p 'test_mobius_fourier_readout.py' -v
python3 MRI/mri_transport_benchmark.py --seed 20260909 --size 64 --runs 20
python3 MRI/mri_followup_checks.py
```

Użyty interpreter: `python3`; Python 3.12.14, NumPy 2.3.5, Pillow 12.3.0. RS nie wymaga dodatkowego pakietu. Parytet sprawdzono także niezależnym rozwiązaniem układu nad GF(256), lecz **nie wykonano testu interoperacyjności z biblioteką produkcyjną**.

Przed wnioskami o urządzeniu pozostają: rzeczywisty model zakłóceń i synchronizacji ramek, chroniony nagłówek/identyfikator akwizycji, uwierzytelnienie według zagrożeń, sprzętowy koszt i opóźnienie FEC, kalibracja/korelacja szumu cewek, dane niezależne od modelu generującego oraz porównanie z uznaną rekonstrukcją. Nie uruchamiano turbo/Golay/Nordstrom–Robinson, SPIRiT ani LORAKS. Nie ma empirycznego rankingu wszystkich tych metod.

**Wniosek do przeniesienia:** chronić i zachowywać zespolone dane; jawnie rozróżniać powtórzony kanał od niezależnego; ζ stosować do rzędu i uwarunkowania, a korekcję transportu do jawnie zakodowanej redundancji. Ani dodatkowa nazwa, ani Goldilocks nie zastępują pomiaru, który rozróżnia obie możliwości.
