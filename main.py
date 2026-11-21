"""Entry point: write the front page image to entry.png.

The output directory is MAKEFUN_OUTPUT_DIR when set, else /output.
The file is written with mode 0644. Only the standard library is used.
"""

import os
import sys

# The grader runs `python3 -P -s /bot/main.py`: -P stops Python from
# prepending the script's directory to sys.path, so the news_image
# package would not be importable without this bootstrap.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
