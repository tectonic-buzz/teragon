# Delta Diraca z bieguna funkcji zeta Riemanna

2026-09-09. Osobna notatka ogólna, poza wątkiem tektonicznym.
Dokładny wniosek z prostego bieguna ζ oraz granicy jądra Cauchy'ego;
bez założenia hipotezy Riemanna. Nie jest to deklaracja pierwszeństwa wyniku.

## Wzór

Dla ε>0 i t∈ℝ niech

\[
D_\varepsilon(t)=\frac{1}{2\pi}\operatorname{Re}\!\left[
\zeta(1+\varepsilon+it)-\zeta(1-\varepsilon+it)
\right].
\]

Wówczas

\[
\boxed{D_\varepsilon\xrightarrow[\varepsilon\downarrow0]{\mathcal D'(\mathbb R)}\delta_0.}
\]

To granica dystrybucyjna, czyli

\[
\forall\varphi\in C_c^\infty(\mathbb R),\qquad
\lim_{\varepsilon\downarrow0}\int_{\mathbb R}
D_\varepsilon(t)\varphi(t)\,dt=\varphi(0).
\]

Delta nie jest tutaj zwykłą funkcją z przypisaną wartością ∞ w zerze.

## Dowód i normalizacja

Jedynym biegunem ζ jest s=1, prosty, o residuum 1. Stąd

\[
\zeta(s)=\frac{1}{s-1}+H(s),\qquad H\in\mathcal O(\mathbb C).
\]

[DLMF 25.2: biegun i rozwinięcie Laurenta](https://dlmf.nist.gov/25.2).

Część biegunowa różnicy daje dokładnie

\[
K_\varepsilon(t)=\frac{1}{2\pi}\left(
\frac{1}{\varepsilon+it}-\frac{1}{-\varepsilon+it}
\right)=\frac{\varepsilon}{\pi(\varepsilon^2+t^2)}.
\]

\[
\int_{\mathbb R}K_\varepsilon(t)\,dt=1,\qquad
K_\varepsilon(0)=\frac{1}{\pi\varepsilon},\qquad
\lim_{\varepsilon\downarrow0}K_\varepsilon(t)=0\quad(t\ne0).
\]

Po podstawieniu t=εu i zbieżności zdominowanej:

\[
\int_{\mathbb R}K_\varepsilon(t)\varphi(t)\,dt
=\int_{\mathbb R}\frac{\varphi(\varepsilon u)}{\pi(1+u^2)}\,du
\longrightarrow\varphi(0).
\]

Pozostała część to

\[
R_\varepsilon(t)=\frac{1}{2\pi}\operatorname{Re}\!\left[
H(1+\varepsilon+it)-H(1-\varepsilon+it)
\right],\qquad D_\varepsilon=K_\varepsilon+R_\varepsilon.
\]

Dla każdego zwartego J⊂ℝ ograniczoność H′ na odpowiednim zwartym
prostokącie daje

\[
\sup_{t\in J}|R_\varepsilon(t)|=O_J(\varepsilon).
\]

Zatem całka Rεφ dąży do zera. To kończy dowód. Normalizacja całki do 1
dotyczy Kε; nie twierdzimy, że całka pełnego Dε po ℝ jest równa 1
dla każdego skończonego ε. Zbieżność testujemy na funkcjach o zwartym
nośniku. [DLMF 1.17: ciągi deltowe i ich interpretacja](https://dlmf.nist.gov/1.17).

## Residuum wyznacza masę

Przy założeniach a,r∈ℝ oraz H∈𝒪(ℂ), dla

\[
f(s)=\frac{r}{s-a}+H(s)
\]

ten sam dowód daje

\[
\frac{1}{2\pi}\operatorname{Re}\!\left[
f(a+\varepsilon+it)-f(a-\varepsilon+it)
\right]
\xrightarrow[\varepsilon\downarrow0]{\mathcal D'(\mathbb R)}r\,\delta_0.
\]

Mechanizm nie jest wyłączną własnością ζ. W przypadku zety r=1.
