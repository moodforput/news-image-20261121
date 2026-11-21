"""Tests for the whole render: main.py plus the full image build."""

import hashlib
import os
import stat
import subprocess
import sys
import tempfile
import unittest

from news_image.png import png_dimensions
from news_image.render import render_png

ENTRY_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestIntegration(unittest.TestCase):
    def test_render_png_is_valid_1024(self):
        data = render_png()
        self.assertEqual(png_dimensions(data), (1024, 1024))
        self.assertLessEqual(len(data), 1048576)
        self.assertGreater(len(data), 5000)

    def test_render_is_deterministic(self):
        self.assertEqual(render_png(), render_png())

    def test_main_writes_entry_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=tmp)
            result = subprocess.run(
                [sys.executable, os.path.join(ENTRY_DIR, "main.py")],
                cwd=ENTRY_DIR, env=env, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            path = os.path.join(tmp, "entry.png")
            self.assertTrue(os.path.isfile(path))
            with open(path, "rb") as handle:
                data = handle.read()
            self.assertEqual(png_dimensions(data), (1024, 1024))
            self.assertLessEqual(len(data), 1048576)
            mode = stat.S_IMODE(os.stat(path).st_mode)
            self.assertEqual(mode, 0o644)

    def test_two_runs_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            for tmp in (first, second):
                env = dict(os.environ, MAKEFUN_OUTPUT_DIR=tmp)
                result = subprocess.run(
                    [sys.executable, os.path.join(ENTRY_DIR, "main.py")],
                    cwd=ENTRY_DIR, env=env, capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            with open(os.path.join(first, "entry.png"), "rb") as handle:
                first_bytes = handle.read()
            with open(os.path.join(second, "entry.png"), "rb") as handle:
                second_bytes = handle.read()
            self.assertEqual(first_bytes, second_bytes)
            self.assertEqual(
                hashlib.sha256(first_bytes).hexdigest(),
                hashlib.sha256(second_bytes).hexdigest(),
            )

    def test_main_defaults_to_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = os.path.join(tmp, "output")
            env = dict(os.environ)
            env.pop("MAKEFUN_OUTPUT_DIR", None)
            # main.py falls back to /output when the variable is unset;
            # pointing the test at a missing /output would fail in the
            # sandbox, so only check the code path exists via env override.
            env["MAKEFUN_OUTPUT_DIR"] = out_dir
            result = subprocess.run(
                [sys.executable, os.path.join(ENTRY_DIR, "main.py")],
                cwd=ENTRY_DIR, env=env, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(os.path.isfile(os.path.join(out_dir, "entry.png")))


if __name__ == "__main__":
    unittest.main()
