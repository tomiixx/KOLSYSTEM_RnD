"""Generuje warianty marki oparte na realnym hero strony KOLSYSTEM.

Tworzy z jednego źródła (SVG z tekstem zapieczonym w krzywe + realna geometria
diagramu cyklu życia EN 50126 przeniesiona z index.html) pliki:

  * logo pionowe (sygnet nad napisem) - warianty na ciemne i jasne tło,
  * grafiki social odzwierciedlające hero strony:
      - Open Graph / social share  1200 x 630,
      - baner LinkedIn (profil)     1584 x 396,
      - okładka strony firmowej LI  1128 x 191.

Każdy plik powstaje jako SVG (krzywe, bez zależności od fontów) i jest
renderowany do PNG tym samym silnikiem co reszta pakietu marki.

Uruchamiać z katalogu głównego repo:
    python brand/tools/build_hero_assets.py
"""
from __future__ import annotations

from pathlib import Path

import fitz
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / "brand"
DESKTOP_FONTS = BRAND / "fonts" / "desktop"
SVG_LOGOS = BRAND / "logos" / "svg"
SOCIAL = BRAND / "digital" / "social"
WEB_BRAND = ROOT / "assets" / "brand"

# --- kolory strony (assets/css/style.css) ---
GRAPHITE = "#14181d"
ANTHRACITE = "#1b2129"
BORDER_D = "#2b333e"
WHITE = "#f5f7fa"
MUTED_D = "#9aa5b1"
YELLOW = "#FFD200"
GRAPHITE_INK = "#14181d"


class VectorFont:
    """Zamienia tekst na ścieżki SVG na podstawie konturów glifów."""

    def __init__(self, path: Path):
        self.font = TTFont(str(path))
        self.upm = self.font["head"].unitsPerEm
        self.cmap = self.font.getBestCmap()
        self.glyphset = self.font.getGlyphSet()
        self.hmtx = self.font["hmtx"]

    def _glyph_name(self, ch: str) -> str:
        name = self.cmap.get(ord(ch))
        if name is None:
            raise KeyError(f"Brak glifu dla znaku {ch!r} (U+{ord(ch):04X})")
        return name

    def text(
        self,
        text: str,
        x: float,
        y: float,
        size: float,
        fill: str,
        anchor: str = "start",
        ls_em: float = 0.0,
        opacity: float | None = None,
    ) -> tuple[str, float]:
        """Zwraca (grupa_svg, szerokość_px). y = linia bazowa."""
        scale = size / self.upm
        ls_units = ls_em * self.upm
        pen_x = 0.0
        glyphs: list[str] = []
        for ch in text:
            gname = self._glyph_name(ch)
            glyph = self.glyphset[gname]
            pen = SVGPathPen(self.glyphset)
            glyph.draw(pen)
            d = pen.getCommands()
            if d:
                glyphs.append(f'<path transform="translate({pen_x:.1f} 0)" d="{d}"/>')
            pen_x += self.hmtx[gname][0] + ls_units
        total_units = pen_x - ls_units if text else 0.0
        width_px = total_units * scale
        if anchor == "middle":
            ox = x - width_px / 2
        elif anchor == "end":
            ox = x - width_px
        else:
            ox = x
        op = f' opacity="{opacity}"' if opacity is not None else ""
        inner = "".join(glyphs)
        group = (
            f'<g fill="{fill}"{op} transform="translate({ox:.2f} {y:.2f}) '
            f'scale({scale:.6f} {-scale:.6f})">{inner}</g>'
        )
        return group, width_px


