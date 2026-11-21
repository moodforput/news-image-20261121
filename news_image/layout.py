"""Page geometry for the 1024x1024 front page.

Masthead band on top, then a 2-by-3 grid of story panels. All
coordinates are absolute pixels on the 1024x1024 page.
"""

WIDTH = 1024
HEIGHT = 1024
MARGIN = 24
PANEL_GAP = 16
ROW_GAP = 12
GRID_TOP = 200

TITLE_SCALE = 5
DATE_SCALE = 6
SUBLINE_SCALE = 3
HEADLINE_SCALE = 4
BODY_SCALE = 3

PANEL_W = (WIDTH - 2 * MARGIN - PANEL_GAP) // 2
PANEL_H = 254

ICON_RADIUS = 58
ICON_PAD = 16
HEADLINE_WIDTH = 316
BODY_WIDTH = 440


def panel_rect(index):
    """(x, y, width, height) of panel number index (0 to 5)."""
    column = index % 2
    row = index // 2
    x = MARGIN + column * (PANEL_W + PANEL_GAP)
    y = GRID_TOP + row * (PANEL_H + ROW_GAP)
    return x, y, PANEL_W, PANEL_H


def masthead_rects():
    """Named rectangles of the masthead band, top to bottom."""
    return {
        "title": (MARGIN, 26, WIDTH - 2 * MARGIN, 35),
        "date": (MARGIN, 74, WIDTH - 2 * MARGIN, 42),
        "rule_red": (MARGIN, 132, WIDTH - 2 * MARGIN, 6),
        "subline": (MARGIN, 148, WIDTH - 2 * MARGIN, 21),
        "rule_black": (MARGIN, 182, WIDTH - 2 * MARGIN, 4),
    }


def icon_centre(panel_x, panel_y):
    """Centre of the pictogram disc inside a panel."""
    return (
        panel_x + ICON_PAD + ICON_RADIUS,
        panel_y + ICON_PAD + ICON_RADIUS,
    )


def headline_origin(panel_x, panel_y):
    """Top-left corner where a panel's headline starts."""
    return panel_x + ICON_PAD + 2 * ICON_RADIUS + 14, panel_y + 20


def body_origin(panel_x, panel_y):
    """Top-left corner where a panel's body text starts."""
    return panel_x + ICON_PAD, panel_y + ICON_PAD + 2 * ICON_RADIUS + 14


def divider_y(panel_y):
    """Y of the thin rule between a panel's headline and its body."""
    return panel_y + ICON_PAD + 2 * ICON_RADIUS + 8
