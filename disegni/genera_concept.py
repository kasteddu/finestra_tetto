#!/usr/bin/env python3
"""Generate an isometric design illustration for the horizontal roof hatch."""

from __future__ import annotations

from pathlib import Path


WIDTH = 1600
HEIGHT = 1000


def point(x: float, y: float, z: float = 0.0) -> tuple[float, float]:
    return (800 + (x - y) * 1.72, 625 + (x + y) * 0.91 - z * 2.1)


def polygon(points: list[tuple[float, float]], fill: str, stroke: str = "none", width: float = 0, opacity: float = 1) -> str:
    values = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return (
        f'<polygon points="{values}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{width}" opacity="{opacity}" stroke-linejoin="round"/>'
    )


def world_polygon(points: list[tuple[float, float, float]], fill: str, stroke: str = "none", width: float = 0, opacity: float = 1) -> str:
    return polygon([point(*values) for values in points], fill, stroke, width, opacity)


def line(
    p1: tuple[float, float],
    p2: tuple[float, float],
    stroke: str,
    width: float = 3,
    dash: str | None = None,
    opacity: float = 1,
) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" '
        f'stroke="{stroke}" stroke-width="{width}" opacity="{opacity}" '
        f'stroke-linecap="round"{dash_attr}/>'
    )


def text(x: float, y: float, value: str, size: float = 24, color: str = "#222831", weight: int = 400) -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" '
        f'font-family="Arial, Helvetica, sans-serif">{value}</text>'
    )


