# py-bopa API Reference

The py-bopa library is split into two layers:

- API layer: high-level client and typed parsing models.
- Repository layer: connector for BOPA webpage and logic to extract information.

## Basic Imports

```python
from bopa.api import Client
from bopa.models import BulletinArticle, BulletinSummary, BulletinSummaryEntry
```

## Client

::: bopa.api.client.Client
    options:
      heading_level: 3
      show_root_heading: true
      show_root_toc_entry: true

## Models

### BulletinSummary

::: bopa.models.bulletin.BulletinSummary
    options:
      heading_level: 3
      show_root_heading: true
      show_root_toc_entry: true

### BulletinSummaryEntry

::: bopa.models.bulletin.BulletinSummaryEntry
    options:
      heading_level: 3
      show_root_heading: true
      show_root_toc_entry: true

### BulletinArticle

::: bopa.models.article.BulletinArticle
    options:
      heading_level: 3
      show_root_heading: true
      show_root_toc_entry: true
