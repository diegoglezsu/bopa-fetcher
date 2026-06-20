from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BulletinSummaryEntry:
    """One disposition entry listed in a BOPA bulletin summary.

    Attributes:
        code: Disposition code (e.g. "2023-11737"), or "N/A" if not found.
        origin: Origin hierarchy string (part / chapter / topic / sub-author).
        description: Short text description of the disposition.
        link_html: URL to the HTML detail page.
        link_pdf: URL to the PDF document.
    """

    code: str
    origin: str
    description: str
    link_html: str
    link_pdf: str

    def to_dict(self) -> dict[str, str]:
        """Serialize the entry to a dictionary.

        Returns:
            Dict with all fields.
        """
        return {
            "code": self.code,
            "origin": self.origin,
            "description": self.description,
            "link_html": self.link_html,
            "link_pdf": self.link_pdf,
        }


@dataclass
class BulletinSummary:
    """Structured summary for one BOPA bulletin.

    Attributes:
        num: Bulletin number.
        date: Publication date.
        summary: List of disposition entries.
    """

    num: str
    date: datetime
    summary: list[BulletinSummaryEntry] = field(default_factory=list)

    @property
    def codes(self):
        """List of non-empty disposition codes in this bulletin."""
        return [entry.code for entry in self.summary if entry.code != "N/A"]

    def to_dict(self) -> dict[str, object]:
        """Serialize the bulletin summary to a dictionary.

        Returns:
            Dict with num, date (dd/mm/YYYY), and serialized entries.
        """
        return {
            "num": self.num,
            "date": self.date.strftime("%d/%m/%Y"),
            "summary": [entry.to_dict() for entry in self.summary],
        }
