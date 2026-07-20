"""Buduje powtarzalne eksporty systemu marki KOLSYSTEM.

Uruchomienie z katalogu głównego:
    python brand/tools/build_brand_assets.py
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import fitz
from fontTools.merge import Merger
from fontTools.ttLib import TTFont as FontToolsFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject
from reportlab.graphics import renderPDF
from reportlab.lib.colors import CMYKColor, HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from svglib.fonts import register_font as register_svg_font
from svglib.svglib import svg2rlg


ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / "brand"
WEB_FONTS = ROOT / "assets" / "fonts"
DESKTOP_FONTS = BRAND / "fonts" / "desktop"
SVG_LOGOS = BRAND / "logos" / "svg"
PNG_LOGOS = BRAND / "logos" / "png"
PDF_LOGOS = BRAND / "logos" / "pdf"
DIGITAL_ICONS = BRAND / "digital" / "icons"
DIGITAL_SOCIAL = BRAND / "digital" / "social"
BUSINESS_CARD = BRAND / "print" / "business-card"
WEB_BRAND = ROOT / "assets" / "brand"
GUIDELINES = BRAND / "guidelines"

GRAPHITE = HexColor("#14181d")
ANTHRACITE = HexColor("#1b2129")
YELLOW = HexColor("#FFD200")
OFF_WHITE = HexColor("#f5f7fa")
GRAY_200 = HexColor("#e6eaee")
MUTED_DARK = HexColor("#5b6672")
MUTED_LIGHT = HexColor("#9aa5b1")

CMYK_GRAPHITE = CMYKColor(0.32, 0.17, 0, 0.89)
CMYK_ANTHRACITE = CMYKColor(0.34, 0.20, 0, 0.84)
CMYK_YELLOW = CMYKColor(0, 0.18, 1, 0)
CMYK_WHITE = CMYKColor(0.02, 0.01, 0, 0.02)
CMYK_MUTED = CMYKColor(0.20, 0.10, 0, 0.45)

FONT_SPECS = [
    ("chakra-petch-500", "ChakraPetch-Medium.ttf"),
    ("chakra-petch-600", "ChakraPetch-SemiBold.ttf"),
    ("chakra-petch-700", "ChakraPetch-Bold.ttf"),
    ("titillium-web-400", "TitilliumWeb-Regular.ttf"),
    ("titillium-web-600", "TitilliumWeb-SemiBold.ttf"),
    ("titillium-web-700", "TitilliumWeb-Bold.ttf"),
    ("jetbrains-mono-400", "JetBrainsMono-Regular.ttf"),
    ("jetbrains-mono-500", "JetBrainsMono-Medium.ttf"),
    ("jetbrains-mono-600", "JetBrainsMono-SemiBold.ttf"),
]

FONT_ALIASES = {
    "Chakra-Medium": "ChakraPetch-Medium.ttf",
    "Chakra-SemiBold": "ChakraPetch-SemiBold.ttf",
    "Chakra-Bold": "ChakraPetch-Bold.ttf",
    "Titillium-Regular": "TitilliumWeb-Regular.ttf",
    "Titillium-SemiBold": "TitilliumWeb-SemiBold.ttf",
    "Titillium-Bold": "TitilliumWeb-Bold.ttf",
    "JetBrains-Regular": "JetBrainsMono-Regular.ttf",
    "JetBrains-Medium": "JetBrainsMono-Medium.ttf",
    "JetBrains-SemiBold": "JetBrainsMono-SemiBold.ttf",
}


def ensure_directories() -> None:
    for directory in (
        DESKTOP_FONTS,
        PNG_LOGOS,
        PDF_LOGOS,
        DIGITAL_ICONS,
        DIGITAL_SOCIAL,
        BUSINESS_CARD / "preview",
        WEB_BRAND,
        GUIDELINES,
    ):
        directory.mkdir(parents=True, exist_ok=True)


def build_desktop_fonts() -> None:
    """Łączy podzbiory latin i latin-ext WOFF2 w pełne fonty TTF."""
    for prefix, output_name in FONT_SPECS:
        latin = WEB_FONTS / f"{prefix}-latin.woff2"
        latin_ext = WEB_FONTS / f"{prefix}-latin-ext.woff2"
        merge_sources = [str(latin), str(latin_ext)]
        temporary_sources: list[Path] = []
        if prefix.startswith("jetbrains-mono"):
            # Podzbiory JetBrains Mono zawierają zmienny VarStore, którego
            # fontTools nie łączy. Tabele układu nie są potrzebne w kroju mono.
            merge_sources = []
            for subset, source in (("latin", latin), ("latin-ext", latin_ext)):
                font = FontToolsFont(source)
                for table in ("GDEF", "GPOS", "GSUB"):
                    if table in font:
                        del font[table]
                font.flavor = None
                temporary = DESKTOP_FONTS / f".{prefix}-{subset}.ttf"
                font.save(temporary)
                temporary_sources.append(temporary)
                merge_sources.append(str(temporary))

        merged = Merger().merge(merge_sources)
        merged.flavor = None
        merged.save(DESKTOP_FONTS / output_name)
        for temporary in temporary_sources:
            temporary.unlink()


def register_fonts() -> None:
    for alias, filename in FONT_ALIASES.items():
        register_svg_font(alias, str(DESKTOP_FONTS / filename))

    pdfmetrics.registerFontFamily(
        "Chakra Petch",
        normal="Chakra-Medium",
        bold="Chakra-Bold",
    )
    pdfmetrics.registerFontFamily(
        "Titillium Web",
        normal="Titillium-Regular",
        bold="Titillium-Bold",
    )
    pdfmetrics.registerFontFamily(
        "JetBrains Mono",
        normal="JetBrains-Regular",
        bold="JetBrains-SemiBold",
    )


def load_svg(path: Path):
    drawing = svg2rlg(str(path))
    if drawing is None:
        raise RuntimeError(f"Nie można odczytać SVG: {path}")
    return drawing


def scaled_drawing(path: Path, width: float, height: float | None = None):
    drawing = load_svg(path)
    scale_x = width / drawing.width
    scale_y = (height / drawing.height) if height else scale_x
    drawing.scale(scale_x, scale_y)
    drawing.width = width
    drawing.height = drawing.height * scale_y
    return drawing


def render_svg_png(
    source: Path,
    destination: Path,
    width: int,
    height: int | None = None,
    transparent: bool = True,
) -> None:
    drawing = scaled_drawing(source, width, height)
    pdf_bytes = renderPDF.drawToString(drawing)
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    pixmap = document[0].get_pixmap(alpha=transparent)
    mode = "RGBA" if transparent else "RGB"
    image = Image.frombytes(mode, (pixmap.width, pixmap.height), pixmap.samples)
    document.close()
    target_height = height or round(drawing.height)
    if image.size != (width, target_height):
        image = image.resize((width, target_height), Image.Resampling.LANCZOS)
    image.save(destination, optimize=True)


def render_svg_pdf(source: Path, destination: Path) -> None:
    renderPDF.drawToFile(load_svg(source), str(destination))


def build_logo_exports() -> None:
    for source in sorted(SVG_LOGOS.glob("*.svg")):
        is_symbol = "symbol" in source.stem
        target_width = 1024 if is_symbol else 2400
        suffix = "1024px" if is_symbol else "2400w"
        render_svg_png(
            source,
            PNG_LOGOS / f"{source.stem}-{suffix}.png",
            target_width,
        )
        render_svg_pdf(source, PDF_LOGOS / f"{source.stem}.pdf")


def build_digital_exports() -> None:
    app_icon = DIGITAL_ICONS / "kolsystem-app-icon.svg"
    favicon = DIGITAL_ICONS / "kolsystem-favicon.svg"
    symbol = SVG_LOGOS / "kolsystem-symbol-primary.svg"
    social_source = DIGITAL_SOCIAL / "kolsystem-social-share-1200x630.svg"

    render_svg_png(app_icon, DIGITAL_ICONS / "apple-touch-icon-180.png", 180, 180, False)
    render_svg_png(app_icon, DIGITAL_ICONS / "app-icon-192.png", 192, 192, False)
    render_svg_png(app_icon, DIGITAL_ICONS / "app-icon-512.png", 512, 512, False)
    render_svg_png(symbol, DIGITAL_ICONS / "avatar-512.png", 512, 512, True)
    render_svg_png(favicon, DIGITAL_ICONS / "favicon-512.png", 512, 512, True)

    favicon_base = Image.open(DIGITAL_ICONS / "favicon-512.png").convert("RGBA")
    for size in (16, 32, 48, 64):
        favicon_base.resize((size, size), Image.Resampling.LANCZOS).save(
            DIGITAL_ICONS / f"favicon-{size}.png"
        )
    favicon_base.save(
        DIGITAL_ICONS / "favicon.ico",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64)],
    )

    render_svg_png(
        social_source,
        DIGITAL_SOCIAL / "kolsystem-social-share-1200x630.png",
        1200,
        630,
        False,
    )


def _rgb_key(color) -> tuple[int, int, int] | None:
    if color is None or not all(hasattr(color, key) for key in ("red", "green", "blue")):
        return None
    return tuple(round(getattr(color, channel) * 255) for channel in ("red", "green", "blue"))


def recolor_for_print(node) -> None:
    replacements = {
        (20, 24, 29): CMYK_GRAPHITE,
        (27, 33, 41): CMYK_ANTHRACITE,
        (255, 210, 0): CMYK_YELLOW,
        (245, 247, 250): CMYK_WHITE,
        (91, 102, 114): CMYK_MUTED,
    }
    for attribute in ("fillColor", "strokeColor"):
        color = getattr(node, attribute, None)
        key = _rgb_key(color)
        if key in replacements:
            setattr(node, attribute, replacements[key])
    for child in getattr(node, "contents", []):
        recolor_for_print(child)


def draw_svg_on_canvas(
    pdf: canvas.Canvas,
    source: Path,
    x: float,
    y: float,
    width: float,
    cmyk: bool = False,
) -> float:
    drawing = scaled_drawing(source, width)
    if cmyk:
        recolor_for_print(drawing)
    renderPDF.draw(drawing, pdf, x, y)
    return drawing.height


def _card_front(pdf: canvas.Canvas) -> None:
    page_width, page_height = 96 * mm, 56 * mm
    pdf.setFillColor(CMYK_GRAPHITE)
    pdf.rect(0, 0, page_width, page_height, stroke=0, fill=1)
    pdf.setStrokeColor(CMYK_ANTHRACITE)
    pdf.setLineWidth(0.12 * mm)
    for x in range(0, 97, 5):
        pdf.line(x * mm, 0, x * mm, page_height)
    for y in range(0, 57, 5):
        pdf.line(0, y * mm, page_width, y * mm)
    pdf.setFillColor(CMYK_YELLOW)
    pdf.rect(0, 0, 2.4 * mm, page_height, stroke=0, fill=1)

    draw_svg_on_canvas(
        pdf,
        SVG_LOGOS / "kolsystem-lockup-primary.svg",
        9 * mm,
        28 * mm,
        65 * mm,
        cmyk=True,
    )
    pdf.rect(9 * mm, 22.5 * mm, 34 * mm, 0.8 * mm, stroke=0, fill=1)
    pdf.setFillColor(CMYK_WHITE)
    pdf.setFont("Chakra-SemiBold", 11.4)
    pdf.drawString(9 * mm, 16.8 * mm, "INŻYNIERIA SYSTEMÓW KRYTYCZNYCH")
    pdf.setFillColor(CMYK_MUTED)
    pdf.setFont("JetBrains-Medium", 6.4)
    pdf.drawString(9 * mm, 11.8 * mm, "MODEL-BASED DESIGN  ·  CENELEC  ·  V&V")


def _card_back(pdf: canvas.Canvas) -> None:
    page_width, page_height = 96 * mm, 56 * mm
    pdf.setFillColor(CMYK_WHITE)
    pdf.rect(0, 0, page_width, page_height, stroke=0, fill=1)
    pdf.setFillColor(CMYK_YELLOW)
    pdf.rect(0, 0, 6 * mm, page_height, stroke=0, fill=1)

    pdf.setFillColor(CMYK_GRAPHITE)
    pdf.setFont("Chakra-Bold", 13)
    pdf.drawString(11 * mm, 43 * mm, "KOLSYSTEM Sp. z o.o.")
    pdf.setFillColor(CMYK_MUTED)
    pdf.setFont("Titillium-SemiBold", 8)
    pdf.drawString(11 * mm, 38 * mm, "Inżynieria systemów krytycznych")
    pdf.setFillColor(CMYK_YELLOW)
    pdf.rect(11 * mm, 34 * mm, 43 * mm, 0.6 * mm, stroke=0, fill=1)

    contacts = (
        (27.5, "kontakt@kolsystem.pl"),
        (21.5, "+48 600 580 325"),
        (15.5, "kolsystem.pl"),
    )
    pdf.setFont("JetBrains-Regular", 7.5)
    for y, value in contacts:
        pdf.setFillColor(CMYK_YELLOW)
        pdf.rect(11 * mm, (y - 0.4) * mm, 1.5 * mm, 1.5 * mm, stroke=0, fill=1)
        pdf.setFillColor(CMYK_GRAPHITE)
        pdf.drawString(15 * mm, y * mm, value)

    pdf.setFillColor(CMYK_MUTED)
    pdf.setFont("Titillium-Regular", 6.7)
    pdf.drawString(11 * mm, 7.8 * mm, "ul. Radockiego 76/8  ·  40-645 Katowice")
    draw_svg_on_canvas(
        pdf,
        SVG_LOGOS / "kolsystem-symbol-on-yellow.svg",
        70 * mm,
        18 * mm,
        20 * mm,
        cmyk=True,
    )


def build_business_card() -> Path:
    output = BUSINESS_CARD / "KOLSYSTEM-business-card-90x50mm-bleed3mm-CMYK.pdf"
    temporary = BUSINESS_CARD / ".business-card-build.pdf"
    pdf = canvas.Canvas(
        str(temporary),
        pagesize=(96 * mm, 56 * mm),
        pageCompression=1,
        pdfVersion=(1, 4),
    )
    pdf.setTitle("KOLSYSTEM - wizytówka firmowa 90 x 50 mm")
    pdf.setAuthor("KOLSYSTEM Sp. z o.o.")
    pdf.setCreator("KOLSYSTEM brand asset builder")
    _card_front(pdf)
    pdf.showPage()
    _card_back(pdf)
    pdf.showPage()
    pdf.save()

    reader = PdfReader(temporary)
    writer = PdfWriter()
    trim = 3 * mm
    for page in reader.pages:
        content = page.get_contents().get_data()
        content = re.sub(rb"(?<![0-9.])0 0 0 rg(?![0-9.])", b"0 0 0 1 k", content)
        content = re.sub(rb"(?<![0-9.])0 0 0 RG(?![0-9.])", b"0 0 0 1 K", content)
        stream = DecodedStreamObject()
        stream.set_data(content)
        page[NameObject("/Contents")] = stream
        page.trimbox.lower_left = (trim, trim)
        page.trimbox.upper_right = (93 * mm, 53 * mm)
        page.bleedbox.lower_left = (0, 0)
        page.bleedbox.upper_right = (96 * mm, 56 * mm)
        writer.add_page(page)
    writer.add_metadata(
        {
            "/Title": "KOLSYSTEM - wizytówka firmowa 90 x 50 mm",
            "/Author": "KOLSYSTEM Sp. z o.o.",
            "/Subject": "CMYK, spad 3 mm, TrimBox 90 x 50 mm, dwie strony",
        }
    )
    with output.open("wb") as handle:
        writer.write(handle)
    temporary.unlink()
    return output


def build_business_card_preview(pdf_path: Path) -> Path:
    document = fitz.open(pdf_path)
    cards: list[Image.Image] = []
    for page in document:
        pixmap = page.get_pixmap(matrix=fitz.Matrix(3.2, 3.2), alpha=False)
        cards.append(Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples))
    document.close()

    margin = 90
    label_height = 55
    gap = 80
    width = margin * 2 + sum(card.width for card in cards) + gap
    height = margin * 2 + label_height + max(card.height for card in cards)
    preview = Image.new("RGB", (width, height), "#e6eaee")
    draw = ImageDraw.Draw(preview)
    label_font = ImageFont.truetype(DESKTOP_FONTS / "ChakraPetch-SemiBold.ttf", 24)
    labels = ("AWERS", "REWERS")
    x = margin
    for card, label in zip(cards, labels):
        shadow = Image.new("RGBA", (card.width + 30, card.height + 30), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rectangle((15, 15, card.width + 15, card.height + 15), fill=(0, 0, 0, 90))
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        preview.paste(shadow, (x - 15, margin + label_height - 15), shadow)
        preview.paste(card, (x, margin + label_height))
        draw.text((x, margin), label, font=label_font, fill="#5b6672")
        x += card.width + gap

    output = BUSINESS_CARD / "preview" / "KOLSYSTEM-business-card-preview.png"
    preview.save(output, optimize=True)
    return output


def draw_wrapped(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    font: str = "Titillium-Regular",
    size: float = 10,
    leading: float | None = None,
    color=GRAPHITE,
) -> float:
    leading = leading or size * 1.35
    pdf.setFont(font, size)
    pdf.setFillColor(color)
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if pdfmetrics.stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    for line in lines:
        pdf.drawString(x, y, line)
        y -= leading
    return y


def guide_header(pdf: canvas.Canvas, number: int, title: str, total: int) -> None:
    page_width, page_height = A4
    pdf.setFillColor(OFF_WHITE)
    pdf.rect(0, 0, page_width, page_height, stroke=0, fill=1)
    pdf.setFillColor(YELLOW)
    pdf.rect(0, page_height - 10 * mm, page_width, 10 * mm, stroke=0, fill=1)
    pdf.setFillColor(GRAPHITE)
    pdf.setFont("JetBrains-SemiBold", 7.5)
    pdf.drawString(18 * mm, page_height - 6.5 * mm, f"KOLSYSTEM / SYSTEM MARKI / {number:02d}")
    pdf.setFont("Chakra-Bold", 25)
    pdf.drawString(18 * mm, page_height - 25 * mm, title)
    pdf.setStrokeColor(GRAY_200)
    pdf.line(18 * mm, 18 * mm, page_width - 18 * mm, 18 * mm)
    pdf.setFillColor(MUTED_DARK)
    pdf.setFont("JetBrains-Regular", 6.5)
    pdf.drawString(18 * mm, 11 * mm, "KOLSYSTEM Sp. z o.o.  ·  WERSJA 1.0  ·  LIPIEC 2026")
    pdf.drawRightString(page_width - 18 * mm, 11 * mm, f"{number}/{total}")


def draw_section_label(pdf: canvas.Canvas, text: str, x: float, y: float) -> None:
    pdf.setFillColor(YELLOW)
    pdf.rect(x, y - 2.5, 13, 3, stroke=0, fill=1)
    pdf.setFillColor(GRAPHITE)
    pdf.setFont("JetBrains-SemiBold", 7)
    pdf.drawString(x + 18, y - 4, text.upper())


def build_guidelines_pdf(social_png: Path, card_preview: Path) -> Path:
    output = GUIDELINES / "KOLSYSTEM-brand-guidelines.pdf"
    pdf = canvas.Canvas(str(output), pagesize=A4, pageCompression=1, pdfVersion=(1, 4))
    pdf.setTitle("KOLSYSTEM - księga identyfikacji wizualnej")
    pdf.setAuthor("KOLSYSTEM Sp. z o.o.")
    total = 9
    page_width, page_height = A4
    margin = 18 * mm
    content_width = page_width - 2 * margin

    # 1. Okładka
    pdf.setFillColor(GRAPHITE)
    pdf.rect(0, 0, page_width, page_height, stroke=0, fill=1)
    pdf.setFillColor(YELLOW)
    pdf.rect(0, 0, 9 * mm, page_height, stroke=0, fill=1)
    draw_svg_on_canvas(
        pdf,
        SVG_LOGOS / "kolsystem-lockup-primary.svg",
        25 * mm,
        page_height - 70 * mm,
        130 * mm,
    )
    pdf.setFillColor(OFF_WHITE)
    pdf.setFont("Chakra-Bold", 35)
    pdf.drawString(25 * mm, page_height - 118 * mm, "SYSTEM MARKI")
    pdf.setFillColor(YELLOW)
    pdf.rect(25 * mm, page_height - 125 * mm, 76 * mm, 2.5 * mm, stroke=0, fill=1)
    pdf.setFillColor(MUTED_LIGHT)
    pdf.setFont("Titillium-Regular", 14)
    pdf.drawString(25 * mm, page_height - 140 * mm, "Zasady identyfikacji wizualnej i produkcji materiałów")
    pdf.setFillColor(OFF_WHITE)
    pdf.setFont("JetBrains-SemiBold", 8)
    pdf.drawString(25 * mm, 28 * mm, "WERSJA 1.0  /  LIPIEC 2026")
    pdf.showPage()

    # 2. Fundament marki
    guide_header(pdf, 2, "Fundament marki", total)
    draw_section_label(pdf, "Idea", margin, page_height - 43 * mm)
    y = draw_wrapped(
        pdf,
        "KOLSYSTEM to jeden, niepodzielony znak słowny. Kolor ujawnia pochodzenie nazwy: KOL od kolei oraz SYSTEM jako obszar kompetencji. Znak nie używa separatora.",
        margin,
        page_height - 53 * mm,
        93 * mm,
        size=11,
        leading=15,
    )
    draw_section_label(pdf, "Obietnica", margin, y - 10)
    draw_wrapped(
        pdf,
        "Rzetelna inżynieria dla systemów, w których bezpieczeństwo, niezawodność i dowody zgodności mają znaczenie krytyczne.",
        margin,
        y - 24,
        93 * mm,
        size=11,
        leading=15,
    )
    pdf.setFillColor(ANTHRACITE)
    pdf.roundRect(125 * mm, 57 * mm, 60 * mm, 155 * mm, 5 * mm, stroke=0, fill=1)
    draw_svg_on_canvas(
        pdf,
        SVG_LOGOS / "kolsystem-symbol-primary.svg",
        137 * mm,
        111 * mm,
        36 * mm,
    )
    pdf.setFillColor(YELLOW)
    pdf.setFont("JetBrains-SemiBold", 7)
    pdf.drawCentredString(155 * mm, 97 * mm, "MAJORYZATOR 2oo3")
    draw_wrapped(
        pdf,
        "Trzy wejścia zbiegają się do węzła decyzji i walidacji. Symbol komunikuje redundancję, weryfikację i odpowiedzialność systemową.",
        136 * mm,
        89 * mm,
        38 * mm,
        size=8.5,
        leading=11,
        color=OFF_WHITE,
    )
    pdf.showPage()

    # 3. Rodzina logo
    guide_header(pdf, 3, "Rodzina logo", total)
    panels = [
        ("LOGO PODSTAWOWE / CIEMNE TŁO", GRAPHITE, "kolsystem-lockup-primary.svg", 178 * mm),
        ("LOGO NA JASNE TŁO", OFF_WHITE, "kolsystem-lockup-light.svg", 126 * mm),
        ("WORDMARK MONO / CIEMNE TŁO", GRAPHITE, "kolsystem-wordmark-mono-white.svg", 74 * mm),
        ("WORDMARK MONO / JASNE LUB ŻÓŁTE TŁO", YELLOW, "kolsystem-wordmark-mono-black.svg", 22 * mm),
    ]
    for label, background, filename, y_mm in panels:
        pdf.setFillColor(background)
        pdf.roundRect(margin, y_mm, content_width, 40 * mm, 3 * mm, stroke=0, fill=1)
        pdf.setFillColor(MUTED_LIGHT if background == GRAPHITE else MUTED_DARK)
        pdf.setFont("JetBrains-SemiBold", 6.5)
        pdf.drawString(margin + 6 * mm, y_mm + 31 * mm, label)
        target_width = 112 * mm if "lockup" in filename else 119 * mm
        draw_svg_on_canvas(
            pdf,
            SVG_LOGOS / filename,
            margin + 6 * mm,
            y_mm + 9 * mm,
            target_width,
        )
    pdf.showPage()

    # 4. Kolor
    guide_header(pdf, 4, "Kolor", total)
    swatches = [
        ("SAFETY YELLOW", YELLOW, "#FFD200", "RGB 255 / 210 / 0", "CMYK 0 / 18 / 100 / 0", GRAPHITE),
        ("GRAPHITE", GRAPHITE, "#14181D", "RGB 20 / 24 / 29", "CMYK 32 / 17 / 0 / 89", OFF_WHITE),
        ("ANTHRACITE", ANTHRACITE, "#1B2129", "RGB 27 / 33 / 41", "CMYK 34 / 20 / 0 / 84", OFF_WHITE),
        ("OFF WHITE", OFF_WHITE, "#F5F7FA", "RGB 245 / 247 / 250", "CMYK 2 / 1 / 0 / 2", GRAPHITE),
    ]
    positions = [(margin, 151 * mm), (108 * mm, 151 * mm), (margin, 71 * mm), (108 * mm, 71 * mm)]
    for data, (x, y_mm) in zip(swatches, positions):
        name, color, hex_value, rgb_value, cmyk_value, ink = data
        pdf.setFillColor(color)
        pdf.roundRect(x, y_mm, 84 * mm, 62 * mm, 3 * mm, stroke=0, fill=1)
        pdf.setFillColor(ink)
        pdf.setFont("Chakra-Bold", 14)
        pdf.drawString(x + 7 * mm, y_mm + 43 * mm, name)
        pdf.setFont("JetBrains-SemiBold", 8)
        pdf.drawString(x + 7 * mm, y_mm + 29 * mm, hex_value)
        pdf.setFont("JetBrains-Regular", 7)
        pdf.drawString(x + 7 * mm, y_mm + 20 * mm, rgb_value)
        pdf.drawString(x + 7 * mm, y_mm + 13 * mm, cmyk_value)
    draw_wrapped(
        pdf,
        "Wartości CMYK są wartościami roboczymi. Przed nakładem drukarskim należy wykonać proof w profilu wskazanym przez drukarnię. Nie konwertuj samodzielnie żółtego na kolor dodatkowy bez uzgodnienia.",
        margin,
        54 * mm,
        content_width,
        size=9,
        leading=12,
        color=MUTED_DARK,
    )
    pdf.showPage()

    # 5. Typografia
    guide_header(pdf, 5, "Typografia", total)
    draw_section_label(pdf, "Display / Chakra Petch", margin, page_height - 44 * mm)
    pdf.setFillColor(GRAPHITE)
    pdf.setFont("Chakra-Bold", 31)
    pdf.drawString(margin, page_height - 65 * mm, "SYSTEMY KRYTYCZNE")
    pdf.setFont("Chakra-SemiBold", 15)
    pdf.drawString(margin, page_height - 78 * mm, "Nagłówki, dane wyróżnione i komunikaty marki")
    draw_section_label(pdf, "Tekst / Titillium Web", margin, page_height - 101 * mm)
    draw_wrapped(
        pdf,
        "Titillium Web prowadzi dłuższe wypowiedzi. Jest techniczny, ale pozostaje lekki i czytelny. W druku stosuj Regular 400 dla tekstu oraz SemiBold 600 dla śródtytułów.",
        margin,
        page_height - 113 * mm,
        content_width,
        size=13,
        leading=18,
    )
    draw_section_label(pdf, "Dane / JetBrains Mono", margin, page_height - 155 * mm)
    pdf.setFont("JetBrains-Regular", 11)
    pdf.setFillColor(GRAPHITE)
    pdf.drawString(margin, page_height - 169 * mm, "EN 50126  ·  MODEL V  ·  SIL  ·  V&V  ·  2oo3")
    pdf.setFillColor(GRAY_200)
    pdf.roundRect(margin, 44 * mm, content_width, 47 * mm, 3 * mm, stroke=0, fill=1)
    pdf.setFillColor(MUTED_DARK)
    pdf.setFont("Titillium-Regular", 9)
    pdf.drawString(margin + 7 * mm, 78 * mm, "Zasada: nie zastępuj fontów ozdobnymi krojami technicznymi.")
    pdf.drawString(margin + 7 * mm, 68 * mm, "Logo zawsze korzysta z dostarczonych krzywych SVG/PDF - nigdy z wpisanego tekstu.")
    pdf.drawString(margin + 7 * mm, 58 * mm, "Fonty desktopowe i licencje OFL znajdują się w brand/fonts/.")
    pdf.showPage()

    # 6. Pole ochronne, skala, kontrast
    guide_header(pdf, 6, "Pole ochronne i czytelność", total)
    pdf.setFillColor(GRAY_200)
    pdf.roundRect(margin, 139 * mm, content_width, 77 * mm, 3 * mm, stroke=0, fill=1)
    pdf.setStrokeColor(YELLOW)
    pdf.setLineWidth(1)
    pdf.setDash(4, 3)
    pdf.rect(31 * mm, 154 * mm, 148 * mm, 45 * mm, stroke=1, fill=0)
    pdf.setDash()
    draw_svg_on_canvas(
        pdf,
        SVG_LOGOS / "kolsystem-lockup-light.svg",
        41 * mm,
        166 * mm,
        128 * mm,
    )
    pdf.setFillColor(MUTED_DARK)
    pdf.setFont("JetBrains-SemiBold", 7)
    pdf.drawString(31 * mm, 204 * mm, "X = WYSOKOŚĆ POLA ŻÓŁTEGO SYGNETU / MINIMUM 0,5 X W LOCKUPIE")
    draw_section_label(pdf, "Minimalne rozmiary", margin, 126 * mm)
    pdf.setFont("Titillium-SemiBold", 11)
    pdf.setFillColor(GRAPHITE)
    pdf.drawString(margin, 112 * mm, "Wordmark: 90 px ekran / 24 mm druk")
    pdf.drawString(margin, 101 * mm, "Sygnet: 16 px ekran / 6 mm druk")
    draw_section_label(pdf, "Kontrast WCAG", margin, 84 * mm)
    ratios = [
        ("Żółty / grafit", "12,28 : 1", YELLOW, GRAPHITE),
        ("Biel / grafit", "16,61 : 1", OFF_WHITE, GRAPHITE),
        ("Żółty / biel", "1,35 : 1 - nie dla tekstu", YELLOW, OFF_WHITE),
    ]
    for index, (label, value, foreground, background) in enumerate(ratios):
        y_mm = 64 - index * 14
        pdf.setFillColor(background)
        pdf.roundRect(margin, y_mm * mm, 76 * mm, 10 * mm, 2 * mm, stroke=0, fill=1)
        pdf.setFillColor(foreground)
        pdf.setFont("JetBrains-SemiBold", 7)
        pdf.drawString(margin + 4 * mm, (y_mm + 3.3) * mm, f"{label}  {value}")
    pdf.showPage()

    # 7. Digital
    guide_header(pdf, 7, "Kanały cyfrowe", total)
    pdf.drawImage(
        str(social_png),
        margin,
        114 * mm,
        width=content_width,
        height=content_width * 630 / 1200,
        preserveAspectRatio=True,
        mask="auto",
    )
    draw_section_label(pdf, "Pakiet", margin, 101 * mm)
    digital_items = [
        "Open Graph / social share: 1200 x 630 px",
        "Avatar i ikona aplikacji: 512 x 512 px",
        "Apple Touch Icon: 180 x 180 px",
        "Favicon: SVG oraz ICO 16 / 32 / 48 / 64 px",
    ]
    y = 88 * mm
    for item in digital_items:
        pdf.setFillColor(YELLOW)
        pdf.rect(margin, y + 2, 5, 5, stroke=0, fill=1)
        pdf.setFillColor(GRAPHITE)
        pdf.setFont("Titillium-SemiBold", 9.5)
        pdf.drawString(margin + 10, y, item)
        y -= 11 * mm
    pdf.showPage()

    # 8. Wizytówka
    guide_header(pdf, 8, "Wizytówka firmowa", total)
    image = Image.open(card_preview)
    preview_width = content_width
    preview_height = preview_width * image.height / image.width
    pdf.drawImage(
        str(card_preview),
        margin,
        page_height - 47 * mm - preview_height,
        width=preview_width,
        height=preview_height,
        preserveAspectRatio=True,
        mask="auto",
    )
    y = page_height - 57 * mm - preview_height
    draw_section_label(pdf, "Specyfikacja produkcyjna", margin, y)
    specs = [
        "Format netto 90 x 50 mm; format pliku 96 x 56 mm.",
        "Spad 3 mm z każdej strony; TrimBox zapisany w PDF.",
        "Dwie strony w jednym pliku PDF; grafika i tekst pozostają wektorowe.",
        "Kolory PDF zapisane jako CMYK; fonty są osadzone.",
        "Przed drukiem potwierdź profil ICC, rodzaj papieru i sposób uszlachetnienia.",
    ]
    y -= 14
    for item in specs:
        pdf.setFillColor(YELLOW)
        pdf.circle(margin + 2.5, y + 3, 2.5, stroke=0, fill=1)
        y = draw_wrapped(
            pdf,
            item,
            margin + 12,
            y,
            content_width - 12,
            size=9.2,
            leading=12,
        ) - 4
    pdf.showPage()

    # 9. Zasady i przekazanie
    guide_header(pdf, 9, "Zasady użycia i przekazanie", total)
    pdf.setFillColor(GRAY_200)
    pdf.roundRect(margin, 137 * mm, 80 * mm, 78 * mm, 3 * mm, stroke=0, fill=1)
    pdf.roundRect(112 * mm, 137 * mm, 80 * mm, 78 * mm, 3 * mm, stroke=0, fill=1)
    pdf.setFillColor(GRAPHITE)
    pdf.setFont("Chakra-Bold", 17)
    pdf.drawString(margin + 7 * mm, 202 * mm, "TAK")
    pdf.drawString(119 * mm, 202 * mm, "NIE")
    yes_items = [
        "Używaj właściwego wariantu tła.",
        "Zachowuj proporcje i pole ochronne.",
        "Skaluj pliki SVG lub PDF.",
        "Sprawdzaj proof przed drukiem.",
    ]
    no_items = [
        "Nie dodawaj separatora w nazwie.",
        "Nie rozciągaj ani nie obracaj logo.",
        "Nie stosuj efektów i gradientów.",
        "Nie używaj żółtego tekstu na bieli.",
    ]
    for items, x in ((yes_items, margin + 7 * mm), (no_items, 119 * mm)):
        y = 188 * mm
        for item in items:
            pdf.setFillColor(YELLOW)
            pdf.rect(x, y + 2, 4, 4, stroke=0, fill=1)
            y = draw_wrapped(pdf, item, x + 9, y, 63 * mm, size=8.5, leading=11) - 5

    draw_section_label(pdf, "Przekazanie plików", margin, 119 * mm)
    draw_wrapped(
        pdf,
        "Do internetu wybieraj SVG lub gotowe PNG z brand/digital. Do druku przekazuj PDF albo SVG oraz informację o docelowym profilu. Nie wysyłaj wykonawcy katalogu assets/ strony - użyj kompletnego katalogu brand/.",
        margin,
        108 * mm,
        content_width,
        size=10,
        leading=14,
    )
    pdf.setFillColor(GRAPHITE)
    pdf.setFont("Chakra-Bold", 18)
    pdf.drawString(margin, 66 * mm, "W razie wątpliwości użyj logo podstawowego")
    pdf.setFillColor(YELLOW)
    pdf.rect(margin, 58 * mm, 66 * mm, 2 * mm, stroke=0, fill=1)
    pdf.setFont("JetBrains-SemiBold", 8)
    pdf.setFillColor(MUTED_DARK)
    pdf.drawString(margin, 47 * mm, "KONTAKT@KOLSYSTEM.PL  ·  KOLSYSTEM.PL")
    pdf.showPage()
    pdf.save()
    return output


def copy_web_assets() -> None:
    copies = {
        SVG_LOGOS / "kolsystem-lockup-primary.svg": WEB_BRAND / "logo-horizontal-primary.svg",
        DIGITAL_ICONS / "kolsystem-favicon.svg": WEB_BRAND / "favicon.svg",
        DIGITAL_ICONS / "favicon.ico": WEB_BRAND / "favicon.ico",
        DIGITAL_ICONS / "apple-touch-icon-180.png": WEB_BRAND / "apple-touch-icon.png",
        DIGITAL_SOCIAL / "kolsystem-social-share-1200x630.png": WEB_BRAND / "social-share-1200x630.png",
    }
    for source, destination in copies.items():
        shutil.copy2(source, destination)


def main() -> None:
    ensure_directories()
    build_desktop_fonts()
    register_fonts()
    build_logo_exports()
    build_digital_exports()
    card_pdf = build_business_card()
    card_preview = build_business_card_preview(card_pdf)
    guidelines_pdf = build_guidelines_pdf(
        DIGITAL_SOCIAL / "kolsystem-social-share-1200x630.png",
        card_preview,
    )
    copy_web_assets()
    print(f"Gotowe: {guidelines_pdf.relative_to(ROOT)}")
    print(f"Gotowe: {card_pdf.relative_to(ROOT)}")
    print(f"Gotowe: {WEB_BRAND.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
