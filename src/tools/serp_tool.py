"""
Ferramenta de Integração SerpAPI
Gerencia todas as interações com a API do SerpAPI.
"""
import requests
from src.config.settings import SERPAPI_API_KEY

class FerramentaSERP:
    def __init__(self):
        self.api_key = SERPAPI_API_KEY
        self.base_url = "https://serpapi.com/search"
    
    def pesquisar_google(self, query, local="Brazil"):
        """Realiza pesquisa estruturada no Google"""
        try:
            params = {
                "q": query,
                "location": local,
                "api_key": self.api_key,
                "engine": "google"
            }
            response = requests.get(self.base_url, params=params)
            return response.json()
        except Exception as e:
            print(f"Erro na pesquisa SERP: {e}")
            return None
    
    def obter_sugestoes_relacionadas(self, query):
        """Obtém sugestões de pesquisa relacionadas"""
        try:
            params = {
                "q": query,
                "api_key": self.api_key,
                "engine": "google_related_questions"
            }
            response = requests.get(self.base_url, params=params)
            results = response.json()
            return results.get("related_questions", [])
        except Exception as e:
            print(f"Erro ao obter sugestões: {e}")
            return []
