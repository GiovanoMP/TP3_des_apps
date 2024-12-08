"""
Coordenador dos agentes de análise
Responsável por orquestrar o fluxo de análise entre os agentes
"""
import os
from .market_analyst import AgenteAnalistaMercado

class CoordinatorAgent:
    def __init__(self, google_api_key: str = None):
        """Inicializa o coordenador com a chave da API do Google"""
        if google_api_key is None:
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if not google_api_key:
                raise ValueError("GOOGLE_API_KEY não encontrada. Configure a variável de ambiente.")
        
        self.analyst = AgenteAnalistaMercado(google_api_key)
        
    def process_query(self, query: str) -> str:
        """
        Processa uma consulta do usuário
        
        Args:
            query (str): A pergunta ou consulta do usuário
            
        Returns:
            str: A resposta processada
        """
        try:
            return self.analyst.process_query(query)
        except Exception as e:
            return f"❌ Erro ao processar consulta: {str(e)}"
