"""A deterministic PNG encoder using only zlib and struct.

The image is true-colour RGB, 8 bits per channel, no interlace, one
IDAT chunk, filter byte 0 on every scanline, zlib level 9. The same
pixels always produce the same bytes.
"""

import struct
import zlib

_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _chunk(kind, body):
    return (
        struct.pack(">I", len(body))
        + kind
        + body
        + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)
    )


def encode_png(width, height, rgb_pixels):
    """Encode width-by-height RGB bytes (3 bytes per pixel) as a PNG."""
    if width <= 0 or height <= 0:
        raise ValueError("PNG size must be positive")
    if len(rgb_pixels) != width * height * 3:
        raise ValueError("pixel data does not match width and height")
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    stride = width * 3
    scanlines = bytearray()
    for row in range(height):
        scanlines.append(0)
        scanlines += rgb_pixels[row * stride:(row + 1) * stride]
    idat = zlib.compress(bytes(scanlines), 9)
    return (
        _SIGNATURE
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"IDAT", idat)
        + _chunk(b"IEND", b"")
    )


def png_dimensions(data):
    """Read (width, height) out of a PNG's IHDR chunk."""
    if len(data) < 24 or data[:8] != _SIGNATURE:
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    return width, height
