"""Eksportuje wizytówkę do SVG z tekstem i pakuje źródła wraz z fontami."""

import base64
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

import fitz


BRAND = Path(__file__).resolve().parents[1]
CARD = BRAND / "print" / "business-card"
OUTPUT = CARD / "editable"
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

# Rodzina, waga i plik odpowiadają kolejnym polom tekstowym w PDF.
FRONT_FONTS = [
    ("Chakra Petch SemiBold", "400", "ChakraPetch-SemiBold.ttf"),
    ("JetBrains Mono", "500", "JetBrainsMono-Medium.ttf"),
]
BACK_FONTS = [
    ("Chakra Petch", "700", "ChakraPetch-Bold.ttf"),
    ("Titillium Web SemiBold", "400", "TitilliumWeb-SemiBold.ttf"),
    *[("JetBrains Mono", "400", "JetBrainsMono-Regular.ttf")] * 3,
    ("Titillium Web", "400", "TitilliumWeb-Regular.ttf"),
]


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    with fitz.open(CARD / "KOLSYSTEM-business-card-90x50mm-bleed3mm-CMYK.pdf") as pdf:
        for page, side, fonts in zip(pdf, ("awers", "rewers"), (FRONT_FONTS, BACK_FONTS)):
            root = ET.fromstring(page.get_svg_image(text_as_path=False))
            root.set("width", "96mm")
            root.set("height", "56mm")
            texts = list(root.iter(f"{{{SVG}}}text"))
            if len(texts) != len(fonts):
                raise ValueError(f"Zmieniono układ tekstów strony: {side}")
            css = []
            for family, weight, filename in dict.fromkeys(fonts):
                data = base64.b64encode((BRAND / "fonts" / "desktop" / filename).read_bytes()).decode()
                css.append(
                    f"@font-face {{font-family:'{family}';font-weight:{weight};"
                    f"src:url(data:font/ttf;base64,{data}) format('truetype');}}"
                )
            style = ET.Element(f"{{{SVG}}}style")
            style.text = "\n".join(css)
            root.insert(0, style)
            for i, (text, (family, weight, _)) in enumerate(zip(texts, fonts), 1):
                text.set("id", f"{side}-tekst-{i}")
                text.set("font-family", family)
                text.set("font-weight", weight)
                # Jedna pozycja startowa zamiast osobnych współrzędnych liter:
                # po zmianie treści nowe litery układają się automatycznie.
                for span in text:
                    if "x" in span.attrib:
                        span.set("x", span.get("x").split()[0])
            ET.ElementTree(root).write(
                OUTPUT / f"KOLSYSTEM-wizytowka-{side}-edytowalna.svg",
                encoding="utf-8", xml_declaration=True,
            )

    with ZipFile(CARD / "KOLSYSTEM-wizytowka-edytowalna.zip", "w", ZIP_DEFLATED) as archive:
        for path in sorted(OUTPUT.iterdir()):
            if path.is_file():
                archive.write(path, path.name)
        for filename in sorted({font[2] for font in FRONT_FONTS + BACK_FONTS}):
            archive.write(BRAND / "fonts" / "desktop" / filename, f"fonty/{filename}")
        for path in sorted((BRAND / "fonts" / "licenses").glob("*.txt")):
            archive.write(path, f"fonty/licencje/{path.name}")
    print("Gotowe: edytowalne SVG oraz paczka ZIP w", CARD)


if __name__ == "__main__":
    main()
