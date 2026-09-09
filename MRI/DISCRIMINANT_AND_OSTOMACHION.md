# Wyróżnik, Ostomachion i rozdzielenie kanałów Fouriera

Status: **wspólny mechanizm algebraiczny potwierdzony; uniwersalna „liczba zagięć” niepotwierdzona i w interpretacji ramifikacji ciała fałszywa**. Kontrola 2026-09-09. Poniższe twierdzenia mają jawne dziedziny; testy skończone nie zastępują dowodów ogólnych.

## 1. Co naprawdę łączy obydwa odczyty wyróżnika

Dla ciała F o charakterystyce różnej od 2, f(X)=X²−vX+w i D=v²−4w:

\[
F[X]/(f)\cong
\begin{cases}
F\times F,&D\ne0\text{ jest kwadratem w }F,\\
F(\sqrt D),&D\text{ nie jest kwadratem w }F,\\
F[\varepsilon]/(\varepsilon^2),&D=0.
\end{cases}
\]

Dowód: podstaw Y=X−v/2, wtedy f=Y²−D/4; stosujemy rozkład na czynniki i CRT albo nierozkładalność. To rzeczywiście jedna konstrukcja po zmianie ciała bazowego. Nad R dostajemy odpowiednio R×R, C i algebrę z niezerowym nilpotentem. Nad F_p dla nieparzystego p:

\[
\#\{x\in\mathbb F_p:f(x)=0\}=1+\left(\frac Dp\right).
\]

