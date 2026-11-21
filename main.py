"""Entry point: write the front page image to entry.png.

The output directory is MAKEFUN_OUTPUT_DIR when set, else /output.
The file is written with mode 0644. Only the standard library is used.
"""

import os
import sys

from news_image.render import render_png

OUTPUT_NAME = "entry.png"


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, OUTPUT_NAME)
    data = render_png()
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
