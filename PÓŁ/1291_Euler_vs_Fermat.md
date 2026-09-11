# Euler vs Fermat

Fermat twierdził, że F_5 = 2^32 + 1 jest pierwszy. Euler wykazał, że jest nie — przez faktoryzację: 641 dzieli F_5.

Dowód:

  F_5 = 2^32 + 1 = 4294967297
  2^32 mod 641 = −1 (mod 641)
  (z tego: F_5 mod 641 = 0)

I to jest dowód: 2^32 + 1 = 4294967297 = 641 · 6700417.

Zatem:

  641 = 5·2^7 + 1 = 5^4 + 2^4

  Euler: (a+b)ⁿ ≡ aⁿ + bⁿ (mod a)
  Fermat: błąd.
