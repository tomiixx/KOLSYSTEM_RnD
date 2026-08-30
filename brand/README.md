# KOLSYSTEM - pakiet marki

Kompletny pakiet identyfikacji wizualnej KOLSYSTEM Sp. z o.o. Wersja 1.0, lipiec 2026.

## Szybki wybór pliku

| Potrzeba | Zalecany plik |
|---|---|
| Logo na ciemnym tle | `logos/svg/kolsystem-lockup-primary.svg` |
| Logo na jasnym tle | `logos/svg/kolsystem-lockup-light.svg` |
| Logo pionowe (sygnet nad napisem) na ciemne tło | `logos/svg/kolsystem-stacked-primary.svg` |
| Logo pionowe (sygnet nad napisem) na jasne tło | `logos/svg/kolsystem-stacked-light.svg` |
| Sam napis na ciemnym tle | `logos/svg/kolsystem-wordmark-primary.svg` |
| Sam napis na jasnym lub żółtym tle | `logos/svg/kolsystem-wordmark-light.svg` |
| Logo do programu biurowego | odpowiedni plik z `logos/png/` |
| Logo wektorowe do druku | odpowiedni plik z `logos/pdf/` lub `logos/svg/` |
| Avatar | `digital/icons/avatar-512.png` |
| Favicon | `digital/icons/kolsystem-favicon.svg` lub `digital/icons/favicon.ico` |
| Grafika do udostępniania strony (Open Graph) | `digital/social/kolsystem-social-share-1200x630.png` |
| Baner LinkedIn (profil / szeroki baner social) | `digital/social/kolsystem-linkedin-banner-1584x396.png` |
| Okładka strony firmowej LinkedIn | `digital/social/kolsystem-linkedin-cover-1128x191.png` |
| Wizytówka do drukarni | `print/business-card/KOLSYSTEM-business-card-90x50mm-bleed3mm-CMYK.pdf` |
| Zasady marki | `guidelines/KOLSYSTEM-brand-guidelines.pdf` |

## Zawartość

```text
brand/
|-- digital/
|   |-- icons/          # favicony, avatar, ikony aplikacyjne
|   `-- social/         # grafiki social (odbicie hero strony): OG 1200x630,
|                       #   baner LinkedIn 1584x396, okładka firmowa 1128x191 - SVG + PNG
|-- fonts/
|   |-- desktop/        # pełne TTF do materiałów marki
|   `-- licenses/       # licencje SIL Open Font License
|-- guidelines/         # pełne zasady w Markdown i księga PDF
|-- logos/
|   |-- svg/            # pliki nadrzędne i zalecane źródła
|   |-- png/            # eksporty rastrowe z przezroczystością
|   `-- pdf/            # eksporty wektorowe do biura i DTP
|-- print/
|   `-- business-card/  # wizytówka, proof i edytowalne źródła
`-- tools/              # generator wszystkich eksportów
```

## Źródła i eksport

Nadrzędne są pliki SVG w `logos/svg/`, `digital/` i `print/**/source/`. Eksporty PNG/PDF
oraz kopie produkcyjne strony można odtworzyć poleceniem:

```powershell
python -m pip install -r brand/tools/requirements.txt
python brand/tools/build_brand_assets.py
```

Generator:

- buduje pełne fonty desktopowe z podzbiorów WOFF2 strony,
- eksportuje logo do PNG i PDF,
- generuje logo pionowe oraz grafiki social odzwierciedlające hero strony
  (nagłówek + realny diagram cyklu życia EN 50126) modułem `build_hero_assets.py`;
  tekst jest zapieczony w krzywe, więc pliki SVG nie zależą od fontów,
- generuje favicony, ikony i grafikę social,
- tworzy dwustronny PDF wizytówki CMYK z TrimBox i spadem,
- tworzy księgę marki PDF,
- kopiuje minimalny zestaw produkcyjny do `assets/brand/`.

Nie edytuj ręcznie plików wygenerowanych, jeśli zmiana powinna przetrwać kolejny eksport.

## Ważne rozdzielenie

`brand/` jest kompletnym pakietem do wykorzystania przez drukarnię, studio DTP, partnera lub
zespół marketingu. `assets/brand/` zawiera wyłącznie lekkie kopie wymagane przez stronę.
Serwis internetowy nie odwołuje się bezpośrednio do katalogu `brand/`.

## Kontakt i odpowiedzialność

Przed dużym nakładem drukarskim zawsze wykonaj proof z profilem ICC wskazanym przez drukarnię.
Pytania dotyczące marki: `biuro@kolsystem.pl`.
