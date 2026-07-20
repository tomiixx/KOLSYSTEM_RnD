# KOLSYSTEM - księga identyfikacji wizualnej

Wersja 1.0, lipiec 2026.

## 1. Idea marki

`KOLSYSTEM` jest jednym, niepodzielonym słowem. Nazwa łączy **KOL** (kolej) oraz **SYSTEM**
(obszar kompetencji), ale podział komunikuje kolor, a nie znak interpunkcyjny:

- `KOL` - biel na ciemnym tle,
- `SYSTEM` - żółty Safety Yellow,
- na jasnym tle cały wordmark jest grafitowy.

Marka komunikuje rzetelną inżynierię systemów, w których bezpieczeństwo, niezawodność,
weryfikacja i dowody zgodności mają znaczenie krytyczne.

## 2. Sygnet 2oo3

Sygnet przedstawia trzy wejścia zbiegające się do węzła decyzji i walidacji. Odwołuje się do
architektury majoryzatora 2oo3, redundancji, weryfikacji i odpowiedzialności systemowej.

Uproszczony favicon ma grubsze elementy i nie zawiera znaku walidacji. Dzięki temu zachowuje
czytelność przy 16 px. Nie zastępuj pełnego sygnetu faviconem w materiałach drukowanych.

## 3. Rodzina logo

| Wariant | Tło | Plik SVG |
|---|---|---|
| Lockup podstawowy | grafit, antracyt, granat | `kolsystem-lockup-primary.svg` |
| Lockup jasny | biel, jasna szarość | `kolsystem-lockup-light.svg` |
| Wordmark podstawowy | grafit, antracyt, granat | `kolsystem-wordmark-primary.svg` |
| Wordmark jasny | biel, jasna szarość | `kolsystem-wordmark-light.svg` |
| Wordmark biały mono | ciemne zdjęcie, grawer, tłoczenie | `kolsystem-wordmark-mono-white.svg` |
| Wordmark grafitowy mono | biel, żółty, jasne zdjęcie | `kolsystem-wordmark-mono-black.svg` |
| Sygnet podstawowy | zastosowania kwadratowe | `kolsystem-symbol-primary.svg` |
| Sygnet na żółtym | jasne kanały i akcent marki | `kolsystem-symbol-on-yellow.svg` |

Pliki SVG i PDF zawierają wordmark zamieniony na krzywe. Nigdy nie odtwarzaj logo przez
wpisanie nazwy fontem.

## 4. Pole ochronne i rozmiary minimalne

- Lockup: minimalne pole ochronne wynosi połowę wysokości sygnetu z każdej strony.
- Wordmark bez sygnetu: minimalne pole ochronne odpowiada wysokości wielkiej litery `K`.
- Wordmark: minimum 90 px na ekranie lub 24 mm w druku.
- Sygnet: minimum 16 px na ekranie lub 6 mm w druku.

Jeżeli miejsce jest mniejsze, użyj samego sygnetu. Nie ściskaj lockupu.

## 5. Kolor

| Nazwa | HEX | RGB | CMYK roboczy | Rola |
|---|---|---|---|---|
| Safety Yellow | `#FFD200` | 255 / 210 / 0 | 0 / 18 / 100 / 0 | akcent, `SYSTEM`, węzeł decyzji |
| Graphite | `#14181D` | 20 / 24 / 29 | 32 / 17 / 0 / 89 | tło główne, tekst na jasnym |
| Anthracite | `#1B2129` | 27 / 33 / 41 | 34 / 20 / 0 / 84 | panele na ciemnym |
| Navy | `#0F1726` | 15 / 23 / 38 | 61 / 39 / 0 / 85 | kontekst kolejowy |
| Off White | `#F5F7FA` | 245 / 247 / 250 | 2 / 1 / 0 / 2 | tekst na ciemnym, jasne tło |

Wartości CMYK są wartościami roboczymi. Wynik zależy od profilu ICC, papieru i technologii
druku. Przed nakładem wykonaj proof. Nie deklaruj odpowiednika Pantone bez osobnej próby.

## 6. Dostępność i kontrast

Zmierzony kontrast WCAG:

- Safety Yellow na Graphite: `12,28:1`,
- Off White na Graphite: `16,61:1`,
- Graphite na Off White: `16,61:1`,
- Safety Yellow na Off White: `1,35:1` - nie stosować dla tekstu ani istotnych symboli.

Na jasnym tle używaj grafitowego wordmarku. Żółty może pozostać akcentem dekoracyjnym,
ale nie może być jedynym nośnikiem informacji.

## 7. Typografia

| Krój | Wagi | Zastosowanie |
|---|---|---|
| Chakra Petch | 500, 600, 700 | nagłówki, wyróżnienia, komunikaty marki |
| Titillium Web | 400, 600, 700 | tekst ciągły, opisy i dokumenty |
| JetBrains Mono | 400, 500, 600 | dane techniczne, normy, etykiety |

Fonty desktopowe znajdują się w `brand/fonts/desktop/`, a wersje WOFF2 strony w
`assets/fonts/`. Wszystkie trzy rodziny są udostępniane na licencji SIL Open Font License.

## 8. Zastosowania cyfrowe

- Open Graph / social share: 1200 x 630 px.
- Avatar: 512 x 512 px.
- Ikona aplikacji: 192 x 192 px i 512 x 512 px.
- Apple Touch Icon: 180 x 180 px, pełne tło bez wstępnego zaokrąglenia narożników.
- Favicon: SVG oraz ICO z rozmiarami 16, 32, 48 i 64 px.

Do internetu preferuj SVG. PNG wybieraj tam, gdzie platforma nie obsługuje wektorów.

## 9. Wizytówka

Wizytówka firmowa jest materiałem ogólnym, ponieważ w projekcie nie ma zatwierdzonego imienia,
stanowiska i bezpośrednich danych pracownika.

- format netto: 90 x 50 mm,
- format ze spadem: 96 x 56 mm,
- spad: 3 mm z każdej strony,
- bezpieczny margines: minimum 4 mm od linii cięcia,
- PDF: dwie strony, CMYK, wektory i osadzone fonty,
- TrimBox: 90 x 50 mm,
- BleedBox i MediaBox: 96 x 56 mm.

PDF nie deklaruje zgodności PDF/X, ponieważ właściwy wariant PDF/X i profil wyjściowy powinny
zostać uzgodnione z konkretną drukarnią. Źródła SVG pozostają w RGB i służą do edycji; do
produkcji używaj dostarczonego PDF albo wykonaj kontrolowaną konwersję w aplikacji DTP.

## 10. Zasady użycia

### Należy

- używać wariantu przeznaczonego dla danego tła,
- zachować proporcje, pole ochronne i rozmiar minimalny,
- skalować z SVG lub PDF,
- zachować dokładny podział koloru po `KOL`,
- wykonać proof przed drukiem.

### Nie należy

- dodawać separatora pomiędzy `KOL` i `SYSTEM`,
- rozciągać, ściskać, pochylać ani obracać logo,
- zmieniać kolejności lub proporcji lockupu,
- dodawać cienia, obrysu, gradientu albo efektu 3D,
- stosować żółtego wordmarku na białym tle,
- używać przypadkowych odcieni żółtego.

## 11. Zarządzanie plikami

Nadrzędne są pliki SVG. Eksporty tworzy `brand/tools/build_brand_assets.py`. Po każdej zmianie
źródeł uruchom generator, sprawdź PDF-y wizualnie i zweryfikuj, że strona nie odwołuje się do
`brand/`. Aktualizując system, zwiększ numer wersji w dokumentacji oraz generatorze.
