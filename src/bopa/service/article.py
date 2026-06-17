from datetime import datetime

import requests
from bs4 import BeautifulSoup

from bopa.constants import BOPA_ARTICLE_ID

from ..models import BulletinArticle
from .links import build_link_html, build_link_pdf, build_origin


class Article:
    """Service for fetching full BOPA article detail pages."""

    def __init__(self, cod=None, num=None, date=None):
        """Initialize the Article service.

        Args:
            cod: Article disposition code (e.g. "2023-11737").
            num: Bulletin number.
            date: Bulletin date as a string (dd/mm/YYYY) or datetime object.
        """

        self.cod = cod
        self.num = num
        self.date = self._parse_date(date) if date is not None else datetime.now()
        self.article = None

    def _parse_date(self, date):
        """Parse a date string or datetime into a datetime object.

        Args:
            date: Date in dd/mm/YYYY format or a datetime object.

        Returns:
            Parsed datetime object.
        """
        if isinstance(date, datetime):
            return date
        return datetime.strptime(date, "%d/%m/%Y")

    def _get_article_html(self):
        """Fetch the HTML content of the article detail page.

        Returns:
            The div containing the article content.

        Raises:
            Exception: If the article div is not found or the article
                has no content.
        """

        response = requests.get(build_link_html(self.date, self.cod), timeout=60)
        soup = BeautifulSoup(response.content, "html.parser")
        article_div = soup.find("div", {"id": BOPA_ARTICLE_ID})

        if article_div is None:
            raise Exception(f"Could not find div with id='{BOPA_ARTICLE_ID}'.")

        if not article_div.get_text(strip=True):
            raise Exception(
                f"Article '{self.cod}' has no content."
            )

        return article_div

    def _parse_article(self):
        """Parse the article HTML into a structured BulletinArticle.

        Extracts origin information from h4/h5/h6/subAuthor elements and
        body text from all remaining child elements.

        Returns:
            BulletinArticle with full content and metadata.
        """

        article_div = self._get_article_html()

        origin_parts = []
        content = []

        for element in article_div.children:
            if element.name == "h4":
                origin_parts.append(element.get_text().strip())
            elif element.name == "h5":
                origin_parts.append(element.get_text().strip())
            elif element.name == "h6":
                origin_parts.append(element.get_text().strip())
            elif element.name == "p" and "subAuthor" in element.get("class", []):
                origin_parts.append(element.get_text().strip())
            else:
                text = element.get_text(separator=" ").strip()
                if text:
                    content.append(text)

        if not content:
            raise Exception(
                f"Article '{self.cod}' was found but has no body content."
            )

        return BulletinArticle(
            code=self.cod,
            num=self.num,
            date=self.date,
            origin=build_origin(*origin_parts),
            content=content,
            link_html=build_link_html(self.date, self.cod),
            link_pdf=build_link_pdf(self.date, self.cod),
        )

    def get_article(self):
        """Return the structured article.

        Results are cached after the first call.

        Returns:
            BulletinArticle for the configured code and date.
        """

        if self.article is None:
            self.article = self._parse_article()
        return self.article
