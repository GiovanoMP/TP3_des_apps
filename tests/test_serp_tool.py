"""
Testes para a ferramenta de integração com SerpAPI
"""
import pytest
from src.tools.serp_tool import FerramentaSERP

def test_pesquisa_google():
    """Testa a pesquisa no Google via SerpAPI"""
    ferramenta = FerramentaSERP()
    resultados = ferramenta.pesquisar_google("marketing digital")
    assert resultados is not None, "A pesquisa não retornou resultados"
    assert isinstance(resultados, dict), "Os resultados devem ser um dicionário"

def test_sugestoes_relacionadas():
    """Testa a obtenção de sugestões relacionadas"""
    ferramenta = FerramentaSERP()
    sugestoes = ferramenta.obter_sugestoes_relacionadas("estratégia de conteúdo")
    assert sugestoes is not None, "Não foram retornadas sugestões"
    assert isinstance(sugestoes, list), "As sugestões devem ser uma lista"
