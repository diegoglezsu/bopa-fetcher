# bopa-fetcher — AGENTS.md

## Commands

```sh
pip install -e ".[dev,docs]"   # install all deps
pytest                          # run all tests
pytest --cov --cov-branch       # coverage (80% target, 1% threshold)
pytest -k "test_name"           # single test
black src/bopa tests            # format
isort src/bopa tests            # sort imports
flake8 src/bopa tests           # lint
mypy src/bopa                   # typecheck (strict: untyped defs = error, python 3.9)
mkdocs build / mkdocs serve     # docs
python scripts/run_bopa-fetcher.py   # run example script
```

## Architecture

`src/bopa/` is a single-package layout (setuptools `find` in `src/`). **Import as `bopa`** (PyPI package name is `bopa-fetcher`).

```
api/__init__.py     → exports Client
api/client.py       → Client facade (sync, blocking I/O)
service/bulletin.py → Bulletin class: fetches + parses summary HTML
service/article.py  → Article class: fetches + parses detail HTML
service/links.py    → URL builder helpers
models/             → dataclasses: BulletinSummary, BulletinSummaryEntry, BulletinArticle
constants.py        → BOPA URLs, HTML element IDs, DATE_MIN
```

- **Fully synchronous** — `requests.get(timeout=60)` + `BeautifulSoup` (html.parser)
- **Date format**: `dd/mm/YYYY` strings in, `datetime` objects stored; `to_dict()` serializes back to `dd/mm/YYYY`
- **Weekend validation**: `Bulletin.__init__` raises `ValueError` for Sat/Sun
- **Silent skip**: `Client.get_bulletins()` / `Client.get_articles()` wrap each day in `except Exception: pass`
- **No custom exceptions**, no async, no DB
- **Minimum date**: `01/01/2000` (constant `DATE_MIN`); earlier dates raise `ValueError` or silently skip

## Testing

- **Mock HTTP**: `monkeypatch.setattr(requests, "get", lambda url, timeout=60: FakeResponse(html))` — `FakeResponse` in `tests/conftest.py`
- **Client tests**: mock `BulletinService` / `ArticleService` classes directly (not `requests`)
- **Fixtures**: standard pytest fixtures in `conftest.py` (`sample_date`, `sample_bulletin_html`, `sample_article_html`, etc.)
- **All tests synchronous** — no `pytest-asyncio`

## Quirks

- `Article.__init__(date=None)` defaults to `datetime.now()` (was a bug, now fixed)
- `BulletinSummary.codes` property filters out entries with `code == "N/A"`
- `build_origin()` joins non-empty args with `" / "`, skips `None`/empty

## CI

- GitHub Actions: `pytest --cov --cov-branch --cov-report=xml` → Codecov
- Python 3.11, Ubuntu latest