# ---------------------------------------------------------------------------
# Diagram cyklu życia EN 50126 - dane przeniesione 1:1 z index.html (hero)
# viewBox źródła: "4 28 732 448"
# ---------------------------------------------------------------------------
DIAGRAM_VIEW = (4, 28, 732, 448)
DIAGRAM_RECTS = [
    (16, 48), (50, 116), (84, 184), (118, 252), (152, 320), (300, 420),
    (418, 370), (452, 320), (486, 252), (520, 184), (554, 116), (588, 48),
]
DIAGRAM_NUMS = [
    ("01", 18, 42), ("02", 52, 110), ("03", 86, 178), ("04", 120, 246),
    ("05", 154, 314), ("06", 302, 414), ("07", 420, 364), ("08", 454, 314),
    ("09", 488, 246), ("10", 522, 178), ("11", 556, 110), ("12", 590, 42),
]
# etykieta: (x, y, [linie]) - anchor middle
DIAGRAM_LABELS = [
    (86, 73, ["KONCEPCJA"]),
    (120, 141, ["DEFINICJA SYSTEMU"]),
    (154, 209, ["ANALIZA RYZYKA"]),
    (188, 277, ["WYMAGANIA SYSTEMOWE"]),
    (222, 337, ["ARCHITEKTURA I", "ALOKACJA WYMAGAŃ"]),
    (370, 437, ["PROJEKTOWANIE", "I IMPLEMENTACJA"]),
    (488, 395, ["PRODUKCJA"]),
    (522, 345, ["INTEGRACJA"]),
    (556, 277, ["WALIDACJA SYSTEMU"]),
    (590, 209, ["ODBIÓR SYSTEMU"]),
    (624, 133, ["EKSPLOATACJA", "I UTRZYMANIE"]),
    (658, 73, ["WYCOFANIE"]),
]
DIAGRAM_LINK = ("M86 68 120 136 154 204 188 272 222 340 370 440 "
                "488 390 522 340 556 272 590 204 624 136 658 68")
DIAGRAM_VERIF = ["M264 272H480", "M298 340H446"]


def diagram_group(mono: VectorFont, tx: float, ty: float, scale: float) -> str:
    """Buduje wektorowy diagram; (tx,ty) = lewy-górny róg, scale wg viewBox."""
    vx, vy, _, _ = DIAGRAM_VIEW
    parts = [f'<g transform="translate({tx:.2f} {ty:.2f}) scale({scale:.5f})">'
             f'<g transform="translate({-vx} {-vy})">']
    # połączenia (pod blokami)
    parts.append(
        f'<path d="{DIAGRAM_LINK}" fill="none" stroke="{BORDER_D}" stroke-width="1.5"/>'
    )
    # przepływ - żółta linia przerywana (klatka statyczna)
    parts.append(
        f'<path d="{DIAGRAM_LINK}" fill="none" stroke="{YELLOW}" stroke-width="1.5" '
        f'stroke-dasharray="5 9" stroke-linecap="round" opacity="0.9"/>'
    )
    # relacje weryfikacji/walidacji
    for d in DIAGRAM_VERIF:
        parts.append(
            f'<path d="{d}" fill="none" stroke="{MUTED_D}" stroke-width="1" '
            f'stroke-dasharray="4 6"/>'
        )
    # bloki faz
    for bx, by in DIAGRAM_RECTS:
        parts.append(
            f'<rect x="{bx}" y="{by}" width="140" height="40" rx="5" '
            f'fill="{ANTHRACITE}" stroke="{BORDER_D}" stroke-width="1.5"/>'
        )
    # numery faz (żółte, anchor start)
    for num, nx, ny in DIAGRAM_NUMS:
        g, _ = mono.text(num, nx, ny, 9, YELLOW, anchor="start", ls_em=0.02, opacity=0.9)
        parts.append(g)
    # etykiety (białe, anchor middle, wielolinijkowe co 13 px)
    for lx, ly, lines in DIAGRAM_LABELS:
        for i, line in enumerate(lines):
            g, _ = mono.text(line, lx, ly + i * 13, 11, WHITE, anchor="middle", ls_em=0.02)
            parts.append(g)
    parts.append("</g></g>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# Sygnet i lockup (przeniesione z plików logo, jako krzywe)
# ---------------------------------------------------------------------------
def symbol_tile(tx: float, ty: float, size: float) -> str:
    """Żółty kafel sygnetu (majoryzator 2oo3) - jak w lockupie na ciemne tło.

    Geometria zgodna z brand/logos/svg/kolsystem-lockup-primary.svg
    (ścieżki prowadzone pod kątem prostym, majoryzator r=90.11).
    """
    s = size / 512.0
    marks = (
        '<rect x="113.83" y="108.97" width="114.77" height="20.65"/>'
        '<rect x="207.96" y="108.97" width="20.65" height="88.91"/>'
        '<rect x="207.96" y="177.24" width="142.04" height="20.65"/>'
        '<rect x="113.83" y="245.68" width="236.17" height="20.65"/>'
        '<rect x="113.83" y="382.38" width="114.77" height="20.65"/>'
        '<rect x="207.96" y="314.12" width="20.65" height="88.91"/>'
        '<rect x="207.96" y="314.12" width="142.04" height="20.65"/>'
        '<circle cx="113.83" cy="119.3" r="33.96"/>'
        '<circle cx="113.83" cy="256" r="33.96"/>'
        '<circle cx="113.83" cy="392.7" r="33.96"/>'
    )
    return (
        f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.6f})">'
        f'<rect width="512" height="512" rx="116" fill="{YELLOW}"/>'
        f'<g fill="{GRAPHITE_INK}">{marks}</g>'
        f'<circle cx="380.25" cy="256" r="90.11" fill="{GRAPHITE_INK}"/>'
        f'<path d="M339.29 261.46 370.69 294.23 429.4 220.5" fill="none" stroke="{YELLOW}" '
        f'stroke-width="19.97" stroke-linecap="round" stroke-linejoin="round"/></g>'
    )


