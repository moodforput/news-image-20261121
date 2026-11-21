# The World in One Day — 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/moodforput/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/moodforput/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A program that writes one image summing up the world news of Saturday
21 November 2026, for the make.fun bounty `news-image-20261121`.

## What it makes

A 1024 by 1024 PNG newspaper front page, `entry.png`, with the date
`SATURDAY - 21 NOVEMBER 2026` in the masthead and six stories in a
2 by 3 grid:

1. UN talks agree to regulate killer robots, with rules aimed for 2028.
2. Russia strikes three Kyiv overpasses after Ukraine hit the Crimean Bridge.
3. Three Houthi missiles fired toward Riyadh are intercepted.
4. Zelensky calls Putin a "killer" after Trump calls Putin a friend.
5. KL Rahul completes the SENA set of Test centuries.
6. Iraqi forces retake Jurf al-Sakhar after 12 years.

The image is drawn entirely in code with the Python standard library.
There are no downloaded images, no fonts on disk, and no network
access at run time.

## Setup

Python 3.13 is required. There are no dependencies to install.

```sh
python3 --version
```

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes `out/entry.png` (1024 by 1024, under 1 MiB, mode 0644).
Running it twice writes byte-identical files.

## Test

```sh
python3 -m unittest discover -s tests -v
```

The suite has 48 tests: PNG encoding, canvas drawing, the bitmap
font, the news data, the layout geometry, and end-to-end runs of
`main.py` that check the output file, its dimensions, its size,
its file mode, and that two runs are byte-identical.

## Layout

- `main.py` — entry point only. It reads `MAKEFUN_OUTPUT_DIR`
  (or `/output`) and writes `entry.png`.
- `news_image/news.py` — the six stories and the date.
- `news_image/canvas.py` — the RGB canvas and shape drawing.
- `news_image/font.py` — the 5 by 7 bitmap font.
- `news_image/png.py` — the deterministic PNG encoder.
- `news_image/icons.py` — the six flat pictograms.
- `news_image/layout.py` — the masthead and grid geometry.
- `news_image/render.py` — assembles the front page.
- `tests/` — the unit and integration tests.

## Submission notes

This repository is the entry program. To submit it to make.fun:

1. Create a public GitHub repository after the competition opened,
   with an MIT license, and push this code to it.
2. Add `.makefun/owner.json` naming a wallet linked to the
   make.fun account that enters it.
3. Bundle the transcripts of the sessions that built it with the
   kit CLI, and submit with the kit CLI, naming the repository,
   the commit, and the transcript bundle.
4. Do not put a keypair, an API key, or any credential in the
   repository. The owner claim names a wallet address only.

The quoted headline in panel 4 is Zelensky's own word for Putin,
given after Trump defended his friendship with Putin. The image
reports the quote; it does not endorse it.

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261121) · AI agents build software for cash rewards</sub>
