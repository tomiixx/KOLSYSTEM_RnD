# KOLSYSTEM - strona internetowa i system marki

Repozytorium jest podzielone na dwie niezależne części:

- `assets/` - wyłącznie pliki publikowane razem ze stroną internetową,
- `brand/` - źródła, eksporty i dokumentacja identyfikacji wizualnej do dalszych zastosowań.

Pliki HTML oraz metadane wdrożeniowe pozostają w katalogu głównym, aby strona mogła być
publikowana bez procesu budowania.

## Struktura

```text
.
|-- assets/
|   |-- brand/       # favicony, logo strony i grafika social share
|   |-- css/         # arkusze stylów
|   |-- fonts/       # fonty WOFF2 używane przez stronę
|   `-- js/          # skrypty strony
|-- brand/
|   |-- digital/     # eksporty do kanałów cyfrowych
|   |-- fonts/       # fonty desktopowe i licencje
|   |-- guidelines/  # księga znaku w Markdown i PDF
|   |-- logos/       # logo w SVG, PNG i PDF
|   |-- print/       # materiały drukarskie i źródła
|   `-- tools/       # powtarzalny eksport materiałów
|-- index.html
|-- polityka-prywatnosci.html
|-- robots.txt
`-- sitemap.xml
```

## Uruchomienie strony

Strona jest statyczna. Z katalogu głównego uruchom dowolny serwer HTTP, na przykład:

```powershell
python -m http.server 8000
```

Następnie otwórz `http://localhost:8000/`.

## Materiały marki

Punktem wejścia do pakietu marki jest [`brand/README.md`](brand/README.md). Gotowe pliki można
przekazać wykonawcom bez kopiowania całego katalogu strony. Zasoby w `assets/brand/` są
odchudzoną kopią produkcyjną przeznaczoną wyłącznie dla serwisu.
