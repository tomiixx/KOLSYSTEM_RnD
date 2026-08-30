"""Generuje angielską wersję strony KOLSYSTEM z polskich źródeł.

Polskie pliki (`index.html`, `polityka-prywatnosci.html`) są jedynym źródłem
prawdy dla struktury i układu. Wersja angielska powstaje z nich automatycznie,
przez podmianę tekstów ze słownika `i18n/en.json`. Dzięki temu obie wersje nie
mogą się rozjechać - zmiana w polskim pliku od razu widać w raporcie jako
brakujące tłumaczenie.

    python tools/build_i18n.py --extract   # wypisz teksty bez tłumaczenia
    python tools/build_i18n.py             # zbuduj en/

Wymaga: beautifulsoup4.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Comment, Doctype

ROOT = Path(__file__).resolve().parents[1]
I18N = ROOT / "i18n" / "en.json"
OUT_DIR = ROOT / "en"

# polski plik -> nazwa pliku w katalogu en/
PAGES = {
    "index.html": "index.html",
    "polityka-prywatnosci.html": "privacy-policy.html",
}

# kanoniczne adresy obu wersji każdej strony
CANONICAL = {
    "index.html": ("https://kolsystem.pl/", "https://kolsystem.pl/en/"),
    "polityka-prywatnosci.html": (
        "https://kolsystem.pl/polityka-prywatnosci.html",
        "https://kolsystem.pl/en/privacy-policy.html",
    ),
}

SKIP_PARENTS = {"script", "style", "svg"}

# atrybuty, których wartości są widoczne dla użytkownika
TEXT_ATTRS = {
    "meta": ("content",),
    "img": ("alt",),
    "a": ("aria-label", "title"),
    "button": ("aria-label", "title"),
    "input": ("placeholder", "aria-label", "value"),
    "textarea": ("placeholder", "aria-label"),
    "section": ("aria-label",),
    "nav": ("aria-label",),
    "div": ("aria-label",),
    "iframe": ("title",),
    "form": ("aria-label",),
    "html": (),
}
# metatagi, których content NIE jest tekstem (adresy, wymiary, kody)
META_SKIP = {
    "viewport", "robots", "theme-color", "author", "twitter:card",
    "og:type", "og:site_name", "og:url", "og:locale", "og:image",
    "og:image:type", "og:image:width", "og:image:height", "twitter:image",
    "charset",
}
# klucze JSON-LD zawierające tekst do tłumaczenia
LD_KEYS = {"name", "description", "alternateName", "jobTitle", "areaServed"}


def meta_key(tag) -> str:
    return (tag.get("name") or tag.get("property") or "").strip()


def norm(text: str) -> str:
    """Normalizuje białe znaki - klucz słownika jest niewrażliwy na łamanie."""
    return re.sub(r"\s+", " ", text).strip()


def collect(soup: BeautifulSoup) -> list[str]:
    """Zwraca wszystkie teksty widoczne dla użytkownika, w kolejności wystąpień."""
    found: list[str] = []

    def add(value: str) -> None:
        v = norm(value)
        if v and any(c.isalpha() for c in v) and v not in found:
            found.append(v)

    for node in soup.find_all(string=True):
        if isinstance(node, (Comment, Doctype)):
            continue
        if node.parent and node.parent.name in SKIP_PARENTS:
            continue
        add(str(node))

    for tag in soup.find_all(True):
        for attr in TEXT_ATTRS.get(tag.name, ()):
            if tag.name == "meta" and meta_key(tag) in META_SKIP:
                continue
            if tag.name == "input" and attr == "value" and tag.get("type") != "submit":
                continue
            if tag.has_attr(attr):
                add(tag[attr])

    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "{}")
        except json.JSONDecodeError:
            continue

        def walk(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k in LD_KEYS and isinstance(v, str):
                        add(v)
                    else:
                        walk(v)
            elif isinstance(obj, list):
                for item in obj:
                    walk(item)

        walk(data)
    return found


def translate_soup(soup: BeautifulSoup, tr: dict[str, str], missing: list[str]) -> None:
    """Podmienia wszystkie teksty na angielskie, w miejscu."""

    def get(value: str) -> str | None:
        key = norm(value)
        if not key or not any(c.isalpha() for c in key):
            return None
        if key in tr and tr[key]:
            return tr[key]
        if key not in missing:
            missing.append(key)
        return None

    for node in list(soup.find_all(string=True)):
        if isinstance(node, (Comment, Doctype)) or (
                node.parent and node.parent.name in SKIP_PARENTS):
            continue
        raw = str(node)
        new = get(raw)
        if new is None:
            continue
        # zachowaj wiodące/końcowe białe znaki, żeby nie sklejać słów z tagami
        lead = raw[: len(raw) - len(raw.lstrip())]
        tail = raw[len(raw.rstrip()):]
        node.replace_with(NavigableString(lead + new + tail))

    for tag in soup.find_all(True):
        for attr in TEXT_ATTRS.get(tag.name, ()):
            if tag.name == "meta" and meta_key(tag) in META_SKIP:
                continue
            if tag.name == "input" and attr == "value" and tag.get("type") != "submit":
                continue
            if tag.has_attr(attr):
                new = get(tag[attr])
                if new is not None:
                    tag[attr] = new

    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "{}")
        except json.JSONDecodeError:
            continue

        def walk(obj):
            if isinstance(obj, dict):
                return {
                    k: (get(v) or v) if (k in LD_KEYS and isinstance(v, str)) else walk(v)
                    for k, v in obj.items()
                }
            if isinstance(obj, list):
                return [walk(i) for i in obj]
            return obj

        script.string = json.dumps(walk(data), ensure_ascii=False, indent=2)


def retarget(soup: BeautifulSoup, source: str) -> None:
    """Przestawia dokument na wersję angielską: język, ścieżki, adresy, hreflang."""
    pl_url, en_url = CANONICAL[source]

    soup.html["lang"] = "en"

    # en/ leży o poziom niżej niż katalog główny
    for tag in soup.find_all(True):
        for attr in ("href", "src", "data-src"):
            if tag.has_attr(attr) and tag[attr].startswith("assets/"):
                tag[attr] = "../" + tag[attr]
        if tag.has_attr("href") and tag["href"] == "polityka-prywatnosci.html":
            tag["href"] = "privacy-policy.html"

    for tag in soup.find_all("link", rel="canonical"):
        tag["href"] = en_url
    for tag in soup.find_all("meta", property="og:url"):
        tag["content"] = en_url
    for tag in soup.find_all("meta", property="og:locale"):
        tag["content"] = "en_GB"

    # aktywna pozycja w przełączniku języka
    for anchor in soup.select(".lang-switch a"):
        english = anchor.get("hreflang") == "en"
        if english:
            anchor["class"] = ["is-active"]
        elif anchor.has_attr("class"):
            del anchor["class"]          # pusty class="" tylko zaśmieca wynik
        if english:
            anchor["aria-current"] = "true"
        elif anchor.has_attr("aria-current"):
            del anchor["aria-current"]


# Wersja angielska polityki prywatności jest tłumaczeniem informacyjnym -
# wiążąca pozostaje wersja polska. Notka pojawia się wyłącznie w en/.
EN_ONLY_NOTICE = (
    "This English version of the privacy policy is provided for information only. "
    "In the event of any discrepancy, the Polish version available at "
    "kolsystem.pl/polityka-prywatnosci.html is the binding text."
)


def add_en_notice(soup: BeautifulSoup) -> None:
    """Wstawia adnotację o wiążącej wersji polskiej na początku treści polityki."""
    article = soup.find("article", class_="legal")
    if article is None:
        return
    box = soup.new_tag("p", attrs={"class": "legal-notice", "lang": "en"})
    box.string = EN_ONLY_NOTICE
    article.insert(0, box)


def hreflang_block(source: str) -> str:
    pl_url, en_url = CANONICAL[source]
    return (
        f'<link rel="alternate" hreflang="pl" href="{pl_url}">\n'
        f'  <link rel="alternate" hreflang="en" href="{en_url}">\n'
        f'  <link rel="alternate" hreflang="x-default" href="{pl_url}">'
    )


def main() -> int:
    extract_only = "--extract" in sys.argv
    tr = json.loads(I18N.read_text(encoding="utf-8")) if I18N.exists() else {}

    if extract_only:
        pending: list[str] = []
        for source in PAGES:
            soup = BeautifulSoup((ROOT / source).read_text(encoding="utf-8"), "html.parser")
            for text in collect(soup):
                if text not in tr and text not in pending:
                    pending.append(text)
        print(json.dumps({t: "" for t in pending}, ensure_ascii=False, indent=2))
        print(f"\n// bez tlumaczenia: {len(pending)}", file=sys.stderr)
        return 0

    OUT_DIR.mkdir(exist_ok=True)
    missing: list[str] = []
    for source, target in PAGES.items():
        soup = BeautifulSoup((ROOT / source).read_text(encoding="utf-8"), "html.parser")
        translate_soup(soup, tr, missing)
        retarget(soup, source)
        if source == "polityka-prywatnosci.html":
            add_en_notice(soup)
        (OUT_DIR / target).write_text(str(soup), encoding="utf-8")
        print(f"ok en/{target}")

    if missing:
        print(f"\nUWAGA: {len(missing)} tekstow bez tlumaczenia:", file=sys.stderr)
        for m in missing[:20]:
            print(f"  - {m[:90]}", file=sys.stderr)
        return 1
    print("Wszystkie teksty przetlumaczone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
