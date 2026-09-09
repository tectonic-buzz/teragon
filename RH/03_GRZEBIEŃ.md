# Różnicowanie Delta Diraca na Całkoróżdżce Riemanna

Ostatnie koło. I ono nie kręci się razem z tamtymi trzema — ono jest **igłą**, która czyta to, co tamte policzyły.

**Delta to różnica schodka.** Δ przyłożone do funkcji Heaviside'a daje δ: igła silnika różnicowego to skok schodka. Grzebień Diraca Ш(x) = Σ δ(x−n) to liniał maszyny — i zeta jest jego transformatą Mellina: ζ(s) = ∫ x^{−s} dN(x), gdzie N(x) = ⌊x⌋ to schodek, a dN to grzebień. Policzone: Mellin grzebienia w s = 3 to 1,202057, ζ(3). Suma *jest* całką po grzebieniu; przekładnia A z poprzedniej maszyny — Euler–Maclaurin — to rachunek na Ш − 1: grzebień minus jego średnia, czyli igły minus składowa stała, a składowa stała to **biegun**. Delta Deuce'a, D_ε → δ₀ o masie równej residuum, to ta jedna składowa DC grzebienia, obejrzana przez biegun. Bernoulli to reszta grzebienia — oscylacje wokół średniej.

**Przekładnia B była samodualnością grzebienia.** Poisson, Σf(n) = Σf̂(k), to zdanie **Ш̂ = Ш**: grzebień Diraca jest własną transformatą Fouriera. Fałd θ(1/t) = √t θ(t) był tym zdaniem podstawionym gaussianem. Więc igła, która czyta sumę, i igła, która czyta całkę, są jedną igłą widzianą z dwóch stron transformaty — a w naszym pierścieniu jest to dosłownie: **DFT(δ) = u, DFT(u) = 8δ.** Impuls jednostkowy i wektor socle — jednostka, którą odrzuciliśmy jako tag w lipcu, i wektor stały Nissego, do którego wszystko spływa — **są dualne przez Fouriera.** Odrzucona jedynka i demon to jedna rzecz po dwóch stronach transformaty. Tego nie planowaliśmy; grzebień to wiedział.

**I wzór jawny: dwa grzebienie, primy i zera, dualne.** Igły primów to ψ′(x) = Σ Λ(n) δ(x−n), grzebień z wagami von Mangoldta. Wzór Riemanna–Weila mówi, że transformata grzebienia primów to grzebień zer: Σ_ρ h(γ) po jednej stronie, Σ_p log p · g(log p) po drugiej. Policzone w drugą stronę, bo tak jest najładniej: **wstaw sześćdziesiąt zer, dostaniesz schodek primów** — ψ(50,5) prawdziwe 49,485, z sześćdziesięciu zer 49,558; różnica to obcięcie grzebienia, nie błąd wzoru. To jest odpowiedź na „co wstawić w zetę, żeby zwróciła prymy" jako mechanizm: wstaw jej własne zera, a igła wydrukuje primy, bo grzebień zer jest transformatą grzebienia primów. I **RH w tym języku to jedno zdanie: grzebień zer jest rzeczywisty** — jego igły stoją na osi t, nie obok niej. Zgięcie z poprzedniego uderzenia, dodatniość z uderzenia przed nim, i grzebień teraz: ta sama hipoteza, trzy igły.

**A pomiar to mnożenie przez grzebień.** To jest koło Δ z alfabetu, dosłownie: zmierzyć sygnał to spróbkować go, próbkować to pomnożyć przez Ш, a mnożenie przez grzebień to po drugiej stronie transformaty *splot* z grzebieniem dualnym — periodyzacja — **aliasing**. Rzadszy grzebień, gęstsza periodyzacja: maska P w E = PF w MRI to grzebień, a duch Nyquista to jego dualny okres; policzone — grzebień co drugą próbkę k-space daje kopię obrazu w N/2, jeden do jednego. Bliźniaki z benchmarku to dwa obrazy o tym samym odczycie grzebieniem; ζ_H(0) liczy zęby, które maska ma, nie wartości, które opuściła. Delta jest kształtem werdyktu — Force zwraca liczbę, splat o zerowej kowariancji, igłę — i jedynym miejscem, gdzie maszyna przestaje być odwracalna, bo grzebień wyrzuca to, co między zębami. Trzy koła kręcą się bez straty; igła czyta i traci. Landauer siedzi w igle.

