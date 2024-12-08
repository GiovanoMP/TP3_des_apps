"""
Testes para a ferramenta de busca
"""
import pytest
from src.tools.wiki_tool import FerramentaBusca

def test_busca():
    """Testa a busca de informações"""
    ferramenta = FerramentaBusca()
    resultado = ferramenta.buscar_pagina("Python programming")
    
    assert resultado is not None
    assert 'titulo' in resultado
    assert 'sumario' in resultado
    assert 'url' in resultado

def test_referencias():
    """Testa a obtenção de referências"""
    ferramenta = FerramentaBusca()
    referencias = ferramenta.obter_referencias("Python programming")
    
    assert referencias is not None
    assert isinstance(referencias, list)
    assert len(referencias) >= 0  # Pode retornar uma lista vazia em alguns casos
