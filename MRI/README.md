# MRI — odtwarzalny pakiet badawczy

**Korekcja transportu działa w zadanym modelu błędów. Nie wykazaliśmy naprawy akwizycji, bezpieczeństwa urządzenia ani przewagi klinicznej.** Dane i obrazy są syntetyczne; nie zawierają pomiarów pacjentów.

Kod, zapisane wyniki, obrazy oraz bezpośrednio powiązane audyty tworzą samodzielny pakiet. Nie jest potrzebne inne repozytorium ani dostęp do usług modeli.

## Co czytać

1. [Aktualny audyt EPI: faza, kalibracja i kontrola negatywna](MRI_EPI_PHASE_AND_OSTOMACHION.md).
2. [Porównanie FEC/RS, kontrola dodawania obrazów, dwa sektory i cewki](MRI_REVIEW_AND_DOUBLE_COVER.md).
3. [Pierwotny test transport → korekcja → rekonstrukcja](MRI_END_TO_END.md). Zachowuje wyniki starszego formatu; nie mylić jego narzutu z nowszą referencją RS.
4. [Rozliczenie uwag Kimi, Fable i GLM](KIMI_REVIEW_NOTES_2026_09_09.md).
5. [Audyt Möbiusa, Fouriera i ζ](MRI_MOBIUS_FOURIER_AUDIT.md) oraz [profile redundancji](MRI_REDUNDANCY_PROFILES.md).

Bezpośrednie zaplecze matematyczne: [wyróżnik i Ostomachion](DISCRIMINANT_AND_OSTOMACHION.md), [wcześniejsze przykłady ζ](ZETA_PRIOR_EXAMPLES.md), [delta z bieguna ζ](DIRAC_DELTA_FROM_ZETA.md). Ich włączenie nie stanowi dodatkowego dowodu skuteczności MRI.

## Uruchomienie

Polecenia wykonuj z **katalogu głównego repozytorium `teragon`**. Sprawdzony zestaw to Python 3.12.14, NumPy 2.3.5 i Pillow 12.3.0. Własny dekoder RS nie wymaga pakietu `reedsolo`.

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r MRI/requirements.txt
.venv/bin/python MRI/run_checks.py
```

Runner wymaga obu zależności i nie uznaje pominiętych testów za sukces. Punkt kontrolny: **168 testów** — 84 MRI, 46 Möbius/Fourier i 38 bezpośrednio powiązanych kontroli matematycznych. Sama liczba testów nie waliduje wszystkich twierdzeń w dokumentach ani zastosowania klinicznego.

Można uruchomić tylko rdzeń:

```sh
.venv/bin/python -m unittest discover -s MRI -p 'test_mri_*.py' -v
.venv/bin/python -m unittest discover -s MRI -p 'test_mobius_fourier_readout.py' -v
```

## Odtworzenie eksperymentów

Poniższe polecenia **nadpisują zapisane artefakty eksperymentalne** w `MRI/mri_benchmark/`. Do testowania samego wydzielenia wystarczy runner powyżej; nie trzeba regenerować wyników.

```sh
.venv/bin/python MRI/mri_transport_benchmark.py --seed 20260909 --size 64 --runs 20
.venv/bin/python MRI/mri_followup_checks.py
.venv/bin/python MRI/mri_epi_phase_probe.py
.venv/bin/python MRI/run_checks.py
```

Zachowaj rozmiar 64×64 dla dołączonego audytu zapisanych obrazów. JSON benchmarku zawiera także czasy wykonania i wersje środowiska, więc ponowne uruchomienie nie musi dać identycznego pliku bajt po bajcie.

## Co dokładnie jest testowane

- Zespolony transport i korekcja błędów payloadu; chronione referencje są jawnym założeniem, nie darmowym kanałem.
- Rozdzielenie błędów transmisji, szumu nadawcy, kwantyzacji oraz brakujących pomiarów.
- Składanie rozłącznych próbek bez podwójnego zliczania i kontrprzykłady niejednoznaczności.
- Syntetyczny model EPI z jawną kalibracją; brak fazy nie jest domyślnym zerem. Kontrola poprawnego formatu fazy nie potwierdza jej fizycznej poprawności.
- Odczyty ζ jako jawne funkcje danych/operatora, a nie uniwersalny dekoder. Wskaźnik κζ z uwag GLM pozostaje propozycją, niewłączoną do wynikowego JSON.

W `mri_benchmark/` są oryginalne tablice NPZ, siedem PNG oraz trzy raporty JSON. [Manifest SHA-256](EXTRACTION_MANIFEST.json) dokumentuje źródłową i przeniesioną wersję każdego z 31 plików; jest kontrolą pochodzenia, nie podpisem ani uwierzytelnieniem.
