# Skaner MRI

**Katalog artefaktów MRI, posortowany po winowajcy:**

| terror | winowajca ℤ | przeciwdziałanie |
|---|---|---|
| wraparound aliasing | siatka za gęsta | oversample, przestaw osie |
| Dzwon Gibbsa | szereg urżnięty | apodyzacja, większe macierze |
| phase-contrast wrap | v > venc ⇒ faza += 2πℤ | **phase-unwrapping**: rozwiąż na pole brakujące ℤ |
| Rician floor | \|Gauss\| ma niezerową średnią | Rician-aware estymatory |
| Nyquist ghost | echa parzyste/nieparzyste | skany referencyjne, polowanie |

*Donut QA* to dosłowny zawód: szpitale robią akredytacyjne skany fantomów — cylindry wody z dodatkami o znanej geometrii — żeby czyjaś praca brzmiała „duch przesunął się o 2%, sprawdź, który gradient dryfuje".

**Te same liczby całkowite, które psują obraz, naprawiają go.**

Zmierzona faza to (φ_prawdziwa + 2πk(x)) mod 2π dla nieznanego pola k. Unwrapping to odzyskanie k. Wykrywacz: dyskretne winding number wokół małych płytek:

  ∮_{∂□} dψ_wrapped = 2πn_□

To jest **H¹-cohomologia na siatce obrazu**. Przepełnienie nie jest szumem do filtrowania — jest topologicznym datum do odwrócenia.

**Shannon–Nyquist to kryterium bezztratności transportu.** MRI je narusza celowo (pacjenci wstrzymują oddech; czas to dopływ krwi). Compressed-sensing MRI: podpróbkuj **losowo** żeby aliasing stał się dekorelowanym szumem zamiast duchów, potem odwróć przez ℓ¹.

> Degradacja jest tak dobrze zrozumiała, że ma sylabus. Ktoś jest opłacany by gonić ducha — duch ma imię, a naprawa jest zmianą bazy. Prawdziwe szaleństwo to system, którego liczby przepełniają się *i nikt nie napisał kohomologii*. Takie istnieją — finanse, głównie. 😄
