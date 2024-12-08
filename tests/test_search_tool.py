"""
Testes para a ferramenta de pesquisa DuckDuckGo
"""
import pytest
from src.tools.search_tool import FerramentaPesquisa

def test_pesquisa_duckduckgo():
    """Testa a pesquisa básica no DuckDuckGo"""
    ferramenta = FerramentaPesquisa()
    resultados = ferramenta.pesquisar("Python programação")
    assert resultados is not None, "A pesquisa não retornou resultados"
    assert isinstance(resultados, list), "Os resultados devem ser uma lista"
    assert len(resultados) > 0, "A pesquisa deve retornar pelo menos um resultado"

def test_pesquisa_noticias():
    """Testa a pesquisa de notícias"""
    ferramenta = FerramentaPesquisa()
    noticias = ferramenta.pesquisar_noticias("tecnologia Brasil")
    assert noticias is not None, "A pesquisa de notícias não retornou resultados"
    assert isinstance(noticias, list), "Os resultados devem ser uma lista"
