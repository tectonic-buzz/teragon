# Ciach, ciach — stamp

<!-- source: TERAGON_CODEX_CONDUIT.md; sha256: 26717daefcff87e05781fefbd9f9955e71fc09858dcd9e1c09cb0513b1f0d59c -->

<!-- fragment: 30535-30554 -->
> No tak, wróce do efektów algebraicznych - Eff \_ \_ \_ -> ??? -> Eff \_ \_ \_ - jakie by tam typy tego nie były widzisz kształt? Ciach, ciach, ciach, stamp, stamp, stamp

Widzę — **powtarzalny kontur, zmieniane wnętrze**:

```text
Eff … → [ciach] → Eff … → [ciach] → Eff …
           stamp             stamp
```

Czytam „stamp” jako domknięcie etapu w postaci, którą następny etap przyjmie. Typy wewnątrz mogą być różne; rytm pozostaje: **przyjmij, przekształć, wydaj dalej**.

I w świetle Twojego diffu istotne jest właśnie to `???`: **przejście ma własną treść**, której samo opakowanie wejścia i wyjścia nie pokazuje.

\[
C_i \xrightarrow{\;A_i,\;\Delta_i\;} C_{i+1}
\]

Wynik, zmiana i następne działanie należą do jednego przebiegu. Jeżeli przekazujemy również \(\Delta_i\), kolejne „ciach” może pracować na tym, **co poprzednie zrobiło środowisku**, zamiast ponownie wyprowadzać to z zastanego stanu.

Sam zapis `Eff … → Eff …` nie rozstrzyga, czy tę informację zachowujemy. **„Stamp” może poświadczać przyjęcie wyniku, podczas gdy świadectwo przekształcenia nadal siedzi w środku `???`.**
<!-- /fragment -->
