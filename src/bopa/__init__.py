"""bopa-fetcher: A Python library for fetching structured information from BOPA.

BOPA (Boletín Oficial del Principado de Asturias) is the official gazette
of the region of Asturias, Spain. This library provides programmatic access
to its bulletins and articles via web scraping.
"""

__author__ = ["Diego González Suárez", "Noelia Rico"]
__email__ = ["gonzalezsdiego@uniovi.es", "noeliarico@uniovi.es"]
__version__ = "0.1.6"

from . import service
from . import api
from . import models
from . import constants
