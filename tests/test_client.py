from unittest.mock import create_autospec

from bopa.api import Client
from bopa.models import BulletinArticle, BulletinSummary, BulletinSummaryEntry
from bopa.service.article import Article as ArticleService
from bopa.service.bulletin import Bulletin as BulletinService

import pytest


class TestClientGetBulletin:
    def test_get_bulletin(self, monkeypatch, sample_datetime):
        expected = BulletinSummary(
            num="123",
            date=sample_datetime,
            summary=[
                BulletinSummaryEntry(
                    code="2023-11737",
                    origin="Part",
                    description="Desc",
                    link_html="https://html",
                    link_pdf="https://pdf",
                )
            ],
        )

        def mock_bulletin_init(self, date):
            self.date = sample_datetime
            self.num = "123"
            self.sumario = None

        monkeypatch.setattr(BulletinService, "__init__", mock_bulletin_init)
        monkeypatch.setattr(
            BulletinService, "get_bulletin", lambda self, **kwargs: expected
        )

        client = Client()
        result = client.get_bulletin("29/12/2023")
        assert result is expected
        assert result.num == "123"
        assert result.date == sample_datetime

    def test_get_bulletin_passes_date(self, monkeypatch):
        captured_dates = []

        def mock_bulletin_init(self, date):
            self.date = None
            self.num = None
            self.sumario = None

        monkeypatch.setattr(BulletinService, "__init__", mock_bulletin_init)
        monkeypatch.setattr(
            BulletinService,
            "get_bulletin",
            lambda self, **kwargs: BulletinSummary(num=None, date=None),
        )

        client = Client()
        result = client.get_bulletin("29/12/2023")
        assert result.num is None


class TestClientGetBulletins:
    def test_success(self, monkeypatch, sample_datetime):
        results = {}

        def mock_bulletin_init(self, date):
            self.date = None
            self.num = None
            self.sumario = None
            self._date_str = date

        monkeypatch.setattr(BulletinService, "__init__", mock_bulletin_init)

        def mock_get_bulletin(self, **kwargs):
            ds = self._date_str
            return BulletinSummary(num=ds.split("/")[0], date=sample_datetime)

        monkeypatch.setattr(BulletinService, "get_bulletin", mock_get_bulletin)

        client = Client()
        bulletins = client.get_bulletins("01/12/2023", "03/12/2023")
        assert len(bulletins) == 3

    def test_skips_failures(self, monkeypatch, sample_datetime):
        call_dates = []

        def mock_bulletin_init(self, date):
            self.date = None
            self.num = None
            self.sumario = None
            self._date_str = date

        monkeypatch.setattr(BulletinService, "__init__", mock_bulletin_init)

        def mock_get_bulletin(self, **kwargs):
            ds = self._date_str
            call_dates.append(ds)
            if ds == "02/12/2023":
                raise Exception("skip")
            return BulletinSummary(num="999", date=sample_datetime)

        monkeypatch.setattr(BulletinService, "get_bulletin", mock_get_bulletin)

        client = Client()
        bulletins = client.get_bulletins("01/12/2023", "03/12/2023")
        assert len(bulletins) == 2


class TestClientGetArticle:
    def test_get_article(self, monkeypatch, sample_datetime, sample_date):
        expected = BulletinArticle(
            code="2023-11737",
            num="123",
            date=sample_datetime,
            origin="Part",
            content=["Body"],
            link_html="https://html",
            link_pdf="https://pdf",
        )

        calls = []

        def mock_article_init(self, cod=None, num=None, date=None):
            calls.append((cod, num, date))
            self.cod = cod
            self.num = num
            self.date = sample_datetime
            self.article = None

        monkeypatch.setattr(ArticleService, "__init__", mock_article_init)
        monkeypatch.setattr(
            ArticleService, "get_article", lambda self, **kwargs: expected
        )

        client = Client()
        result = client.get_article("2023-11737", sample_date)
        assert result is expected
        assert result.code == "2023-11737"
        assert len(calls) == 1
        assert calls[0][0] == "2023-11737"


