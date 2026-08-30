# Publikacja strony KOLSYSTEM na hostingu domena.pl

Ta instrukcja zastępuje obecną stronę WordPress nową, statyczną stroną HTML.
Nie zmienia domeny, DNS, kont pocztowych ani planu hostingowego.

## Co zostanie opublikowane

Do katalogu strony `/kolsystem.pl/kolsystem_pl/` trafią:

```text
.htaccess
assets/
en/
index.html
polityka-prywatnosci.html
robots.txt
sitemap.xml
```

Nie wgrywaj katalogów `brand/`, `i18n/` i `tools/` ani plików `README.md` i tej instrukcji - to źródła i narzędzia, nie treść serwisu. Katalog `en/` jest generowany (`python tools/build_i18n.py`), ale na serwer trafia. Plik `.htaccess` zachowuje
przekierowanie `www.kolsystem.pl` na `kolsystem.pl` oraz adresy starej strony:

- `https://kolsystem.pl/o-nas/` → sekcja „O firmie”;
- `https://kolsystem.pl/kontakt/` → sekcja „Kontakt”.

## Zanim zaczniesz

1. Zaplanuj publikację poza godzinami, w których zwykle pojawiają się zapytania
   od klientów.
2. Przygotuj lokalny folder na kopię, np.
   `C:\Users\szcze\Desktop\backup-kolsystem-2026-08-25`.
3. Upewnij się, że dane na nowej stronie są aktualne. W szczególności sprawdź
   adres firmy, adresy e-mail i numery telefonów.
4. Zapamiętaj, że obecny formularz kontaktowy otwiera program pocztowy
   odwiedzającego. Nie wysyła wiadomości automatycznie z serwera.

## 1. Utworzenie osobnego konta FTP

Nie zmieniaj haseł istniejących skrzynek e-mail ani nie używaj przypadkowego
loginu z listy dostępów.

