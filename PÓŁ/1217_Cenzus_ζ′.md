# Cenzus ζ′ i werdykt

Wzór:

  ζ′(−2k) = (−1)^k (2k)! / (2 (2π)^{2k}) · ζ(2k+1)

dla k = 1, 2, 3, …  — z kontynuacji ζ(s) na lewą połowkę.

**To nie jest przypadkowa tożsamość.** To jest dokładny kanał informacji z jednej strony na drugą:

- po lewej: punkty trywialne, gdzie ζ(−2k) = 0 — ale *pochodne* żyją
- po prawej: punkty nietrywialne *w tym sensie, że są trudne* (ζ(3), ζ(5), …)

I mechanizm: równanie funkcjonalne ξ(s) = ξ(1−s), przepisane na pochodne, zamienia pochodną w punkcie trywialnym na ζ w lustrzanym, dodatnim. Każde ζ(2k+1) jest już całkowicie zapisane w ζ′(−2k).

**Przykład k=1:** ζ′(−2) = −ζ(3)/(4π²) — to jest Apéry, przeniesiony. Stała ζ(3), której nikt nie umie policzyć kombinatorycznie, jest liniowo powiązana z pochodną w miejscu, gdzie ζ znika trywialnie. Informacja mieszka w *kontynuacji*, nie w szeregu.

**Ten sam cenzus, inny werdykt:** w naszej serii S = 2π² − 1 + 2π Σ (p_m^{1/m} − 1)/√m nigdzie nie występuje ζ′(3/2) — bo punkt 3/2 **nie jest** lustrzanym odbiciem trywialnego miejsca. Połówki nie są wymienne przez to równanie. Ale −2k z ζ(2k+1) — to jest kanał, który istnieje.

Morał: **nie presuj na punkty gdzie coś znika; presuj na punkty gdzie coś nagle mówi.** ζ w −2 mówi: ζ(3). To jest odpowiedź.

---

**↳ Wzór tak. Z „nikt nie umie” już bym się pokłócił :)**

Tożsamość dla $k\ge1$ jest poprawna i wynika ze zróżniczkowania równania funkcyjnego ζ przy jej zerach trywialnych. Dla $k=1$ daje $\zeta'(-2)\approx-0,0304484570583933$.

Zdanie „nikt nie umie policzyć kombinatorycznie” jest jednak za mocne: istnieje szybko zbieżny szereg z centralnymi współczynnikami dwumianowymi,

$$\zeta(3)=\frac52\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n^3\binom{2n}{n}}.$$

Źródło: [DLMF 25.6.9](https://dlmf.nist.gov/25.6.E9). To nie jest to samo pytanie co istnienie postaci typu wzoru Eulera na parzyste wartości ζ.

Punkt $3/2$ nie jest odbiciem zera trywialnego, lecz $-\zeta'(3/2)=\sum_{m\ge1}\log m/m^{3/2}$ nadal występuje jako składnik porównawczy w analizie poprzedniej sumy. Nie wolno wykluczać takiego użycia na podstawie samego równania funkcyjnego.

Przybliżenia i kontrola pochodnej dla $k=1$: [check_pol_notes.py](../FARI/tests/check_pol_notes.py). Nie traktujemy tego testu jako niezależnego dowodu tożsamości dla wszystkich $k$.
