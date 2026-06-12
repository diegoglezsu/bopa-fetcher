from datetime import datetime, timedelta

from datetime import datetime, timedelta

from ..service.bulletin import Bulletin
from ..service.article import Article


class Client:
    """A client class to interact with the BOPA API and fetch bulletins and articles."""
    def get_bulletin(self, date: str) -> Bulletin:
        """Returns the bulletin for a specific date.

        Parameters
        ----------
        date : str
            Date in format dd/mm/YYYY.

        Returns
        -------
        Bulletin
            The bulletin corresponding to the date.
        """
        bulletin = Bulletin(date=date)
        bulletin._get_articles()
        return bulletin

    def get_bulletins(self, date_from: str, date_to: str) -> list[Bulletin]:
        """Returns all bulletins in a date range.

        Parameters
        ----------
        date_from : str
            Start date in format dd/mm/YYYY.
        date_to : str
            End date in format dd/mm/YYYY.

        Returns
        -------
        list[Bulletin]
            List of bulletins in the specified range.    
        """
        date_from = datetime.strptime(date_from, "%d/%m/%Y")
        date_to = datetime.strptime(date_to, "%d/%m/%Y")

        bulletins = []
        current_date = date_from
        while current_date <= date_to:
            fecha_str = current_date.strftime("%d/%m/%Y")
            try:
                bulletins.append(self.get_bulletin(fecha_str))
            except Exception:
                pass
            current_date += timedelta(days=1)

        return bulletins

    def get_article(self, cod: str, num: str, date: str) -> Article:
        """Returns the article for a specific code and number.

        Parameters
        ----------
        cod : str
            Code of the article.
        num : str
            Bulletin number of the article.
        date : str
            Date in format dd/mm/YYYY.

        Returns
        -------
        Article
            The article corresponding to the code and number.
        """
        return Article(cod=cod, num=num, date=datetime.strptime(date, "%d/%m/%Y"))

    def get_articles(self, date_from: str, date_to: str) -> list[Article]:
        """Returns all articles in a date range.

        Parameters
        ----------
        date_from : str
            Start date in format dd/mm/YYYY.
        date_to : str
            End date in format dd/mm/YYYY.

        Returns
        -------
        list[Article]
            List of articles in the specified range.
        """
        articles = [
            a for b in self.get_bulletins(date_from, date_to) for a in b.articles
        ]
        return articles
