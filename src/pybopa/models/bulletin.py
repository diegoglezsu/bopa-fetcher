from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BulletinSummaryEntry:
    """One disposition listed in a BOPA summary."""

    code: str
    origin: str
    description: str
    link_html: str
    link_pdf: str

    def to_dict(self):
        return {
            "code": self.code,
            "origin": self.origin,
            "description": self.description,
            "link_html": self.link_html,
            "link_pdf": self.link_pdf,
        }


@dataclass
class BulletinSummary:
    """Structured summary for one BOPA bulletin."""

    num: str
    date: datetime
    summary: list[BulletinSummaryEntry] = field(default_factory=list)

    @property
    def codes(self):
        return [entry.code for entry in self.summary if entry.code != "N/A"]

    def to_dict(self):
        return {
            "num": self.num,
            "date": self.date.strftime("%d/%m/%Y"),
            "summary": [entry.to_dict() for entry in self.summary],
        }
