from datetime import datetime

import pytest


class FakeResponse:
    def __init__(self, content, status_code=200):
        self.content = content.encode("utf-8") if isinstance(content, str) else content
        self.status_code = status_code


@pytest.fixture
def sample_date():
    return "29/12/2023"


@pytest.fixture
def sample_datetime():
    return datetime(2023, 12, 29)


@pytest.fixture
def sample_bulletin_html():
    return """
    <h1 class="gpa-mt-xl">Boletín número 123</h1>
    <div id="bopa-boletin">
      <h4>I. Principado de Asturias</h4>
      <h5>Disposiciones Generales</h5>
      <h6>Consejería de Presidencia</h6>
      <p class="subAuthor">Subdirección General</p>
      <dl>
        <dt>Descripción de la disposición [Cód. 2023-11737]</dt>
      </dl>
      <h4>II. Otra Sección</h4>
      <h5>Otro Capítulo</h5>
      <h6>Otro Tema</h6>
      <dl>
        <dt>Sin código visible</dt>
      </dl>
    </div>
    """


@pytest.fixture
def sample_article_html():
    return """
    <div id="bopa-articulo">
      <h4>I. Principado de Asturias</h4>
      <h5>Disposiciones Generales</h5>
      <h6>Consejería de Presidencia</h6>
      <p class="subAuthor">Subdirección General</p>
      <p>Texto del artículo número uno.</p>
      <p>Más contenido del artículo.</p>
    </div>
    """


@pytest.fixture
def minimal_bulletin_html():
    return """
    <h1 class="gpa-mt-xl">Boletín número 456</h1>
    <div id="bopa-boletin">
      <h4>Única Sección</h4>
      <h5>Único Capítulo</h5>
      <h6>Único Tema</h6>
      <dl>
        <dt>Disposición [2024-00001]</dt>
      </dl>
    </div>
    """
