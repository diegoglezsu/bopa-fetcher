import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from bopa.constants import BOPA_BULLETIN_ID, SUMMARY_URL

from ..models import BulletinSummary, BulletinSummaryEntry
from .links import build_link_html, build_link_pdf, build_origin


class Bulletin:
    """Service for fetching BOPA bulletin summaries from the web portal."""

    def __init__(self, date=None):
        """Initialize the Bulletin service.

        Args:
            date: Bulletin date in dd/mm/YYYY format. Defaults to today.
                Weekdays only — Saturdays and Sundays raise a ValueError.
        """

        if date is None:
            self.date = datetime.now()
        else:
            try:
                self.date = datetime.strptime(date, "%d/%m/%Y")
            except ValueError:
                raise ValueError(
                    "Invalid date format. Please provide a date in dd/mm/yyyy format."
                )
            # saturday and sunday BOPA is not available
            if self.date.weekday() in [5, 6]:
                raise ValueError(
                    "Invalid date. The BOPA bulletin is not published on Saturdays and Sundays."
                )

        self.num = None
        self.summary = None
        self.articles = []

    def _get_bulletin_html(self):
        """Fetch the HTML content of the bulletin summary page.

        Returns:
            The div containing the bulletin entries.

        Raises:
            Exception: If the bulletin div is not found on the page.
        """

        day = self.date.strftime("%d")
        month = self.date.strftime("%m")
        year = self.date.strftime("%Y")
        url = f"{SUMMARY_URL}?p_r_p_summaryDate={day}%2F{month}%2F{year}"

        response = requests.get(url, timeout=60)
        soup = BeautifulSoup(response.content, "html.parser")

        h1_element = soup.find("h1", class_="gpa-mt-xl")
        if h1_element:
            match = re.search(r"\b(\d+)\b", h1_element.get_text())
            if match:
                self.num = match.group(1)

        boletin_div = soup.find("div", {"id": BOPA_BULLETIN_ID})

        if boletin_div:
            return boletin_div

        raise Exception(f"Could not find div with id='{BOPA_BULLETIN_ID}'.")

    def _parse_summary(self):
        """Parse the bulletin HTML into a structured summary.

        Iterates over the child elements of the bulletin div, tracking
        the current part (h4), chapter (h5), topic (h6), and sub-author
        (p.subAuthor), then extracts each disposition entry from <dl><dt>
        elements.

        Returns:
            BulletinSummary with all entries parsed.
        """

        boletin_div = self._get_bulletin_html()

        entries = []
        current_part = None
        current_chapter = None
        current_topic = None
        current_subauthor = None

        for element in boletin_div.children:
            if element.name == "h4":
                current_part = element.get_text().strip()
                current_chapter = None
                current_topic = None
                current_subauthor = None

            elif element.name == "h5" and current_part:
                current_chapter = element.get_text().strip()
                current_topic = None
                current_subauthor = None

            elif element.name == "h6" and current_chapter:
                current_topic = element.get_text().strip()
                current_subauthor = None

            elif (
                element.name == "p"
                and current_topic
                and "subAuthor" in element.get("class", [])
            ):
                current_subauthor = element.get_text().strip()

            elif element.name == "dl" and current_topic:
                for dt in element.find_all("dt"):
                    dt_text = dt.get_text(separator=" ").strip()
                    code_match = re.search(r"\[[^\]]*?(\d{4}-\d+)[^\]]*\]", dt_text)
                    if code_match:
                        code = code_match.group(1)
                        dt_text = dt_text.replace(code_match.group(0), "").strip()
                    else:
                        code = "N/A"

                    entries.append(
                        BulletinSummaryEntry(
                            code=code,
                            origin=build_origin(
                                current_part,
                                current_chapter,
                                current_topic,
                                current_subauthor,
                            ),
                            description=dt_text,
                            link_html=build_link_html(self.date, code),
                            link_pdf=build_link_pdf(self.date, code),
                        )
                    )

        return BulletinSummary(num=self.num, date=self.date, summary=entries)

    def get_bulletin(self):
        """Return the structured bulletin summary.

        Results are cached after the first call.

        Returns:
            BulletinSummary for the configured date.
        """

        if self.summary is None:
            self.summary = self._parse_summary()
        return self.summary

