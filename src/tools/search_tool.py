"""
Ferramenta de Busca
Gerencia buscas de informações usando APIs públicas.
"""
import requests
import json
from datetime import datetime, timedelta

class FerramentaPesquisa:
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
        self.news_api_url = "https://newsapi.org/v2/everything"
        self.headers = {
            'User-Agent': 'ContentCraftAI/1.0 (Educational Project)'
        }
    
    def pesquisar(self, query, max_resultados=10):
        """Realiza pesquisa usando APIs públicas"""
        try:
            # Formata a query para a URL
            query_formatada = query.replace(" ", "_").lower()
            response = requests.get(
                f"{self.base_url}{query_formatada}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return [{
                    'title': data.get('title', query),
                    'link': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    'snippet': data.get('extract', 'Informação não disponível')
                }]
            
            # Fallback: retorna um resultado genérico
            return [{
                'title': query,
                'link': f'https://www.google.com/search?q={query}',
                'snippet': 'Não foi possível encontrar informações detalhadas.'
            }]
            
        except Exception as e:
            print(f"Erro ao realizar pesquisa: {e}")
            return []
    
    def pesquisar_noticias(self, query, max_resultados=5):
        """Pesquisa notícias relacionadas ao termo"""
        try:
            # Como não temos acesso à API de notícias, retornamos links de busca
            data_atual = datetime.now()
            resultados = []
            
            for i in range(max_resultados):
                data = data_atual - timedelta(days=i)
                resultados.append({
                    'title': f'Buscar notícias sobre {query}',
                    'link': f'https://news.google.com/search?q={query}&hl=pt-BR',
                    'source': 'Google News',
                    'date': data.strftime('%Y-%m-%d')
                })
            
            return resultados
            
        except Exception as e:
            print(f"Erro ao pesquisar notícias: {e}")
            return []
