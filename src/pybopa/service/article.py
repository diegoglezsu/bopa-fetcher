import requests
import re
import json
from bs4 import BeautifulSoup


class Article:
    """
    A class to represent an article in the Official Bulletin of the Principality of Asturias (BOPA).

    Attributes
    ----------
    cod : str
        The article code.
    num : str
        The bulletin number.
    date : datetime
        The bulletin date.
    origin: str
        The source of the article (e.g., "SESPA").
    content : list
        The parsed content of the article.
    link_html : str
        The URL to the HTML version of the article.
    link_pdf : str
        The URL to the PDF version of the article.
    """

    def __init__(self, cod=None, num=None, date=None):
        """
        Builds all necessary attributes for the Article object.

        Parameters
        ----------
        cod : str, optional
            The article code (default is None).
        num : str, optional
            The bulletin number (default is None).
        date : datetime, optional
            The bulletin date (default is None).
        """
        self.cod = cod
        self.num = num
        self.date = date
        self._link_html = self._build_link_html()
        self._link_pdf = self._build_link_pdf()
        self.content = self._get_article()

    def _build_link_html(self):
        base = "https://miprincipado.asturias.es/bopa/disposiciones"
        params = (
            "p_p_id=pa_sede_bopa_web_portlet_SedeBopaDispositionWeb"
            "&p_p_lifecycle=0"
            "&_pa_sede_bopa_web_portlet_SedeBopaDispositionWeb_mvcRenderCommandName=%2Fdisposition%2Fdetail"
            f"&p_r_p_dispositionText={self.cod}"
            f"&p_r_p_dispositionReference={self.cod}"
            f"&p_r_p_dispositionDate={self.date.strftime('%d%%2F%m%%2F%Y')}"
        )
        return f"{base}?{params}"

    def _build_link_pdf(self):
        return (
            f"https://miprincipado.asturias.es/bopa/"
            f"{self.date.strftime('%Y/%m/%d')}/{self.cod}.pdf"
        )

    def get_link_html(self):
        return self._link_html

    def get_link_pdf(self):
        return self._link_pdf

    def _get_article(self):
        """
        Fetches and parses the article content from the specified URL.

        Returns
        -------
        list
            A list with the article content.
        """

        url = self._link_html

        response = requests.get(url, timeout=60)
        html_content = response.content

        soup = BeautifulSoup(html_content, "html.parser")

        disposition_div = soup.find("div", {"id": "bopa-articulo"})

        text_list = []

        for element in disposition_div.find_all():
            text_list.append(element.get_text(separator=' '))

        text_list = [text for text in text_list if text.strip()]

        return (text_list)

    def _extract_num_and_date(self, text):
        """
        Extracts the code number and date from the provided text.

        Parameters
        ----------
        text : str
            The text from which to extract the code number and date.

        Returns
        -------
        None
        """

        pattern = r"Nº (\d+) del ([0-9]+) de (\w+) de (\d{4})"

        match = re.search(pattern, text)

        if match:
            code_number = match.group(1)
            day = match.group(2)
            month_str = match.group(3)
            year = match.group(4)

            month_dict = {
                "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
                "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
                "septiembre": "09", "octubre": "10", "noviembre": "11",
                "diciembre": "12"
            }
            month = month_dict.get(month_str.lower(), "00")

            formatted_date = f"{day}/{month}/{year}"

            print("Code number:", code_number)
            print("Date:", formatted_date)
        else:
            print("Code number and date not found.")

    def get_content(self):
        """
        Returns the content of the article.

        Returns
        -------
        list
            A list with the article content.
        """
        return self.content

    def __str__(self):
        """
        Returns a string representation of the Article object.

        Returns
        -------
        str
            A JSON string representing the Article object.
        """

        formatted_date = self.date.strftime("%d/%m/%Y")

        dict_representation = {
            "num": self.num,
            "date": formatted_date,
            "cod": self.cod,
            "link_html": self._link_html,
            "link_pdf": self._link_pdf,
            "content": self.content
        }

        return json.dumps(dict_representation, ensure_ascii=False, indent=4)
