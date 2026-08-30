# KOLSYSTEM – strona internetowa

Statyczna strona firmowa KOLSYSTEM. Repozytorium zawiera wyłącznie pliki niezbędne do publikacji serwisu.

## Struktura

```text
.
|-- assets/
|   |-- brand/  # logo, favicon i grafika Open Graph
|   |-- css/    # arkusze stylów
|   |-- fonts/  # lokalnie hostowane fonty WOFF2
|   `-- js/     # skrypty strony
|-- brand/      # pakiet marki (generowany, patrz brand/tools/)
|-- en/         # wersja angielska - GENEROWANA, nie edytuj ręcznie
|-- i18n/
|   `-- en.json # słownik tłumaczeń polski -> angielski
|-- tools/
|   `-- build_i18n.py
|-- index.html
|-- polityka-prywatnosci.html
|-- robots.txt
`-- sitemap.xml
```

## Dwujęzyczność

Polskie pliki w katalogu głównym są **jedynym źródłem prawdy** dla treści
i układu. Wersja angielska w `en/` jest z nich generowana - nigdy jej nie
edytuj bezpośrednio, bo najbliższy build nadpisze zmiany.

Po każdej zmianie treści w `index.html` lub `polityka-prywatnosci.html`:

```powershell
python tools/build_i18n.py --extract   # pokaże teksty bez tłumaczenia
python tools/build_i18n.py             # zbuduje en/
```

Nowe lub zmienione zdanie polskie zgłasza się jako brakujące tłumaczenie -
dopisz je do `i18n/en.json` i zbuduj ponownie. Dzięki temu obie wersje nie
mogą się po cichu rozjechać.

Komunikaty JavaScriptu (walidacja formularza, treść wiadomości e-mail) idą za
atrybutem `lang` dokumentu - słownik `STRINGS` na początku
`assets/js/script.js`. Adresy: `/` po polsku, `/en/` po angielsku, powiązane
znacznikami `hreflang` i przełącznikiem w nagłówku.

Angielska polityka prywatności zawiera adnotację, że wiążąca pozostaje wersja
polska. Wstawia ją generator, nie ma jej w polskim źródle.

## Uruchomienie lokalne

```powershell
python -m http.server 8000
```

Następnie otwórz `http://localhost:8000/`.
