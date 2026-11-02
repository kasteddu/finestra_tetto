#!/usr/bin/env python3
"""Generate the preliminary dimension sheet in SVG and PDF without dependencies."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import asin, cos, degrees, hypot, radians, sin, sqrt
from pathlib import Path


PAGE_W = 420.0
PAGE_H = 297.0
SCALE = 10.0  # 1:10, therefore 1 cm on site = 1 mm on paper.
MM_TO_PT = 72.0 / 25.4

SLOPE_LENGTH_CM = 120.0
CROSS_WIDTH_CM = 93.0
HIGH_EDGE_CM = 53.0
LOW_EDGE_CM = 10.0
RISE_CM = HIGH_EDGE_CM - LOW_EDGE_CM
ANGLE_DEG = degrees(asin(RISE_CM / SLOPE_LENGTH_CM))
HORIZONTAL_RUN_CM = sqrt(SLOPE_LENGTH_CM**2 - RISE_CM**2)

INK = "#20252b"
MUTED = "#626b74"
ACCENT = "#b45309"
PALE = "#d9dee3"
WHITE = "#ffffff"


@dataclass
class Text:
    x: float
    y: float
    value: str
    size: float = 3.0
    anchor: str = "start"
    bold: bool = False
    color: str = INK
    rotation: float = 0.0


@dataclass
class Line:
    x1: float
    y1: float
    x2: float
    y2: float
    width: float = 0.25
    color: str = INK
    dash: tuple[float, ...] | None = None


@dataclass
class Rect:
    x: float
    y: float
    w: float
    h: float
    width: float = 0.35
    color: str = INK
    fill: str = "none"
    dash: tuple[float, ...] | None = None


@dataclass
class Polygon:
    points: list[tuple[float, float]]
    fill: str = WHITE
    color: str = INK
    width: float = 0.2


Primitive = Text | Line | Rect | Polygon


@dataclass
class Sheet:
    primitives: list[Primitive] = field(default_factory=list)

    def text(self, x: float, y: float, value: str, **kwargs: object) -> None:
        self.primitives.append(Text(x, y, value, **kwargs))

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        *,
        width: float = 0.25,
        color: str = INK,
        dash: tuple[float, ...] | None = None,
    ) -> None:
        self.primitives.append(Line(x1, y1, x2, y2, width, color, dash))

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        width: float = 0.35,
        color: str = INK,
        fill: str = "none",
        dash: tuple[float, ...] | None = None,
    ) -> None:
        self.primitives.append(Rect(x, y, w, h, width, color, fill, dash))

    def polygon(
        self,
        points: list[tuple[float, float]],
        *,
        fill: str = WHITE,
        color: str = INK,
        width: float = 0.2,
    ) -> None:
        self.primitives.append(Polygon(points, fill, color, width))

    def dim_h(
        self,
        x1: float,
        x2: float,
        y: float,
        label: str,
        *,
        extension_from: float | None = None,
        size: float = 3.2,
    ) -> None:
        if extension_from is not None:
            self.line(x1, extension_from, x1, y + 2.0, width=0.18, color=MUTED)
            self.line(x2, extension_from, x2, y + 2.0, width=0.18, color=MUTED)
        self.line(x1, y, x2, y, width=0.22, color=ACCENT)
        self._tick(x1, y, 0.0)
        self._tick(x2, y, 0.0)
        self.text((x1 + x2) / 2, y - 1.6, label, size=size, anchor="middle", bold=True)

    def dim_v(
        self,
        x: float,
        y1: float,
        y2: float,
        label: str,
        *,
        extension_from: float | None = None,
        size: float = 3.2,
    ) -> None:
        if extension_from is not None:
            self.line(extension_from, y1, x - 2.0, y1, width=0.18, color=MUTED)
            self.line(extension_from, y2, x - 2.0, y2, width=0.18, color=MUTED)
        self.line(x, y1, x, y2, width=0.22, color=ACCENT)
        self._tick(x, y1, 90.0)
        self._tick(x, y2, 90.0)
        self.text(x - 1.6, (y1 + y2) / 2, label, size=size, anchor="middle", bold=True, rotation=270)

    def dim_aligned(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        label: str,
        *,
        offset: float = 7.0,
        size: float = 3.2,
    ) -> None:
        dx = x2 - x1
        dy = y2 - y1
        length = hypot(dx, dy)
        nx = -dy / length
        ny = dx / length
        ax, ay = x1 + nx * offset, y1 + ny * offset
        bx, by = x2 + nx * offset, y2 + ny * offset
        self.line(ax, ay, bx, by, width=0.22, color=ACCENT)
        self._tick(ax, ay, degrees(0.0))
        self._tick(bx, by, degrees(0.0))
        rotation = degrees(asin(43.0 / 120.0)) * -1
        self.text(
            (ax + bx) / 2,
            (ay + by) / 2 - 1.6,
            label,
            size=size,
            anchor="middle",
            bold=True,
            rotation=rotation,
        )

    def _tick(self, x: float, y: float, rotation_deg: float) -> None:
        angle = radians(rotation_deg + 45.0)
        half = 1.25
        self.line(
            x - cos(angle) * half,
            y - sin(angle) * half,
            x + cos(angle) * half,
            y + sin(angle) * half,
            width=0.3,
            color=ACCENT,
        )


def build_sheet() -> Sheet:
    s = Sheet()

    # Sheet frame and heading.
    s.rect(8, 8, PAGE_W - 16, PAGE_H - 16, width=0.45)
    s.text(15, 17, "FINESTRA TETTO", size=5.4, bold=True)
    s.text(15, 23, "RILEVO GEOMETRICO PRELIMINARE", size=3.1, color=MUTED)
    s.line(15, 28, PAGE_W - 15, 28, width=0.3)

    panel_y, panel_h = 34.0, 174.0
    s.rect(14, panel_y, 126, panel_h, width=0.25, color=PALE)
    s.rect(146, panel_y, 144, panel_h, width=0.25, color=PALE)
    s.rect(296, panel_y, 110, panel_h, width=0.25, color=PALE)

    # A - true-size view of the inclined opening.
    s.text(20, 42, "A - VISTA ORTOGONALE AL PIANO", size=3.4, bold=True)
    s.text(20, 47, "vera grandezza, telaio non rappresentato", size=2.4, color=MUTED)
    opening_x, opening_y = 31.0, 58.0
    opening_w = CROSS_WIDTH_CM / SCALE
    opening_h = SLOPE_LENGTH_CM / SCALE
    s.rect(opening_x, opening_y, opening_w, opening_h, width=0.6)
    s.line(
        opening_x + opening_w / 2,
        opening_y - 3,
        opening_x + opening_w / 2,
        opening_y + opening_h + 3,
        width=0.16,
        color=MUTED,
        dash=(3, 2),
    )
    s.line(
        opening_x - 3,
        opening_y + opening_h / 2,
        opening_x + opening_w + 3,
        opening_y + opening_h / 2,
        width=0.16,
        color=MUTED,
        dash=(3, 2),
    )
    s.dim_h(opening_x, opening_x + opening_w, 52, "93", extension_from=opening_y)
    s.dim_v(opening_x + opening_w + 10, opening_y, opening_y + opening_h, "120", extension_from=opening_x + opening_w)
    s.text(opening_x + opening_w / 2, opening_y + 6, "LATO ALTO  +53", size=2.7, anchor="middle", bold=True, color=ACCENT)
    s.text(opening_x + opening_w / 2, opening_y + opening_h - 5, "LATO BASSO  +10", size=2.7, anchor="middle", bold=True, color=ACCENT)

    # B - section along the slope.
    s.text(152, 42, "B - SEZIONE LUNGO LA PENDENZA", size=3.4, bold=True)
    s.text(152, 47, "quote verticali riferite allo stesso piano", size=2.4, color=MUTED)
    datum_y = 196.0
    low_x, low_y = 166.0, datum_y - LOW_EDGE_CM / SCALE
    high_x = low_x + HORIZONTAL_RUN_CM / SCALE
    high_y = datum_y - HIGH_EDGE_CM / SCALE
    s.line(154, datum_y, 286, datum_y, width=0.35, color=MUTED, dash=(5, 2))
    s.line(low_x, low_y, high_x, high_y, width=1.0, color=INK)
    s.line(low_x, low_y, low_x, datum_y, width=0.22, color=MUTED, dash=(2, 2))
    s.line(high_x, high_y, high_x, datum_y, width=0.22, color=MUTED, dash=(2, 2))
    s.dim_h(low_x, high_x, 204, f"{HORIZONTAL_RUN_CM:.1f}", extension_from=datum_y, size=2.8)
    s.dim_v(low_x - 6, low_y, datum_y, "10", extension_from=low_x, size=2.8)
    s.dim_v(high_x + 7, high_y, datum_y, "53", extension_from=high_x, size=2.8)
    s.dim_aligned(low_x, low_y, high_x, high_y, "120", offset=-12, size=2.8)
    s.line(low_x + 18, low_y, low_x + 30, low_y - 3.5, width=0.22, color=ACCENT)
    s.text(low_x + 19, low_y + 6.5, f"{ANGLE_DEG:.1f} DEG", size=2.8, bold=True, color=ACCENT)
    s.text(154, 208.0, "Piano di riferimento orizzontale", size=2.2, color=MUTED)

    # C - horizontal projection.
    s.text(302, 42, "C - PROIEZIONE ORIZZONTALE", size=3.4, bold=True)
    s.text(302, 47, "luce in pianta", size=2.4, color=MUTED)
    plan_x, plan_y = 305.0, 59.0
    plan_w = CROSS_WIDTH_CM / SCALE
    plan_h = HORIZONTAL_RUN_CM / SCALE
    s.rect(plan_x, plan_y, plan_w, plan_h, width=0.6)
    s.dim_h(plan_x, plan_x + plan_w, 54, "93", extension_from=plan_y, size=2.8)
    s.dim_v(plan_x + plan_w + 8, plan_y, plan_y + plan_h, f"{HORIZONTAL_RUN_CM:.1f}", extension_from=plan_x + plan_w, size=2.6)
    s.text(plan_x + plan_w / 2, plan_y + 6, "LATO ALTO", size=2.4, anchor="middle", color=ACCENT)
    s.text(plan_x + plan_w / 2, plan_y + plan_h - 4, "LATO BASSO", size=2.4, anchor="middle", color=ACCENT)

    # Notes and title block.
    s.line(14, 214, PAGE_W - 14, 214, width=0.35)
    s.text(15, 220, "NOTE DI RILIEVO", size=3.1, bold=True)
    notes = [
        "Misure nette: 120 cm lungo la linea di massima pendenza; 93 cm trasversale.",
        "Quote verticali 53 / 10 cm assunte rispetto allo stesso piano orizzontale.",
        f"Dimensioni derivate: dislivello 43 cm; angolo {ANGLE_DEG:.1f} DEG; proiezione 112,0 x 93 cm.",
        "Spessori, telai, cerniere, fissaggi e copertura sono da rilevare e NON sono quotati.",
    ]
    for index, note in enumerate(notes):
        s.text(15, 227 + index * 5.2, f"- {note}", size=2.55)

    s.line(260, 214, 260, 280, width=0.3)
    s.text(266, 220, "FINESTRA_TETTO", size=3.8, bold=True)
    s.text(266, 225, "Rilievo geometrico dell'apertura", size=2.5, color=MUTED)
    s.line(260, 229, 406, 229, width=0.2)
    info = [
        ("TAVOLA", "A-01"),
        ("REV.", "R0"),
        ("DATA", "02.11.2026"),
        ("SCALA", "1:10"),
        ("UNITA", "cm"),
    ]
    for index, (key, value) in enumerate(info):
        col = index % 3
        row = index // 3
        x = 267 + col * 46
        y = 238 + row * 17
        s.text(x, y, key, size=2.0, color=MUTED)
        s.text(x, y + 5, value, size=3.0, bold=True)
    s.line(260, 254, 406, 254, width=0.2)
    s.text(266, 261, "STATO", size=2.0, color=MUTED)
    s.text(266, 266, "PRELIMINARE - NON PER COSTRUZIONE", size=2.55, bold=True, color=ACCENT)
    s.text(266, 273, "Verificare tutte le quote sul posto.", size=2.35, color=MUTED)

    s.line(14, 280, PAGE_W - 14, 280, width=0.2)
    s.text(15, 285, "finestra_tetto | documento tecnico preliminare", size=2.15, color=MUTED)
    s.text(PAGE_W - 15, 285, "A-01 / R0", size=2.15, anchor="end", color=MUTED)
    return s


def svg_bytes(sheet: Sheet) -> bytes:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}mm" height="{PAGE_H}mm" viewBox="0 0 {PAGE_W} {PAGE_H}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
    ]
    for item in sheet.primitives:
        if isinstance(item, Line):
            dash = f' stroke-dasharray="{" ".join(map(str, item.dash))}"' if item.dash else ""
            parts.append(
                f'<line x1="{item.x1}" y1="{item.y1}" x2="{item.x2}" y2="{item.y2}" '
                f'stroke="{item.color}" stroke-width="{item.width}"{dash}/>'
            )
        elif isinstance(item, Rect):
            dash = f' stroke-dasharray="{" ".join(map(str, item.dash))}"' if item.dash else ""
            parts.append(
                f'<rect x="{item.x}" y="{item.y}" width="{item.w}" height="{item.h}" '
                f'fill="{item.fill}" stroke="{item.color}" stroke-width="{item.width}"{dash}/>'
            )
        elif isinstance(item, Polygon):
            points = " ".join(f"{x},{y}" for x, y in item.points)
            parts.append(
                f'<polygon points="{points}" fill="{item.fill}" stroke="{item.color}" '
                f'stroke-width="{item.width}"/>'
            )
        elif isinstance(item, Text):
            weight = "700" if item.bold else "400"
            transform = (
                f' transform="rotate({item.rotation} {item.x} {item.y})"'
                if item.rotation
                else ""
            )
            parts.append(
                f'<text x="{item.x}" y="{item.y}" fill="{item.color}" font-size="{item.size}" '
                f'font-family="Arial, Helvetica, sans-serif" font-weight="{weight}" '
                f'text-anchor="{item.anchor}"{transform}>{escape_xml(item.value)}</text>'
            )
    parts.append("</svg>")
    return ("\n".join(parts) + "\n").encode("utf-8")


def escape_xml(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def pdf_bytes(sheet: Sheet) -> bytes:
    content: list[str] = [
        "1 J 1 j",
        f"0 0 {PAGE_W * MM_TO_PT:.3f} {PAGE_H * MM_TO_PT:.3f} re 1 1 1 rg f",
    ]
    for item in sheet.primitives:
        if isinstance(item, Line):
            set_pdf_stroke(content, item.color, item.width, item.dash)
            content.append(
                f"{item.x1 * MM_TO_PT:.3f} {(PAGE_H - item.y1) * MM_TO_PT:.3f} m "
                f"{item.x2 * MM_TO_PT:.3f} {(PAGE_H - item.y2) * MM_TO_PT:.3f} l S"
            )
        elif isinstance(item, Rect):
            set_pdf_stroke(content, item.color, item.width, item.dash)
            fill, stroke = pdf_fill_stroke(item.fill, item.color)
            content.append(
                f"{item.x * MM_TO_PT:.3f} {(PAGE_H - item.y - item.h) * MM_TO_PT:.3f} "
                f"{item.w * MM_TO_PT:.3f} {item.h * MM_TO_PT:.3f} re {fill} {stroke}"
            )
        elif isinstance(item, Polygon):
            r, g, b = hex_to_rgb(item.fill)
            content.append(f"{r:.4f} {g:.4f} {b:.4f} rg")
            first, *rest = item.points
            content.append(f"{first[0] * MM_TO_PT:.3f} {(PAGE_H - first[1]) * MM_TO_PT:.3f} m")
            for x, y in rest:
                content.append(f"{x * MM_TO_PT:.3f} {(PAGE_H - y) * MM_TO_PT:.3f} l")
            set_pdf_stroke(content, item.color, item.width)
            content.append("h B")
        elif isinstance(item, Text):
            text = item.value.encode("cp1252", "replace").decode("latin-1")
            text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            r, g, b = hex_to_rgb(item.color)
            font = "F2" if item.bold else "F1"
            font_size = item.size * MM_TO_PT
            estimate = item.size * 0.52 * len(item.value)
            x = item.x
            if item.anchor == "middle":
                x -= estimate / 2
            elif item.anchor == "end":
                x -= estimate
            angle = radians(item.rotation)
            c, sn = cos(angle), -sin(angle)
            content.append(f"{r:.4f} {g:.4f} {b:.4f} rg")
            content.append(
                f"BT /{font} {font_size:.3f} Tf "
                f"{c:.6f} {sn:.6f} {-sn:.6f} {c:.6f} "
                f"{x * MM_TO_PT:.3f} {(PAGE_H - item.y) * MM_TO_PT:.3f} Tm "
                f"({text}) Tj ET"
            )

    stream = ("\n".join(content) + "\n").encode("latin-1", "replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_W * MM_TO_PT:.3f} "
            f"{PAGE_H * MM_TO_PT:.3f}] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> "
            f"/Contents 6 0 R >>"
        ).encode("ascii"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
        f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
        + stream
        + b"endstream",
    ]

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode("ascii"))
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(output)


def set_pdf_stroke(
    content: list[str],
    color: str,
    width_mm: float,
    dash: tuple[float, ...] | None = None,
) -> None:
    r, g, b = hex_to_rgb(color)
    content.append(f"{r:.4f} {g:.4f} {b:.4f} RG")
    content.append(f"{width_mm * MM_TO_PT:.3f} w")
    if dash:
        values = " ".join(f"{value * MM_TO_PT:.3f}" for value in dash)
        content.append(f"[{values}] 0 d")
    else:
        content.append("[] 0 d")


def pdf_fill_stroke(fill: str, stroke: str) -> tuple[str, str]:
    if fill == "none":
        return "n", "S"
    r, g, b = hex_to_rgb(fill)
    return f"{r:.4f} {g:.4f} {b:.4f} rg", "B"


def hex_to_rgb(value: str) -> tuple[float, float, float]:
    value = value.lstrip("#")
    return tuple(int(value[index : index + 2], 16) / 255 for index in (0, 2, 4))


def main() -> None:
    output_dir = Path(__file__).resolve().parent.parent
    sheet = build_sheet()
    (output_dir / "finestra_tetto_A01.svg").write_bytes(svg_bytes(sheet))
    (output_dir / "finestra_tetto_A01.pdf").write_bytes(pdf_bytes(sheet))
    print(f"Generated preliminary drawing in {output_dir}")


if __name__ == "__main__":
    main()
