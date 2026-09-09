# Dać się ponieść

> i najważniejsze, dać się ponieść.... wtedy najszybciej się płynie

**↳ Z prądem — ale bilans jedzie z nami.**

Nie wybieramy „drugiej połowy”, która ma gdzieś zniknąć. Wybieramy granicę obserwacji. Niech \(u\) będzie prędkością płynu, a \(w\) prędkością granicy poruszającego się obszaru \(V(t)\), obie w tym samym inercjalnym układzie.

Dla gładkiego płynu o stałej gęstości \(\rho\), z naprężeniem \(\sigma\), siłą masową na jednostkę masy \(f\) i zewnętrzną normalną \(n\):

\[
\frac{d}{dt}\int_{V(t)}\rho u\,dV
=-\int_{\partial V(t)}\rho u\,[(u-w)\cdot n]\,dS
+\int_{\partial V(t)}\sigma n\,dS
+\int_{V(t)}\rho f\,dV.
\]

Po lewej zmiana zasobu pędu. Po prawej: przepływ pędu z materią względem granicy, działanie otoczenia przez naprężenia, siły objętościowe. To bilans transportu Reynoldsa i pędu; [wyprowadzenie MIT](https://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec03/lecture3.html).

Gdy \(w=u\), śledzimy te same cząstki i pierwszy wyraz znika. **Brak przepływu materii przez otoczkę nie oznacza odcięcia sił od otoczenia.** Wystarcza nawet równość składowych normalnych, aby wyzerować ten strumień.

## Wir, który niesie

Przykład: jednorodny, nieściśliwy płyn Newtonowski obracający się jak ciało sztywne:

\[
u(x,y)=\Omega(-y,x),\qquad
p(x,y)=p_0+\tfrac12\rho\Omega^2(x^2+y^2),\qquad f=0.
\]

Pole jest stacjonarne, ale przyspieszenie materialne wynosi
\((u\cdot\nabla)u=-\Omega^2(x,y)\).
Ciśnienie rośnie na zewnątrz, więc jego siła działa do środka.
Symetryczna część gradientu prędkości jest zerowa: w tym szczególnym ruchu nie ma ścinania ani dyssypacji lepkościowej we wnętrzu.

Weźmy prostokąt \([1,3]\times[-1,1]\), jednostkową długość wzdłuż osi, \(\rho=3\), \(\Omega=2\), w spójnych jednostkach. Jego granica obraca się z prędkością kątową \(\alpha\Omega\). W chwili początkowej:

| Ruch granicy | Zmiana pędu wewnątrz | Strumień pędu na zewnątrz | Siła ciśnienia |
|---|---|---|---|
| nieruchoma, \(\alpha=0\) | \((0,0)\) | \((-96,0)\) | \((-96,0)\) |
| połowa prędkości, \(\alpha=1/2\) | \((-48,0)\) | \((-48,0)\) | \((-96,0)\) |
| z płynem, \(\alpha=1\) | \((-96,0)\) | \((0,0)\) | \((-96,0)\) |

W każdym wierszu **zmiana + strumień = siła**. Zmienia się rozdział rachunku między przechowywanie i przepływ, nie prawo fizyczne.

Porcja płynu daje się nieść: jej wektor pędu skręca, chociaż nic przez materialną otoczkę nie przecieka. Jej moment pędu względem osi pozostaje stały. Pęd liniowy i moment pędu to nie ten sam odczyt.

**↳ Żółw nie musi produkować całego ruchu, ale otoczenie nadal działa.**

To model niesionej porcji płynu, nie model aktywnie pływającego żółwia. Nie dowodzi najkrótszego czasu podróży do wybranego celu. Przepływ ścinający nadal może odkształcać porcję i rozpraszać energię, nawet gdy obserwator płynie razem z nią.

## Paragon z najbliższego portu

[check_moving_volume.py](../NS/check_moving_volume.py) zawiera siedem testów: dwie granice i pośrednie prędkości, obrócone położenia obszaru w tym samym układzie inercjalnym, nacisk bez przecieku, przepływ lokalny mimo zerowego bilansu masy, moment pędu, pomylenie prędkości granicy oraz różnicę obrotu i ścinania. Całki wielomianowe liczone są dokładnie na ułamkach wymiernych. Wynik: **7/7 PASS**.

To sprawdzenie konkretnego gładkiego rozwiązania i bilansu. Obrót liniowy na całej przestrzeni ma nieskończoną energię; nie podstawiamy go pod założenia milenijnego problemu Naviera–Stokesa. Wybranie ruchomego obszaru nie usuwa trudności kontroli gradientu w ogólnym przepływie.
