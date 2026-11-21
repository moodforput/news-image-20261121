"""Assemble the 1024x1024 front page and encode it as PNG bytes."""

from news_image.canvas import Canvas
from news_image.font import draw_text, text_height, text_width, wrap_text
from news_image.icons import draw_icon
from news_image.layout import (
    BODY_SCALE,
    BODY_WIDTH,
    DATE_SCALE,
    GRID_TOP,
    HEADLINE_SCALE,
    HEADLINE_WIDTH,
    HEIGHT,
    ICON_RADIUS,
    MARGIN,
    PANEL_GAP,
    SUBLINE_SCALE,
    TITLE_SCALE,
    WIDTH,
    body_origin,
    divider_y,
    headline_origin,
    icon_centre,
    masthead_rects,
    panel_rect,
)
from news_image.news import DATE_LINE, INK, STORIES, SUBLINE, TITLE
from news_image.png import encode_png

PAPER = (247, 243, 232)
PANEL_FILL = (255, 255, 255)
RULE_RED = (185, 28, 28)
DIVIDER = (203, 213, 225)
MUTED = (71, 85, 105)


def _tint(accent):
    """A pale tint of an accent colour, for the icon disc."""
    return tuple(255 - (255 - channel) // 4 for channel in accent)


def _draw_masthead(canvas):
    rects = masthead_rects()
    title_x = (WIDTH - text_width(TITLE, TITLE_SCALE)) // 2
    draw_text(canvas, title_x, rects["title"][1], TITLE, INK, TITLE_SCALE)
    date_x = (WIDTH - text_width(DATE_LINE, DATE_SCALE)) // 2
    draw_text(canvas, date_x, rects["date"][1], DATE_LINE, INK, DATE_SCALE)
    x, y, w, h = rects["rule_red"]
    canvas.rect(x, y, w, h, RULE_RED)
    sub_x = (WIDTH - text_width(SUBLINE, SUBLINE_SCALE)) // 2
    draw_text(canvas, sub_x, rects["subline"][1], SUBLINE, MUTED, SUBLINE_SCALE)
    x, y, w, h = rects["rule_black"]
    canvas.rect(x, y, w, h, INK)


def _draw_panel(canvas, story):
    index = story["n"] - 1
    x, y, w, h = panel_rect(index)
    accent = story["accent"]
    canvas.rect(x, y, w, h, PANEL_FILL)
    canvas.rect(x, y, w, 3, accent)
    canvas.rect(x, y, 3, h, accent)
    canvas.rect(x + w - 3, y, 3, h, accent)
    canvas.rect(x, y + h - 3, w, 3, accent)
    cx, cy = icon_centre(x, y)
    canvas.circle(cx, cy, ICON_RADIUS, _tint(accent))
    canvas.circle(cx, cy, ICON_RADIUS, accent, fill=False)
    draw_icon(canvas, story["icon"], cx, cy, ICON_RADIUS, accent, _tint(accent))
    hx, hy = headline_origin(x, y)
    lines = wrap_text(story["headline"], HEADLINE_SCALE, HEADLINE_WIDTH)
    line_y = hy
    for line in lines:
        draw_text(canvas, hx, line_y, line, accent, HEADLINE_SCALE)
        line_y += text_height(HEADLINE_SCALE) + 6
    dy = divider_y(y)
    canvas.line(x + 16, dy, x + w - 16, dy, DIVIDER, 1)
    bx, by = body_origin(x, y)
    body_lines = wrap_text(story["body"], BODY_SCALE, BODY_WIDTH)
    line_y = by
    for line in body_lines:
        draw_text(canvas, bx, line_y, line, INK, BODY_SCALE)
        line_y += text_height(BODY_SCALE) + 6
    number = str(story["n"])
    number_x = x + w - 16 - text_width(number, BODY_SCALE)
    draw_text(canvas, number_x, y + 10, number, accent, BODY_SCALE)


def render():
    """Build the front page and return its Canvas."""
    canvas = Canvas(WIDTH, HEIGHT, PAPER)
    _draw_masthead(canvas)
    for story in STORIES:
        _draw_panel(canvas, story)
    return canvas


def render_png():
    """Build the front page and return its PNG bytes."""
    canvas = render()
    return encode_png(canvas.width, canvas.height, canvas.pixels())
