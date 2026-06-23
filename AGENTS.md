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
```

- **Fully synchronous** — `requests.get(timeout=60)` + `BeautifulSoup` (html.parser)
- **Date format**: `dd/mm/YYYY` everywhere (strings in, `datetime` objects stored)
- **Weekend validation**: `Bulletin.__init__` raises `ValueError` for Sat/Sun
- **Silent skip**: `Client.get_bulletins()` / `Client.get_articles()` catch all exceptions per day
- **No custom exceptions**, no async, no DB

## Testing

- **Mock HTTP**: use `monkeypatch.setattr(requests, "get", lambda url, timeout=60: FakeResponse(html))` — see `tests/conftest.py:FakeResponse`
- **Client tests**: mock `BulletinService` / `ArticleService` classes, not `requests`
- **All tests synchronous** — no fixtures, no `pytest-asyncio`

## Quirks

- `Article.__init__(date=None)` defaults to `datetime.now()` (was a bug, now fixed)
- `BulletinSummary.codes` property filters out entries with `code == "N/A"`
- `build_origin()` joins non-empty args with `" / "`, skips `None`/empty
- `to_dict()` serializes `date` as `dd/mm/YYYY` string

## CI

- GitHub Actions: `pytest --cov --cov-branch --cov-report=xml` → Codecov
- Python 3.11, Ubuntu latest
