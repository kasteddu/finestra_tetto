#!/usr/bin/env python3
"""Generate a dimensioned orthogonal sheet for the book-opening variant."""

from __future__ import annotations

from math import asin, cos, degrees, radians, sin, sqrt
from pathlib import Path

from genera_disegno import ACCENT, INK, MUTED, PAGE_H, PAGE_W, PALE, Sheet, pdf_bytes, svg_bytes
from genera_orizzontale import arrow, circle


SCALE = 20.0
OPENING_WIDTH_CM = 120.0
OPENING_DEPTH_CM = 93.0
INCLINED_LENGTH_CM = 120.0
LOW_EDGE_CM = 10.0
HIGH_EDGE_CM = 53.0
OPEN_ANGLE_DEG = 75.0

RISE_CM = HIGH_EDGE_CM - LOW_EDGE_CM
SLOPE_ANGLE_DEG = degrees(asin(RISE_CM / INCLINED_LENGTH_CM))
OLD_PLAN_DEPTH_CM = sqrt(INCLINED_LENGTH_CM**2 - RISE_CM**2)
FRONT_EXTENSION_CM = OPENING_WIDTH_CM - OLD_PLAN_DEPTH_CM
LEAF_WIDTH_CM = OPENING_WIDTH_CM / 2
LEAF_RISE_CM = LEAF_WIDTH_CM * sin(radians(OPEN_ANGLE_DEG))
LEAF_INWARD_CM = LEAF_WIDTH_CM * cos(radians(OPEN_ANGLE_DEG))
CENTRE_GAP_CM = OPENING_WIDTH_CM - 2 * LEAF_INWARD_CM