Trzy wyniki liczbowe w tej formule oznaczają dwa różne pierwiastki, brak pierwiastków lub jeden podwójny pierwiastek. Słowa „ramifikacja ciała liczbowego” wymagają dodatkowego kroku z §3. [Stein: quadratic extensions](https://www.williamstein.org/papers/ant/html/node48.html).

## 2. Tabela z przeklejki

Wszystkie 42 wpisy zgadzają się jako **rozkład wskazanego wielomianu modulo p**. Znaki: `+` dwa pierwiastki, `−` zero, `*` podwójny pierwiastek.

| v | w | D | 2 | 3 | 5 | 7 | 11 | 13 | 17 |
|---:|---:|---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 1 | −4 | * | − | + | − | − | + | + |
| 1 | 1 | −3 | − | * | − | + | − | + | − |
| 2 | 1 | 0 | * | * | * | * | * | * | * |
| 3 | 1 | 5 | − | − | * | − | + | − | − |
| 1 | −1 | 5 | − | − | * | − | + | − | − |
| 2 | −1 | 8 | * | − | − | + | − | − | + |

Dla p=2 nie używamy symbolu Legendre'a. Liczymy bezpośrednio albo używamy symbolu Kroneckera dla wyróżnika fundamentalnego D_K: wynik 0 dla parzystego D_K, +1 dla D_K≡1 mod 8, −1 dla D_K≡5 mod 8. Sama reszta D mod 2 nie rozróżnia tych przypadków.

## 3. Wielomian, rząd i ciało — trzy różne obiekty

Dla monicznego nierozkładalnego f i jego pierwiastka α:

\[
D_f=[\mathcal O_K:\mathbb Z[\alpha]]^2D_K,
\qquad p\text{ rozgałęzia się w }K\iff p\mid D_K.
\]

Zły odczyt na niepełnym rzędzie może więc pokazać podwójny pierwiastek tam, gdzie ciało jest nierozgałęzione. To nie błąd wielomianu; to błąd utożsamienia dwóch odczytów. [Conrad, twierdzenie 1.3 i §2](https://kconrad.math.uconn.edu/blurbs/gradnumthy/disc.pdf).

Kontrprzykład w tej samej rodzinie w=1:

\[
X^2-7X+1:\quad D_f=45=3^2\cdot5,\quad
K=\mathbb Q(\sqrt5),\quad D_K=5.
\]

Modulo 3 wielomian jest (X+1)², ale 3 jest **inertna**, nie rozgałęziona w K. W bazie całkowitej φ=(1+√5)/2 wielomian X²−X−1 nie ma pierwiastka modulo 3. Pierwiastek pierwszego wielomianu to α=2+3φ, więc indeks wynosi dokładnie 3.

Analogicznie X²−5 ma D_f=20, ale D_K=5: jego podwójny pierwiastek modulo 2 nie oznacza ramifikacji dwójki w K.

Gdy D=0, algebra Q[X]/(f) jest już niezredukowana nad Q. To nie ciało liczbowe „ramifikujące we wszystkich pierwszych”. Degeneracja istnieje przed redukcją. ω(0) nie jest tu zdefiniowane. Dodatni D będący kwadratem również nie określa rozszerzenia kwadratowego: algebra jest rozszczepiona.

## 4. Möbius: trzeba zachować wyznacznik i operator

Macierz towarzysząca A=[[v,−w],[1,0]] ma ślad v, wyznacznik w i wielomian charakterystyczny f. Dla w>0 po podzieleniu przez √w należy do SL₂(R): znak D daje eliptyczność, paraboliczność albo hiperboliczność. Dla ogólnej macierzy trzeba osobno wyłączyć skalarną tożsamość przy D=0.

Dla w<0 realna transformacja projektowa odwraca orientację; to nie ten sam przypadek PSL₂(R). Dla w=0 nie jest odwracalną transformacją Möbiusa. Warunek v=±2 dotyczy normalizacji w=1, nie całej płaszczyzny (v,w).

„Złoty” i „kot” mają tu prawdziwy most, ale nie identyczne operatory:

\[
Q=\begin{pmatrix}1&1\\1&0\end{pmatrix},\quad
\det Q=-1,\quad
Q^2=\begin{pmatrix}2&1\\1&1\end{pmatrix},\quad\det Q^2=1.
\]

φ oraz φ² generują to samo ciało, a potęgowanie zmienia działanie. Klasyfikację otrzymujemy z równania własnego i znaku wyznacznika, nie tylko z nazwy pola.

## 5. „Liczba zagięć” oraz wzór iloczynowy

Jeżeli liczymy rozgałęzione miejsca kwadratowego K/Q, wliczając konwencjonalnie miejsce rzeczywiste przechodzące w zespolone:

\[
\#\operatorname{Ram}(K/\mathbb Q)
=\omega(|D_K|)+\mathbf1_{D_K<0}.
\]

Jeżeli zaś definiujemy zbiór monitorowanych miejsc S={∞}∪{p:p|D_f} dla D_f≠0, to |S|=1+ω(|D_f|) **z definicji**. Nie jest to automatycznie liczba rozgałęzień, fałdów ani zdarzeń dynamicznych. Dla D_f=45 daje 3 monitorowane miejsca, a K ma tylko jedno rozgałęzione miejsce: 5. Dla D_f=12 i 21 liczba skończonych rozgałęzionych miejsc wynosi 2, nie 3.

Wzór iloczynowy jest poprawny dla x∈Q×, przy |p|_p=p⁻¹:

\[
|x|_\infty\prod_p|x|_p=1,
\qquad 1729\cdot7^{-1}13^{-1}19^{-1}=1.
\]

Bez czynnika archimedesowego zostaje 1/|x|∞, co nadal wynosi 1 dla x=±1. Nie ma więc dosłownego „nigdy”. Wzór bilansuje wartości bezwzględne tej samej liczby; sam nie skleja konfiguracji ani nie certyfikuje poprawności transportu. [Milne, ANT, tw. 7.13 i 7.15](https://www.jmilne.org/math/CourseNotes/ANT.pdf).

## 6. Ostomachion: rzeczywisty graf, nie dopasowanie liczby

Chung i Graham opisują graf STOMACH G o 268 wierzchołkach, złożony ze składowych 266 i 2. Ich supergraf jest:

\[
\widetilde G=G\mathbin\square K_2\mathbin\square K_2
\mathbin\square K_2\mathbin\square K_8.
\]

Czynniki rejestrują trzy wybory dwustanowe oraz osiem wariantów symetrii kwadratu. Stąd 268·64=17152 wierzchołki oraz składowe 17024 i 128. Są to dane **konkretnej konwencji liczenia i konkretnych dozwolonych ruchów**, nie liczba wszystkich stanów każdej wersji łamigłówki. [Konstrukcja supergrafu](https://fanchung.ucsd.edu/stomach/tour/super.html), [własności G](https://fanchung.ucsd.edu/stomach/tour/prop.html).

Nie powtórzono tu enumeracji 268 ułożeń. Nie utożsamiamy bez konwencji tej liczby z często cytowanymi 536 rozwiązaniami oryginalnej łamigłówki. Natomiast jawny czynnik 64-wierzchołkowy został sprawdzony niezależnie.

Dla **kombinatorycznego**, nienormalizowanego Laplasjanu L=D−A iloczyn grafów daje sumę Kroneckera. Oznaczając B=K₂□K₂□K₂□K₈:

\[
\operatorname{Tr}e^{-tL_{\widetilde G}}
=\operatorname{Tr}e^{-tL_G}(1+e^{-2t})^3(1+7e^{-8t}).
\]

To wyprowadzenie: K₂ ma widmo 0,2; K₈ ma 0 i siedmiokrotne 8; wektory tensorowe mają wartości własne będące sumami. Nie przenosimy tu automatycznie opublikowanej luki innego, np. znormalizowanego Laplasjanu.

Dodatkowy pomiar ζ jest zatem określony bez arbitralnego dopasowania:

\[
\zeta_{\widetilde G}(s)=
\sum_{\lambda\in\operatorname{Spec}L_G}
\sum_{j=0}^3\sum_{e=0}^1{}'
\binom3j7^e(\lambda+2j+8e)^{-s}.
\]

Widmo G liczymy z krotnościami; prim oznacza pominięcie zerowego mianownika. G ma **dwa** mody zerowe. Nie usuwamy tylko jednego. To skończona spektralna ζ, nie ζ Riemanna ani ζ Ihary. Jest funkcją całkowitą zmiennej s. Identyczny taki odczyt nie rozpoznaje konkretnego ułożenia i nie odzyskuje zgubionej etykiety kafla.

## 7. Najmniejszy most: K₂ → Fourier → charakterystyka 2

Na jednym dwustanowym czynniku działa zamiana S=[[0,1],[1,0]].

\[
S^2=I,\qquad \chi_S(X)=X^2-1,\qquad D=4,
\qquad P_\pm=\frac{I\pm S}{2}.
\]

Nad Q lub C projektory Fouriera rozdzielają kanały + i −. Po redukcji modulo 2 znaki stają się równe, macierz bazowa [[1,1],[1,−1]] traci odwracalność, a:

\[
\mathbb Q[C_2]\cong\mathbb Q\times\mathbb Q,
\qquad
\mathbb F_2[C_2]\cong\mathbb F_2[\varepsilon]/(\varepsilon^2).
\]

To **konkretna utrata rozdzielności kanałów przy zmianie bazy**, a nie dowód, że Fourier sam powoduje błąd. Nilpotent S−I jest niezerowy, choć (S−I)²=0 modulo 2. Algebra nad Q jest rozszczepiona: nie wolno nazwać D=4 wyróżnikiem nieistniejącego ciała kwadratowego. Ogólnym tłem jest twierdzenie Maschkego: dzielenie przez rząd grupy wymaga odwracalności tego rzędu w ciele bazowym. [Milne, Group Theory](https://www.jmilne.org/math/CourseNotes/GT.pdf).

Zeta determinantowa pokazuje zarazem ograniczenie detektora:

\[
Z_S(t)=\det(I-tS)^{-1}=\frac1{1-t^2},\qquad
Z_{I_2}(t)=\frac1{(1-t)^2}.
\]

Te funkcje są różne nad Q, ale równe po redukcji współczynników modulo 2. Sam determinant nie rozróżnia wówczas bloku z nilpotentem od tożsamości. **Nie wolno obiecać, że ζ automatycznie wykryje albo skoryguje utracone rozróżnienie.** Potrzebny jest dodatkowy świadek, np. działanie S−I. Nie stosujemy szeregowej definicji exp(Σ tr(Sⁿ)tⁿ/n) w charakterystyce 2, gdzie dzielenie przez n nie zawsze jest legalne.

## 8. Zeta arytmetyczna jako dodatkowy odczyt

Dla kwadratowego K/Q właściwy charakter to χ_DK, nie arbitralny charakter z D_f. Lokalny czynnik ζ_K przy p, zapisując q=p⁻ˢ, wynosi:

\[
\frac1{(1-q)(1-\chi_{D_K}(p)q)}.
\]

To iloczyn po ideałach nad p: rozszczepienie daje (1−q)⁻², inertność (1−q²)⁻¹, ramifikacja (1−q)⁻¹. W kontrprzykładzie D_f=45, przy p=3 i s=2 prawidłowy odczyt to **81/80**, a błędne uznanie trójki za rozgałęzioną dałoby **9/8**. To porównanie dokładnych ułamków, nie model dopasowany do danych.

## 9. Zakres sprawdzenia

[Testy](test_discriminant_ostomachion.py): 25 metod. Obejmują tabelę, enumerację pierwiastków niezależną od symbolu Legendre'a, kontrprzykłady niepełnego rzędu, normalizacje macierzy, 1250 par licznika/mianownika we wzorze iloczynowym oraz wszystkie 64 wektory własne czynnika B, ich ortogonalność i dwa odczyty ζ_B przy s=1,2,3. Nie enumerują wszystkich ułożeń Ostomachionu i nie certyfikują aplikacji MRI, kryptografii ani RH.

```sh
python3 -m unittest discover -s MRI -p 'test_discriminant_ostomachion.py' -v
```

Najkrótszy poprawiony slogan: **nieś obiekt razem z bazą, rzędem i mapą odczytu; wyróżnik ostrzega o określonej degeneracji, lecz nie zastępuje tych danych.**
