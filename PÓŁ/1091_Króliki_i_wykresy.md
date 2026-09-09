# Króliki i wykresy

Kilka oddzielnych obliczeń, każde samodzielne.

**Dwa odczyty ζ na bajtach.**

Dla bajtów xᵢ ∈ {0,…,255}:

  A₀(x) = diag(xᵢ+1),   A₁(x) = diag(i·(xᵢ+1)),   ζ_A(s) = tr A^{−s}

W s=−1: c₀(x) = Σ(xᵢ+1), c₁(x) = Σ i(xᵢ+1).

Kontrola negatywna: (2,2,2,2) i (3,0,3,2) mają oba odczyty takie same — błąd (1,−2,1,0) niewidoczny. Dwie zmiany (2,2,2)→(3,2,3) dają dekoder zwracający (3,0,3) — legalnie wyglądające niepoprawienie. Mechanizmem są **dwie sumy momentów zapisane jako odczyty ζ**. Nic więcej.

**Möbius, F₁, czyli czy skaner jest butelką Kleina.**

Bustrofedon EPI — każda linia k-space czytana w przeciwnym kierunku niż poprzednia — to odbicie ślizgowe (x,y)↦(−x,y+1). Iloraz torusa przez wolne działanie ℤ/2 = butelka Kleina ✓.

Ale kluczowa korekta: **duch siedzi w N/2, bo podział parzyste/nieparzyste to dwa kosety podgrupy 2ℤ — nietrywialny koset ląduje w N/2; trywialny (DC) w 0.** Pozycja ducha to koset przesunięcia, nie punkt stały inwersji. Ghost/main = tan(φ/2) — **pół kąta**, bo nakrycie jest dwukrotne; ten sam mechanizm, dla którego spinor potrzebuje 4π.

Wolna inwolucja daje czystą dekompozycję parzystości bez residuów; ramifikowana daje dekompozycję *plus* ograniczenie w punkcie rozgałęzienia. Ta sama grupa, inny stabilizator, inna księgowość.

> Nie przechowuj kocyklu — wylicz go z nakładek.

Linie nieparzyste i parzyste widzą ten sam obiekt, więc φ daje się z ich zgodności (metody bezreferencyjne: Buonocore–Gao). Estymuj holonomię z danych, nie z kalibracji.