class TestClientGetArticles:
    def test_returns_articles(self, monkeypatch, sample_datetime):
        captured = []

        def mock_bulletin_init(self, date):
            self.date = sample_datetime
            self.num = "123"
            self.sumario = None
            self._date_str = date

        monkeypatch.setattr(BulletinService, "__init__", mock_bulletin_init)

        def mock_get_bulletin(self, **kwargs):
            entries = [
                BulletinSummaryEntry("2023-00001", "Part", "A", "", ""),
                BulletinSummaryEntry("2023-00002", "Part", "B", "", ""),
            ]
            return BulletinSummary(num="123", date=sample_datetime, summary=entries)

        monkeypatch.setattr(BulletinService, "get_bulletin", mock_get_bulletin)

        articles_created = {}

        def mock_article_init(self, cod, num, date):
            self.cod = cod
            self.num = num
            self.date = sample_datetime
            self.article = None

        monkeypatch.setattr(ArticleService, "__init__", mock_article_init)

        def mock_get_article(self, **kwargs):
            return BulletinArticle(
                code=self.cod,
                num=self.num,
                date=sample_datetime,
                origin="Part",
                content=[f"Content of {self.cod}"],
                link_html="",
                link_pdf="",
            )

        monkeypatch.setattr(ArticleService, "get_article", mock_get_article)

        client = Client()
        articles = client.get_articles("29/12/2023", "29/12/2023")
        assert len(articles) == 2
        assert articles[0].code == "2023-00001"
        assert articles[1].code == "2023-00002"

    def test_skips_failures_gracefully(self, monkeypatch, sample_datetime):
        def mock_bulletin_init(self, date):
            self.date = sample_datetime
            self.num = "123"
            self.sumario = None
            self._date_str = date

        monkeypatch.setattr(BulletinService, "__init__", mock_bulletin_init)

        call_count = 0

        def mock_get_bulletin(self, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count > 1:
                raise Exception("fail")
            entries = [BulletinSummaryEntry("2023-00001", "Part", "A", "", "")]
            return BulletinSummary(num="123", date=sample_datetime, summary=entries)

        monkeypatch.setattr(BulletinService, "get_bulletin", mock_get_bulletin)

        def mock_article_init(self, cod, num, date):
            self.cod = cod
            self.num = num
            self.date = sample_datetime
            self.article = None

        monkeypatch.setattr(ArticleService, "__init__", mock_article_init)

        monkeypatch.setattr(
            ArticleService,
            "get_article",
            lambda self, **kwargs: BulletinArticle(
                code=self.cod,
                num=self.num,
                date=sample_datetime,
                origin="Part",
                content=["Body"],
                link_html="",
                link_pdf="",
            ),
        )

        client = Client()
        articles = client.get_articles("29/12/2023", "30/12/2023")
        assert len(articles) == 1

    def test_filters_by_text_contains(self, monkeypatch, sample_datetime):
        def mock_bulletin_init(self, date):
            self.date = sample_datetime
            self.num = "123"
            self.sumario = None
            self._date_str = date

        monkeypatch.setattr(BulletinService, "__init__", mock_bulletin_init)

        def mock_get_bulletin(self, **kwargs):
            tc = kwargs.get("text_contains")
            entries = [
                BulletinSummaryEntry("2023-00001", "Part", "Alpha", "", ""),
                BulletinSummaryEntry("2023-00002", "Part", "Beta", "", ""),
            ]
            if tc:
                entries = [e for e in entries if tc.lower() in e.description.lower()]
            return BulletinSummary(num="123", date=sample_datetime, summary=entries)

        monkeypatch.setattr(BulletinService, "get_bulletin", mock_get_bulletin)

        def mock_article_init(self, cod, num, date):
            self.cod = cod
            self.num = num
            self.date = sample_datetime
            self.article = None

        monkeypatch.setattr(ArticleService, "__init__", mock_article_init)

        def mock_get_article(self, **kwargs):
            return BulletinArticle(
                code=self.cod,
                num=self.num,
                date=sample_datetime,
                origin="Part",
                content=[f"Content of {self.cod}"],
                link_html="",
                link_pdf="",
            )

        monkeypatch.setattr(ArticleService, "get_article", mock_get_article)

        client = Client()
        articles = client.get_articles("29/12/2023", "29/12/2023", text_contains="Alpha")
        assert len(articles) == 1
        assert articles[0].code == "2023-00001"

    def test_filters_by_origin_contains(self, monkeypatch, sample_datetime):
        def mock_bulletin_init(self, date):
            self.date = sample_datetime
            self.num = "123"
            self.sumario = None
            self._date_str = date

        monkeypatch.setattr(BulletinService, "__init__", mock_bulletin_init)

        def mock_get_bulletin(self, **kwargs):
            oc = kwargs.get("origin_contains")
            entries = [
                BulletinSummaryEntry("2023-00001", "Part A", "Alpha", "", ""),
                BulletinSummaryEntry("2023-00002", "Part B", "Beta", "", ""),
            ]
            if oc:
                entries = [e for e in entries if oc.lower() in e.origin.lower()]
            return BulletinSummary(num="123", date=sample_datetime, summary=entries)

        monkeypatch.setattr(BulletinService, "get_bulletin", mock_get_bulletin)

        def mock_article_init(self, cod, num, date):
            self.cod = cod
            self.num = num
            self.date = sample_datetime
            self.article = None

        monkeypatch.setattr(ArticleService, "__init__", mock_article_init)

        def mock_get_article(self, **kwargs):
            return BulletinArticle(
                code=self.cod,
                num=self.num,
                date=sample_datetime,
                origin="Part",
                content=[f"Content of {self.cod}"],
                link_html="",
                link_pdf="",
            )

        monkeypatch.setattr(ArticleService, "get_article", mock_get_article)

        client = Client()
        articles = client.get_articles(
            "29/12/2023", "29/12/2023", origin_contains="Part A"
        )
        assert len(articles) == 1
        assert articles[0].code == "2023-00001"
