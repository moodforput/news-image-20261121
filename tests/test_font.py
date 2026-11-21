"""Tests for the 5x7 bitmap font (news_image.font)."""

import unittest

from news_image.canvas import Canvas
from news_image.font import FONT_CHARS, GLYPHS, draw_text, text_width, wrap_text
from news_image.news import all_text


class TestFont(unittest.TestCase):
    def test_every_glyph_is_7_rows_of_5_bits(self):
        for char, rows in GLYPHS.items():
            self.assertEqual(len(char), 1, char)
            self.assertEqual(len(rows), 7, char)
            for row in rows:
                self.assertIsInstance(row, int)
                self.assertGreaterEqual(row, 0)
                self.assertLessEqual(row, 0b11111)

    def test_space_is_blank_and_letters_are_not(self):
        self.assertEqual(GLYPHS[" "], (0, 0, 0, 0, 0, 0, 0))
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            self.assertGreater(sum(bin(row).count("1") for row in GLYPHS[char]), 0, char)

    def test_every_character_used_is_covered(self):
        used = set("".join(all_text()))
        missing = sorted(ch for ch in used if ch not in GLYPHS)
        self.assertEqual(missing, [], "characters with no glyph: %r" % missing)

    def test_text_width_grows_with_scale_and_length(self):
        self.assertEqual(text_width("A", 1), 5)
        self.assertEqual(text_width("AB", 1), 11)
        self.assertEqual(text_width("A", 2), 10)
        self.assertEqual(text_width("A", 3), 15)
        self.assertGreater(text_width("HELLO", 4), text_width("HI", 4))

    def test_draw_text_paints_pixels(self):
        canvas = Canvas(200, 60, (255, 255, 255))
        width = draw_text(canvas, 10, 10, "A", (0, 0, 0), scale=4)
        self.assertEqual(width, text_width("A", 4))
        self.assertGreater(canvas.count_colour((0, 0, 0)), 0)
        self.assertEqual(canvas.get(10, 10), (255, 255, 255))

    def test_draw_text_unknown_character_raises(self):
        canvas = Canvas(50, 20, (255, 255, 255))
        with self.assertRaises(KeyError):
            draw_text(canvas, 0, 0, "~", (0, 0, 0), scale=2)

    def test_wrap_text_respects_width(self):
        lines = wrap_text("THE QUICK BROWN FOX JUMPS", scale=3, max_width=100)
        self.assertGreaterEqual(len(lines), 2)
        for line in lines:
            self.assertLessEqual(text_width(line, 3), 100)
        self.assertEqual(" ".join(lines), "THE QUICK BROWN FOX JUMPS")

    def test_wrap_single_long_word_is_kept_whole(self):
        lines = wrap_text("INTERCEPTS", scale=4, max_width=50)
        self.assertEqual(lines, ["INTERCEPTS"])

    def test_font_chars_sorted(self):
        self.assertEqual(FONT_CHARS, sorted(GLYPHS.keys()))


if __name__ == "__main__":
    unittest.main()