def build_sheet() -> Sheet:
    s = Sheet()
    s.rect(8, 8, PAGE_W - 16, PAGE_H - 16, width=0.45)
    s.text(15, 17, "FINESTRA TETTO / VARIANTE 03", size=5.2, bold=True)
    s.text(15, 23, "GEOMETRIA QUOTATA - APERTURA A LIBRO SU PIANO ORIZZONTALE", size=3.1, color=MUTED)
    s.line(15, 28, PAGE_W - 15, 28, width=0.3)

    # A - plan.
    s.rect(14, 34, 190, 116, width=0.25, color=PALE)
    s.text(20, 42, "A - PIANTA DEL TELAIO ORIZZONTALE", size=3.5, bold=True)
    s.text(20, 47, "due ante 60 x 93 cm; porta frontale invariata", size=2.35, color=MUTED)
    clear_x, clear_y = 38.0, 66.0
    clear_w = OPENING_WIDTH_CM / SCALE
    clear_h = OPENING_DEPTH_CM / SCALE

    # New fixed perimeter glazing.
    s.rect(clear_x - 7, clear_y - 7, clear_w + 14, 7, width=0.35, fill="#d9eef5")
    s.rect(clear_x - 7, clear_y, 7, clear_h, width=0.35, fill="#d9eef5")
    s.rect(clear_x + clear_w, clear_y, 7, clear_h, width=0.35, fill="#d9eef5")
    s.rect(clear_x - 7, clear_y + clear_h, 18, 7, width=0.35, fill="#d9eef5")
    s.rect(clear_x + clear_w - 11, clear_y + clear_h, 18, 7, width=0.35, fill="#d9eef5")

    # Clear opening and two nominal leaves.
    s.rect(clear_x, clear_y, clear_w, clear_h, width=0.7)
    s.line(clear_x + clear_w / 2, clear_y, clear_x + clear_w / 2, clear_y + clear_h, width=0.45, color=ACCENT, dash=(3, 2))
    s.line(clear_x, clear_y, clear_x, clear_y + clear_h, width=0.85, color=ACCENT)
    s.line(clear_x + clear_w, clear_y, clear_x + clear_w, clear_y + clear_h, width=0.85, color=ACCENT)
    s.text(clear_x + clear_w / 4, clear_y + 18, "ANTA SX", size=2.7, anchor="middle", bold=True)
    s.text(clear_x + clear_w * 3 / 4, clear_y + 18, "ANTA DX", size=2.7, anchor="middle", bold=True)
    s.text(clear_x + clear_w / 2, clear_y + clear_h / 2 + 3, "BATTUTA", size=2.2, anchor="middle", color=ACCENT)

    # Existing front door shown as a preserved element.
    door_x = clear_x + clear_w / 2 - 10
    door_y = clear_y + clear_h + 2
    s.rect(door_x, door_y, 20, 11, width=0.55, color=ACCENT, fill="#fffaf0", dash=(3, 2))
    s.text(door_x + 10, door_y + 4.4, "PORTA", size=2.2, anchor="middle", bold=True, color=ACCENT)
    s.text(door_x + 10, door_y + 8, "INVARIATA", size=2.0, anchor="middle", color=ACCENT)

    s.dim_h(clear_x, clear_x + clear_w, 59, "120", extension_from=clear_y - 7, size=2.9)
    s.dim_h(clear_x, clear_x + clear_w / 2, 54, "60", size=2.5)
    s.dim_h(clear_x + clear_w / 2, clear_x + clear_w, 54, "60", size=2.5)
    s.dim_v(clear_x + clear_w + 17, clear_y, clear_y + clear_h, "93", extension_from=clear_x + clear_w + 7, size=2.9)
    s.text(24, 137, "LEGENDA", size=2.7, bold=True)
    s.text(24, 142, "Linea arancione: asse cerniera", size=2.25, color=ACCENT)
    s.text(24, 147, "Bordo azzurro: vetro fisso perimetrale", size=2.25)
    s.text(24, 152, "Prospetto della porta: invariato", size=2.25)

    # B - longitudinal section.
    s.rect(210, 34, 196, 116, width=0.25, color=PALE)
    s.text(216, 42, "B - SEZIONE LONGITUDINALE", size=3.5, bold=True)
    s.text(216, 47, "raccordo tra vecchio piano inclinato e nuovo piano orizzontale", size=2.35, color=MUTED)
    datum_y = 139.0
    end_x = 358.0
    high_y = datum_y - HIGH_EDGE_CM / SCALE
    low_y = datum_y - LOW_EDGE_CM / SCALE
    old_front_x = end_x - OLD_PLAN_DEPTH_CM / SCALE
    new_front_x = end_x - OPENING_WIDTH_CM / SCALE
    s.line(218, datum_y, 377, datum_y, width=0.45, color=MUTED)
    s.text(218, 143, "QUOTA DI RIFERIMENTO +0", size=2.2, color=MUTED)

    # Existing inclined edge as a reference, not the proposed geometry.
    s.line(old_front_x, low_y, end_x, high_y, width=0.55, color=MUTED, dash=(4, 2))
    s.line(new_front_x, high_y, end_x, high_y, width=0.8, color=INK)
    s.line(new_front_x, high_y, new_front_x, low_y, width=0.35, color=ACCENT)
    s.line(new_front_x - 7, low_y, old_front_x, low_y, width=0.55, color=ACCENT)
    s.line(old_front_x, low_y, old_front_x, high_y, width=0.3, color=MUTED, dash=(2, 2))
    s.line(end_x, high_y, end_x, low_y, width=0.3, color=MUTED, dash=(2, 2))
    s.rect(new_front_x - 1.5, high_y, 3.0, low_y - high_y, width=0.45, fill="#d9eef5")
    s.line(new_front_x - 3, (high_y + low_y) / 2, 245, 117, width=0.2, color=MUTED)
    s.text(247, 116, "VETRO FISSO FRONTALE", size=2.2, bold=True)

    s.dim_v(368, high_y, datum_y, "53", extension_from=end_x, size=2.7)
    s.dim_v(374, low_y, datum_y, "10", extension_from=old_front_x, size=2.7)
    s.dim_h(new_front_x, end_x, 149, "120", size=2.7)
    s.dim_h(old_front_x, end_x, 142, "112,0", size=2.5)
    s.line(new_front_x - 3, low_y + 2, new_front_x - 3, high_y - 2, width=0.2, color=ACCENT)
    s.text(new_front_x - 12, (low_y + high_y) / 2, "43", size=2.5, anchor="middle", bold=True, color=ACCENT, rotation=270)
    s.text(248, 126, f"vecchia inclinazione {SLOPE_ANGLE_DEG:.1f} DEG", size=2.25, color=MUTED)
    s.text(334, 91, "nuovo telaio orizzontale", size=2.3, bold=True)
    s.line(332, 93, 330, high_y - 2, width=0.2, color=MUTED)

    # C - cross-section with the two leaves open.
    s.rect(14, 156, 190, 84, width=0.25, color=PALE)
    s.text(20, 164, "C - SEZIONE TRASVERSALE A LIBRO", size=3.5, bold=True)
    s.text(20, 169, f"anta aperta {OPEN_ANGLE_DEG:.0f} DEG; schema geometrico", size=2.35, color=MUTED)
    plane_y = 222.0
    left_hinge = (75.0, 210.0)
    right_hinge = (135.0, 210.0)
    leaf_len = LEAF_WIDTH_CM / SCALE
    angle = radians(OPEN_ANGLE_DEG)
    left_free = (left_hinge[0] + leaf_len * cos(angle), left_hinge[1] - leaf_len * sin(angle))
    right_free = (right_hinge[0] - leaf_len * cos(angle), right_hinge[1] - leaf_len * sin(angle))
    s.line(45, plane_y, 165, plane_y, width=0.4, color=MUTED)
    s.line(left_hinge[0], left_hinge[1], right_hinge[0], right_hinge[1], width=0.45, color=MUTED, dash=(3, 2))
    s.line(left_hinge[0], left_hinge[1], left_free[0], left_free[1], width=1.1)
    s.line(right_hinge[0], right_hinge[1], right_free[0], right_free[1], width=1.1)
    circle(s, *left_hinge, 2.1, color=ACCENT)
    circle(s, *right_hinge, 2.1, color=ACCENT)
    s.text(left_free[0], left_free[1] - 3, "ANTA SX", size=2.4, anchor="middle")
    s.text(right_free[0], right_free[1] - 3, "ANTA DX", size=2.4, anchor="middle")

    # Gas springs.
    left_base = (88.0, plane_y)
    left_leaf = (
        left_hinge[0] + leaf_len * 0.58 * cos(angle),
        left_hinge[1] - leaf_len * 0.58 * sin(angle),
    )
    right_base = (122.0, plane_y)
    right_leaf = (
        right_hinge[0] - leaf_len * 0.58 * cos(angle),
        right_hinge[1] - leaf_len * 0.58 * sin(angle),
    )
    for base, leaf_point in ((left_base, left_leaf), (right_base, right_leaf)):
        s.line(base[0], base[1], leaf_point[0], leaf_point[1], width=1.2, color=ACCENT)
        circle(s, base[0], base[1], 1.3, color=ACCENT)
    s.text(30, 233, "2 PISTONI: UNO PER ANTA", size=2.4, bold=True, color=ACCENT)
    s.text(30, 238, "Forza e corsa da calcolare sul peso reale.", size=2.2, color=MUTED)

    # D - calculation schedule.
    s.rect(210, 156, 196, 84, width=0.25, color=PALE)
    s.text(216, 164, "D - CALCOLI GEOMETRICI", size=3.5, bold=True)
    s.text(216, 169, "dimensioni in cm; quota verticale dello stato iniziale", size=2.35, color=MUTED)
    rows = [
        ("Luce orizzontale richiesta", "120 x 93"),
        ("Ante", "2 x (60 x 93)"),
        ("Dislivello iniziale", "53 - 10 = 43"),
        ("Angolo iniziale inclinato", f"{SLOPE_ANGLE_DEG:.1f} DEG"),
        ("Proiezione orizzontale iniziale", f"{OLD_PLAN_DEPTH_CM:.1f}"),
        ("Estensione necessaria sul fronte", f"{FRONT_EXTENSION_CM:.1f}"),
        ("Sollevamento libero dell'anta", f"{LEAF_RISE_CM:.1f}"),
        ("Distanza libera centrale in pianta", f"{CENTRE_GAP_CM:.1f}"),
    ]
    for index, (label, value) in enumerate(rows):
        y = 179 + index * 6.5
        s.text(216, y, label, size=2.25)
        s.text(399, y, value, size=2.35, anchor="end", bold=True)
        if index < len(rows) - 1:
            s.line(216, y + 1.7, 399, y + 1.7, width=0.08, color=PALE)
    s.text(216, 234, "Ipotesi: asse cerniera a +53 cm; angolo apertura 75 DEG.", size=2.15, color=MUTED)

    # Title block.
    s.line(14, 246, 406, 246, width=0.35)
    s.text(20, 254, "FINESTRA_TETTO / VARIANTE 03", size=3.8, bold=True)
    s.text(20, 259, "Ricalcolo geometrico con apertura orizzontale a libro", size=2.5, color=MUTED)
    s.text(250, 254, "TAVOLA", size=2.0, color=MUTED)
    s.text(250, 259, "A-04", size=3.2, bold=True)
    s.text(292, 254, "REV.", size=2.0, color=MUTED)
    s.text(292, 259, "R0", size=3.2, bold=True)
    s.text(326, 254, "SCALA", size=2.0, color=MUTED)
    s.text(326, 259, "1:20", size=3.2, bold=True)
    s.text(363, 254, "DATA", size=2.0, color=MUTED)
    s.text(363, 259, "02.11.2026", size=3.0, bold=True)
    s.line(14, 264, 406, 264, width=0.2)
    s.text(20, 270, "STATO", size=2.0, color=MUTED)
    s.text(44, 270, "PRELIMINARE - NON PER COSTRUZIONE", size=2.6, bold=True, color=ACCENT)
    s.text(20, 276, "Verificare quota del cordolo, larghezza porta, spessori del telaio e peso delle ante.", size=2.25)
    s.text(20, 282, "La proiezione orizzontale dei 120 cm inclinati è 112,0 cm; il nuovo fronte aggiunge circa 8,0 cm.", size=2.25)
    return s


def main() -> None:
    output_dir = Path(__file__).resolve().parent.parent / "varianti" / "variante_03"
    output_dir.mkdir(parents=True, exist_ok=True)
    sheet = build_sheet()
    (output_dir / "finestra_tetto_A04_geometria_a_libro.svg").write_bytes(svg_bytes(sheet))
    (output_dir / "finestra_tetto_A04_geometria_a_libro.pdf").write_bytes(pdf_bytes(sheet))
    print(f"Generated recalculated drawing in {output_dir}")


if __name__ == "__main__":
    main()
