"""
Testes para a ferramenta de integração com OpenAI
"""
import pytest
from src.tools.openai_tool import FerramentaOpenAI

def test_conexao_openai():
    """Testa a conexão com a API da OpenAI"""
    ferramenta = FerramentaOpenAI()
    prompt = "Olá, isso é um teste de conexão."
    resposta = ferramenta.gerar_conteudo(prompt)
    assert resposta is not None, "A API da OpenAI não retornou resposta"
    assert isinstance(resposta, str), "A resposta deve ser uma string"
