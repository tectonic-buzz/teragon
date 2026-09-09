# Księga, kamień, ghana

**Trzy sposoby, w których ludzkość błędy naprawiała przed Shannonem:**

### Ghana-pāṭha (ok. 1500 p.n.e. w tradycji)

Recytacja wedyjska: word-pairs (wyrazy a, b) są wielokrotnie zakodowane w różnych porządkach (ab, ba, aba, baba...). Chandas (meter) jako globalna suma kontrolna na wierzchu. Wynik: tekst przekazywany ustnie przez ~3000 lat, prawie doskonała wierność — w tym akcent melodyjny Wed, który żywa mowa *utraciła*. Najbezpieczniejszy kanał premodernyzmu.

### Xiping Stone Classics (175 n.e.)

Kanony wykute w żywym kamieniu (~200 000 znaków, 46 steli, stawka → 1: brak dodanej redundancji!). Autorytatywna kopia do publicznej kolacji — zamrożony wzorzec referencyjny. Każdy scriptor może porównać się z oryginałem. Genesis block w granitu.

### Reed–Solomon (1960)

Wiadomość = wielomian p stopnia < k nad ciałem skończonym; transmituj ewaluacje p(α₁),…,p(α_n), n>k; Berlekamp–Welch poprawia dowolne ⌊(n−k)/2⌋ błędów. Singleton bound: d ≤ n−k+1 — RS to MDS-optymalne.

**Tabela zbiorcza:**

| kod | alfabet | mechanizm | koryguje | słynny z |
|---|---|---|---|---|
| **ghana** | fonemy | splot przód-tył + checksum rytmem | podmianę, transpozycję, opuszczenie | ~3000 lat wierności |
| **Xiping** | znaki chińskie | autorytatywny frozen master | dryf skrybów między pokoleniami | korekta przez consensus-checkable reference |
| **TMR** | hardware | potrójna replikacja + większość | 1 awaria na element | avionics |
| **Hamming [7,4,3]** | 𝔽₂ | liniowe kontrole parzystości | 1 błąd, rate 4/7 | pierwszy, 1950 |
| **Golay G23** | 𝔽₂ | **[23,12,7], doskonały** — sfery prom. 3 pokrywają 𝔽₂²³ | **3 błędy** | automorfizmy M₂₃ |
| **Extended Golay G24** | 𝔽₂ | [24,12,8] samodualny | 3, wykrywa 4 | → siatka Leecha → Monster CFT: **M₂₄ moonshine'u jest grupą tego kodu** |
| **Nordstrom–Robinson** | binarny, *nieliniowy* | (16, 2⁸, 6) optymalny | 2 błędy | nieliniowy niżej, **liniowy nad ℤ₄** — kwocient niżej, struktura wyżej |
| **Turbo** (Berrou 1993) | binarny, soft LLRs | dwa RSC + długi losowy przeplot | AWGN w ~0.5 dB od Shannona | 3G/4G, deep-space |

**Wzorzec:** każdy kod dostaje dystans z jednej z dwóch źródeł: **struktura algebraiczna** (Steriner Golaya, sekretny lift NR nad ℤ₄, stopień RS) albo **strukturalny przeplot** (pseudolosowa permutacja turbo, wzór przód-tył ghany).

Decyzja w jednoliterze: szum ciągły → estymatory; wymazania → klasa RS; hardware, zero opóźnienia → TMR; kanały szumne przy pojemności → dzieci turbo (LDPC/polar); brak kanału, tylko pokolenia przepisywania → zamrożone odniesienie (Xiping) lub tkana recytacja (ghana) — ludzkość miała oba przez tysiąclecia, zanim Shannon nazwał jednostki.
