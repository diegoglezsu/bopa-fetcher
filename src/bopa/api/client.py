from datetime import datetime, timedelta

from bopa.constants import DATE_MIN

from ..models import BulletinArticle, BulletinSummary
from ..service.article import Article
from ..service.bulletin import Bulletin


class Client:
    """A client class to interact with the BOPA API and fetch bulletins and articles."""

    def get_bulletin(
        self, date: str, text_contains: str | None = None
    ) -> BulletinSummary:
        """Fetch the bulletin summary for a specific date.

        Args:
            date: Date in dd/mm/YYYY format (e.g. "29/12/2023").
            text_contains: Optional string to filter entries by.

        Returns:
            BulletinSummary corresponding to the given date.
        """

        if not date:
            raise ValueError("The 'date' parameter is required.")
        
        if datetime.strptime(date, "%d/%m/%Y") < DATE_MIN:
            raise ValueError(f"date must be on or after {DATE_MIN}.")

        return Bulletin(date=date).get_bulletin(text_contains=text_contains)

    def get_bulletins(
        self, date_from: str, date_to: str, text_contains: str | None = None
    ) -> list[BulletinSummary]:
        """Fetch all bulletin summaries in a date range.

        Args:
            date_from: Start date in dd/mm/YYYY format.
            date_to: End date in dd/mm/YYYY format.
            text_contains: Optional string to filter entries by.

        Returns:
            List of BulletinSummary objects for each weekday in the range.
        """
        date_from = datetime.strptime(date_from, "%d/%m/%Y")
        date_to = datetime.strptime(date_to, "%d/%m/%Y")

        if date_from > date_to:
            raise ValueError("date_from must be earlier than or equal to date_to.")
        
        if date_from < DATE_MIN:
            raise ValueError(f"date_from must be on or after {DATE_MIN}.")

        summaries = []
        current_date = date_from
        while current_date <= date_to:
            fecha_str = current_date.strftime("%d/%m/%Y")
            try:
                summaries.append(
                    self.get_bulletin(fecha_str, text_contains=text_contains)
                )
            except Exception:
                pass
            current_date += timedelta(days=1)

        return summaries

    def get_article(self, cod: str, date: str) -> BulletinArticle:
        """Fetch a specific article by code and date.

        Args:
            cod: Article disposition code (e.g. "2023-11737").
            date: Date in dd/mm/YYYY format.

        Returns:
            BulletinArticle with full content and metadata.
        """

        if not cod or not date:
            raise ValueError("Both 'cod' and 'date' must be provided.")
        
        if datetime.strptime(date, "%d/%m/%Y") < DATE_MIN:
            raise ValueError(f"date must be on or after {DATE_MIN}.")

        return Article(cod=cod, date=date).get_article()

    def get_articles(
        self, date_from: str, date_to: str, text_contains: str | None = None
    ) -> list[BulletinArticle]:
        """Fetch all articles in a date range.

        Iterates over each day in the range, retrieves the bulletin summary,
        and fetches the full content of every article listed.

        Args:
            date_from: Start date in dd/mm/YYYY format.
            date_to: End date in dd/mm/YYYY format.
            text_contains: Optional string to filter bulletin entries by.

        Returns:
            List of BulletinArticle objects in the range.
        """
        articles = []
        start_date = datetime.strptime(date_from, "%d/%m/%Y")
        end_date = datetime.strptime(date_to, "%d/%m/%Y")

        if start_date > end_date:
            raise ValueError("date_from must be earlier than or equal to date_to.")
        
        if start_date < DATE_MIN:
            raise ValueError(f"date_from must be on or after {DATE_MIN}.")

        current_date = start_date
        while current_date <= end_date:
            fecha_str = current_date.strftime("%d/%m/%Y")
            try:
                bulletin = self.get_bulletin(fecha_str, text_contains=text_contains)
                articles.extend(
                    Article(cod=cod, num=bulletin.num, date=bulletin.date).get_article()
                    for cod in bulletin.codes
                )
            except Exception:
                pass
            current_date += timedelta(days=1)

        return articles
