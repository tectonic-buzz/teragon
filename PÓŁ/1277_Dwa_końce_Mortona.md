# Dwa końce adresu Mortona

<!-- source: TERAGON_CODEX_CONDUIT.md; sha256: 26717daefcff87e05781fefbd9f9955e71fc09858dcd9e1c09cb0513b1f0d59c -->

<!-- fragment: 31415-31446 -->
### 2. Morton działa — ale są dwa kierunki przybliżania

Odtworzyłem dokładnie:

\[
(19,30,5,2,1)\;\xleftrightarrow{\ M\ }\;3217781.
\]

Dodatkowo przeszło **20 000 nowych prób** dla pięciu współrzędnych 16-bitowych: pakowanie, rozpakowanie i oba poniższe rodzaje obcięcia.

Przy przeplocie od najmłodszych bitów:

\[
M(u)=\sum_{b\ge0}\sum_{a=0}^{4}u_{a,b}\,2^{5b+a}.
\]

Mamy dwie różne, dokładne tożsamości — działania po prawej są współrzędnościowe:

\[
\boxed{M(u)\bmod2^{5k}=M(u\bmod2^k)}
\]

\[
\boxed{\left\lfloor\frac{M(u)}{2^{5k}}\right\rfloor
=M\!\left(\left\lfloor\frac{u}{2^k}\right\rfloor\right)}.
\]

Pierwsza zachowuje **klasę kongruencji**: najmłodsze bity, bliskość 2-adyczną. Druga usuwa szczegóły przestrzenne: daje **komórkę grubszego podziału**.

Fable połączył te dwa odczyty w jeden „prefiks”. Można czytać prefiksy od obu końców, ale otrzymuje się inne sąsiedztwa. Przykładowo \(15\) i \(16\) są sąsiadami liczbowymi, a już ich najmłodsze bity się różnią. Morton nie daje więc gwarancji, że każdy przestrzenny sąsiad ma długi wspólny prefiks. [Opis przeplotu i indeksowania przestrzennego, University of Maryland](https://www.cs.umd.edu/class/spring2018/cmsc425/Lects/lect08-encl-indices.pdf).

A historyczny szczegół pasuje tu wyjątkowo dobrze: raport Mortona z 1966 roku dotyczył **geodezyjnej bazy danych i sekwencjonowania plików**. To udokumentowane zastosowanie, nie dopowiedziana genealogia. [Oryginalny raport IBM](https://dominoweb.draco.res.ibm.com/0dabf9473b9c86d48525779800566a39.html).
<!-- /fragment -->
