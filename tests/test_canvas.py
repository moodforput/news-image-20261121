"""Tests for the RGB canvas rasterizer (news_image.canvas)."""

import unittest

from news_image.canvas import Canvas


class TestCanvas(unittest.TestCase):
    def test_fill_and_get(self):
        canvas = Canvas(10, 8, (1, 2, 3))
        self.assertEqual(canvas.get(0, 0), (1, 2, 3))
        self.assertEqual(canvas.get(9, 7), (1, 2, 3))
        canvas.set(5, 5, (9, 9, 9))
        self.assertEqual(canvas.get(5, 5), (9, 9, 9))

    def test_out_of_bounds_is_clipped(self):
        canvas = Canvas(4, 4, (0, 0, 0))
        canvas.set(-1, 0, (255, 255, 255))
        canvas.set(4, 0, (255, 255, 255))
        canvas.set(0, -1, (255, 255, 255))
        canvas.set(0, 4, (255, 255, 255))
        self.assertEqual(canvas.count_colour((255, 255, 255)), 0)
        canvas.rect(-2, -2, 6, 6, (7, 7, 7))
        self.assertEqual(canvas.count_colour((7, 7, 7)), 16)

    def test_rect(self):
        canvas = Canvas(10, 10, (0, 0, 0))
        canvas.rect(2, 3, 4, 2, (255, 0, 0))
        self.assertEqual(canvas.count_colour((255, 0, 0)), 8)
        self.assertEqual(canvas.get(2, 3), (255, 0, 0))
        self.assertEqual(canvas.get(5, 4), (255, 0, 0))
        self.assertEqual(canvas.get(6, 4), (0, 0, 0))

    def test_horizontal_and_vertical_lines(self):
        canvas = Canvas(10, 10, (0, 0, 0))
        canvas.line(0, 5, 9, 5, (0, 255, 0))
        self.assertEqual(canvas.count_colour((0, 255, 0)), 10)
        canvas.line(3, 0, 3, 9, (0, 0, 255))
        self.assertEqual(canvas.get(3, 5), (0, 0, 255))
        self.assertEqual(canvas.count_colour((0, 0, 255)), 10)

    def test_diagonal_line(self):
        canvas = Canvas(10, 10, (0, 0, 0))
        canvas.line(0, 0, 9, 9, (255, 255, 0))
        self.assertEqual(canvas.get(0, 0), (255, 255, 0))
        self.assertEqual(canvas.get(5, 5), (255, 255, 0))
        self.assertEqual(canvas.get(9, 9), (255, 255, 0))
        self.assertGreaterEqual(canvas.count_colour((255, 255, 0)), 10)

    def test_filled_circle(self):
        canvas = Canvas(21, 21, (0, 0, 0))
        canvas.circle(10, 10, 5, (255, 0, 0))
        self.assertEqual(canvas.get(10, 10), (255, 0, 0))
        self.assertEqual(canvas.get(10, 5), (255, 0, 0))
        self.assertEqual(canvas.get(15, 10), (255, 0, 0))
        self.assertEqual(canvas.get(10, 4), (0, 0, 0))
        self.assertEqual(canvas.get(16, 10), (0, 0, 0))

    def test_circle_outline(self):
        canvas = Canvas(21, 21, (0, 0, 0))
        canvas.circle(10, 10, 5, (0, 255, 0), fill=False)
        self.assertEqual(canvas.get(10, 10), (0, 0, 0))
        self.assertEqual(canvas.get(10, 5), (0, 255, 0))
        self.assertEqual(canvas.get(15, 10), (0, 255, 0))

    def test_triangle_and_polygon(self):
        canvas = Canvas(20, 20, (0, 0, 0))
        canvas.triangle((2, 18), (18, 18), (10, 2), (0, 0, 255))
        self.assertEqual(canvas.get(10, 16), (0, 0, 255))
        self.assertEqual(canvas.get(10, 4), (0, 0, 255))
        self.assertEqual(canvas.get(0, 0), (0, 0, 0))
        canvas.polygon([(2, 2), (8, 2), (8, 8), (2, 8)], (255, 128, 0))
        self.assertEqual(canvas.get(5, 5), (255, 128, 0))

    def test_pixels_roundtrip(self):
        canvas = Canvas(3, 2, (10, 20, 30))
        self.assertEqual(len(canvas.pixels()), 3 * 2 * 3)
        self.assertEqual(canvas.pixels()[:3], bytes((10, 20, 30)))

    def test_zero_size_rejected(self):
        with self.assertRaises(ValueError):
            Canvas(0, 5)
        with self.assertRaises(ValueError):
            Canvas(5, 0)


if __name__ == "__main__":
    unittest.main()
