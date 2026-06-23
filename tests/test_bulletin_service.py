import requests
from bs4 import BeautifulSoup

from bopa.service.bulletin import Bulletin
from tests.conftest import FakeResponse


class TestBulletinInit:
    def test_with_valid_date(self):
        b = Bulletin(date="29/12/2023")
        assert b.date.strftime("%d/%m/%Y") == "29/12/2023"
        assert b.num is None
        assert b.summary is None

    def test_without_date(self):
        b = Bulletin()
        assert b.date is not None
        assert b.summary is None

    def test_invalid_date_format(self):
        with pytest.raises(ValueError, match="Invalid date format"):
            Bulletin(date="29-12-2023")

    def test_weekend_saturday(self):
        with pytest.raises(ValueError, match="not published on Saturdays and Sundays"):
            Bulletin(date="30/12/2023")

    def test_weekend_sunday(self):
        with pytest.raises(ValueError, match="not published on Saturdays and Sundays"):
            Bulletin(date="31/12/2023")


class TestBulletinGetBulletin:
    def test_success(self, monkeypatch, sample_bulletin_html, sample_date):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin()

        assert summary.num == "123"
        assert summary.date.strftime("%d/%m/%Y") == sample_date
        assert len(summary.summary) == 2

        entry = summary.summary[0]
        assert entry.code == "2023-11737"
        assert "Principado de Asturias" in entry.origin
        assert "Subdirección General" in entry.origin
        assert "Descripción de la disposición" in entry.description
        assert "2023-11737" in entry.link_html
        assert "2023-11737" in entry.link_pdf

        entry2 = summary.summary[1]
        assert entry2.code == "N/A"

    def test_caching(self, monkeypatch, sample_bulletin_html, sample_date):
        call_count = 0

        def mock_get(url, timeout=60):
            nonlocal call_count
            call_count += 1
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        r1 = b.get_bulletin()
        r2 = b.get_bulletin()
        assert r1 is r2
        assert call_count == 1

    def test_missing_div_raises(self, monkeypatch, sample_date):
        html = "<html><body>No div here</body></html>"

        def mock_get(url, timeout=60):
            return FakeResponse(html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        with pytest.raises(Exception, match="Could not find div with id='bopa-boletin'"):
            b.get_bulletin()

    def test_h1_without_number(self, monkeypatch, sample_date):
        html = """
        <h1 class="gpa-mt-xl">No number here</h1>
        <div id="bopa-boletin">
          <h4>Única Sección</h4>
          <h5>Tema</h5>
          <h6>Subtema</h6>
          <dl><dt>Desc [2023-00001]</dt></dl>
        </div>
        """

        def mock_get(url, timeout=60):
            return FakeResponse(html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin()
        assert summary.num is None

    def test_parse_with_hierarchy_gaps(self, monkeypatch, sample_date):
        html = """
        <div id="bopa-boletin">
          <h4>Solo Parte</h4>
          <h5>Solo Capítulo</h5>
          <h6>Solo Tema</h6>
          <dl><dt>Desc [2023-00001]</dt></dl>
        </div>
        """

        def mock_get(url, timeout=60):
            return FakeResponse(html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin()
        assert len(summary.summary) == 1
        assert summary.summary[0].code == "2023-00001"

    def test_dl_without_dt_children(self, monkeypatch, sample_date):
        html = """
        <div id="bopa-boletin">
          <h4>Parte</h4>
          <h5>Capítulo</h5>
          <h6>Tema</h6>
          <dl></dl>
        </div>
        """

        def mock_get(url, timeout=60):
            return FakeResponse(html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin()
        assert len(summary.summary) == 0


class TestBulletinTextContains:
    def test_filter_by_description(self, monkeypatch, sample_bulletin_html, sample_date):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin(text_contains="Descripción")
        assert len(summary.summary) == 1
        assert summary.summary[0].code == "2023-11737"

    def test_filter_by_origin(self, monkeypatch, sample_bulletin_html, sample_date):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin(text_contains="Principado")
        assert len(summary.summary) == 1
        assert "Principado de Asturias" in summary.summary[0].origin

    def test_filter_by_code(self, monkeypatch, sample_bulletin_html, sample_date):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin(text_contains="2023-11737")
        assert len(summary.summary) == 1
        assert summary.summary[0].code == "2023-11737"

    def test_no_match_returns_empty(self, monkeypatch, sample_bulletin_html, sample_date):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin(text_contains="XYZZZZ")
        assert len(summary.summary) == 0

    def test_case_insensitive(self, monkeypatch, sample_bulletin_html, sample_date):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin(text_contains="descripción")
        assert len(summary.summary) == 1

    def test_none_returns_all(self, monkeypatch, sample_bulletin_html, sample_date):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin(text_contains=None)
        assert len(summary.summary) == 2

    def test_preserves_caching_without_filter(
        self, monkeypatch, sample_bulletin_html, sample_date
    ):
        call_count = 0

        def mock_get(url, timeout=60):
            nonlocal call_count
            call_count += 1
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        r1 = b.get_bulletin()
        r2 = b.get_bulletin(text_contains=None)
        assert r1 is r2
        assert call_count == 1

    def test_bypasses_cache_with_filter(
        self, monkeypatch, sample_bulletin_html, sample_date
    ):
        call_count = 0

        def mock_get(url, timeout=60):
            nonlocal call_count
            call_count += 1
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        r1 = b.get_bulletin()
        r2 = b.get_bulletin(text_contains="Descripción")
        assert r1 is not r2
        assert call_count == 2


class TestBulletinOriginContains:
    def test_filter_by_origin(self, monkeypatch, sample_bulletin_html, sample_date):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin(origin_contains="Principado")
        assert len(summary.summary) == 1
        assert "Principado de Asturias" in summary.summary[0].origin

    def test_no_match_returns_empty(self, monkeypatch, sample_bulletin_html, sample_date):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin(origin_contains="XYZZZZ")
        assert len(summary.summary) == 0

    def test_case_insensitive(self, monkeypatch, sample_bulletin_html, sample_date):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin(origin_contains="principado")
        assert len(summary.summary) == 1

    def test_none_returns_all(self, monkeypatch, sample_bulletin_html, sample_date):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin(origin_contains=None)
        assert len(summary.summary) == 2

    def test_combined_with_text_contains(
        self, monkeypatch, sample_bulletin_html, sample_date
    ):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin(
            text_contains="Descripción", origin_contains="Principado"
        )
        assert len(summary.summary) == 1

    def test_combined_no_match(self, monkeypatch, sample_bulletin_html, sample_date):
        def mock_get(url, timeout=60):
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        summary = b.get_bulletin(
            text_contains="Descripción", origin_contains="XYZZZZ"
        )
        assert len(summary.summary) == 0

    def test_caching_bypassed_with_filter(
        self, monkeypatch, sample_bulletin_html, sample_date
    ):
        call_count = 0

        def mock_get(url, timeout=60):
            nonlocal call_count
            call_count += 1
            return FakeResponse(sample_bulletin_html)

        monkeypatch.setattr(requests, "get", mock_get)

        b = Bulletin(date=sample_date)
        r1 = b.get_bulletin()
        r2 = b.get_bulletin(origin_contains="Principado")
        assert r1 is not r2
        assert call_count == 2


import pytest
