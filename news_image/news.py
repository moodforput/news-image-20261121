"""The news of Saturday 21 November 2026, as the image reports it.

Every story here happened, or was first reported, on 21 November 2026.
"""

TITLE = "THE WORLD IN ONE DAY"
DATE_LINE = "SATURDAY - 21 NOVEMBER 2026"
SUBLINE = "SIX STORIES FROM ONE DAY AROUND THE WORLD"

TEAL = (15, 118, 110)
RED = (185, 28, 28)
AMBER = (180, 83, 9)
BLUE = (30, 64, 175)
SLATE = (51, 65, 85)
INK = (17, 24, 39)

STORIES = [
    {
        "n": 1,
        "headline": "KILLER ROBOTS",
        "body": "UN TALKS AIM FOR RULES BY 2028",
        "icon": "robot",
        "accent": TEAL,
    },
    {
        "n": 2,
        "headline": "KYIV BRIDGES HIT",
        "body": "RUSSIA STRIKES THREE KYIV OVERPASSES",
        "icon": "bridge",
        "accent": RED,
    },
    {
        "n": 3,
        "headline": "RIYADH INTERCEPTS",
        "body": "THREE MISSILES TOWARD RIYADH DOWNED",
        "icon": "intercept",
        "accent": AMBER,
    },
    {
        "n": 4,
        "headline": '"PUTIN IS A KILLER"',
        "body": "ZELENSKY ANSWERS TRUMP ON PUTIN",
        "icon": "quote",
        "accent": BLUE,
    },
    {
        "n": 5,
        "headline": "RAHUL'S SENA SET",
        "body": "FIRST INDIAN OPENER WITH TONS IN ALL 4 SENA LANDS",
        "icon": "cricket",
        "accent": SLATE,
    },
    {
        "n": 6,
        "headline": "IRAQ RETAKES TOWN",
        "body": "JURF AL-SAKHAR FREE AFTER 12 YEARS",
        "icon": "town",
        "accent": TEAL,
    },
]


def all_text():
    """Every string the image draws, in reading order."""
    lines = [TITLE, DATE_LINE, SUBLINE]
    for story in STORIES:
        lines.append(story["headline"])
        lines.append(story["body"])
        lines.append(str(story["n"]))
    return lines
