"""Tests for the news data (news_image.news).

The image must cover Saturday 21 November 2026 only. Stories from
Friday 20 November 2026 must not appear anywhere in the rendered text.
"""

import re
import unittest

from news_image.font import text_width
from news_image.news import DATE_LINE, STORIES, SUBLINE, TITLE, all_text

# Words and phrases that belong to 20 November 2026 stories, not 21 Nov.
BANNED_20_NOV = [
    "MYANMAR", "ROHINGYA", "SHENZHEN", "COP31", "FOSSIL",
    "GTA", "NVIDIA", "DENMARK", "UFO", "PERU", "AKVAN",
    "NIKKEI", "SUMMIT DECLARATION",
]

HYPE_WORDS = ["SHOCKING", "UNBELIEVABLE", "HUGE", "BREAKING", "MASSIVE",
              "INCREDIBLE", "STUNNING", "AMAZING"]


class TestNews(unittest.TestCase):
    def test_six_stories(self):
        self.assertEqual(len(STORIES), 6)
        self.assertEqual([story["n"] for story in STORIES], [1, 2, 3, 4, 5, 6])

    def test_date_is_21_november_2026(self):
        self.assertEqual(DATE_LINE, "SATURDAY - 21 NOVEMBER 2026")
        self.assertIn("21 NOVEMBER 2026", DATE_LINE)
        self.assertIn("SATURDAY", DATE_LINE)

    def test_each_story_has_headline_body_icon(self):
        for story in STORIES:
            self.assertTrue(story["headline"].strip())
            self.assertTrue(story["body"].strip())
            self.assertTrue(story["icon"].strip())
            self.assertEqual(len(story["accent"]), 3)
            self.assertTrue(all(0 <= channel <= 255 for channel in story["accent"]))

    def test_facts_present(self):
        joined = " ".join(all_text())
        for fact in ["KILLER ROBOTS", "2028", "KYIV", "RIYADH", "PUTIN",
                     "KILLER", "RAHUL", "SENA", "JURF AL-SAKHAR", "12 YEARS"]:
            self.assertIn(fact, joined, "missing fact: %s" % fact)

    def test_no_20_november_story_text(self):
        joined = " ".join(all_text())
        for word in BANNED_20_NOV:
            self.assertNotIn(word, joined, "banned 20-Nov word present: %s" % word)

    def test_no_other_dates_in_text(self):
        joined = " ".join(all_text())
        self.assertNotIn("20 NOVEMBER", joined)
        self.assertNotIn("19 NOVEMBER", joined)
        self.assertNotIn("22 NOVEMBER", joined)
        self.assertNotIn("23 NOVEMBER", joined)
        self.assertNotIn("2025", joined)
        self.assertNotIn("2024", joined)
        months = re.findall(r"\b(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|"
                            r"AUGUST|SEPTEMBER|OCTOBER|DECEMBER)\b", joined)
        self.assertEqual(months, [])

    def test_headline_lines_are_short(self):
        for story in STORIES:
            lines = story["headline"].split(" ")
            self.assertLessEqual(len(story["headline"]), 20, story["headline"])

    def test_body_lines_are_short(self):
        for story in STORIES:
            self.assertLessEqual(len(story["body"]), 55, story["body"])
            wrapped = []
            words = story["body"].split(" ")
            current = ""
            for word in words:
                trial = (current + " " + word).strip()
                if text_width(trial, 3) <= 440:
                    current = trial
                else:
                    wrapped.append(current)
                    current = word
            wrapped.append(current)
            self.assertLessEqual(len(wrapped), 2, story["body"])

    def test_no_hype_words(self):
        joined = " ".join(all_text())
        for word in HYPE_WORDS:
            self.assertNotIn(word, joined, "hype word present: %s" % word)

    def test_gta_and_quote_wording(self):
        joined = " ".join(all_text())
        self.assertNotIn("RELEASED", joined)
        self.assertIn("ZELENSKY", joined)

    def test_title_and_subline(self):
        self.assertEqual(TITLE, "THE WORLD IN ONE DAY")
        self.assertIn("SIX STORIES", SUBLINE)


if __name__ == "__main__":
    unittest.main()
