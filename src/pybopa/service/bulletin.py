import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from pybopa.constants import BOPA_URL, DISPOSITONS_URL, SUMMARY_URL

from ..models import BulletinSummary, BulletinSummaryEntry


class Bulletin:
    """
    Service for fetching BOPA summaries and article detail pages.
    """

    def __init__(self, date=None):
        """
        Builds all necessary attributes for the Bulletin service.

        Parameters
        ----------
        date : str, optional
            The bulletin date in dd/mm/yyyy format. Defaults to today.
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
        self.sumario = None
        self.articles = []

    def _get_bulletin_html(self):
        """
        Fetches the HTML content of the bulletin summary page.

        Returns
        -------
        bs4.element.Tag
            The div containing the bulletin if found.

        Raises
        ------
        Exception
            If the div with id='bopa-boletin' is not found.
        """

        day = self.date.strftime("%d")
        month = self.date.strftime("%m")
        year = self.date.strftime("%Y")
        url = (
            SUMMARY_URL,
            f"?p_r_p_summaryDate={day}%2F{month}%2F{year}"
        )

        response = requests.get(url, timeout=60)
        soup = BeautifulSoup(response.content, "html.parser")

        h1_element = soup.find("h1", class_="gpa-mt-xl")
        if h1_element:
            match = re.search(r"\b(\d+)\b", h1_element.get_text())
            if match:
                self.num = match.group(1)

        boletin_div = soup.find("div", {"id": "bopa-boletin"})

        if boletin_div:
            return boletin_div

        raise Exception("Could not find div with id='bopa-boletin'.")

    def _build_article_link_html(self, code):
        params = (
            "p_p_id=pa_sede_bopa_web_portlet_SedeBopaDispositionWeb"
            "&p_p_lifecycle=0"
            "&_pa_sede_bopa_web_portlet_SedeBopaDispositionWeb_mvcRenderCommandName=%2Fdisposition%2Fdetail"
            f"&p_r_p_dispositionText={code}"
            f"&p_r_p_dispositionReference={code}"
            f"&p_r_p_dispositionDate={self.date.strftime('%d%%2F%m%%2F%Y')}"
        )
        return f"{DISPOSITONS_URL}?{params}"

    def _build_article_link_pdf(self, code):
        return (
            BOPA_URL,
            f"{self.date.strftime('%Y/%m/%d')}/{code}.pdf"
        )

    def _build_origin(self, *parts):
        return " / ".join(part for part in parts if part)

    def _parse_summary(self):
        """
        Parses the bulletin content and returns it as a structured summary.

        Returns
        -------
        BulletinSummary
            Structured summary for the bulletin.
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
                            origin=self._build_origin(
                                current_part,
                                current_chapter,
                                current_topic,
                                current_subauthor,
                            ),
                            description=dt_text,
                            link_html=self._build_article_link_html(code),
                            link_pdf=self._build_article_link_pdf(code),
                        )
                    )

        return BulletinSummary(num=self.num, date=self.date, summary=entries)

    def get_bulletin(self):
        """
        Returns the structured bulletin summary.

        Returns
        -------
        BulletinSummary
            The bulletin summary as a Python object.
        """

        if self.sumario is None:
            self.sumario = self._parse_summary()
        return self.sumario

