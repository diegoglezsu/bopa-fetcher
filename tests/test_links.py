from datetime import datetime

from bopa.service.links import build_link_html, build_link_pdf, build_origin


def test_build_link_html(sample_datetime):
    url = build_link_html(sample_datetime, "2023-11737")
    assert "disposiciones" in url
    assert "2023-11737" in url
    assert "%2F" in url


def test_build_link_pdf(sample_datetime):
    url = build_link_pdf(sample_datetime, "2023-11737")
    assert url.endswith("/2023/12/29/2023-11737.pdf")
    assert "bopa" in url


def test_build_origin_all_parts():
    result = build_origin("Part", "Chapter", "Topic", "SubAuthor")
    assert result == "Part / Chapter / Topic / SubAuthor"


def test_build_origin_some_empty():
    result = build_origin("Part", "", "Topic", None)
    assert result == "Part / Topic"


def test_build_origin_all_empty():
    result = build_origin("", None, "")
    assert result == ""


def test_build_origin_no_args():
    result = build_origin()
    assert result == ""
