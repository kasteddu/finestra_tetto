#!/usr/bin/env python3
"""Generate preliminary drawings for a horizontal sliding glass roof hatch."""

from __future__ import annotations

from math import cos, pi, sin
from pathlib import Path

from genera_disegno import (
    ACCENT,
    INK,
    MUTED,
    PAGE_H,
    PAGE_W,
    PALE,
    Sheet,
    pdf_bytes,
    svg_bytes,
)


SCALE = 20.0  # 1:20, therefore 1 cm on site = 0.5 mm on paper.
OPENING_WIDTH_CM = 120.0
OPENING_DEPTH_CM = 93.0


def arrow(
    sheet: Sheet,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    color: str = ACCENT,
    width: float = 0.45,
) -> None:
    sheet.line(x1, y1, x2, y2, width=width, color=color)
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    nx, ny = -uy, ux
    head = 3.0
    sheet.polygon(
        [
            (x2, y2),
            (x2 - ux * head + nx * 1.3, y2 - uy * head + ny * 1.3),
            (x2 - ux * head - nx * 1.3, y2 - uy * head - ny * 1.3),
        ],
        fill=color,
        color=color,
    )


def circle(sheet: Sheet, x: float, y: float, radius: float, *, color: str = INK, width: float = 0.3) -> None:
    points = [
        (x + cos(2 * pi * index / 32) * radius, y + sin(2 * pi * index / 32) * radius)
        for index in range(32)
    ]
    sheet.polygon(points, fill="none", color=color, width=width)


