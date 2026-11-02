#!/usr/bin/env python3
"""Generate an isometric concept for the two-leaf book-opening roof window."""

from __future__ import annotations

from math import cos, radians, sin
from pathlib import Path

from genera_concept import HEIGHT, WIDTH, line, point, polygon, text, world_polygon


OPENING_W = 120.0
OPENING_D = 93.0
HINGE_Z = 30.0
OPEN_ANGLE = radians(70.0)


def left_map(x: float, y: float, z: float = HINGE_Z) -> tuple[float, float, float]:
    return (x * cos(OPEN_ANGLE), y, z + x * sin(OPEN_ANGLE))


def right_map(x: float, y: float, z: float = HINGE_Z) -> tuple[float, float, float]:
    distance = OPENING_W - x
    return (OPENING_W - distance * cos(OPEN_ANGLE), y, z + distance * sin(OPEN_ANGLE))


def leaf_polygon(
    mapper,
    x_points: tuple[float, ...],
    y_points: tuple[float, ...],
    fill: str,
    stroke: str = "none",
    width: float = 0,
    opacity: float = 1,
) -> str:
    corners = [
        (x_points[0], y_points[0], HINGE_Z),
        (x_points[1], y_points[0], HINGE_Z),
        (x_points[1], y_points[1], HINGE_Z),
        (x_points[0], y_points[1], HINGE_Z),
    ]
    return world_polygon([mapper(*corner) for corner in corners], fill, stroke, width, opacity)


