"""Tests for the page geometry (news_image.layout)."""

import unittest

from news_image.font import text_width, wrap_text
from news_image.layout import (
    BODY_SCALE,
    GRID_TOP,
    HEADLINE_SCALE,
    HEIGHT,
    MARGIN,
    PANEL_GAP,
    PANEL_H,
    PANEL_W,
    WIDTH,
    masthead_rects,
    panel_rect,
)
from news_image.news import STORIES


class TestLayout(unittest.TestCase):
    def test_page_is_1024(self):
        self.assertEqual((WIDTH, HEIGHT), (1024, 1024))

    def test_panels_inside_page(self):
        for index in range(6):
            x, y, w, h = panel_rect(index)
            self.assertGreaterEqual(x, MARGIN)
            self.assertGreaterEqual(y, GRID_TOP)
            self.assertEqual(w, PANEL_W)
            self.assertEqual(h, PANEL_H)
            self.assertLessEqual(x + w, WIDTH - MARGIN)
            self.assertLessEqual(y + h, HEIGHT - MARGIN + 14)

    def test_panels_do_not_overlap(self):
        rects = [panel_rect(index) for index in range(6)]

        def overlaps(a, b):
            ax, ay, aw, ah = a
            bx, by, bw, bh = b
            return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah

        for i in range(6):
            for j in range(i + 1, 6):
                self.assertFalse(overlaps(rects[i], rects[j]), (i, j))

    def test_grid_is_two_by_three(self):
        first_row = [panel_rect(i)[1] for i in range(2)]
        second_row = [panel_rect(i)[1] for i in range(2, 4)]
        third_row = [panel_rect(i)[1] for i in range(4, 6)]
        self.assertEqual(len(set(first_row)), 1)
        self.assertEqual(len(set(second_row)), 1)
        self.assertEqual(len(set(third_row)), 1)
        self.assertLess(first_row[0], second_row[0])
        self.assertLess(second_row[0], third_row[0])
        self.assertEqual(panel_rect(1)[0] - panel_rect(0)[0], PANEL_W + PANEL_GAP)

    def test_masthead_rects_are_stacked(self):
        rects = masthead_rects()
        self.assertLess(rects["title"][1], rects["date"][1])
        self.assertLess(rects["date"][1], rects["subline"][1])
        self.assertLess(rects["subline"][1], GRID_TOP)
        for name, (x, y, w, h) in rects.items():
            self.assertGreaterEqual(x, 0, name)
            self.assertLessEqual(x + w, WIDTH, name)
            self.assertGreater(h, 0, name)

    def test_headline_wraps_to_two_lines(self):
        for story in STORIES:
            lines = wrap_text(story["headline"], HEADLINE_SCALE, 316)
            self.assertLessEqual(len(lines), 2, story["headline"])
            for line in lines:
                self.assertLessEqual(text_width(line, HEADLINE_SCALE), 316)

    def test_body_wraps_to_two_lines(self):
        for story in STORIES:
            lines = wrap_text(story["body"], BODY_SCALE, 440)
            self.assertLessEqual(len(lines), 2, story["body"])
            for line in lines:
                self.assertLessEqual(text_width(line, BODY_SCALE), 440)


if __name__ == "__main__":
    unittest.main()