# ścieżki napisu KOLSYSTEM (z kolsystem-wordmark-primary.svg)
WORDMARK_WHITE = ("M65 0H201V293H307L476 0H629L424 349L646 700H490L306 409H201V700H65Z "
                  "M766 585V115L881 0H1241L1356 115V585L1241 700H881ZM1169 584 1220 533V167"
                  "L1169 116H953L902 167V533L953 584Z M1536 0H1672V585H2022V700H1536Z")
WORDMARK_YELLOW = ("M2582 592V492H2716V551L2749 584H2956L2990 550V434L2957 401H2692L2584 293"
                   "V108L2692 0H3008L3116 108V209H2982V149L2949 116H2751L2718 149V252L2751 285"
                   "H3016L3124 393V590L3014 700H2690Z M3478 414 3229 0H3378L3545 287H3547L3714 0"
                   "H3863L3614 414V700H3478Z M3973 592V492H4107V551L4140 584H4347L4381 550V434"
                   "L4348 401H4083L3975 293V108L4083 0H4399L4507 108V209H4373V149L4340 116H4142"
                   "L4109 149V252L4142 285H4407L4515 393V590L4405 700H4081Z M4844 115H4635V0"
                   "H5189V115H4980V700H4844Z M5329 0H5835V115H5465V292H5806V405H5465V585H5835"
                   "V700H5329Z M5995 0H6121L6329 452H6331L6540 0H6666V700H6535V274H6533L6372 602"
                   "H6288L6128 274H6126V700H5995Z")
# napis w układzie wewnętrznym zajmuje x:65..6256, y:0..700
WORDMARK_W = 6256 - 65
WORDMARK_H = 700


def wordmark_group(tx: float, ty: float, height: float, main_fill: str) -> tuple[str, float]:
    """Rysuje napis o zadanej wysokości; zwraca (svg, szerokość_px)."""
    s = height / WORDMARK_H
    width = WORDMARK_W * s
    g = (
        f'<g transform="translate({tx - 65 * s:.2f} {ty:.2f}) scale({s:.6f})">'
        f'<path fill="{main_fill}" d="{WORDMARK_WHITE}"/>'
        f'<path fill="{YELLOW}" transform="translate(-410 0)" d="{WORDMARK_YELLOW}"/>'
        f'</g>'
    )
    return g, width


def lockup_group(tx: float, ty: float, symbol_size: float, main_fill: str) -> tuple[str, float]:
    """Poziomy lockup: sygnet + napis wyśrodkowany w pionie. Zwraca (svg, szer.)."""
    gap = symbol_size * 0.30
    wm_height = symbol_size * 0.52
    wm_y_baseline = ty + (symbol_size + wm_height) / 2  # dolna krawędź napisu
    sym = symbol_tile(tx, ty, symbol_size)
    wm, wm_w = wordmark_group(tx + symbol_size + gap, wm_y_baseline - wm_height, wm_height, main_fill)
    total = symbol_size + gap + wm_w
    return sym + wm, total


