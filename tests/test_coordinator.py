"""
Testes para o Agente Coordenador
"""
import pytest
from src.agents.coordinator import CoordinatorAgent

def test_inicializacao_coordenador():
    """Testa a inicialização do agente coordenador"""
    coordenador = CoordinatorAgent()
    assert coordenador.ferramenta_wiki is not None
    assert coordenador.ferramenta_serp is not None
    assert coordenador.ferramenta_pesquisa is not None
    assert coordenador.ferramenta_openai is not None

def test_analise_tema():
    """Testa a análise de um tema específico"""
    coordenador = CoordinatorAgent()
    resultados = coordenador.iniciar_analise("Marketing Digital")
    
    assert resultados is not None
    assert isinstance(resultados, dict)
    assert 'wiki' in resultados
    assert 'google' in resultados
    assert 'duckduckgo' in resultados
    assert 'sugestoes' in resultados
    assert 'noticias' in resultados

def test_geracao_insights():
    """Testa a geração de insights"""
    coordenador = CoordinatorAgent()
    coordenador.iniciar_analise("Marketing Digital")
    insights = coordenador.gerar_insights()
    
    assert insights is not None
    assert isinstance(insights, str)
    assert len(insights) > 0