def build_svg() -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6f2eb"/><stop offset="1" stop-color="#dce6e8"/></linearGradient>',
        '<linearGradient id="deck" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9dfcf"/><stop offset="1" stop-color="#cbb99f"/></linearGradient>',
        '<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#75bfd1" stop-opacity=".70"/><stop offset=".48" stop-color="#d8f3f7" stop-opacity=".35"/><stop offset="1" stop-color="#4b98ae" stop-opacity=".62"/></linearGradient>',
        '<linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#eef1f3"/><stop offset=".5" stop-color="#77828c"/><stop offset="1" stop-color="#343c43"/></linearGradient>',
        '<radialGradient id="shade"><stop offset="0" stop-color="#26343a" stop-opacity=".24"/><stop offset="1" stop-color="#26343a" stop-opacity="0"/></radialGradient>',
        '<filter id="blur"><feGaussianBlur stdDeviation="9"/></filter>',
        "</defs>",
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>',
        '<ellipse cx="850" cy="695" rx="530" ry="285" fill="url(#shade)"/>',
    ]

    # Rooftop slab.
    slab = [(-88, -72, 0), (255, -72, 0), (255, 235, 0), (-88, 235, 0)]
    parts.append(world_polygon(slab, "url(#deck)", "#a99780", 3))
    for value in range(0, 241, 12):
        parts.append(
            line(
                point(-88, value, 0.3),
                point(255, value, 0.3),
                "#b4a58f",
                1.3,
                opacity=0.55,
            )
        )
        parts.append(
            line(
                point(value, -72, 0.4),
                point(value, 235, 0.4),
                "#c4b6a2",
                0.8,
                opacity=0.35,
            )
        )

    # Opening: recessed staircase and visible depth.
    opening = [(0, 0), (120, 0), (120, 93), (0, 93)]
    parts.append(world_polygon([(x, y, -54) for x, y in opening], "#152128"))
    parts.append(world_polygon([(0, 0, -54), (0, 93, -54), (0, 93, 0), (0, 0, 0)], "#677176"))
    parts.append(world_polygon([(0, 93, -54), (120, 93, -54), (120, 93, 0), (0, 93, 0)], "#e4ded4"))
    parts.append(world_polygon([(120, 0, -54), (120, 93, -54), (120, 93, 0), (120, 0, 0)], "#8b9599"))
    parts.append(world_polygon([(0, 0, -54), (120, 0, -54), (120, 0, 0), (0, 0, 0)], "#d8d2c8"))
    for index in range(5):
        inset = 8 + index * 8
        z = -46 + index * 8
        parts.append(
            world_polygon(
                [
                    (inset, 12 + index * 7, z),
                    (110 - inset / 2, 12 + index * 7, z),
                    (110 - inset / 2, 25 + index * 7, z),
                    (inset, 25 + index * 7, z),
                ],
                "#b6aa98",
                "#8a7d6e",
                1,
            )
        )

    # Fixed raised frame and drainage lip.
    parts.append(world_polygon([(x, y, 3.5) for x, y in opening], "#303a40", "#11181c", 10))
    parts.append(world_polygon([(x, y, 5.0) for x, y in opening], "none", "url(#metal)", 6))

    # Long rails and parking support.
    for x in (-7.0, 123.0):
        parts.append(
            world_polygon(
                [(x, -10, 5), (x + 6, -10, 5), (x + 6, 202, 5), (x, 202, 5)],
                "url(#metal)",
                "#3f4b53",
                2,
            )
        )
        parts.append(world_polygon([(x, -10, 9), (x + 6, -10, 9), (x + 6, 202, 9), (x, 202, 9)], "#d8dde0"))

    # Sliding glass panel in the open/parked position.
    panel = [(0, 100), (120, 100), (120, 190), (0, 190)]
    shadow = [(x + 5, y + 5, 4.8) for x, y in panel]
    parts.append(world_polygon(shadow, "#28343a", opacity=0.2))
    parts.append(world_polygon([(x, y, 10) for x, y in panel], "url(#glass)", "#3b6d7d", 3))
    # Aluminum perimeter of the glass carrier.
    parts.append(world_polygon([(0, 100, 10), (120, 100, 10), (120, 108, 10), (0, 108, 10)], "url(#metal)", "#3b454d", 2))
    parts.append(world_polygon([(0, 182, 10), (120, 182, 10), (120, 190, 10), (0, 190, 10)], "url(#metal)", "#3b454d", 2))
    parts.append(world_polygon([(0, 100, 10), (8, 100, 10), (8, 190, 10), (0, 190, 10)], "url(#metal)", "#3b454d", 2))
    parts.append(world_polygon([(112, 100, 10), (120, 100, 10), (120, 190, 10), (112, 190, 10)], "url(#metal)", "#3b454d", 2))
    # Reflections on glass.
    for x in (18, 42, 68, 90):
        parts.append(line(point(x, 112, 10.5), point(x + 22, 178, 10.5), "#ffffff", 5, opacity=0.42))

    # Closed-position ghost.
    parts.append(world_polygon([(x, y, 11) for x, y in opening], "none", "#f7fbfc", 3, 0.9))
    for x1, y1, x2, y2 in ((0, 0, 120, 93), (120, 0, 0, 93)):
        parts.append(line(point(x1, y1, 11), point(x2, y2, 11), "#f7fbfc", 2, "8 7", 0.75))

    # Motion arrow.
    start = point(60, 62, 26)
    end = point(60, 88, 26)
    parts.append(line(start, end, "#b45309", 7))
    ex, ey = end
    parts.append(f'<polygon points="{ex:.1f},{ey:.1f} {ex-13:.1f},{ey-17:.1f} {ex+13:.1f},{ey-17:.1f}" fill="#b45309"/>')

    # Labels and leader lines.
    labels = [
        ((655, 452), (585, 385), "VETRO STRATIFICATO", "PANNELLO APERTO"),
        ((955, 650), (1080, 735), "LUCE LIBERA", "120 x 93 cm"),
        ((1050, 497), (1265, 448), "GUIDA SUPERIORE", "CARRELLI ANTISOLLEVAMENTO"),
        ((540, 795), (420, 870), "VANO SCALA", "PROTEZIONE ANTICADUTA"),
    ]
    for point_xy, label_xy, title, subtitle in labels:
        parts.append(line(point_xy, label_xy, "#45535b", 2, opacity=0.72))
        parts.append(f'<circle cx="{point_xy[0]}" cy="{point_xy[1]}" r="5" fill="#45535b"/>')
        parts.append(text(label_xy[0], label_xy[1], title, 19, "#253139", 700))
        parts.append(text(label_xy[0], label_xy[1] + 24, subtitle, 17, "#5c6a72"))

    # Title and disclaimer.
    parts.append(text(70, 84, "FINESTRA TETTO", 48, "#1e292f", 700))
    parts.append(text(70, 122, "Apertura orizzontale con vetro scorrevole sopra il piano", 27, "#52616a"))
    parts.append(text(70, 923, "CONCEPT TECNICO - scala e particolari da verificare", 18, "#6d777e"))
    parts.append(text(1530, 923, "A-02 / R0", 18, "#6d777e"))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    output = Path(__file__).resolve().parent.parent / "varianti" / "variante_01" / "concept_orizzontale.svg"
    output.write_text(build_svg(), encoding="utf-8")
    print(f"Generated isometric concept illustration: {output}")


if __name__ == "__main__":
    main()