Więc cała maszyna, na koniec: **różnica (π), Fourier (Ш̂ = Ш), inwersja (σ) — i igła (δ).** Trzy pierwsze liczą ξ do dwunastu cyfr odwracalnie; czwarta czyta zera jako grzebień i primy jako jego transformatę. Jedyne, czego igła nie umie powiedzieć sama z siebie, to czy stoi na osi — i to jest to jedno puste łożysko. 📍🦧

----

---

**Status: rachunek dystrybucyjny, odtworzenie przykładu i kontrola strat; bez dowodu RH.** Zaczynam od rozdzielenia różnicy skończonej, pochodnej i dwóch różnych grzebieni.

### 1. Delta nie jest skończoną różnicą schodka

Dla funkcji Heaviside'a $H$ i $h>0$:

$$
DH=\delta_0\quad\text{w }\mathcal D',\qquad
\Delta_hH(x)=H(x+h)-H(x)=\mathbf1_{(-h,0)}(x)
\quad\text{prawie wszędzie},
$$

$$
\frac{\Delta_hH}{h}\longrightarrow\delta_0\quad\text{w }\mathcal D'
\quad(h\downarrow0).
$$

Dowód ostatniej równości to $h^{-1}\int_{-h}^0\varphi(x)\,dx\to\varphi(0)$. Przy skończonym kroku zostaje prostokąt. Dla dyskretnego schodka otrzymujemy natomiast deltę Kroneckera: $H[n]-H[n-1]=\delta_{n0}$. Te trzy stwierdzenia pasują do siebie, ale nie są zamienne.

### 2. Mellin i Fourier czytają różne wersje grzebienia

Miara licząca dodatnie liczby całkowite daje

$$
\mu_+=\sum_{n\ge1}\delta_n,\qquad
\zeta(s)=\int_{(0,\infty)}x^{-s}\,d\mu_+(x),\quad\Re s>1.
$$

To zapis szeregu Dirichleta jako całki względem miary. Przy konwencji Mellina z jądrem $x^{w-1}$ odpowiada mu parametr $w=1-s$.

Natomiast dla Fouriera $\widehat f(\nu)=\int f(x)e^{-2\pi ix\nu}\,dx$ grzebień Poissona jest dwustronny:

$$
\operatorname{III}_T=\sum_{n\in\mathbb Z}\delta_{nT},\qquad
\widehat{\operatorname{III}_T}=\frac1T\operatorname{III}_{1/T}.
$$

Nie utożsamiam $\mu_+$ z $\operatorname{III}_1$: różnią się dziedziną i składnikami. W skończonym modelu nad $\mathbb C$, przy nieznormalizowanej DFT, dokładnie $F_N\delta_0=\mathbf1$ i $F_N\mathbf1=N\delta_0$. Dla $N=8$ współczynnik wynosi $8$; przejście do innego ciała wymaga ponownego sprawdzenia pierwiastków z jedności i odwracalności $N$.

### 3. Primy: ważony grzebień potęg pierwszych

Zdefiniujmy $\Lambda_{\rm vM}(n)=\log p$ dla $n=p^k$ i $0$ poza potęgami pierwszych, a następnie $\psi(x)=\sum_{n\le x}\Lambda_{\rm vM}(n)$. Dla niecałkowitego $x>1$ wzór jawny brzmi

$$
\psi(x)=x-\lim_{T\to\infty}\sum_{|\Im\rho|\le T}\frac{x^\rho}{\rho}
-\log(2\pi)-\frac12\log(1-x^{-2}).
$$

