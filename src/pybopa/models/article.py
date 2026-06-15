    

from dataclasses import dataclass
import datetime


@dataclass
class BulletinArticle:
    """Full content for one BOPA article."""

    code: str
    num: str
    date: datetime
    origin: str
    content: list[str]
    link_html: str
    link_pdf: str

    def to_dict(self):
        return {
            "code": self.code,
            "num": self.num,
            "date": self.date.strftime("%d/%m/%Y"),
            "origin": self.origin,
            "content": self.content,
            "link_html": self.link_html,
            "link_pdf": self.link_pdf,
        }