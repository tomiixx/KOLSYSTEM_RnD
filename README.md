# KOLSYSTEM – strona internetowa

Statyczna strona firmowa KOLSYSTEM. Repozytorium zawiera wyłącznie pliki niezbędne do publikacji serwisu.

## Struktura

```text
.
|-- assets/
|   |-- brand/  # logo i favicon wykorzystywane przez stronę
|   |-- css/    # arkusze stylów
|   |-- fonts/  # lokalnie hostowane fonty WOFF2
|   `-- js/     # skrypty strony
|-- index.html
|-- polityka-prywatnosci.html
|-- robots.txt
`-- sitemap.xml
```

## Uruchomienie lokalne

```powershell
python -m http.server 8000
```

Następnie otwórz `http://localhost:8000/`.
