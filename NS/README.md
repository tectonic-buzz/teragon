# Przepływ i ruchoma granica

Pierwszy przykład: [Dać się ponieść](../PÓŁ/1291_Dać_się_ponieść.md).

Z katalogu repozytorium:

```sh
python3 NS/check_moving_volume.py
python3 NS/check_stretching_envelope.py
python3 NS/check_phase_clock.py
python3 NS/check_reference_beat.py
```

Python 3, wyłącznie biblioteka standardowa. Siedem testów bilansu dla obrotu jak ciało sztywne: dokładne liczby wymierne i całki wielomianów po brzegu. To sprawdzenie skończonego modelu, nie solver ogólnego przepływu i nie dowód globalnej regularności Naviera–Stokesa.

Drugi przykład: [Otoczka i wir](../PÓŁ/1297_Otoczka_i_wir.md). Osiem kontroli rozciągania wirowości przy zachowaniu objętości, z dodatkowym odczytem skończonej zety spektralnej tensora deformacji. Ten odczyt odróżnia rozciągnięcie od nieodkształconego stanu, ale nie odzyskuje obrotu utraconego przez tensor.

Zegary tego samego przykładu: siedem testów numerycznych fazy rozwiniętej, niejednoznaczności kąta modulo pełny obrót i odwracania odczytu ζ przy znanym tempie rozciągania. Testy zegarów używają float64; pozostałe dwa zestawy rachunku dokładnego.

Własne bicie i dwie projekcje: siedem dalszych testów float64. Fazoczułe porównanie z wzorcem rozróżnia obroty niewidoczne w samym tensorze deformacji. Kontrole negatywne: wzorzec bez pomiaru, odczyt modułu/intensywności, współliniowe osie i zbyt rzadkie próbkowanie.