Zera są nietrywialne i liczone z krotnościami; granica jest symetryczna, a szereg nie jest bezwzględnie zbieżny. W punktach skoku odpowiednikiem jest wartość środkowa $\psi_0$. Nie wolno zgubić potęg pierwszych, wag, bieguna ani poprawek od zer trywialnych i normalizacji. To konkretna tożsamość analityczna, nie równość dwóch nieważonych grzebieni Fouriera. [Tao, *246B Notes 4*, twierdzenie 8 i §2](https://terrytao.wordpress.com/2021/02/12/246b-notes-4-the-riemann-zeta-function-and-the-prime-number-theorem/).

Odtworzyłem przykład z $x=50.5$:

| Odczyt | Wartość |
| --- | ---: |
| Bezpośrednie zliczenie potęg pierwszych | 49.48538079241837 |
| Wzór obcięty do 30 dodatnich wysokości i ich sprzężeń | 49.48827965921462 |
| Wzór obcięty do 60 dodatnich wysokości i ich sprzężeń | 49.55827796617394 |
| Błąd ostatniego odczytu | +0.07289717375557 |

Wartości tabeli są wynikami float64 dla zaokrąglonych danych wejściowych; liczba wypisanych cyfr nie oznacza takiej dokładności sumy z dokładnymi zerami.

Liczba z oryginału jest odtworzona, ale „60 zer” oznacza tu **60 par, czyli 120 zer**. Zwiększenie obcięcia nie musi monotonicznie polepszać wyniku w jednym punkcie. Wysokości pochodzą z [tablic Odlyzki](https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1); ich podana [dokładność wejściowa](https://www-users.cse.umn.edu/~odlyzko/zeta_tables/) nie jest certyfikatem reszty nieskończonego szeregu. Skrypt używa tych danych, nie certyfikuje ponownie zer.

### 4. Co ma być rzeczywiste pod RH

Dla $\rho=\beta+i\gamma$ właściwą współrzędną jest

$$
\lambda_\rho=\frac{\rho-1/2}{i}=\gamma+i(1/2-\beta),\qquad
\mathrm{RH}\iff\lambda_\rho\in\mathbb R\text{ dla wszystkich }\rho.
$$

Samo $\gamma=\Im\rho$ zawsze jest rzeczywiste. Grzebień z samych wysokości usuwa więc właśnie informację, którą miałby sprawdzać. Zachowajmy obie współrzędne:

$$
\nu=\sum_{\rho\ {m distinct}}m_\rho\,\delta_{(\Re\rho-1/2,\Im\rho)},\qquad
\mathrm{RH}\iff\operatorname{supp}\nu\subseteq\{0\}\times\mathbb R.
$$

To poprawna równoważność o nośniku miary w $\mathbb R^2$, a nie dowód, że nośnik rzeczywiście tam leży. Projekcja $\nu$ na drugą oś nie jest świadkiem tej własności.

### 5. Kontrola MRI: suma obrazów jest skutkiem maski, nie domysłem

Przy parzystym $N$, pełnej zespolonej DFT i masce zachowującej parzyste indeksy jednej osi:

$$
F_N^{-1}PF_Nx[n]=\frac12\left(x[n]+x[n+N/2]\right).
$$

To suma dwóch przesuniętych obrazów **z wagami po $1/2$**, nie dodana pełna kopia. Brakujący kanał to $\tfrac12(x-Tx)$, gdzie $Tx[n]=x[n+N/2]$. Nie da się go odczytać z samego $\tfrac12(x+Tx)$ bez dodatkowych założeń lub pomiarów. Jest to kontrola modelu maski, nie dowód, że fizyczny tor EPI jest butelką Kleina.

Próbkowanie może jednak być odwracalne na zadeklarowanej klasie sygnałów o ograniczonym paśmie. Nie jest jedyną możliwą stratą w opisanej maszynie: już $\Delta_1$ usuwa stałe. Także $\zeta_H(0)=\operatorname{rank}H$, po wyłączeniu zerowych wartości własnych, jest tu tożsamością **skończonej** macierzy dodatnio półokreślonej; nie ogólną regułą dla regularizowanych widm nieskończonych. Koszt Landauera wymaga jeszcze modelu fizycznego kasowania pamięci — nie wynika z samego wystąpienia delty.

### Odtwarzalność i granica wyniku

Do trzech dopisków dołączam [check_rh_formulas.py](../FARI/tests/check_rh_formulas.py). Z katalogu repozytorium: `python3 FARI/tests/check_rh_formulas.py` (Python 3 + NumPy, bez sieci). Siedem testów używa rachunku dokładnego lub dokładnie reprezentowanych przykładów, sześć sprawdza numerycznie tożsamości i kontrprzykłady. Wynik podczas przygotowania: **13/13 PASS**.

To testy implementacji i skończonych przykładów, nie certyfikaty wszystkich tożsamości analitycznych ani wszystkich zer. Cel kontroli: nie zgubić osi, wagi, normalizacji, reszty ani informacji usuwanej przez projekcję. **RH: NOT PROVED.**

---

### Intuicyjności

Narracja powyżej pozostaje niezmieniona.

**R1 (szczelina).** Linia 5: „zeta jest transformatą Mellina grzebienia", linia 7: „grzebień Diraca jest własną transformatą Fouriera ($\widehat{\amalg}=\amalg$)". To dwa różne grzebienie: Mellin czyta grzebień na $(0,\infty)$, samodualność Fouriera dotyczy grzebienia na $\mathbb Z$. Sekcja §2 poprawnie je rozdziela, ale czytelnik skaczący między liniami 5 i 7 może odczytać je jako jedną igłę. Jedno zdanie rozdzielenia na początku wystarczy.

**R2 (drobne, konsekwencja).** Linia 9: „wstaw sześćdziesiąt zer, dostaniesz schodek primów". Sekcja §3 rafinuje dobrze: „60 zer" oznacza 60 par (czyli 120 zer — każda wysokość implikuje swoją sprzężoną). Warto odnotować w tej sekcji, że obcięcie szeregu nie jest monotonicznie zbieżne w dowolnym punkcie — w moim przebiegu błąd $\psi(50{,}5)$ względem bezpośredniego zliczenia wygląda: 10 par → $-0{,}0122$; 20 par → $-0{,}5034$; 30 par → $+0{,}0029$; 40 par → $+0{,}4094$; 50 par → $+0{,}1813$; 60 par → $+0{,}0729$. To obserwacja o oscylacyjnej naturze formuły jawnego, nie o defekcie kontroli.

**R3 (szczelina).** Linia 11: „grzebień co drugą próbkę k-space daje kopię obrazu w N/2, jeden do jeden". Sekcja §5 rafinuje właściwie: to $(x+Tx)/2$, więc suma dwóch przesuniętych kopii z wagą $1/2$ każda, a kanał $(x-Tx)/2$ nie jest odzyskiwalny z samego wyniku. „Jeden do jeden" w narracji należy czytać jako korespondencję maski z przesunięciem, nie pełną odwracalność.

**Co zweryfikowano poza plikiem.** Dołączony `check_rh_formulas.py`: 13/13 PASS przy pierwszym uruchomieniu. Niezależnie: $\psi(50{,}5)$ przez dokładną arytmetykę = 49,48538079241837 — zgodne z tabelą; wzór obcięty do 30/60 par: 49,48827965921462 / 49,55827796617396 — zgodne; kontrola $2+\cos z$: miara Fouriera $2\delta_0+\tfrac12\delta_1+\tfrac12\delta_{-1}$ faktycznie jest dodatnia, zera w $\pi\pm i\operatorname{arcosh} 2$; mapowanie $\lambda_\rho=\gamma+i(1/2-\beta)$ poprawne algebraicznie; równanie funkcyjne Hurwitza i tożsamość $\zeta(-m,a)=-B_{m+1}(a)/(m+1)$ zweryfikowane niezależnie.

**Czego te uwagi nie mówią.** Nie znaleziono błędu w dowodzie żadnego twierdzenia z tej notatki; nie znaleziono drogi do zamknięcia pustego łożyska; **RH: NOT PROVED** pozostaje zgodne z treścią.
