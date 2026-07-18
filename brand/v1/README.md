# System identyfikacji — KOLSYSTEM Sp. z o.o.

Logo w kierunku **typograficznym**: mocny znak słowny w foncie strony (Chakra Petch),
z jednym elementem akcentowym — **żółtym „dwukropkiem systemowym"** między `KOL` a `SYSTEM`.

## Koncept

`KOL : SYSTEM` — dwukropek to celowe, wielowarstwowe odniesienie:

- **kod / namespace** (`kol::system`) — język inżynierów MATLAB/Simulink, C/C++, embedded;
- **węzeł sygnału / punkt kontrolny** — dwa punkty łączące dwie części nazwy;
- **relacja / zależność** — „coś : coś", jak w specyfikacji wymagań.

Nazwa firmy to złożenie **KOLej + SYSTEM**; dwukropek elegancko oddziela oba człony,
nie rozbijając czytelności marki. Jedyny kolor akcentowy to żółty „safety" `#FFD200`.

## Kolory

| Rola | Nazwa | HEX |
|------|-------|-----|
| Tło główne / tusz na jasnym | grafit | `#14181d` |
| Panele na ciemnym | antracyt | `#1b2129` |
| Sekcja kolejowa | granat | `#0f1726` |
| Tusz na ciemnym | biel | `#f5f7fa` |
| **Akcent (dwukropek)** | **żółty safety** | **`#FFD200`** |
| Tekst na żółtym | grafit | `#14181d` |

## Typografia

- **Chakra Petch 700** — wordmark i nagłówki (`--font-display`).
- **Titillium Web** — tekst ciągły (`--font-body`).
- **JetBrains Mono** — dane techniczne, etykiety (`--font-mono`).

W plikach logo litery są **skonwertowane na krzywe** (kontury wektorowe), więc renderują się
identycznie niezależnie od tego, czy font jest zainstalowany. Na stronie logo składane jest
z żywego fontu + akcentu CSS (`.logo-colon`), aby pozostać ostre i lekkie.

## Pliki

| Plik | Zastosowanie |
|------|--------------|
| `kolsystem-wordmark-primary.svg` | Podstawowy — biały tusz + żółty dwukropek, **na ciemnym tle** |
| `kolsystem-wordmark-light.svg` | Grafitowy tusz + żółty dwukropek, **na jasnym tle** |
| `kolsystem-wordmark-mono-white.svg` | Jednokolorowy biały (knockout, foto, tłoczenie) |
| `kolsystem-wordmark-mono-black.svg` | Jednokolorowy grafit — **również na żółtym tle** |
| `kolsystem-icon.svg` | Sygnet `K:S` w zaokrąglonym kwadracie — avatar, social, app icon |
| `kolsystem-icon-on-yellow.svg` | Sygnet na żółtym rewersie |
| `kolsystem-favicon.svg` | Sygnet z ciaśniejszym marginesem — favicon (czytelny do 16 px) |

Rastrowe (wygenerowane z sygnetu): `../favicon.ico` (16/32/48/64) oraz `../apple-touch-icon.png` (180×180).

## Pole ochronne i rozmiary minimalne

- **Pole ochronne:** dookoła logo zachowaj wolną przestrzeń równą **wysokości wielkiej litery „K"**.
- **Wordmark — min. szerokość:** 90 px (ekran) / 24 mm (druk).
- **Sygnet — min.:** 16 px (ekran) / 6 mm (druk).

## Zasady (do / don't)

**Rób:**
- Używaj wersji `primary` na ciemnym, `light` na jasnym, `mono-black` na żółtym.
- Zachowaj żółty wyłącznie na dwukropku (jeden akcent = dyscyplina).
- Dbaj o kontrast tła (WCAG AA).

**Nie rób:**
- Nie zmieniaj koloru ani proporcji dwukropka, nie zamieniaj go na zwykły znak `:`.
- Nie rozstrzeliwuj, nie ściskaj, nie pochylaj, nie obracaj wordmarku.
- Nie dodawaj cienia, obrysu, gradientu ani efektów.
- Nie koloruj liter na żółto (żółte są tylko kropki dwukropka).
- Nie umieszczaj logo na tle o niskim kontraście lub na zdjęciu bez przyciemnienia.

## Do zrobienia (opcjonalnie)

- `../og-image.png` (1200×630) — warto odświeżyć zgodnie z nowym znakiem przy okazji.

---

Pliki źródłowe wygenerowane z `fonts/chakra-petch-700-latin.woff2` (Chakra Petch, OFL).