# ---------------------------------------------------------------------------
# Wspólne elementy tła
# ---------------------------------------------------------------------------
def _blend(bg: str, fg: str, alpha: float) -> str:
    """Miesza fg na bg z danym kryciem i zwraca kolor #rrggbb.

    svglib ignoruje atrybut `opacity` na liniach - renderuje je w pełnym
    kolorze. Krycie trzeba więc wpiec w sam kolor pociągnięcia.
    """
    b = tuple(int(bg[i:i + 2], 16) for i in (1, 3, 5))
    f = tuple(int(fg[i:i + 2], 16) for i in (1, 3, 5))
    m = tuple(round(bb + (ff - bb) * alpha) for bb, ff in zip(b, f))
    return "#%02x%02x%02x" % m


def grid_lines(w: float, h: float, step: float = 44, base: float = 0.035,
               focus: tuple[float, float] = (0.30, 0.20)) -> str:
    """Siatka inżynieryjna z winietą, odwzorowanie `.hero-bg` ze style.css:

        background-image: linear-gradient(rgba(255,255,255,0.035) 1px, ...)
        background-size:  44px 44px
        mask-image: radial-gradient(75rem 40rem at 30% 20%, #000 40%, transparent 100%)

    Maska jest eliptyczna: pełne krycie do 40% promienia, potem liniowe
    wygaszanie do zera na 100%. Krycie wpieczone w kolor (patrz _blend).
    """
    cx, cy = focus[0] * w, focus[1] * h
    seg = step

    def alpha_at(px: float, py: float) -> float:
        t = (((px - cx) / w) ** 2 + ((py - cy) / h) ** 2) ** 0.5
        if t <= 0.40:
            return base
        return base * max(0.0, 1.0 - (t - 0.40) / 0.60)

    # segmenty grupowane po kolorze - mniej węzłów w SVG
    by_color: dict[str, list[str]] = {}

    def add(x1: float, y1: float, x2: float, y2: float) -> None:
        a = alpha_at((x1 + x2) / 2, (y1 + y2) / 2)
        if a < 0.002:
            return
        col = _blend(GRAPHITE, WHITE, a)
        if col == GRAPHITE:          # nieodróżnialne od tła
            return
        by_color.setdefault(col, []).append(
            f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"/>'
        )

    x = step
    while x < w:
        y = 0.0
        while y < h:
            y2 = min(y + seg, h)
            add(x, y, x, y2)
            y += seg
        x += step
    y = step
    while y < h:
        x = 0.0
        while x < w:
            x2 = min(x + seg, w)
            add(x, y, x2, y)
            x += seg
        y += step

    out = []
    for col, lines in by_color.items():
        out.append(f'<g stroke="{col}" stroke-width="1">' + "".join(lines) + "</g>")
    return "".join(out)


def blueprint_corner(x: float, y: float, size: float, kind: str) -> str:
    """Narożnik 'blueprint' (jak wokół diagramu w hero)."""
    if kind == "tl":
        d = f"M{x} {y+size}V{y}H{x+size}"
    else:  # br
        d = f"M{x} {y-size}V{y}H{x-size}"
    return f'<path d="{d}" fill="none" stroke="{YELLOW}" stroke-width="2" opacity="0.85"/>'


def svg_document(w: int, h: int, body: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="KOLSYSTEM">'
        f'<title>{title}</title>{body}</svg>'
    )


# ---------------------------------------------------------------------------
# Render SVG -> PNG (ten sam łańcuch co build_brand_assets.py)
# ---------------------------------------------------------------------------
def render_pdf(svg_path: Path, pdf_path: Path) -> None:
    renderPDF.drawToFile(svg2rlg(str(svg_path)), str(pdf_path))


