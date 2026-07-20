# Wizytówka KOLSYSTEM

Dwustronna, ogólna wizytówka firmowa. Nie zawiera fikcyjnego pracownika ani stanowiska.

## Pliki

- `KOLSYSTEM-business-card-90x50mm-bleed3mm-CMYK.pdf` - gotowy plik drukarski, awers i rewers,
- `preview/KOLSYSTEM-business-card-preview.png` - proof ekranowy obu stron,
- `source/kolsystem-business-card-front.svg` - edytowalny awers RGB,
- `source/kolsystem-business-card-back.svg` - edytowalny rewers RGB.

## Parametry produkcyjne

- netto: 90 x 50 mm,
- brutto: 96 x 56 mm,
- spad: 3 mm,
- bezpieczny margines: 4 mm od linii cięcia,
- kolor gotowego PDF: CMYK,
- strony: 1 - awers, 2 - rewers,
- TrimBox: 90 x 50 mm,
- BleedBox i MediaBox: 96 x 56 mm,
- fonty: osadzone,
- kod QR: celowo pominięty, aby materiał nie zależał od niezatwierdzonego celu przekierowania.

## Personalizacja

Aktualny projekt jest gotową wizytówką firmową. Wersję osobową należy przygotować dopiero po
zatwierdzeniu imienia i nazwiska, stanowiska, adresu e-mail oraz telefonu bezpośredniego.
Zmiany nanieś w źródle rewersu i analogicznie w funkcji `_card_back()` generatora, aby źródło
oraz PDF pozostały zgodne.

## Przekazanie do drukarni

Przed nakładem potwierdź z drukarnią:

1. wymagany profil ICC i wariant PDF/X,
2. rodzaj i gramaturę papieru,
3. dopuszczalny poziom całkowitego pokrycia farbą,
4. orientację rewersu przy druku dwustronnym,
5. ewentualne uszlachetnienie.

Dostarczony PDF nie deklaruje PDF/X, ponieważ profil i standard należy dobrać do konkretnego
procesu produkcyjnego. Ma poprawne wymiary, spad, TrimBox oraz robocze wartości CMYK.