def build_svg() -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        "<defs>",
        '<linearGradient id="bg2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f8f4ec"/><stop offset="1" stop-color="#dbe7e8"/></linearGradient>',
        '<linearGradient id="deck2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8decd"/><stop offset="1" stop-color="#c9b79d"/></linearGradient>',
        '<linearGradient id="glass2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a9e2ea" stop-opacity=".78"/><stop offset=".48" stop-color="#eefcfd" stop-opacity=".38"/><stop offset="1" stop-color="#5094aa" stop-opacity=".74"/></linearGradient>',
        '<linearGradient id="metal2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f1f3f4"/><stop offset=".5" stop-color="#77838b"/><stop offset="1" stop-color="#2f3940"/></linearGradient>',
        '<radialGradient id="shade2"><stop offset="0" stop-color="#26343a" stop-opacity=".2"/><stop offset="1" stop-color="#26343a" stop-opacity="0"/></radialGradient>',
        "</defs>",
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg2)"/>',
        '<ellipse cx="830" cy="700" rx="540" ry="275" fill="url(#shade2)"/>',
    ]

    # Roof deck.
    parts.append(
        world_polygon(
            [(-95, -85, 0), (265, -85, 0), (265, 245, 0), (-95, 245, 0)],
            "url(#deck2)",
            "#a69279",
            3,
        )
    )
    for value in range(-72, 246, 12):
        parts.append(line(point(-95, value, 0.3), point(265, value, 0.3), "#b4a58e", 1.2, opacity=0.55))
        parts.append(line(point(value, -85, 0.4), point(value, 245, 0.4), "#c4b6a2", 0.8, opacity=0.3))

    # Stair opening.
    opening = [(0, 0), (120, 0), (120, 93), (0, 93)]
    parts.append(world_polygon([(x, y, -58) for x, y in opening], "#111c22"))
    parts.append(world_polygon([(0, 0, -58), (0, 93, -58), (0, 93, HINGE_Z), (0, 0, HINGE_Z)], "#59666d"))
    parts.append(world_polygon([(0, 93, -58), (120, 93, -58), (120, 93, HINGE_Z), (0, 93, HINGE_Z)], "#d8d2c8"))
    parts.append(world_polygon([(120, 0, -58), (120, 93, -58), (120, 93, HINGE_Z), (120, 0, HINGE_Z)], "#7b878d"))
    for index in range(5):
        z = -50 + index * 8
        parts.append(
            world_polygon(
                [
                    (12, 15 + index * 8, z),
                    (105, 15 + index * 8, z),
                    (105, 28 + index * 8, z),
                    (12, 28 + index * 8, z),
                ],
                "#b7aa96",
                "#887b6b",
                1,
            )
        )

    # Fixed glazed perimeter around the new horizontal frame.
    glass = "url(#glass2)"
    parts.append(world_polygon([(-12, -9, HINGE_Z), (132, -9, HINGE_Z), (132, -9, 0), (-12, -9, 0)], glass, "#477888", 2, 0.82))
    parts.append(world_polygon([(-9, 0, HINGE_Z), (-9, 93, HINGE_Z), (-9, 93, 0), (-9, 0, 0)], glass, "#477888", 2, 0.8))
    parts.append(world_polygon([(129, 0, HINGE_Z), (129, 93, HINGE_Z), (129, 93, 0), (129, 0, 0)], glass, "#477888", 2, 0.8))
    parts.append(world_polygon([(0, 96, HINGE_Z), (45, 96, HINGE_Z), (45, 96, 0), (0, 96, 0)], glass, "#477888", 2, 0.82))
    parts.append(world_polygon([(75, 96, HINGE_Z), (120, 96, HINGE_Z), (120, 96, 0), (75, 96, 0)], glass, "#477888", 2, 0.82))

    # Existing front door, kept unchanged.
    parts.append(world_polygon([(45, 96, 47), (75, 96, 47), (75, 96, 0), (45, 96, 0)], "#eff4f4", "#46545b", 3, 0.96))
    parts.append(world_polygon([(48, 95.5, 43), (72, 95.5, 43), (72, 95.5, 4), (48, 95.5, 4)], "#c6dce2", "#6f858e", 1.5, 0.94))
    parts.append(line(point(68, 95, 22), point(68, 95, 16), "#3e4b51", 3))

    # Fixed horizontal frame and hinges.
    parts.append(world_polygon([(x, y, HINGE_Z) for x, y in ((0, 0), (120, 0), (120, 93), (0, 93))], "none", "url(#metal2)", 8))
    parts.append(line(point(0, 0, HINGE_Z + 2), point(0, 93, HINGE_Z + 2), "#b45309", 6))
    parts.append(line(point(120, 0, HINGE_Z + 2), point(120, 93, HINGE_Z + 2), "#b45309", 6))

    # Two opened glass leaves, each rotating around an opposite outer edge.
    parts.append(leaf_polygon(left_map, (0, 60), (0, 93), "url(#glass2)", "#3a6b7a", 4))
    parts.append(leaf_polygon(right_map, (60, 120), (0, 93), "url(#glass2)", "#3a6b7a", 4))

    for mapper, x1, x2 in ((left_map, 0, 60), (right_map, 60, 120)):
        parts.append(line(point(*mapper(x1, 0, HINGE_Z)), point(*mapper(x1, 93, HINGE_Z)), "#59656c", 5))
        parts.append(line(point(*mapper(x2, 0, HINGE_Z)), point(*mapper(x2, 93, HINGE_Z)), "#59656c", 5))
        for y in (3, 18, 33, 48, 63, 78, 90):
            start = mapper(x1 + 2, y, HINGE_Z + 0.8)
            end = mapper(x2 - 2, y, HINGE_Z + 0.8)
            parts.append(line(point(*start), point(*end), "#ffffff", 3, opacity=0.35))

    # A gas piston under each opened leaf.
    left_piston_base = point(34, 72, HINGE_Z - 2)
    left_leaf_point = point(*left_map(35, 72, HINGE_Z + 2))
    right_piston_base = point(86, 72, HINGE_Z - 2)
    right_leaf_point = point(*right_map(85, 72, HINGE_Z + 2))
    for start, end in ((left_piston_base, left_leaf_point), (right_piston_base, right_leaf_point)):
        parts.append(line(start, end, "#b45309", 7))
        parts.append(f'<circle cx="{start[0]:.1f}" cy="{start[1]:.1f}" r="5" fill="#7c3706"/>')
        parts.append(f'<circle cx="{end[0]:.1f}" cy="{end[1]:.1f}" r="5" fill="#7c3706"/>')

    # Motion and symmetry arrows.
    centre_top = point(60, 30, HINGE_Z)
    left_arrow = point(32, 30, HINGE_Z + 49)
    right_arrow = point(88, 30, HINGE_Z + 49)
    parts.append(line(centre_top, point(28, 30, HINGE_Z + 12), "#f5fbfc", 3, "7 6", 0.8))
    parts.append(line(centre_top, point(92, 30, HINGE_Z + 12), "#f5fbfc", 3, "7 6", 0.8))

    # Labels.
    labels = [
        ((650, 330), (460, 245), "ANTA SINISTRA", "cerniera sul lato esterno"),
        ((1020, 370), (1160, 292), "ANTA DESTRA", "cerniera sul lato opposto"),
        ((950, 635), (1120, 688), "VETRO FISSO PERIMETRALE", "raccorda le altezze esistenti"),
        ((775, 790), (495, 850), "PORTA FRONTALE", "esistente e invariata"),
        ((875, 590), (1110, 535), "2 PISTONI A GAS", "uno per anta"),
    ]
    for point_xy, label_xy, title, subtitle in labels:
        parts.append(line(point_xy, label_xy, "#46545b", 2, opacity=0.72))
        parts.append(f'<circle cx="{point_xy[0]}" cy="{point_xy[1]}" r="5" fill="#46545b"/>')
        parts.append(text(label_xy[0], label_xy[1], title, 19, "#253139", 700))
        parts.append(text(label_xy[0], label_xy[1] + 24, subtitle, 17, "#5c6a72"))

    parts.append(text(64, 82, "FINESTRA TETTO / A LIBRO", 43, "#1e292f", 700))
    parts.append(text(64, 118, "Due ante vetrate, pistoni simmetrici e porta frontale invariata", 25, "#52616a"))
    parts.append(polygon([(52, 135), (55, 143), (63, 146), (55, 149), (52, 157), (49, 149), (41, 146), (49, 143)], "#b45309"))
    parts.append(text(72, 154, "CONCEPT TECNICO", 17, "#8a4a1b", 700))
    parts.append(text(64, 928, "Schema preliminare - quote, pesi e fissaggi da verificare", 18, "#6d777e"))
    parts.append(text(1535, 928, "A-03 / R0", 18, "#6d777e"))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    output = Path(__file__).resolve().parent.parent / "varianti" / "variante_02" / "concept_a_libro.svg"
    output.write_text(build_svg(), encoding="utf-8")
    print(f"Generated book-opening concept illustration: {output}")


if __name__ == "__main__":
    main()
