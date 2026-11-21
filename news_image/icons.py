"""Flat pictograms, one per story, drawn with shapes only.

Each draw function paints inside a disc of radius r centred at
(cx, cy). The disc itself is painted by the renderer; the icon draws
its figure in the foreground colour, using the background colour for
cut-outs such as eyes and windows.
"""

import math


def _arc(canvas, cx, cy, radius, start_deg, end_deg, colour, steps=24):
    """Draw an arc as short line segments."""
    previous = None
    for i in range(steps + 1):
        angle = math.radians(start_deg + (end_deg - start_deg) * i / steps)
        point = (round(cx + radius * math.cos(angle)),
                 round(cy + radius * math.sin(angle)))
        if previous is not None:
            canvas.line(previous[0], previous[1], point[0], point[1], colour, 3)
        previous = point


def _robot(canvas, cx, cy, r, fg, bg):
    head_w = int(r * 0.95)
    head_h = int(r * 0.62)
    head_x = cx - head_w // 2
    head_y = cy - int(r * 0.62)
    canvas.line(cx, head_y, cx, head_y - int(r * 0.22), fg, 3)
    canvas.circle(cx, head_y - int(r * 0.28), max(3, r // 12), fg)
    canvas.rect(head_x, head_y, head_w, head_h, fg)
    eye_r = max(3, r // 11)
    canvas.circle(cx - head_w // 4, head_y + head_h // 3, eye_r, bg)
    canvas.circle(cx + head_w // 4, head_y + head_h // 3, eye_r, bg)
    canvas.rect(cx - head_w // 4, head_y + int(head_h * 0.68),
                head_w // 2, max(2, r // 16), bg)
    body_w = int(r * 1.15)
    body_y = head_y + head_h + int(r * 0.08)
    canvas.rect(cx - body_w // 2, body_y, body_w, int(r * 0.42), fg)
    canvas.rect(cx - int(r * 0.12), body_y + int(r * 0.12),
                int(r * 0.24), int(r * 0.18), bg)


def _bridge(canvas, cx, cy, r, fg, bg):
    deck_y = cy - int(r * 0.05)
    left = cx - int(r * 0.85)
    right = cx + int(r * 0.85)
    canvas.line(left, deck_y, right, deck_y, fg, 5)
    _arc(canvas, cx - int(r * 0.42), deck_y, int(r * 0.42), 180, 360, fg)
    _arc(canvas, cx + int(r * 0.42), deck_y, int(r * 0.42), 180, 360, fg)
    for px in (left + int(r * 0.12), cx, right - int(r * 0.12)):
        canvas.line(px, deck_y, px, deck_y + int(r * 0.45), fg, 4)
    water_y = deck_y + int(r * 0.62)
    canvas.line(cx - int(r * 0.6), water_y, cx - int(r * 0.1), water_y, fg, 3)
    canvas.line(cx + int(r * 0.1), water_y, cx + int(r * 0.6), water_y, fg, 3)


def _intercept(canvas, cx, cy, r, fg, bg):
    tip_x = cx + int(r * 0.55)
    tip_y = cy - int(r * 0.55)
    tail_x = cx - int(r * 0.15)
    tail_y = cy + int(r * 0.15)
    canvas.line(tail_x, tail_y, tip_x, tip_y, fg, 5)
    canvas.triangle((tip_x, tip_y),
                    (tip_x - int(r * 0.28), tip_y + int(r * 0.02)),
                    (tip_x - int(r * 0.02), tip_y + int(r * 0.28)), fg)
    burst_x = cx - int(r * 0.35)
    burst_y = cy + int(r * 0.35)
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        canvas.line(burst_x, burst_y,
                    round(burst_x + int(r * 0.34) * math.cos(rad)),
                    round(burst_y + int(r * 0.34) * math.sin(rad)), fg, 3)
    canvas.circle(burst_x, burst_y, max(3, r // 12), fg)
    _arc(canvas, cx, cy + int(r * 0.15), int(r * 0.7), 20, 160, fg)


def _quote(canvas, cx, cy, r, fg, bg):
    """Two large comma-shaped quotation marks."""
    for centre_x in (cx - int(r * 0.30), cx + int(r * 0.30)):
        centre_y = cy - int(r * 0.18)
        radius = int(r * 0.24)
        canvas.circle(centre_x, centre_y, radius, fg)
        canvas.triangle(
            (centre_x - radius, centre_y + int(radius * 0.4)),
            (centre_x + int(radius * 0.9), centre_y + int(r * 0.62)),
            (centre_x + int(radius * 0.3), centre_y - int(radius * 0.2)),
            fg,
        )


def _cricket(canvas, cx, cy, r, fg, bg):
    stump_top = cy + int(r * 0.05)
    stump_bottom = cy + int(r * 0.75)
    for offset in (-int(r * 0.16), 0, int(r * 0.16)):
        canvas.rect(cx + offset - 2, stump_top, 5, stump_bottom - stump_top, fg)
    canvas.rect(cx - int(r * 0.2), stump_top - 4, int(r * 0.4), 4, fg)
    bat_base_x = cx + int(r * 0.30)
    bat_base_y = cy + int(r * 0.55)
    bat_top_x = cx + int(r * 0.75)
    bat_top_y = cy - int(r * 0.55)
    dx = bat_top_x - bat_base_x
    dy = bat_top_y - bat_base_y
    length = (dx * dx + dy * dy) ** 0.5
    nx, ny = -dy / length, dx / length
    half = max(3, r // 13)
    canvas.polygon([
        (round(bat_base_x + nx * half), round(bat_base_y + ny * half)),
        (round(bat_top_x + nx * half), round(bat_top_y + ny * half)),
        (round(bat_top_x - nx * half), round(bat_top_y - ny * half)),
        (round(bat_base_x - nx * half), round(bat_base_y - ny * half)),
    ], fg)
    canvas.circle(cx - int(r * 0.5), cy - int(r * 0.45), max(5, r // 7), fg)
    canvas.circle(cx - int(r * 0.5), cy - int(r * 0.45), max(2, r // 18), bg)


def _town(canvas, cx, cy, r, fg, bg):
    base_y = cy + int(r * 0.7)
    canvas.rect(cx - int(r * 0.85), cy + int(r * 0.1),
                int(r * 0.5), base_y - (cy + int(r * 0.1)), fg)
    canvas.rect(cx - int(r * 0.28), cy - int(r * 0.25),
                int(r * 0.56), base_y - (cy - int(r * 0.25)), fg)
    canvas.rect(cx + int(r * 0.35), cy + int(r * 0.3),
                int(r * 0.5), base_y - (cy + int(r * 0.3)), fg)
    for wx in (cx - int(r * 0.62), cx - int(r * 0.1), cx + int(r * 0.55)):
        for wy in (cy + int(r * 0.25), cy + int(r * 0.5)):
            canvas.rect(wx, wy, max(3, r // 12), max(3, r // 12), bg)
    pole_x = cx + int(r * 0.05)
    canvas.line(pole_x, cy - int(r * 0.25), pole_x, cy - int(r * 0.85), fg, 3)
    canvas.triangle((pole_x, cy - int(r * 0.85)),
                    (pole_x + int(r * 0.5), cy - int(r * 0.68)),
                    (pole_x, cy - int(r * 0.52)), fg)


ICONS = {
    "robot": _robot,
    "bridge": _bridge,
    "intercept": _intercept,
    "quote": _quote,
    "cricket": _cricket,
    "town": _town,
}


def draw_icon(canvas, name, cx, cy, radius, fg, bg):
    """Draw the named pictogram inside the disc at (cx, cy)."""
    draw = ICONS[name]  # raises KeyError for an unknown icon name
    draw(canvas, cx, cy, radius, fg, bg)
