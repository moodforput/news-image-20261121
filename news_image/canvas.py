"""An RGB canvas: a flat bytearray with simple shape drawing."""


class Canvas:
    """Width-by-height image of 24-bit RGB pixels, row-major order."""

    def __init__(self, width, height, background=(255, 255, 255)):
        if width <= 0 or height <= 0:
            raise ValueError("canvas size must be positive")
        self.width = width
        self.height = height
        self._data = bytearray(background) * (width * height)

    def _offset(self, x, y):
        return (y * self.width + x) * 3

    def set(self, x, y, colour):
        """Set one pixel; silently clips coordinates outside the canvas."""
        if 0 <= x < self.width and 0 <= y < self.height:
            offset = self._offset(x, y)
            self._data[offset] = colour[0]
            self._data[offset + 1] = colour[1]
            self._data[offset + 2] = colour[2]

    def get(self, x, y):
        offset = self._offset(x, y)
        return (self._data[offset], self._data[offset + 1], self._data[offset + 2])

    def fill(self, colour):
        self._data = bytearray(colour) * (self.width * self.height)

    def rect(self, x, y, width, height, colour):
        """Fill an axis-aligned rectangle, clipped to the canvas."""
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.width, x + width)
        y1 = min(self.height, y + height)
        for row in range(y0, y1):
            start = self._offset(x0, row)
            span = (x1 - x0) * 3
            self._data[start:start + span] = bytes(colour) * (x1 - x0)

    def line(self, x0, y0, x1, y1, colour, thickness=1):
        """Draw a line with Bresenham's algorithm."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        step_x = 1 if x0 < x1 else -1
        step_y = 1 if y0 < y1 else -1
        error = dx + dy
        x, y = x0, y0
        while True:
            if thickness <= 1:
                self.set(x, y, colour)
            else:
                half = thickness // 2
                self.rect(x - half, y - half, thickness, thickness, colour)
            if x == x1 and y == y1:
                break
            doubled = 2 * error
            if doubled >= dy:
                error += dy
                x += step_x
            if doubled <= dx:
                error += dx
                y += step_y

    def circle(self, cx, cy, radius, colour, fill=True):
        """Draw a circle; filled, or a one-pixel outline when fill is False."""
        if radius <= 0:
            return
        for y in range(cy - radius, cy + radius + 1):
            dy = y - cy
            half = int((radius * radius - dy * dy) ** 0.5)
            if fill:
                self.rect(cx - half, y, half * 2 + 1, 1, colour)
            else:
                self.set(cx - half, y, colour)
                self.set(cx + half, y, colour)
        if not fill:
            for x in range(cx - radius, cx + radius + 1):
                dx = x - cx
                half = int((radius * radius - dx * dx) ** 0.5)
                self.set(x, cy - half, colour)
                self.set(x, cy + half, colour)

    def polygon(self, points, colour):
        """Fill a polygon with the scanline rule."""
        if len(points) < 3:
            return
        top = min(y for _, y in points)
        bottom = max(y for _, y in points)
        for y in range(top, bottom + 1):
            crossings = []
            count = len(points)
            for i in range(count):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % count]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    span = y1 - y0
                    crossings.append(x0 + (y - y0) * (x1 - x0) / span)
            crossings.sort()
            for i in range(0, len(crossings) - 1, 2):
                left = int(round(crossings[i]))
                right = int(round(crossings[i + 1]))
                if right >= left:
                    self.rect(left, y, right - left + 1, 1, colour)

    def triangle(self, a, b, c, colour):
        self.polygon([a, b, c], colour)

    def count_colour(self, colour):
        total = 0
        for offset in range(0, len(self._data), 3):
            if (self._data[offset], self._data[offset + 1], self._data[offset + 2]) == colour:
                total += 1
        return total

    def pixels(self):
        return bytes(self._data)
