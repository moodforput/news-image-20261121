"""Tests for the deterministic PNG encoder (news_image.png)."""

import struct
import unittest
import zlib

from news_image.png import encode_png, png_dimensions


def _solid_rgb(width, height, colour):
    return bytes(colour) * (width * height)


class TestPng(unittest.TestCase):
    def test_signature_and_ihdr(self):
        data = encode_png(4, 3, _solid_rgb(4, 3, (10, 20, 30)))
        self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(png_dimensions(data), (4, 3))
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((width, height), (4, 3))
        self.assertEqual(data[24], 8)  # bit depth
        self.assertEqual(data[25], 2)  # colour type RGB
        self.assertEqual(data[26], 0)  # no compression method other than deflate
        self.assertEqual(data[27], 0)  # filter method 0
        self.assertEqual(data[28], 0)  # no interlace

    def test_crc_valid_for_every_chunk(self):
        data = encode_png(8, 8, _solid_rgb(8, 8, (200, 100, 50)))
        pos = 8
        chunks = []
        while pos < len(data):
            length = struct.unpack(">I", data[pos:pos + 4])[0]
            kind = data[pos + 4:pos + 8]
            body = data[pos + 8:pos + 8 + length]
            stored_crc = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
            self.assertEqual(zlib.crc32(kind + body) & 0xFFFFFFFF, stored_crc)
            chunks.append(kind)
            pos += 12 + length
        self.assertEqual(chunks[0], b"IHDR")
        self.assertIn(b"IDAT", chunks)
        self.assertEqual(chunks[-1], b"IEND")

    def test_deterministic_bytes(self):
        pixels = bytes((i * 7) % 256 for i in range(32 * 32 * 3))
        first = encode_png(32, 32, pixels)
        second = encode_png(32, 32, pixels)
        self.assertEqual(first, second)

    def test_1024_image_encodes(self):
        data = encode_png(1024, 1024, _solid_rgb(1024, 1024, (247, 243, 232)))
        self.assertEqual(png_dimensions(data), (1024, 1024))
        self.assertLessEqual(len(data), 1048576)

    def test_wrong_pixel_length_rejected(self):
        with self.assertRaises(ValueError):
            encode_png(4, 4, b"\x00" * 10)
        with self.assertRaises(ValueError):
            encode_png(0, 4, b"")

    def test_decodes_to_same_pixels(self):
        width, height = 6, 5
        pixels = bytes((x * 40 + y * 3) % 256 for y in range(height) for x in range(width) for _ in range(3))
        data = encode_png(width, height, pixels)
        pos = 8
        idat = b""
        while pos < len(data):
            length = struct.unpack(">I", data[pos:pos + 4])[0]
            kind = data[pos + 4:pos + 8]
            if kind == b"IDAT":
                idat += data[pos + 8:pos + 8 + length]
            pos += 12 + length
        raw = zlib.decompress(idat)
        self.assertEqual(len(raw), height * (1 + width * 3))
        rebuilt = b"".join(raw[y * (1 + width * 3) + 1:(y + 1) * (1 + width * 3)] for y in range(height))
        self.assertEqual(rebuilt, pixels)


if __name__ == "__main__":
    unittest.main()