def render_png(svg_path: Path, png_path: Path, width: int, transparent: bool) -> None:
    drawing = svg2rlg(str(svg_path))
    scale = width / drawing.width
    height = round(drawing.height * scale)
    drawing.scale(scale, scale)
    drawing.width = width
    drawing.height = drawing.height * scale
    pdf_bytes = renderPDF.drawToString(drawing)
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pix = doc[0].get_pixmap(alpha=transparent)
    mode = "RGBA" if transparent else "RGB"
    img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
    doc.close()
    if img.size != (width, height):
        img = img.resize((width, height), Image.Resampling.LANCZOS)
    img.save(png_path, optimize=True)


def wrap_text(vf: VectorFont, text: str, size: float, max_width: float,
              ls_em: float = 0.0) -> list[str]:
    def measure(s: str) -> float:
        if not s:
            return 0.0
        units = sum(vf.hmtx[vf._glyph_name(c)][0] for c in s)
        units += ls_em * vf.upm * (len(s) - 1)
        return units * size / vf.upm

    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        cand = f"{cur} {word}".strip()
        if measure(cand) <= max_width or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def button_primary(chakra_sb: VectorFont, x: float, y: float, label: str,
                   size: float = 15) -> str:
    _, w_txt = chakra_sb.text(label, 0, 0, size, "#000", ls_em=0.06)
    pad_x, pad_y = 26, 15
    w = w_txt + 2 * pad_x
    h = size + 2 * pad_y
    ch = 12  # ścięcie rogu
    d = f"M{x} {y}H{x+w}V{y+h-ch}L{x+w-ch} {y+h}H{x}Z"
    tg, _ = chakra_sb.text(label, x + pad_x, y + pad_y + size * 0.76, size,
                           GRAPHITE_INK, ls_em=0.06)
    return f'<path d="{d}" fill="{YELLOW}"/>' + tg, w, h


def button_ghost(chakra_sb: VectorFont, x: float, y: float, label: str,
                 size: float = 15) -> str:
    _, w_txt = chakra_sb.text(label, 0, 0, size, "#000", ls_em=0.06)
    pad_x, pad_y = 26, 15
    w = w_txt + 2 * pad_x
    h = size + 2 * pad_y
    rect = (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h:.1f}" rx="6" '
            f'fill="none" stroke="{BORDER_D}" stroke-width="2"/>')
    tg, _ = chakra_sb.text(label, x + pad_x, y + pad_y + size * 0.76, size,
                           WHITE, ls_em=0.06)
    return rect + tg, w, h


# ---------------------------------------------------------------------------
# 1. Logo pionowe (sygnet nad napisem)
# ---------------------------------------------------------------------------
def build_stacked(main_fill: str, title: str) -> str:
    pad = 46
    sym = 300
    gap = 48
    wm_h = 46
    wm_w = wm_h * (WORDMARK_W / WORDMARK_H)
    content_w = max(sym, wm_w)
    W = round(content_w + 2 * pad)
    H = round(pad + sym + gap + wm_h + pad)
    sx = (W - sym) / 2
    sy = pad
    wm_left = (W - wm_w) / 2
    wm_top = sy + sym + gap
    body = symbol_tile(sx, sy, sym)
    wm, _ = wordmark_group(wm_left, wm_top, wm_h, main_fill)
    body += wm
    return svg_document(W, H, body, title)


# ---------------------------------------------------------------------------
# 2. Grafiki social - odzwierciedlenie hero strony
# ---------------------------------------------------------------------------
def eyebrow_text() -> str:
    return "IEC 61508 · SYSTEMY KRYTYCZNE · MBD"


LEAD_TEXT = ("Wspieramy rozwój systemów przemysłowych i innych systemów krytycznych, "
             "w których bezpieczeństwo, niezawodność i rygor procesu inżynieryjnego "
             "mają kluczowe znaczenie. Pracujemy w oparciu o IEC 61508, "
             "Model-Based Design oraz technologie MATLAB i Simulink.")


