from datetime import datetime

from bopa.models import BulletinArticle, BulletinSummary, BulletinSummaryEntry


class TestBulletinSummaryEntry:
    def test_creation(self):
        entry = BulletinSummaryEntry(
            code="2023-11737",
            origin="Part / Chapter / Topic",
            description="Test description",
            link_html="https://example.com/html",
            link_pdf="https://example.com/pdf",
        )
        assert entry.code == "2023-11737"
        assert entry.origin == "Part / Chapter / Topic"
        assert entry.description == "Test description"
        assert entry.link_html == "https://example.com/html"
        assert entry.link_pdf == "https://example.com/pdf"

    def test_to_dict(self):
        entry = BulletinSummaryEntry(
            code="2023-11737",
            origin="Part",
            description="Desc",
            link_html="https://html",
            link_pdf="https://pdf",
        )
        d = entry.to_dict()
        assert d == {
            "code": "2023-11737",
            "origin": "Part",
            "description": "Desc",
            "link_html": "https://html",
            "link_pdf": "https://pdf",
        }


class TestBulletinSummary:
    def test_creation(self, sample_datetime):
        entry = BulletinSummaryEntry(
            code="2023-11737",
            origin="Part",
            description="Desc",
            link_html="https://html",
            link_pdf="https://pdf",
        )
        summary = BulletinSummary(
            num="123", date=sample_datetime, summary=[entry]
        )
        assert summary.num == "123"
        assert summary.date == sample_datetime
        assert len(summary.summary) == 1

    def test_codes_filters_na(self, sample_datetime):
        entries = [
            BulletinSummaryEntry("2023-11737", "Part", "A", "", ""),
            BulletinSummaryEntry("N/A", "Part", "B", "", ""),
            BulletinSummaryEntry("2023-11738", "Part", "C", "", ""),
        ]
        summary = BulletinSummary(num="123", date=sample_datetime, summary=entries)
        assert summary.codes == ["2023-11737", "2023-11738"]

    def test_codes_empty_when_all_na(self, sample_datetime):
        entries = [
            BulletinSummaryEntry("N/A", "Part", "A", "", ""),
        ]
        summary = BulletinSummary(num="123", date=sample_datetime, summary=entries)
        assert summary.codes == []

    def test_codes_empty_when_no_entries(self, sample_datetime):
        summary = BulletinSummary(num="123", date=sample_datetime)
        assert summary.codes == []

    def test_to_dict(self, sample_datetime):
        entry = BulletinSummaryEntry("2023-11737", "Part", "Desc", "html", "pdf")
        summary = BulletinSummary(num="123", date=sample_datetime, summary=[entry])
        d = summary.to_dict()
        assert d["num"] == "123"
        assert d["date"] == "29/12/2023"
        assert len(d["summary"]) == 1
        assert d["summary"][0]["code"] == "2023-11737"


class TestBulletinArticle:
    def test_creation(self, sample_datetime):
        article = BulletinArticle(
            code="2023-11737",
            num="123",
            date=sample_datetime,
            origin="Part / Chapter",
            content=["Line 1", "Line 2"],
            link_html="https://html",
            link_pdf="https://pdf",
        )
        assert article.code == "2023-11737"
        assert article.num == "123"
        assert article.date == sample_datetime
        assert article.origin == "Part / Chapter"
        assert article.content == ["Line 1", "Line 2"]

    def test_to_dict(self, sample_datetime):
        article = BulletinArticle(
            code="2023-11737",
            num="123",
            date=sample_datetime,
            origin="Part",
            content=["Body"],
            link_html="https://html",
            link_pdf="https://pdf",
        )
        d = article.to_dict()
        assert d == {
            "code": "2023-11737",
            "num": "123",
            "date": "29/12/2023",
            "origin": "Part",
            "content": ["Body"],
            "link_html": "https://html",
            "link_pdf": "https://pdf",
        }
