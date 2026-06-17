from datetime import datetime

import requests
from bs4 import BeautifulSoup

from bopa.constants import BOPA_ARTICLE_ID

from ..models import BulletinArticle
from .links import build_link_html, build_link_pdf, build_origin


class Article:
    """
    Service for fetching BOPA article detail pages.
    """

    def __init__(self, cod=None, num=None, date=None):
        """
        Builds all necessary attributes for the Article service.

        Parameters
        ----------
        cod : str
            Article disposition code.
        num : str
            Bulletin number.
        date : str or datetime
            Bulletin date.
        """

        self.cod = cod
        self.num = num
        self.date = self._parse_date(date)
        self.article = None

    def _parse_date(self, date):
        if isinstance(date, datetime):
            return date
        return datetime.strptime(date, "%d/%m/%Y")

    def _get_article_html(self):
        f"""
        Fetches the HTML content of the article detail page.

        Returns
        -------
        bs4.element.Tag
            The div containing the article if found.

        Raises
        ------
        ArticleNotFoundError
            If the div with id='{BOPA_ARTICLE_ID}' is not found or is empty.
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
        """
        Parses the article content and returns it as a structured object.

        Returns
        -------
        BulletinArticle
            Structured article with full content.
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
        """
        Returns the structured article.

        Returns
        -------
        BulletinArticle
            The article as a Python object.
        """

        if self.article is None:
            self.article = self._parse_article()
        return self.article