def build_og(chakra: VectorFont, chakra_sb: VectorFont, mono: VectorFont,
             titi: VectorFont) -> str:
    W, H = 1200, 630
    mx = 70
    body = [f'<rect width="{W}" height="{H}" fill="{GRAPHITE}"/>', grid_lines(W, H)]

    # diagram po prawej (jak w hero), z narożnikami blueprint
    d_scale = 0.62
    d_w = DIAGRAM_VIEW[2] * d_scale
    d_h = DIAGRAM_VIEW[3] * d_scale
    d_x = W - d_w - 46
    d_y = (H - d_h) / 2 + 6
    body.append(blueprint_corner(d_x - 14, d_y - 14, 26, "tl"))
    body.append(blueprint_corner(d_x + d_w + 14, d_y + d_h + 14, 26, "br"))
    body.append(diagram_group(mono, d_x, d_y, d_scale))

    # eyebrow
    g, _ = mono.text(eyebrow_text(), mx, 112, 15, YELLOW, ls_em=0.12)
    body.append(g)

    # nagłówek 3 wiersze
    h_size = 62
    lh = h_size * 1.16
    lines = ["INŻYNIERIA", "SYSTEMÓW", "KRYTYCZNYCH"]
    base = 205
    last_w = 0.0
    for i, line in enumerate(lines):
        y = base + i * lh
        if i == 2:  # akcent - żółte podkreślenie pod ostatnim wierszem
            _, last_w = chakra.text(line, 0, 0, h_size, WHITE, ls_em=0.005)
            uy = y - h_size * 0.06
            body.append(f'<rect x="{mx}" y="{uy:.1f}" width="{last_w:.1f}" '
                        f'height="{h_size*0.16:.1f}" fill="{YELLOW}"/>')
        g, w = chakra.text(line, mx, y, h_size, WHITE, ls_em=0.005)
        body.append(g)

    # lead - układany od dołu, żeby nigdy nie wszedł na przyciski
    btn_y = 545
    lead_size, lead_gap = 18, 26
    lead_lines = wrap_text(titi, LEAD_TEXT, lead_size, 480)
    lead_last = btn_y - 26                      # linia bazowa ostatniego wiersza
    lead_y = lead_last - (len(lead_lines) - 1) * lead_gap
    for i, line in enumerate(lead_lines):
        g, _ = titi.text(line, mx, lead_y + i * lead_gap, lead_size, MUTED_D)
        body.append(g)

    # przyciski
    bp, bw, bh = button_primary(chakra_sb, mx, btn_y, "POZNAJ NASZE KOMPETENCJE")
    body.append(bp)
    bg, _, _ = button_ghost(chakra_sb, mx + bw + 16, btn_y, "POROZMAWIAJ Z EKSPERTEM")
    body.append(bg)

    return svg_document(W, H, "".join(body),
                        "KOLSYSTEM - inżynieria systemów krytycznych")


def build_linkedin_banner(chakra: VectorFont, mono: VectorFont) -> str:
    W, H = 1584, 396
    body = [f'<rect width="{W}" height="{H}" fill="{GRAPHITE}"/>', grid_lines(W, H)]

    # diagram po prawej, skala do wysokości
    d_scale = 0.60
    d_w = DIAGRAM_VIEW[2] * d_scale
    d_h = DIAGRAM_VIEW[3] * d_scale
    d_x = W - d_w - 70
    d_y = (H - d_h) / 2
    body.append(blueprint_corner(d_x - 16, d_y - 16, 28, "tl"))
    body.append(blueprint_corner(d_x + d_w + 16, d_y + d_h + 16, 28, "br"))
    body.append(diagram_group(mono, d_x, d_y, d_scale))

    mx = 84
    # lockup u góry
    lk, _ = lockup_group(mx, 40, 66, WHITE)
    body.append(lk)

    # eyebrow
    g, _ = mono.text(eyebrow_text(), mx, 178, 14, YELLOW, ls_em=0.11)
    body.append(g)

    # nagłówek - 2 wiersze
    h_size = 54
    lh = h_size * 1.14
    base = 236
    lines = ["INŻYNIERIA SYSTEMÓW", "KRYTYCZNYCH"]
    for i, line in enumerate(lines):
        y = base + i * lh
        if i == 1:
            _, w = chakra.text(line, 0, 0, h_size, WHITE, ls_em=0.005)
            body.append(f'<rect x="{mx}" y="{y - h_size*0.06:.1f}" width="{w:.1f}" '
                        f'height="{h_size*0.16:.1f}" fill="{YELLOW}"/>')
        g, _ = chakra.text(line, mx, y, h_size, WHITE, ls_em=0.005)
        body.append(g)

    return svg_document(W, H, "".join(body),
                        "KOLSYSTEM - baner LinkedIn")


