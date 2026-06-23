# bopa-fetcher

[![Tests](https://github.com/diegoglezsu/bopa-fetcher/actions/workflows/tests.yml/badge.svg)](https://github.com/diegoglezsu/bopa-fetcher/actions/workflows/tests.yml)
[![CodeQL](https://github.com/diegoglezsu/bopa-fetcher/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/diegoglezsu/bopa-fetcher/actions/workflows/github-code-scanning/codeql)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=diegoglezsu_bopa-fetcher&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=diegoglezsu_bopa-fetcher)
[![Codecov status](https://codecov.io/github/diegoglezsu/bopa-fetcher/badge.svg?branch=main&service=github)](https://app.codecov.io/github/diegoglezsu/bopa-fetcher)
[![PyPI version](https://img.shields.io/pypi/v/bopa-fetcher.svg)](https://pypi.org/project/bopa-fetcher/)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://diegoglezsu.github.io/bopa-fetcher/)
[![DOI](https://zenodo.org/badge/1193786609.svg)]()

## Description

![bopa-fetcher Logo](https://raw.githubusercontent.com/diegoglezsu/bopa-fetcher/main/docs/assets/logo.png)

**bopa-fetcher** is a Python library for programmatic access to the official bulletins of the Principality of Asturias (BOPA). It allows users to search, retrieve, and analyze bulletin summaries and individual articles in a structured manner.

## Why bopa-fetcher?

[BOPA (Boletín Oficial del Principado de Asturias)](https://miprincipado.asturias.es/bopa) is the official gazette of the region of Asturias, Spain. Researchers, legal professionals, and journalists often need to search, download, and analyze large volumes of legislative and administrative documents. **bopa-fetcher** provides a simple, programmatic interface to:

- Retrieve bulletin summaries and articles as structured Python objects.
- Search across date ranges for both bulletins and individual articles.
- Export data to dictionaries for integration with data analysis pipelines (pandas, NumPy, etc.).
- Avoid manual scraping by handling HTML parsing and URL construction internally.

> [!WARNING]
> BOPA bulletins are available in the portal from **01/01/2000** onwards. Requests for earlier dates will return no data.

## Main features

- **Legal research**: Download and analyze official bulletins for a specific time period to track legislative changes.
- **Data journalism**: Collect structured data from BOPA for investigative reporting on regional governance.
- **Policy analysis**: Extract and categorize dispositions by origin (council, council board, presidency, etc.) for quantitative studies.
- **Archive building**: Build reproducible datasets of Asturian official publications for academic research.

## Quick Start

### Installation

Install from PyPI:

```bash
pip install bopa-fetcher
```

### Basic Usage Example

Fetch acts for a publication date:

```python
from bopa.api import Client
client = Client()

# Get the bulletin summary for 29/12/2023
bulletin = client.get_bulletin(date="29/12/2023")
print(bulletin.to_dict())

# get specific article by code
article = client.get_article(cod="2023-11737", date="29/12/2023")
print(f"  article: {article.to_dict()}")

```

### Use Case Examples

The repository includes runnable scripts with examples and use cases of the library. These scripts can be found in the `scripts/` directory.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions or suggestions, feel free to reach out to the corresponding author:

- **Author**: Diego González Suárez, Noelia Rico Pachón
- **Email**: <gonzalezsdiego@uniovi.es>,<noeliarico@uniovi.es>

## Acknowledgements

## Citation
