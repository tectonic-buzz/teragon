# FARI — فری

**9999987899999** — liczba pierwsza, czytana w obie strony tak samo.

[STWIERDZAM ŻE NIE TWIERDZĘ](9999987899999_STWIERDZAM_ŻE_NIE_TWIERDZĘ.md)

## Testy

Z katalogu repozytorium, Python 3 + NumPy:

```sh
python3 FARI/tests/check_rh_formulas.py
python3 FARI/tests/check_fari_prime.py
python3 FARI/tests/check_pol_notes.py
```

- [Formuły i kontrprzykłady](tests/check_rh_formulas.py): 13 testów przeniesionych z RH, bez zmiany rachunków. Rozróżniają arytmetykę dokładną od kontroli numerycznych.
- [Lustrzana pierwsza](tests/check_fari_prime.py): palindrom oraz pełny, rekurencyjny certyfikat Lucasa; wyłącznie arytmetyka całkowita, bez losowania i bez zależności zewnętrznych.

Pierwszy zestaw sprawdza skończone przykłady, nie dowodzi RH. Drugi certyfikuje pierwszość jednej wskazanej liczby. Trzeci zawiera cztery kontrole numeryczne do komentarzy w PÓŁ: liczność sita, sumę dwiema drogami i dwa odczyty pochodnej ζ.

## Rozmowy i rachunki obok

- [Ramifiksacja](../RH/01_RAMIFIKSACJA.md), [Całkoróżdżka](../RH/02_CAŁKORÓŻDŻKA.md), [Grzebień](../RH/03_GRZEBIEŃ.md) — wraz z dotychczasowymi dopiskami weryfikacyjnymi.
- [Seria Firoozbakht](../PÓŁ/1187_Firoozbakht_seria.md) i [Cenzus ζ′](../PÓŁ/1217_Cenzus_ζ′.md) — oryginalne notatki robocze z oddzielonymi komentarzami po weryfikacji; rachunki komentarzy odtwarza [check_pol_notes.py](tests/check_pol_notes.py).
- [PÓŁ](../PÓŁ/README.md) — reszta rozmowy.

Zależności: [requirements.txt](requirements.txt). Testy nie korzystają z sieci.
