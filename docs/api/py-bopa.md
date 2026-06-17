# py-bopa API Reference

The py-bopa library is split into two layers:

- API layer: high-level client and typed parsing models.
- Repository layer: connector for BOPA webpage and logic to extract information.

## Basic Imports

```python
from bopa.api import Client
from bopa.models import BulletinArticle, BulletinSummary, BulletinSummaryEntry
```

## Api Functions

::: bopa.api.client.Client
    options:
      heading_level: 3
      show_root_heading: true
      show_root_toc_entry: true

## Models

::: bopa.models.bulletin.BulletinSummary
    options:
      heading_level: 3
      show_root_heading: true
      show_root_toc_entry: true

::: bopa.models.bulletin.BulletinSummaryEntry
    options:
      heading_level: 3
      show_root_heading: true
      show_root_toc_entry: true

::: bopa.models.article.BulletinArticle
    options:
      heading_level: 3
      show_root_heading: true
      show_root_toc_entry: true
