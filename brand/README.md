# System identyfikacji — KOLSYSTEM Sp. z o.o.

Logo w kierunku **typograficznym**: mocny, niepodzielony znak słowny w foncie strony
(Chakra Petch 700), w którym **złożenie nazwy wyraża kolor**, a nie separator.

## Koncept

`KOLSYSTEM` — jedno słowo, bez dwukropka. Nazwa to złożenie **KOLej + SYSTEM**;
zamiast rozdzielać oba człony znakiem interpunkcyjnym, oddaje je **kontrast koloru**:

- **`KOL`** — biały tusz (`#f5f7fa`),
- **`SYSTEM`** — żółty „safety" (`#FFD200`).

Dzięki temu marka czyta się jako jedna całość, a jednocześnie niesie swój rodowód.
Znika przy tym wieloznaczność dwukropka z v1 (kojarzonego z adresem URL, godziną
czy proporcją) i „gadżetowy" charakter sparowanych kropek.

> Poprzednia wersja z „dwukropkiem systemowym" jest zarchiwizowana w [`v1/`](v1/).

## Kolory

| Rola | Nazwa | HEX |
|------|-------|-----|
| Tło główne / tusz na jasnym | grafit | `#14181d` |
| Panele na ciemnym | antracyt | `#1b2129` |
| Sekcja kolejowa | granat | `#0f1726` |
| Tusz „KOL" na ciemnym | biel | `#f5f7fa` |
| **Tusz „SYSTEM" / akcent** | **żółty safety** | **`#FFD200`** |
| Tekst na żółtym | grafit | `#14181d` |

## Typografia

- **Chakra Petch 700** — wordmark i nagłówki (`--font-display`).
- **Titillium Web** — tekst ciągły (`--font-body`).
- **JetBrains Mono** — dane techniczne, etykiety (`--font-mono`).

W plikach logo litery są **skonwertowane na krzywe** (kontury wektorowe), więc renderują się
identycznie niezależnie od tego, czy font jest zainstalowany. Na stronie logo składane jest
z żywego fontu + koloru CSS (`.logo-text` + `.logo-sys`), aby pozostać ostre i lekkie.

## Sygnet

Symbol **majoryzatora 2oo3** (redundancja / głosowanie większościowe) w zaokrąglonym kwadracie:
**trzy białe węzły wejściowe** zbiegają się do **żółtego węzła‑majoryzatora** ze znakiem
walidacji (√). Odwołuje się do rdzenia pracy KOLSYSTEM — **bezpieczeństwa funkcjonalnego**
(architektury fault‑tolerant), **weryfikacji i walidacji** oraz **systemów** — bez wątku kolejowego.
Zastępuje wcześniejszy monogram i daje marce czytelny znak pod avatar / app‑icon / favicon.

Favicon używa **uproszczonego wariantu** (grubsze linie, bez wewnętrznego √), aby pozostać
czytelny do 16 px.

## Pliki

| Plik | Zastosowanie |
|------|--------------|
| `kolsystem-wordmark-primary.svg` | Podstawowy — „KOL" biały + „SYSTEM" żółty, **na ciemnym tle** |
| `kolsystem-wordmark-light.svg` | **Na jasnym tle** — jednokolorowy grafit (żółć nie ma kontrastu na jasnym; podział koloru żyje na ciemnym) |
| `kolsystem-wordmark-mono-white.svg` | Jednokolorowy biały (knockout, foto, tłoczenie) |
| `kolsystem-wordmark-mono-black.svg` | Jednokolorowy grafit — **również na żółtym tle** |
| `kolsystem-icon.svg` | Sygnet 2oo3 w zaokrąglonym kwadracie — avatar, social, app icon |
| `kolsystem-icon-on-yellow.svg` | Sygnet 2oo3 na żółtym rewersie (grafit) |
| `kolsystem-favicon.svg` | Sygnet 2oo3, wariant uproszczony — favicon (czytelny do 16 px) |

Rastrowe (wygenerowane z sygnetu): [`../favicon.ico`](../favicon.ico) (16/32/48/64) oraz
[`../apple-touch-icon.png`](../apple-touch-icon.png) (180×180).

## Pole ochronne i rozmiary minimalne

- **Pole ochronne:** dookoła logo zachowaj wolną przestrzeń równą **wysokości wielkiej litery „K"**.
- **Wordmark — min. szerokość:** 90 px (ekran) / 24 mm (druk).
- **Sygnet — min.:** 16 px (ekran) / 6 mm (druk).

## Zasady (do / don't)

**Rób:**
- Na ciemnym tle używaj wersji `primary` (biały „KOL" + żółty „SYSTEM").
- Na jasnym tle używaj `light` (grafit), a na żółtym — `mono-black`.
- Utrzymuj jeden odcień żółci `#FFD200` w całym systemie.
- Dbaj o kontrast tła (WCAG AA).

**Nie rób:**
- Nie wstawiaj z powrotem dwukropka ani żadnego separatora między „KOL" a „SYSTEM".
- Nie koloruj „SYSTEM" na żółto na jasnym tle (brak kontrastu) — użyj wtedy `light`.
- Nie rozstrzeliwuj, nie ściskaj, nie pochylaj, nie obracaj wordmarku.
- Nie dodawaj cienia, obrysu, gradientu ani efektów.
- Nie zmieniaj podziału koloru (np. „KOL" na żółto).

## Do zrobienia (opcjonalnie)

- `../og-image.png` (1200×630) — warto odświeżyć zgodnie z nowym znakiem (bez dwukropka).

---

Pliki źródłowe wygenerowane z `fonts/chakra-petch-700-latin.woff2` (Chakra Petch, OFL).
