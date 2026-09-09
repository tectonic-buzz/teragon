# Pętla niwelacyjna

<!-- source: TERAGON_CODEX_CONDUIT.md; sha256: 26717daefcff87e05781fefbd9f9955e71fc09858dcd9e1c09cb0513b1f0d59c -->

<!-- fragment: 20631-20647 -->
### 2. Pętla: domyka się potencjał, niekoniecznie surowa niwelacja

Dla ustalonego, zachowawczego pola:
\[
\oint dW=0.
\]
Natomiast lokalny przyrost niwelacyjny opisany przez
\[
\alpha=-\frac{dW}{g}
\]
nie musi być formą dokładną, ponieważ \(g\) zmienia się przestrzennie. **Surowa pętla niwelacyjna może więc nie domknąć się nawet przy idealnym pomiarze.** Dopiero odpowiednio przeliczone różnice potencjału powinny się sumować do zera. NOAA opisuje właśnie przejście od odczytów niwelacyjnych i grawitacji do wyrównywanych liczb geopotencjalnych. [NOAA — korekty niwelacji](https://www.ngs.noaa.gov/PUBS_LIB/TMNOSNGS34.html).

Kodrzewo pasuje konkretnie: dla spójnego grafu z \(12\) wierzchołkami i \(17\) krawędziami jest
\[
17-12+1=6
\]
niezależnych cykli. To sześć warunków zgodności. **Nazwanie każdego niedomknięcia obstrukcją Čecha wymaga dodatkowego modelu sklejania**; błąd pomiarowy nie staje się automatycznie nieusuwalną przeszkodą topologiczną.
<!-- /fragment -->
