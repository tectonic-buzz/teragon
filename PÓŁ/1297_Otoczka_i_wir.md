# Otoczka płynie, ale się rozciąga

> jeśli czegoś potrzebujesz, jestem tuż tuż obok, i jak fala spirala wiruje ;)

**↳ Pierwszy port był o przecieku. Ten jest o kształcie otoczki.**

Gdy śledzimy te same cząstki nieściśliwego płynu, objętość pozostaje stała. Odległości między cząstkami już nie muszą. Zniknięcie przepływu przez ruchomą granicę nie czyni wnętrza sztywnym.

W równaniu wirowości, bez siły zewnętrznej:

\[
\frac{D\omega}{Dt}=(\omega\cdot\nabla)u+\nu\Delta\omega.
\]

Pochodna materialna idzie z prądem. Po prawej nadal zostają rozciąganie/obracanie wirowości oraz dyfuzja. [MIT — struktury wirowe i rozciąganie](https://ocw.mit.edu/courses/2-20-marine-hydrodynamics-13-021-spring-2005/resources/lecture8/).

## Jeden dokładny przykład

Stałe \(a>0\), \(\rho>0\), \(\Omega_0\in\mathbb R\), brak siły masowej; lepkość stała. Niech

\[
\Omega(t)=\Omega_0 e^{at},\qquad
u=\left(-\tfrac a2x-\Omega y,\quad
\Omega x-\tfrac a2y,\quad az\right).
\]

W dwóch kierunkach płyn się zwęża, w trzecim wydłuża, a wokół trzeciej osi obraca.

\[
\nabla\cdot u=0,\qquad
\omega=\nabla\times u=(0,0,2\Omega),\qquad
\frac{D\omega}{Dt}=a\omega.
\]

To nie tylko wybrane pole prędkości: z ciśnieniem

\[
p=-\frac{\rho}{2}
\left[
\left(\frac{a^2}{4}-\Omega^2\right)(x^2+y^2)+a^2z^2
\right]+p_0(t)
\]

spełnia równania nieściśliwego Naviera–Stokesa punktowo. Dla \(u=A(t)x\):

\[
A'+A^2=\operatorname{diag}
\left(\tfrac{a^2}{4}-\Omega^2,\,
\tfrac{a^2}{4}-\Omega^2,\,
a^2\right)=-\frac1\rho\nabla^2p,
\qquad \Delta u=0.
\]

Właśnie warunek \(\Omega'=a\Omega\) kasuje antysymetryczną część przyspieszenia, której nie można zastąpić gradientem ciśnienia.

## Ta sama objętość, inna długość

Oznaczmy \(s=e^{at}\). Mapa ruchu to \(x(t)=F(t)X\), gdzie

\[
F(t)=R_{\theta(t)}
\operatorname{diag}(s^{-1/2},s^{-1/2},s),\qquad
\theta(t)=\frac{\Omega_0}{a}(s-1).
\]

\(R_\theta\) obraca w płaszczyźnie \(xy\). Mamy

\[
\det F=1,\qquad
\omega(t)=F(t)\omega(0)=s\,\omega(0).
\]

Równość dla wirowości dotyczy tego przykładu, w którym \(\Delta\omega=0\); nie usuwamy lepkości z ogólnego równania.

Przy \(s=2\): objętość bez zmiany, długość osiowa ×2, pole przekroju poprzecznego ÷2, wirowość ×2 (jeśli początkowo niezerowa). Zapas \(\tfrac12\int|\omega|^2\,dV\) w materialnej porcji rośnie ×4. Nic nie musi przepłynąć przez jej granicę.

## ζ jako dodatkowy odczyt — dokładnie nazwany

Weźmy tensor deformacji \(C=F^\top F\). Jego wartości własne są bezwymiarowymi kwadratami wydłużeń:

\[
C=\operatorname{diag}(s^{-1},s^{-1},s^2),\qquad
\zeta_C(q):=\operatorname{tr}(C^{-q})
=2s^q+s^{-2q}.
\]

To **skończona zeta spektralna tensora**, nie zeta Riemanna i nie korektor błędów.

Objętość daje \(\det C=1\), rząd daje \(\zeta_C(0)=3\): oba odczyty nie zmieniają się. Natomiast

\[
\zeta_C(1)\big|_{s=1}=3,\qquad
\zeta_C(1)\big|_{s=2}=\frac{17}{4}.
\]

**↳ Objętość mówi „tyle samo”, ten odczyt ζ mówi „inaczej rozciągnięte”.**

Ale \(\Omega_0\) w \(C\) nie występuje. Dwa przepływy o tym samym \(a\), jeden bez obrotu, drugi z obrotem, mają identyczne \(C(t)\) i identyczne wszystkie \(\zeta_C(q)\), a różną wirowość. Zeta tego tensora nie zastąpi pomiaru obrotu. Znowu: odczyt zależy od tego, czego jest odczytem.

## Kto płaci?

Dla \(\mu=\rho\nu>0\) i \(D=(A+A^\top)/2\):

\[
2\mu D:D=3\mu a^2>0.
\]

Lepkość rozprasza energię, choć \(\Delta u=0\). Zerowa dywergencja stałego naprężenia lepkiego nie oznacza zerowej pracy naprężeń na brzegu ani zerowej dyssypacji.

Pole liniowe na całej przestrzeni ma nieskończoną energię. Na wyciętym obszarze działa otoczenie; nie mamy izolowanej maszyny produkującej wir za darmo. Wzrost jest wykładniczy w czasie, nie osobliwy w skończonym czasie. Ten przykład nie spełnia globalnych warunków problemu milenijnego. [Warunki Clay](https://www.claymath.org/wp-content/uploads/2022/02/MPPc.pdf).

[Osiem odtwarzalnych kontroli](../NS/check_stretching_envelope.py): dokładna arytmetyka wymierna dla wskazanych parametrów, w tym kontrola negatywna „ta sama ζ, różny obrót”. Ogólne tożsamości wyprowadzono powyżej; skończony test nie zastępuje dowodu ich ogólności.

---

> Cuando estas dando vueltas acordate, es la misma palabra hacer un relajo, y relajarse
>
> Reloj, mide tiempo

**↳ Reloj. Tylko który zegar właśnie czytamy?**

W tym przykładzie faza obrotu ma tempo \(\dot\theta=\Omega_0e^{at}\), a logarytm wydłużenia ma tempo \(\frac{d}{dt}\log s=a\). Wspólny czas \(t\), dwa różne odczyty ruchu. Przy \(\Omega_0>0\) kolejne pełne obroty zajmują coraz mniej czasu; liczba obrotów nie jest liniowym zegarem.

\[
\theta=\frac{\Omega_0}{a}(s-1),\qquad
t=\frac1a\log\left(1+\frac{a\theta}{\Omega_0}\right)
\quad(\Omega_0\ne0).
\]

Tutaj \(\theta\) oznacza fazę rozwiniętą, z zachowaną liczbą obrotów, nie sam kąt modulo \(2\pi\). Odczyt czasu wymaga również znanych \(a\), \(\Omega_0\) i początku pomiaru.

A relaksacja? Nie wynika z samego obrotu: ten model rozciąga i wzmacnia wir. Lepkość rozprasza energię, ale otoczenie wykonuje pracę. Słowne sąsiedztwo podpowiedziało pytanie; rachunek rozdzielił odpowiedzi.

---

**↳ Poprawka do mojego „zegara z tej ζ nie odzyskamy”: którego zegara?**

Obrotu faktycznie nie: \(\Omega_0\) zostało zgubione. Ale dla znanego \(a>0\) i gałęzi \(t\ge0\) odczyt

\[
Z(t)=\zeta_C(1)=2e^{at}+e^{-2at},\qquad
Z'(t)=2a(e^{at}-e^{-2at})
\]

jest ściśle rosnący dla \(t>0\). Pozwala więc odzyskać czas od nieodkształconego stanu. Przykładowo \(Z=17/4\) daje \(e^{at}=2\), czyli \(t=\log2/a\). Nie wymaga to znajomości obrotu.

Ta odwrotność ma warunki: bez znanego \(a\) odczyt wyznacza tylko iloczyn \(at\). W pobliżu początku

\[
Z(t)=3+3a^2t^2+O(t^3),
\]

więc odwrotność pozostaje ciągła, ale jej czułość liniowa \(dt/dZ\) rośnie bez ograniczenia przy \(Z\downarrow3\). Nie ma tam stałego ograniczenia wzmocnienia błędu proporcjonalnego do błędu odczytu. Jednoznaczność i dobre uwarunkowanie to osobne pytania.

Z kolei zegar fazowy czytany tylko modulo \(2\pi\) gubi licznik obrotów. Dla \(\Omega_0>0\), \(0\le\phi<2\pi\) i \(k=0,1,\ldots\):

\[
t_k=\frac1a\log\left(1+\frac{a}{\Omega_0}(\phi+2\pi k)\right)
\]

to różne chwile o tym samym fazorze \(e^{i\phi}\). Nawet gładkość ruchu nie odzyska obrotów schowanych między rzadkimi próbkami bez dodatkowego ograniczenia prędkości fazowej.

[check_phase_clock.py](../NS/check_phase_clock.py): siedem kontroli numerycznych odwrotności, utraty obrotów, nieznanego tempa i czułości przy początku. To nie jest korekcja danych, których instrument nie zarejestrował — to rozdzielenie tego, jakie dane wystarczają do którego zegara.

---

> Rozróżnia, jeśli ma dodakowe własne bicie
>
> głowa w jedną, głowa w drógą i patrz na punkt odbicia
>
> jak takiego nie ma, to se pomyśl i jest

**↳ Własne bicie: odniesienie plus porównanie, nie samo tykanie.**

Rozbudujmy instrument. Oprócz \(C\) mierzy fazor obrotu \(q(t)=e^{i\theta(t)}\), względem wzorca \(r(t)=e^{i\omega_r t}\). Ich zespolone porównanie to

\[
b=q\overline r,\qquad
\operatorname{Im}(\overline b\,\dot b)=\Omega_0e^{at}-\omega_r.
\]

Przy znanym \(a,t,\omega_r\) odzyskujemy

\[
\Omega_0=e^{-at}\big[\operatorname{Im}(\overline b\,\dot b)+\omega_r\big].
\]

To rozróżnia poprzednich bliźniaków: przy \(a=\omega_r=1\), \(t=\log2\), oba mają \(\zeta_C(1)=17/4\), ale \(\Omega_0=1\) daje tempo różnicy faz \(1\), a \(\Omega_0=2\) daje \(3\). Informację wnosi pomiar fazy obrotu. Para \((\zeta_C,r)\) bez tego pomiaru nadal ich nie rozróżnia; sam moduł \(|b|=1\) również nie.

Punkt zerowy fazy można wybrać umownie. Wspólna zmiana \(q\mapsto e^{i\alpha}q\), \(r\mapsto e^{i\alpha}r\) nie zmienia \(b\). Wirtualne odniesienie jest legalne; wirtualna odpowiedź badanego przepływu nie zastępuje pomiaru.

**↳ Dwie strony: prosty model dwóch projekcji.**

Dla zespolonego odczytu \(z=X+iY\) wybierzmy osie pod kątami \(\pm\beta\):

\[
m_+=X\cos\beta+Y\sin\beta,\qquad
m_-=X\cos\beta-Y\sin\beta.
\]

Gdy \(\sin(2\beta)\ne0\),

\[
X=\frac{m_++m_-}{2\cos\beta},\qquad
Y=\frac{m_+-m_-}{2\sin\beta}.
\]

To dwa odczyty tego samego stanu — jednoczesne albo z uwzględnionym ruchem między nimi. Dla \(\beta=\pi/4\) osie są prostopadłe; przeciwne kierunki na jednej osi nie dają drugiej składowej. Jeśli wcześniej zostało tylko \(C\) lub moduł, obracanie samego układu współrzędnych brakującej fazy nie odtworzy.

Nadal potrzebne jest rozróżnienie próbek od ciągłego przebiegu: własny wzorzec nie usuwa obrotów utraconych między próbkami. Test pokazuje dwa różne \(\Omega_0\) z identycznym \(b\) na obu końcach przedziału. Z kolei rzeczywista intensywność interferencji \(|q+r|^2=2+2\operatorname{Re}b\) daje tylko cosinus różnicy faz, nie jej pełny znak.

[check_reference_beat.py](../NS/check_reference_beat.py): siedem kontroli numerycznych porównania z wzorcem, dwóch projekcji oraz ich ograniczeń. To model bez szumu; nie dowód nowego czujnika ani odzyskiwania niezarejestrowanych danych przez samą zetę.
