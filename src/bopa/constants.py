"""Constants for BOPA web portal URLs and HTML element identifiers."""

from datetime import datetime


BOPA_URL = "https://miprincipado.asturias.es/bopa"

DISPOSITONS_URL = BOPA_URL + "/disposiciones"

SUMMARY_URL = "https://miprincipado.asturias.es/bopa-sumario"

BOPA_ARTICLE_ID = "bopa-articulo"
BOPA_BULLETIN_ID = "bopa-boletin"

DATE_MIN = datetime(2000, 1, 1)  # Minimum date for BOPA bulletins