1. Zaloguj się do [panelu hostingowego](https://hosting.domena.pl/).
2. W lewym menu kliknij **Loginy poczty i FTP**.
3. Kliknij **Dodaj login** lub **Nowy login**.
4. Wybierz typ konta **FTP** (nie „Poczta”).
5. Ustaw login, np. `kolsystem_ftp`, oraz długie, unikalne hasło.
6. Zapisz dane logowania w menedżerze haseł i kliknij **Zapisz**.

Jeżeli panel nie pokazuje możliwości wyboru typu „FTP”, nie zmieniaj istniejącego
loginu. Zrób zrzut tego ekranu i skorzystaj z obecnego konta FTP tylko wtedy,
gdy masz pewność, że nie jest ono równocześnie używane przez pocztę.

## 2. Nadanie kontu FTP dostępu do strony

1. W lewym menu wybierz **WWW → Strony WWW**.
2. Wybierz wirtualkę `kolsystem.pl`.
3. Otwórz zakładkę **Udzielanie dostępu**.
4. Z listy **Konto ftp** wybierz utworzone konto `kolsystem_ftp`.
5. Kliknij **udostępnij**.

Ta operacja nadaje loginowi dostęp do plików strony. Nie klikaj **udostępnij**
dla konta, którego nie rozpoznajesz.

## 3. Połączenie przez FileZilla

1. Otwórz FileZillę i wybierz **Plik → Menedżer stron → Nowy adres**.
2. Ustaw:

   | Pole | Wartość |
   | --- | --- |
   | Protokół | FTP |
   | Host | `ftp.kolsystem.pl` |
   | Szyfrowanie | „Użyj explicit FTP przez TLS, jeśli dostępne” |
   | Typ logowania | Normalny |
   | Użytkownik | `kolsystem_ftp` |
   | Hasło | Hasło utworzone w kroku 1 |

3. Kliknij **Połącz**.
4. W prawym panelu wejdź do `kolsystem.pl`, a następnie do `kolsystem_pl`.
   Pełna ścieżka to `/kolsystem.pl/kolsystem_pl/`.

Uwaga: katalog strony NIE jest katalogiem `/kolsystem.pl/`. Leży poziom niżej,
w `/kolsystem.pl/kolsystem_pl/`. Potwierdzono to, porównując rozmiar pliku
`license.txt` na serwerze (19 935 B) z plikiem serwowanym pod
`https://kolsystem.pl/license.txt`.

W `/kolsystem.pl/` leżą pozostałości nieużywanej strony statycznej z 2018 roku
(`css`, `images`, `js`, `index.html`) oraz katalog `.backupfiles201811090…`.
Nie wgrywaj tam nowej strony i nie kasuj tych plików — nie mają wpływu na to,
co widzi odwiedzający. Nie używaj też katalogu `public_html`; na tym hostingu
go nie ma.

## 4. Kopia bezpieczeństwa starego WordPressa

### Pliki strony

1. W lewym panelu FileZilli przejdź do utworzonego folderu kopii.
2. W prawym panelu, w katalogu `/kolsystem.pl/kolsystem_pl/`, zaznacz
   wszystkie pliki i katalogi obecnej strony.
3. Kliknij prawym przyciskiem i wybierz **Pobierz**.
4. Poczekaj, aż w dolnym panelu FileZilli nie będzie oczekujących ani
   nieudanych transferów.
5. Otwórz lokalny folder kopii i upewnij się, że są w nim m.in. `wp-content`,
   `wp-admin`, `wp-includes` oraz `wp-config.php`.

### Baza danych WordPressa

1. W panelu domena.pl kliknij **Bazy SQL → MySQL**.
2. Odszukaj bazę używaną przez WordPress. Jej nazwę i użytkownika można
   rozpoznać w pobranym pliku `wp-config.php` po wartościach `DB_NAME` i
   `DB_USER`.
3. Otwórz bazę w phpMyAdmin.
4. Wybierz **Eksport → Szybki → SQL → Wykonaj**.
5. Zachowaj plik `.sql` w tym samym lokalnym folderze kopii.

Nie usuwaj bazy danych ani kont pocztowych. Baza może pozostać na hostingu po
przełączeniu strony; będzie potrzebna do ewentualnego powrotu do WordPressa.

### Stan starej instalacji

Daty modyfikacji plików rdzenia WordPressa nie są spójne. Większość pochodzi
z 14.02.2020, ale `wp-signup.php` ma 7.08.2026, a `readme.html` 12.08.2026.
Pliki rdzenia jednej wersji powinny mieć wspólną datę. Do tego większość
plików PHP ma uprawnienia `0666`, czyli zapis dla wszystkich.

To nie jest dowód włamania, ale wystarczający powód, by traktować kopię jako
niepewną:

1. Trzymaj kopię lokalnie i nie udostępniaj jej w sieci.
2. Przeskanuj folder kopii programem antywirusowym.
3. Nie otwieraj plików PHP z kopii na serwerze ani w środowisku z PHP.
4. Po zakończonej migracji zmień hasło do panelu domena.pl.

Migracji to nie blokuje — usuwasz całą tę instalację, więc problem znika razem
z nią. Ma to natomiast znaczenie dla planu awaryjnego na końcu instrukcji.

## 5. Przełączenie na nową stronę

Zacznij ten krok dopiero, gdy lokalna kopia plików i eksport bazy są kompletne.

1. W katalogu `/kolsystem.pl/kolsystem_pl/` usuń pliki i katalogi
   WordPressa, w tym:

   ```text
   wp-admin/
   wp-content/
   wp-includes/
   index.php
   wp-config.php
   wp-*.php
   xmlrpc.php
   ```

2. Nie usuwaj katalogu `.well-known`, jeśli jest widoczny. Może być używany do
   obsługi certyfikatu SSL.
3. Usuń starą regułę WordPressa `.htaccess`, jeżeli istnieje.
4. W lewym panelu FileZilli otwórz katalog projektu:

   ```text
   C:\Users\szcze\Desktop\KOLSYSTEM_www
   ```

5. Wgraj do `/kolsystem.pl/kolsystem_pl/` dokładnie te elementy:

   ```text
   .htaccess
   assets/
   en/
   index.html
   polityka-prywatnosci.html
   robots.txt
   sitemap.xml
   ```

6. Poczekaj na zakończenie transferów i sprawdź, czy po prawej stronie
   FileZilli widać `index.html`, `.htaccess` oraz katalog `assets`.

## 6. Konfiguracja HTTPS i przekierowań

1. W panelu hostingowym kliknij **WWW → Certyfikaty SSL**.
2. Upewnij się, że certyfikat obejmuje `kolsystem.pl`. Obecna strona działa pod
   HTTPS, więc nie należy usuwać ani wyłączać istniejącego certyfikatu.
3. Plik `.htaccess` obsługuje wymuszenie HTTPS, przekierowanie
   `www.kolsystem.pl` na `kolsystem.pl` oraz stare adresy WordPressa. Zawiera
   też kompresję i nagłówki cache — każdy taki blok jest zabezpieczony
   warunkiem `IfModule`, więc brak modułu na serwerze nie wywoła błędu.
4. Nie zmieniaj rekordów DNS ani delegacji domeny — domena już wskazuje na ten
   hosting.

Jeśli po wgraniu `.htaccess` zobaczysz błąd 500, usuń tylko ten nowy plik,
przywróć poprzedni z kopii i zgłoś problem do pomocy domena.pl. Nie usuwaj
pozostałych nowych plików strony.

## 7. Kontrola po publikacji

Otwórz poniższe adresy w prywatnym oknie przeglądarki:

| Adres | Oczekiwany efekt |
| --- | --- |
| `https://kolsystem.pl/` | nowa strona KOLSYSTEM |
| `http://kolsystem.pl/` | przekierowanie na HTTPS |
| `https://www.kolsystem.pl/` | przekierowanie na `https://kolsystem.pl/` |
| `https://kolsystem.pl/o-nas/` | przekierowanie do sekcji „O firmie” |
| `https://kolsystem.pl/kontakt/` | przekierowanie do sekcji „Kontakt” |
| `https://kolsystem.pl/polityka-prywatnosci.html` | polityka prywatności |
| `https://kolsystem.pl/robots.txt` | plik robots.txt |
| `https://kolsystem.pl/sitemap.xml` | mapa strony XML |
| `https://kolsystem.pl/en/` | angielska wersja strony |
| `https://kolsystem.pl/en/privacy-policy.html` | angielska polityka prywatności |

Dodatkowo sprawdź:

1. Menu na komputerze i telefonie.
2. Linki telefoniczne i e-mailowe.
3. Formularz — pola wymagane powinny pokazać błędy, a poprawne zgłoszenie
   powinno otworzyć program pocztowy.
4. Baner cookies oraz ręczne wczytanie mapy po wyrażeniu zgody.
5. Certyfikat kłódki przy adresie strony.
6. Przełącznik PL/EN w nagłówku - w obie strony, na komputerze i telefonie.

## 8. Po publikacji

1. W Google Search Console prześlij ponownie adres:

   ```text
   https://kolsystem.pl/sitemap.xml
   ```

2. Przez co najmniej 14 dni zachowaj lokalną kopię WordPressa i bazę danych.
3. Sprawdzaj w panelu **WWW → Statystyki**, czy strona otrzymuje ruch i czy
   nie pojawiają się błędy wejść na stare adresy.
4. Rozważ podpięcie formularza do serwerowego wysyłania e-maili przed
   rozpoczęciem kampanii lub działań reklamowych.

## Powrót do starej strony w razie problemu

Traktuj to jako ostateczność, nie pierwszy odruch. Przywracasz instalację
o niepewnym stanie (patrz „Stan starej instalacji"), więc najpierw sprawdź,
czy problemu nie da się rozwiązać na nowej stronie.

1. Usuń nowo wgrane pliki statyczne z katalogu `/kolsystem.pl/kolsystem_pl/`.
2. Wgraj z lokalnej kopii wszystkie pliki WordPressa, w tym poprzedni
   `.htaccess`.
3. Bazy danych nie importuj, o ile nie została zmieniona lub usunięta.
4. Otwórz `https://kolsystem.pl/` w prywatnym oknie przeglądarki i sprawdź,
   czy powróciła poprzednia strona.
