# Heine–Borel

Zwarte = domknięte i ograniczone; równoważnie: **każde pokrycie otwarte ma podpokrycie skończone.**

Cała moc jest w drugim zdaniu: zwartość to licencja na przejście od lokalnie do globalnie w skończenie wielu krokach. Dokładnie to, o co prosi każde descent, każdy certyfikat i każda membrana.

### Miejsce 1: certyfikator

`winding()` dzieli bok prostokąta na pół aż obraz segmentu zmieści się w otwartej półpłaszczyźnie, z budżetem Δ=24. Dlaczego to w ogóle kończy się skończenie? Heine–Borel. Brzeg jest zwarty, „dobre segmenty" (gdzie ξ nie znika i argument nie przekracza π) są pokryciem otwartym — więc skończenie wiele wystarcza.

Lepiej: **liczba Lebesgue'a.** Dla pokrycia otwartego zbioru zwartego istnieje δ takie, że każdy odcinek krótszy niż δ leży w jednym elemencie pokrycia. Oszacowanie z góry: z |ξ| ≥ m i |ξ′| ≤ M dostajesz siatkę a priori:

  δ = m/(2M),   Δs ≤ πm/(2M)

certyfikat terminacji przed liczeniem, nie po.

I druga strona: **pas krytyczny nie jest zwarty** — nieograniczony w t — więc żaden skończony certyfikat pudełkowy nie objmie wszystkich zer. Certyfikaty pudełkowe potwierdzają zwarte rzeczy; RH mówi o niezwartej.

### Miejsce 2: membrana

Dychotomia czarnej dziury: cykliczna dywergencja wraca do stanu (wykrywalna), generatywna mieli świeże stany w nieskończoność. Czytane przez Bolzano–Weierstrass (równoważny Heine–Borelowi w ℝⁿ): w przestrzeni *zwartej* każdy nieskończony bieg ma punkt skupienia. **Klasa generatywna to niezwartość.**

Więc domknij: census już to robi (ślepy na wartości), więc w ilorazie przez plan wartości Y-następnik ma ten sam stan strukturalny co obrót. Czarna dziura kluczona na strukturze mod wartości strzela od razu; klasyfikujesz przez to, co zrobiła *wartość*: struktura wraca, wartość nie maleje → DYWERGENCJA orzeczona, bez budżetu; struktura wraca, wartość ściśle maleje → terminacja. To terminacja przez zmianę rozmiaru — Lee–Jones–Ben-Amram 2001 — dowód idzie przez Ramseya, czyli przez nieskończoną szufladkę, czyli przez zwartość.

### Miejsce 3: Dragon

Dziewięć kart to *skończone* pokrycie; skończoność bierze się stąd, że stan po uzwarceniu jest zwarty. Bez brzegu w nieskończoności pokrycie nie ma prawa być skończone, a bez skończonego pokrycia nie ma skończonego nerwu Čecha ani holimu.

> Heine–Borel w zdaniu: kompaktyfikacja to to, co zamienia nieskończone pokrycie w dziewięć kart.

Historia: Borel 1895 dla pokryć przeliczalnych, Lebesgue rozszerzył — Francja. Ale użycie (Baire, Borel, kategorie, zbiory borelowskie) dojrzało w Warszawie i Lwowie w Fundamentach. Jedno twierdzenie, którym obie szkoły grały tą samą gęsią.