def build_horizontal_sheet() -> Sheet:
    s = Sheet()
    s.rect(8, 8, PAGE_W - 16, PAGE_H - 16, width=0.45)
    s.text(15, 17, "FINESTRA TETTO / VARIANTE ORIZZONTALE", size=5.2, bold=True)
    s.text(15, 23, "PROGETTO DI MASSIMA - COPERCHIO VETRATO SCORREVOLE", size=3.1, color=MUTED)
    s.line(15, 28, PAGE_W - 15, 28, width=0.3)

    # Panel A - plan.
    s.rect(14, 34, 150, 128, width=0.25, color=PALE)
    s.text(20, 42, "A - PIANTA / CHIUSO E APERTO", size=3.4, bold=True)
    s.text(20, 47, "scala 1:20; scorrimento lungo 93 cm", size=2.35, color=MUTED)
    roof_x, roof_y = 24.0, 56.0
    s.rect(roof_x, roof_y, 76.0, 76.0, width=0.25, color=PALE, fill="#f7f8f9")
    clear_x, clear_y = 32.0, 63.0
    clear_w = OPENING_WIDTH_CM / SCALE
    clear_h = OPENING_DEPTH_CM / SCALE
    s.rect(clear_x, clear_y, clear_w, clear_h, width=0.7, color=INK)
    s.text(clear_x + clear_w / 2, clear_y + clear_h / 2, "LUCE", size=2.7, anchor="middle", bold=True)
    s.rect(clear_x - 2, clear_y - 2, clear_w + 4, clear_h + 4, width=0.3, color=MUTED, dash=(3, 2))
    panel_y = clear_y + clear_h + 4
    s.rect(clear_x - 2, panel_y, clear_w + 4, clear_h + 4, width=0.5, color=ACCENT, dash=(4, 2))
    s.text(clear_x + clear_w / 2, panel_y + clear_h / 2 + 5, "PANNELLO VETRATO", size=2.4, anchor="middle", color=ACCENT)
    s.text(clear_x + clear_w / 2, panel_y + clear_h / 2 + 9, "IN POSIZIONE APERTA", size=2.4, anchor="middle", color=ACCENT)
    s.dim_h(clear_x, clear_x + clear_w, 59, "120", extension_from=clear_y - 2, size=2.8)
    s.dim_v(clear_x + clear_w + 9, clear_y, clear_y + clear_h, "93", extension_from=clear_x + clear_w, size=2.8)
    s.dim_v(clear_x + clear_w + 16, panel_y, panel_y - 4 + clear_h, "93", size=2.8)
    arrow(s, clear_x + clear_w / 2, clear_y + clear_h + 1, clear_x + clear_w / 2, panel_y - 1)
    s.text(clear_x + clear_w / 2 + 3, clear_y + clear_h + 4, "DIREZIONE DI SCORRIMENTO", size=2.25, color=ACCENT)
    s.text(20, 156, "Il pannello scorre sopra il telaio fisso.", size=2.3)

    # Panel B - transverse section, closed.
    s.rect(169, 34, 116, 128, width=0.25, color=PALE)
    s.text(175, 42, "B - SEZIONE TRASVERSALE", size=3.4, bold=True)
    s.text(175, 47, "chiuso; spessori schematici", size=2.35, color=MUTED)
    x1, x2 = 185.0, 245.0
    deck_y = 133.0
    s.line(177, deck_y, 270, deck_y, width=0.45)
    s.rect(x1 - 7, deck_y - 23, 7, 23, width=0.35, fill="#eceff1")
    s.rect(x2, deck_y - 23, 7, 23, width=0.35, fill="#eceff1")
    s.dim_h(x1, x2, deck_y + 8, "120", extension_from=deck_y - 23, size=2.8)
    s.rect(x1 - 3, 96, x2 - x1 + 6, 5, width=0.55, fill="#d9eef5")
    s.text((x1 + x2) / 2, 99.5, "VETRO LAMINATO", size=2.2, anchor="middle")
    s.line(x1 - 2, 106, x2 + 2, 106, width=0.5, color=ACCENT)
    s.text((x1 + x2) / 2, 111, "TELAIO SCORREVOLE", size=2.3, anchor="middle", bold=True, color=ACCENT)
    s.line(x1, 117, x1 + 4, 117, width=0.4)
    s.line(x2 - 4, 117, x2, 117, width=0.4)
    s.text((x1 + x2) / 2, 120, "BATTUTA + GUARNIZIONE EPDM", size=2.15, anchor="middle")
    s.text(175, 151, "Quota verticale fuori scala.", size=2.25, color=MUTED)

    # Panel C - longitudinal section, open.
    s.rect(290, 34, 116, 128, width=0.25, color=PALE)
    s.text(296, 42, "C - SEZIONE LONGITUDINALE", size=3.4, bold=True)
    s.text(296, 47, "pannello arretrato; soglia libera", size=2.35, color=MUTED)
    deck2_y = 135.0
    open_x = 304.0
    open_w = OPENING_DEPTH_CM / SCALE
    panel_w = open_w + 2
    s.line(297, deck2_y, 398, deck2_y, width=0.45)
    s.rect(open_x - 3, deck2_y - 17, 3, 17, width=0.35, fill="#eceff1")
    s.rect(open_x + open_w, deck2_y - 17, 3, 17, width=0.35, fill="#eceff1")
    # Closed-position ghost, then open panel parked above the adjacent deck.
    s.rect(open_x - 1, 102, panel_w, 5, width=0.3, color=MUTED, dash=(3, 2))
    parked_x = open_x + open_w
    s.rect(parked_x, 92, panel_w, 5, width=0.55, fill="#d9eef5")
    s.line(open_x - 1, 112, open_x + panel_w, 112, width=0.35, color=MUTED, dash=(3, 2))
    s.line(parked_x, 104, parked_x + panel_w, 104, width=0.45, color=ACCENT)
    s.dim_h(open_x, open_x + open_w, deck2_y + 8, "93", extension_from=deck2_y - 17, size=2.8)
    s.dim_h(open_x, parked_x, 82, "93", size=2.8)
    arrow(s, 312, 82, 358, 82)
    s.text(322, 78, "CORSA / PARCHEGGIO", size=2.25, color=ACCENT, bold=True)
    s.text(297, 151, "La guida sporge oltre il vano scala.", size=2.25, color=MUTED)

    # Panel D - mechanism and overlapping seal detail.
    s.rect(14, 169, 205, 75, width=0.25, color=PALE)
    s.text(20, 177, "D - DETTAGLIO TIPO CARRELLO E TENUTA", size=3.4, bold=True)
    s.text(20, 182, "schema, non in scala", size=2.35, color=MUTED)
    rail_y = 217.0
    s.rect(28, rail_y, 100, 7, width=0.4, fill="#e4e7ea")
    s.text(34, rail_y + 4.5, "GUIDA / CONTROGUIDA IN ALLUMINIO", size=2.25)
    for x in (55.0, 91.0):
        circle(s, x, rail_y - 4, 3.2, width=0.4)
        s.text(x + 6, rail_y - 5, "RULLO ANTISOLLEVAMENTO", size=2.1)
    s.rect(35, 195, 85, 5, width=0.5, fill="#d9eef5")
    s.text(78, 199, "VETRO STRATIFICATO DI SICUREZZA", size=2.2, anchor="middle")
    s.line(120, 200, 190, 210, width=0.2, color=MUTED, dash=(2, 2))
    s.text(132, 217, "Guarnizioni EPDM a doppia battuta", size=2.25)
    s.text(133, 222, "Drenaggio perimetrale e canale raccolta", size=2.25)
    s.text(133, 227, "Finecorsa meccanico regolabile", size=2.25)

    # Notes and title block.
    s.rect(224, 169, 182, 41, width=0.25, color=PALE)
    s.text(230, 177, "IPOTESI DI PROGETTO", size=3.1, bold=True)
    notes = [
        "Luce netta 120 x 93 cm. Scorrimento lungo il lato da 93 cm.",
        "Pannello vetrato unico; area di parcheggio adiacente all'apertura.",
        "Movimento motorizzato consigliato; sblocco manuale di emergenza.",
        "Protezione anticaduta obbligatoria sul vano scala.",
    ]
    for index, note in enumerate(notes):
        s.text(230, 184 + index * 5.3, f"- {note}", size=2.25)

    s.line(224, 214, 406, 214, width=0.35)
    s.text(230, 221, "FINESTRA_TETTO", size=3.8, bold=True)
    s.text(230, 226, "Variante orizzontale a scorrimento", size=2.5, color=MUTED)
    s.line(224, 231, 406, 231, width=0.2)
    info = [
        ("TAVOLA", "A-02"),
        ("REV.", "R0"),
        ("SCALA", "1:20"),
        ("DATA", "02.11.2026"),
        ("UNITA", "cm"),
        ("STATO", "PRELIMINARE"),
    ]
    for index, (key, value) in enumerate(info):
        col = index % 3
        row = index // 3
        x = 230 + col * 57
        y = 240 + row * 17
        s.text(x, y, key, size=2.0, color=MUTED)
        s.text(x, y + 5, value, size=2.9, bold=True)
    s.text(230, 274, "NON PER COSTRUZIONE - VERIFICARE INGOMBRI E SUPPORTI", size=2.3, bold=True, color=ACCENT)

    s.line(14, 280, PAGE_W - 14, 280, width=0.2)
    s.text(15, 285, "finestra_tetto | variante orizzontale preliminare", size=2.15, color=MUTED)
    s.text(PAGE_W - 15, 285, "A-02 / R0", size=2.15, anchor="end", color=MUTED)
    return s


def main() -> None:
    output_dir = Path(__file__).resolve().parent.parent / "varianti" / "variante_01"
    sheet = build_horizontal_sheet()
    (output_dir / "finestra_tetto_A02_orizzontale.svg").write_bytes(svg_bytes(sheet))
    (output_dir / "finestra_tetto_A02_orizzontale.pdf").write_bytes(pdf_bytes(sheet))
    print(f"Generated horizontal concept drawing in {output_dir}")


if __name__ == "__main__":
    main()
