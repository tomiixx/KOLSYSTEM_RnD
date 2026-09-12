# Edytowalna wizytówka KOLSYSTEM

- `KOLSYSTEM-wizytowka-awers-edytowalna.svg` - przód wizytówki.
- `KOLSYSTEM-wizytowka-rewers-edytowalna.svg` - tył wizytówki.

Otwórz SVG w edytorze grafiki wektorowej obsługującym ten format, np. Inkscape.
Narzędziem tekstowym zmienisz treści, a narzędziem zaznaczania przesuniesz elementy
i zmienisz ich kolory. Logo pozostaje grafiką wektorową z literami w krzywych.
Kod QR również jest wektorowy; po zmianie adresu strony trzeba wygenerować nowy kod.

Fonty są osadzone w SVG do podglądu w przeglądarce. Przed edycją w programie
graficznym zainstaluj dołączone do ZIP pliki TTF z folderu `fonty`, ponieważ
nie każdy edytor odczytuje fonty osadzone w SVG. Licencje znajdują się obok fontów.
W repozytorium te same fonty są dostępne w `brand/fonts/desktop`.

Wymiar strony to 96 × 56 mm ze spadem 3 mm z każdej strony.
Po przycięciu wizytówka ma 90 × 50 mm, jak na pierwotnym podglądzie.
Pliki edycyjne używają RGB. Przy przygotowaniu nowego PDF do druku uwzględnij
spad i wymagania kolorystyczne drukarni.

Zmiany w SVG nie aktualizują automatycznie istniejącego PDF ani generatora marki.
Ponowny eksport poleceniem `python brand/tools/build_editable_business_card.py`
odtwarza SVG z bieżącego PDF i nadpisuje pliki edycyjne, dlatego własne warianty
zapisuj pod innymi nazwami.
