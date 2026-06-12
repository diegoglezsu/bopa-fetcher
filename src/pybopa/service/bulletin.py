import json
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from .article import Article


class Bulletin:
    """
    A class to represent an Official Bulletin of the Principality of Asturias (BOPA).

    Attributes
    ----------
    num : str, optional
        The bulletin number (default is None).
    date : datetime
        The bulletin date.
    cods : list
        A list of disposition codes in the bulletin.
    sumario : dict
        The parsed summary content of the bulletin.
    articles : list
        A list of Article objects representing the bulletin's dispositions.
    """

    def __init__(self, date=None):
        """
        Builds all necessary attributes for the Bulletin object.

        Parameters
        ----------
        date : str, optional
            The bulletin date (default is None).
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

        self.cods = []
        self.sumario = self._get_sumario()
        self.articles = []

    def _get_boletin(self):
        """
        Fetches the HTML content of the bulletin from the specified URL.

        Returns
        -------
        bs4.element.Tag
            The div containing the bulletin if found, otherwise raises an exception.

        Raises
        ------
        Exception
            If the div with id='bopa-boletin' is not found.
        """

        day = self.date.strftime("%d")
        month = self.date.strftime("%m")
        year = self.date.strftime("%Y")
        url = f"https://miprincipado.asturias.es/bopa-sumario?p_r_p_summaryDate={
            day}%2F{month}%2F{year}"

        response = requests.get(url, timeout=60)
        html_content = response.content

        soup = BeautifulSoup(html_content, "html.parser")

        h1_element = soup.find('h1', class_='gpa-mt-xl')
        if h1_element:
            match = re.search(r'Boletín Nº (\d+)', h1_element.get_text())
            if match:
                self.num = match.group(1)

        boletin_div = soup.find("div", {"id": "bopa-boletin"})

        if boletin_div:
            return boletin_div
        else:
            raise Exception("Could not find div with id='bopa-boletin'.")

    def _get_sumario(self):
        """
        Parses the bulletin content and returns it as a structured dictionary.

        Returns
        -------
        dict
            A dictionary containing the structured content of the bulletin.
        """

        boletin_div = self._get_boletin()

        headers_dict = {}

        current_h4 = None
        current_h5 = None
        current_h6 = None
        current_subauthor = None

        for element in boletin_div.children:

            if element.name == 'h4':
                current_h4 = element.get_text().strip()
                headers_dict[current_h4] = {}
                current_h5 = None
                current_h6 = None
                current_subauthor = None

            elif element.name == 'h5' and current_h4:
                current_h5 = element.get_text().strip()
                headers_dict[current_h4][current_h5] = {}
                current_h6 = None
                current_subauthor = None

            elif element.name == 'h6' and current_h4 and current_h5:
                current_h6 = element.get_text().strip()
                headers_dict[current_h4][current_h5][current_h6] = []
                current_subauthor = None

            elif element.name == 'p' and current_h6 and 'subAuthor' in element.get('class', []):
                current_subauthor = element.get_text().strip()

            elif element.name == 'dl' and current_h6:
                for dt in element.find_all('dt'):
                    entry = {}
                    dt_text = dt.get_text(separator=' ').strip()

                    code_match = re.search(r'\[Cód\. (\d+-\d+)\]', dt_text)
                    if code_match:
                        code = code_match.group(1)
                        dt_text = dt_text.replace(
                            code_match.group(0), '').strip()
                        self.cods.append(code)
                    else:
                        code = 'N/A'

                    entry['description'] = dt_text
                    entry['code'] = code
                    if current_subauthor:
                        entry['subauthor'] = current_subauthor

                    headers_dict[current_h4][current_h5][current_h6].append(
                        entry)

        return headers_dict

    def get_sumario(self):
        """
        Returns the bulletin summary.

        Returns
        -------
        dict
            A dictionary containing the bulletin summary.
        """
        return self.sumario

    def get_cod_disposiciones(self):
        """
        Returns a list of disposition codes in the bulletin.

        Returns
        -------
        list
            A list of disposition codes in the bulletin.
        """
        return self.cods

    def _get_articles(self):
        """
        Fetches the articles of the bulletin from sede.asturias.

        Returns
        -------
        list
            A list of Disposicion objects representing the bulletin's dispositions.
        """

        if not self.articles:
            for code in self.cods:
                article = Article(
                    cod=code, num=self.num, date=self.date)
                self.articles.append(article)
        return self.articles
