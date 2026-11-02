#!/usr/bin/env python3
"""Generate the preliminary two-leaf book-opening roof window drawing."""

from __future__ import annotations

from math import cos, radians, sin
from pathlib import Path

from genera_disegno import ACCENT, INK, MUTED, PAGE_H, PAGE_W, PALE, Sheet, pdf_bytes, svg_bytes
from genera_orizzontale import arrow, circle


SCALE = 20.0
OPENING_WIDTH_CM = 120.0
OPENING_DEPTH_CM = 93.0
LEAF_WIDTH_CM = OPENING_WIDTH_CM / 2
OPEN_ANGLE = 70.0


def build_sheet() -> Sheet:
    s = Sheet()
    s.rect(8, 8, PAGE_W - 16, PAGE_H - 16, width=0.45)
    s.text(15, 17, "FINESTRA TETTO / APERTURA A LIBRO", size=5.2, bold=True)
    s.text(15, 23, "DUE ANTE A VETRO, PISTONI SIMMETRICI, PORTA FRONTALE INVARIATA", size=3.1, color=MUTED)
    s.line(15, 28, PAGE_W - 15, 28, width=0.3)

    # A - plan.
    s.rect(14, 34, 162, 128, width=0.25, color=PALE)
    s.text(20, 42, "A - PIANTA", size=3.4, bold=True)
    s.text(20, 47, "due ante; porta sul fronte; fasce vetrate perimetrali", size=2.35, color=MUTED)
    clear_x, clear_y = 35.0, 65.0
    clear_w = OPENING_WIDTH_CM / SCALE
    clear_h = OPENING_DEPTH_CM / SCALE

    # Fixed glazed perimeter, interrupted at the existing front door.
    s.rect(clear_x - 7, clear_y - 7, clear_w + 14, 7, width=0.35, color=INK, fill="#d9eef5")
    s.rect(clear_x - 7, clear_y, 7, clear_h, width=0.35, color=INK, fill="#d9eef5")
    s.rect(clear_x + clear_w, clear_y, 7, clear_h, width=0.35, color=INK, fill="#d9eef5")
    s.rect(clear_x - 7, clear_y + clear_h, 16, 7, width=0.35, color=INK, fill="#d9eef5")
    s.rect(clear_x + clear_w - 9, clear_y + clear_h, 16, 7, width=0.35, color=INK, fill="#d9eef5")

    s.rect(clear_x, clear_y, clear_w, clear_h, width=0.7, color=INK)
    s.line(clear_x + clear_w / 2, clear_y, clear_x + clear_w / 2, clear_y + clear_h, width=0.35, color=MUTED, dash=(3, 2))
    s.line(clear_x, clear_y, clear_x, clear_y + clear_h, width=0.8, color=ACCENT)
    s.line(clear_x + clear_w, clear_y, clear_x + clear_w, clear_y + clear_h, width=0.8, color=ACCENT)
    s.text(clear_x + clear_w / 4, clear_y + clear_h / 2, "ANTA SX", size=2.6, anchor="middle", bold=True)
    s.text(clear_x + clear_w * 3 / 4, clear_y + clear_h / 2, "ANTA DX", size=2.6, anchor="middle", bold=True)
    s.text(clear_x, clear_y - 2.2, "CERNIERA", size=2.1, color=ACCENT, bold=True)
    s.text(clear_x + clear_w, clear_y - 2.2, "CERNIERA", size=2.1, anchor="end", color=ACCENT, bold=True)

    door_x, door_y = clear_x + clear_w / 2 - 10, clear_y + clear_h + 2
    s.rect(door_x, door_y, 20, 11, width=0.5, color=ACCENT, fill="#fffaf0", dash=(3, 2))
    s.text(door_x + 10, door_y + 4.5, "PORTA", size=2.2, anchor="middle", bold=True, color=ACCENT)
    s.text(door_x + 10, door_y + 8, "ESISTENTE", size=2.0, anchor="middle", color=ACCENT)
    s.dim_h(clear_x, clear_x + clear_w, 58, "120", extension_from=clear_y - 7, size=2.8)
    s.dim_h(clear_x, clear_x + clear_w / 2, 54, "60", size=2.5)
    s.dim_h(clear_x + clear_w / 2, clear_x + clear_w, 54, "60", size=2.5)
    s.dim_v(clear_x + clear_w + 17, clear_y, clear_y + clear_h, "93", extension_from=clear_x + clear_w + 7, size=2.8)
    s.text(20, 128, "VETRO FISSO PERIMETRALE", size=2.3, color=ACCENT, bold=True)
    s.text(20, 133, "La fascia riallinea le quote senza modificare la porta.", size=2.25)
    arrow(s, 66, 141, 66, 124, width=0.35)
    s.text(20, 156, "FRONTE / ACCESSO ESISTENTE", size=2.5, bold=True)

    # B - front elevation.
    s.rect(182, 34, 110, 128, width=0.25, color=PALE)
    s.text(188, 42, "B - PROSPETTO FRONTALE", size=3.4, bold=True)
    s.text(188, 47, "schema; altezze da rilevare", size=2.35, color=MUTED)
    fx, fy, fw = 207.0, 82.0, 60.0
    fh = 70.0
    s.line(190, 155, 284, 155, width=0.45)
    s.rect(fx, fy, fw, fh, width=0.6)
    s.rect(fx - 7, fy, 7, fh, width=0.35, fill="#d9eef5")
    s.rect(fx + fw, fy, 7, fh, width=0.35, fill="#d9eef5")
    s.rect(fx, fy, fw, 5, width=0.55, fill="#d9eef5")
    s.line(fx + fw / 2, fy + 5, fx + fw / 2, 132, width=0.35, color=MUTED, dash=(3, 2))
    s.text(fx + fw / 4, fy + 14, "ANTA SX", size=2.25, anchor="middle")
    s.text(fx + fw * 3 / 4, fy + 14, "ANTA DX", size=2.25, anchor="middle")
    s.rect(fx + fw / 2 - 11, 128, 22, 27, width=0.55, color=ACCENT, dash=(3, 2))
    s.text(fx + fw / 2, 140, "PORTA", size=2.4, anchor="middle", bold=True, color=ACCENT)
    s.text(fx + fw / 2, 144.5, "INVARIATA", size=2.15, anchor="middle", color=ACCENT)
    s.text(188, 166, "Le fasce vetrate laterali e superiore formano", size=2.2)
    s.text(188, 171, "il raccordo verso il nuovo telaio orizzontale.", size=2.2)

    # C - cross-section with the two leaves open.
    s.rect(298, 34, 108, 128, width=0.25, color=PALE)
    s.text(304, 42, "C - SEZIONE A LIBRO", size=3.4, bold=True)
    s.text(304, 47, f"aperto circa {OPEN_ANGLE:.0f} DEG; schema", size=2.35, color=MUTED)
    left_hinge = (316.0, 114.0)
    right_hinge = (376.0, 114.0)
    leaf = LEAF_WIDTH_CM / SCALE
    angle = radians(OPEN_ANGLE)
    left_free = (left_hinge[0] + leaf * cos(angle), left_hinge[1] - leaf * sin(angle))
    right_free = (right_hinge[0] - leaf * cos(angle), right_hinge[1] - leaf * sin(angle))
    s.line(305, 151, 399, 151, width=0.45)
    s.line(left_hinge[0], left_hinge[1], left_hinge[0], 151, width=0.35, color=MUTED)
    s.line(right_hinge[0], right_hinge[1], right_hinge[0], 151, width=0.35, color=MUTED)
    s.line(left_hinge[0], left_hinge[1], left_free[0], left_free[1], width=1.0, color=INK)
    s.line(right_hinge[0], right_hinge[1], right_free[0], right_free[1], width=1.0, color=INK)
    s.line(left_hinge[0], left_hinge[1], right_hinge[0], right_hinge[1], width=0.3, color=MUTED, dash=(3, 2))
    s.text(left_free[0], left_free[1] - 3, "ANTA SX", size=2.25, anchor="middle")
    s.text(right_free[0], right_free[1] - 3, "ANTA DX", size=2.25, anchor="middle")
    circle(s, *left_hinge, 2.2, color=ACCENT)
    circle(s, *right_hinge, 2.2, color=ACCENT)

    # One gas spring per leaf, drawn schematically.
    left_anchor = (326.0, 144.0)
    left_leaf_anchor = (
        left_hinge[0] + leaf * 0.58 * cos(angle),
        left_hinge[1] - leaf * 0.58 * sin(angle),
    )
    right_anchor = (366.0, 144.0)
    right_leaf_anchor = (
        right_hinge[0] - leaf * 0.58 * cos(angle),
        right_hinge[1] - leaf * 0.58 * sin(angle),
    )
    for anchor, leaf_anchor in ((left_anchor, left_leaf_anchor), (right_anchor, right_leaf_anchor)):
        s.line(anchor[0], anchor[1], leaf_anchor[0], leaf_anchor[1], width=1.2, color=ACCENT)
        circle(s, anchor[0], anchor[1], 1.5, color=ACCENT)
        circle(s, leaf_anchor[0], leaf_anchor[1], 1.5, color=ACCENT)
    s.text(312, 159, "1 PISTONE A GAS PER ANTA", size=2.25, color=ACCENT, bold=True)
    s.text(312, 164, "ANCORAGGI SIMMETRICI", size=2.25, color=ACCENT)

    # D - key detail.
    s.rect(14, 169, 205, 75, width=0.25, color=PALE)
    s.text(20, 177, "D - DETTAGLIO CERNIERA / PISTONE", size=3.4, bold=True)
    s.text(20, 182, "schema funzionale, non in scala", size=2.35, color=MUTED)
    s.rect(29, 221, 110, 7, width=0.45, fill="#e4e7ea")
    s.text(34, 225.5, "TELAIO FISSO / FASCIA VETRATA", size=2.2)
    hinge = (145.0, 221.0)
    leaf_end = (105.0, 199.0)
    s.line(hinge[0], hinge[1], leaf_end[0], leaf_end[1], width=1.0)
    circle(s, hinge[0], hinge[1], 3.0, color=ACCENT)
    s.text(101, 197, "ANTA VETRATA", size=2.25)
    piston_base = (49.0, 234.0)
    piston_leaf = (113.0, 207.0)
    s.line(piston_base[0], piston_base[1], piston_leaf[0], piston_leaf[1], width=1.7, color=ACCENT)
    s.line(piston_base[0] - 2, piston_base[1] + 2, piston_base[0] + 2, piston_base[1] - 2, width=0.5, color=ACCENT)
    s.text(47, 242, "PISTONE", size=2.3, color=ACCENT, bold=True)
    s.text(151, 199, "Cerniera continua o", size=2.2)
    s.text(151, 203, "serie pesante.", size=2.2)
    s.text(151, 211, "Guarnizione centrale", size=2.2)
    s.text(151, 215, "a doppia battuta.", size=2.2)

    # Notes and title block.
    s.rect(224, 169, 182, 41, width=0.25, color=PALE)
    s.text(230, 177, "REGOLE DI PROGETTO", size=3.1, bold=True)
    notes = [
        "Due ante nominali 60 x 93 cm; luce complessiva 120 x 93 cm.",
        "Due pistoni a gas, uno per anta, con ancoraggi speculari.",
        "Porta frontale esistente mantenuta senza modifiche.",
        "Vetro fisso perimetrale per raccordare le quote esistenti.",
    ]
    for index, note in enumerate(notes):
        s.text(230, 185 + index * 5.4, f"- {note}", size=2.25)

    s.line(224, 214, 406, 214, width=0.35)
    s.text(230, 221, "FINESTRA_TETTO", size=3.8, bold=True)
    s.text(230, 226, "Variante a libro con due ante", size=2.5, color=MUTED)
    s.line(224, 231, 406, 231, width=0.2)
    info = [
        ("TAVOLA", "A-03"),
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
    s.text(230, 274, "NON PER COSTRUZIONE - PISTONI DA CALIBRARE SUL PESO REALE", size=2.15, bold=True, color=ACCENT)

    s.line(14, 280, PAGE_W - 14, 280, width=0.2)
    s.text(15, 285, "finestra_tetto | variante a libro preliminare", size=2.15, color=MUTED)
    s.text(PAGE_W - 15, 285, "A-03 / R0", size=2.15, anchor="end", color=MUTED)
    return s


def main() -> None:
    output_dir = Path(__file__).resolve().parent.parent / "varianti" / "variante_02"
    sheet = build_sheet()
    (output_dir / "finestra_tetto_A03_a_libro.svg").write_bytes(svg_bytes(sheet))
    (output_dir / "finestra_tetto_A03_a_libro.pdf").write_bytes(pdf_bytes(sheet))
    print(f"Generated book-opening drawing in {output_dir}")


if __name__ == "__main__":
    main()
