"""
Configurações para os testes do ContentCraft AI
"""
import pytest
import os
from dotenv import load_dotenv

@pytest.fixture(autouse=True)
def load_env():
    """Carrega variáveis de ambiente antes de cada teste"""
    load_dotenv()
    # Verifica se as chaves necessárias estão presentes
    assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY não encontrada"
    assert os.getenv("SERPAPI_API_KEY"), "SERPAPI_API_KEY não encontrada"
