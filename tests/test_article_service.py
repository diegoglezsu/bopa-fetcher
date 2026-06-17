from datetime import datetime

import requests

from bopa.service.article import Article
from tests.conftest import FakeResponse

import pytest


class TestArticleInit:
    def test_with_all_params(self, sample_date):
        a = Article(cod="2023-11737", num="123", date=sample_date)
        assert a.cod == "2023-11737"
        assert a.num == "123"
        assert a.date.strftime("%d/%m/%Y") == sample_date
        assert a.article is None

    def test_without_params(self):
        a = Article()
        assert a.cod is None
        assert a.num is None
        assert a.date is not None
        assert a.article is None


class TestArticleParseDate:
    def test_with_string(self, sample_date):
        a = Article()
        result = a._parse_date(sample_date)
        assert isinstance(result, datetime)
        assert result.strftime("%d/%m/%Y") == sample_date

    def test_with_datetime(self, sample_datetime):
        a = Article()
        result = a._parse_date(sample_datetime)
        assert result is sample_datetime

    def test_invalid_string(self):
        a = Article()
        with pytest.raises(ValueError):
            a._parse_date("not-a-date")


class TestArticleGetArticle:
    def test_success(self, monkeypatch, sample_article_html, sample_date):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_article_html)

        monkeypatch.setattr(requests, "get", mock_get)

        a = Article(cod="2023-11737", num="123", date=sample_date)
        article = a.get_article()

        assert article.code == "2023-11737"
        assert article.num == "123"
        assert article.date.strftime("%d/%m/%Y") == sample_date
        assert "Principado de Asturias" in article.origin
        assert "Subdirección General" in article.origin
        assert len(article.content) == 2
        assert "Texto del artículo" in article.content[0]

    def test_caching(self, monkeypatch, sample_article_html, sample_date):
        call_count = 0

        def mock_get(url, timeout=60):
            nonlocal call_count
            call_count += 1
            return FakeResponse(sample_article_html)

        monkeypatch.setattr(requests, "get", mock_get)

        a = Article(cod="2023-11737", date=sample_date)
        r1 = a.get_article()
        r2 = a.get_article()
        assert r1 is r2
        assert call_count == 1

    def test_missing_div_raises(self, monkeypatch, sample_date):
        html = "<html><body>No article div</body></html>"

        def mock_get(url, timeout=60):
            return FakeResponse(html)

        monkeypatch.setattr(requests, "get", mock_get)

        a = Article(cod="2023-11737", date=sample_date)
        with pytest.raises(Exception, match="Could not find div with id='bopa-articulo'"):
            a.get_article()

    def test_empty_content_raises(self, monkeypatch, sample_date):
        html = '<div id="bopa-articulo">  </div>'

        def mock_get(url, timeout=60):
            return FakeResponse(html)

        monkeypatch.setattr(requests, "get", mock_get)

        a = Article(cod="2023-11737", date=sample_date)
        with pytest.raises(Exception, match="has no content"):
            a.get_article()

    def test_missing_body_content_raises(self, monkeypatch, sample_date):
        html = """
        <div id="bopa-articulo">
          <h4>Parte</h4>
        </div>
        """

        def mock_get(url, timeout=60):
            return FakeResponse(html)

        monkeypatch.setattr(requests, "get", mock_get)

        a = Article(cod="2023-11737", date=sample_date)
        with pytest.raises(Exception, match="has no body content"):
            a.get_article()

    def test_only_origin_no_body(self, monkeypatch, sample_date):
        html = """
        <div id="bopa-articulo">
          <h4>Parte</h4>
          <h5>Capítulo</h5>
          <p class="subAuthor">Autor</p>
        </div>
        """

        def mock_get(url, timeout=60):
            return FakeResponse(html)

        monkeypatch.setattr(requests, "get", mock_get)

        a = Article(cod="2023-11737", date=sample_date)
        with pytest.raises(Exception, match="has no body content"):
            a.get_article()