def build_linkedin_cover(chakra: VectorFont, mono: VectorFont) -> str:
    W, H = 1128, 191
    body = [f'<rect width="{W}" height="{H}" fill="{GRAPHITE}"/>', grid_lines(W, H)]

    d_scale = 0.34
    d_w = DIAGRAM_VIEW[2] * d_scale
    d_h = DIAGRAM_VIEW[3] * d_scale
    d_x = W - d_w - 54
    d_y = (H - d_h) / 2
    body.append(diagram_group(mono, d_x, d_y, d_scale))

    mx = 60
    lk, _ = lockup_group(mx, 34, 52, WHITE)
    body.append(lk)
    g, _ = mono.text(eyebrow_text(), mx, 150, 12.5, YELLOW, ls_em=0.11)
    body.append(g)

    return svg_document(W, H, "".join(body), "KOLSYSTEM - okładka LinkedIn")


def main() -> None:
    SOCIAL.mkdir(parents=True, exist_ok=True)
    chakra = VectorFont(DESKTOP_FONTS / "ChakraPetch-Bold.ttf")
    chakra_sb = VectorFont(DESKTOP_FONTS / "ChakraPetch-SemiBold.ttf")
    mono = VectorFont(DESKTOP_FONTS / "JetBrainsMono-Regular.ttf")
    titi = VectorFont(DESKTOP_FONTS / "TitilliumWeb-Regular.ttf")

    # 1) logo pionowe -> logos/svg (PNG/PDF dogeneruje główny build)
    jobs: list[tuple[Path, str, int, bool]] = []
    (SVG_LOGOS / "kolsystem-stacked-primary.svg").write_text(
        build_stacked(WHITE, "KOLSYSTEM - logo pionowe na ciemne tło"), encoding="utf-8")
    (SVG_LOGOS / "kolsystem-stacked-light.svg").write_text(
        build_stacked(GRAPHITE_INK, "KOLSYSTEM - logo pionowe na jasne tło"), encoding="utf-8")

    # 2) grafiki social -> digital/social
    social_specs = [
        ("kolsystem-social-share-1200x630.svg", build_og(chakra, chakra_sb, mono, titi), 1200),
        ("kolsystem-linkedin-banner-1584x396.svg", build_linkedin_banner(chakra, mono), 1584),
        ("kolsystem-linkedin-cover-1128x191.svg", build_linkedin_cover(chakra, mono), 1128),
    ]
    for name, svg, width in social_specs:
        svg_path = SOCIAL / name
        svg_path.write_text(svg, encoding="utf-8")
        png_path = SOCIAL / name.replace(".svg", ".png")
        render_png(svg_path, png_path, width, transparent=False)
        print("ok", png_path.relative_to(ROOT))

    # PNG + PDF logo pionowego (parytet z resztą rodziny logo)
    for name in ("kolsystem-stacked-primary", "kolsystem-stacked-light"):
        render_png(SVG_LOGOS / f"{name}.svg", BRAND / "logos" / "png" / f"{name}-2400w.png",
                   2400, transparent=True)
        render_pdf(SVG_LOGOS / f"{name}.svg", BRAND / "logos" / "pdf" / f"{name}.pdf")
        print("ok", (BRAND / 'logos' / 'png' / f'{name}-2400w.png').relative_to(ROOT))

    # aktualizacja produkcyjnej grafiki OG strony (realne odbicie hero)
    web_og = WEB_BRAND / "social-share-1200x630.png"
    if web_og.parent.exists():
        import shutil
        shutil.copy2(SOCIAL / "kolsystem-social-share-1200x630.png", web_og)
        print("ok", web_og.relative_to(ROOT))

    print("Gotowe.")


if __name__ == "__main__":
    main()
