# Getting Started

## Requirements

- Python 3.7+
- Internet access

## Installation

Install from PyPI:

```bash
pip install py-bopa
```

Or install from source with development dependencies:

```bash
pip install -e .[dev,docs]
```

## First Query 🚀

Fetch a bulletin summary for a specific date:

```python
from bopa.api import Client

client = Client()

# Get the bulletin summary for 29/12/2023
bulletin = client.get_bulletin(date="29/12/2023")
print(bulletin.to_dict())
```

Fetch an individual article:

```python
from bopa.api import Client

client = Client()

# Get a specific article by code and date
article = client.get_article(cod="2023-11737", date="29/12/2023")
print(f"Origin: {article.origin}")
print(f"Content: {article.content[:3]}...")  # First 3 paragraphs
print(f"PDF: {article.link_pdf}")
```

Fetch bulletins across a date range:

```python
from bopa.api import Client

client = Client()

bulletins = client.get_bulletins(date_from="01/06/2025", date_to="10/06/2025")
for b in bulletins:
    print(f"Bulletin #{b.num} - {b.date.strftime('%d/%m/%Y')}: {len(b.summary)} entries")
```

### Run Example Scripts

The repository includes runnable scripts with examples. These can be found in the [`scripts`](https://github.com/diegoglezsu/py-bopa/tree/main/scripts) directory:

```bash
python scripts/run_py-bopa.py
```
