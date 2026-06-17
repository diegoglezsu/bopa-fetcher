
from dataclasses import dataclass
import datetime


@dataclass
class BulletinArticle:
    """Full content for one BOPA article.

    Attributes:
        code: Disposition code (e.g. "2023-11737").
        num: Bulletin number.
        date: Publication date.
        origin: Origin hierarchy string (part / chapter / topic / sub-author).
        content: List of text paragraphs comprising the article body.
        link_html: URL to the HTML detail page.
        link_pdf: URL to the PDF document.
    """

    code: str
    num: str
    date: datetime
    origin: str
    content: list[str]
    link_html: str
    link_pdf: str

    def to_dict(self):
        """Serialize the article to a dictionary.

        Returns:
            Dict with all fields; date is formatted as dd/mm/YYYY.
        """
        return {
            "code": self.code,
            "num": self.num,
            "date": self.date.strftime("%d/%m/%Y"),
            "origin": self.origin,
            "content": self.content,
            "link_html": self.link_html,
            "link_pdf": self.link_pdf,
        }