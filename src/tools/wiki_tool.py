"""
Ferramenta de Busca de Informações
Gerencia buscas de informações usando APIs públicas.
"""
import requests
import json

class FerramentaBusca:
    def __init__(self, idioma='pt-br'):
        self.idioma = idioma
        self.base_url = "https://api.bing.microsoft.com/v7.0/search"
        # Fallback para uma API pública que não requer autenticação
        self.fallback_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
    
    def buscar_pagina(self, termo):
        """Busca informações sobre um termo"""
        try:
            # Tenta usar a API da Wikipedia como fallback
            # Remove espaços e caracteres especiais
            termo_formatado = termo.replace(" ", "_").lower()
            response = requests.get(f"{self.fallback_url}{termo_formatado}")
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'titulo': data.get('title', termo),
                    'sumario': data.get('extract', 'Informação não disponível'),
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', '')
                }
            
            # Se não encontrar, retorna um resultado genérico
            return {
                'titulo': termo,
                'sumario': 'Não foi possível encontrar informações detalhadas.',
                'url': f'https://www.google.com/search?q={termo}'
            }
            
        except Exception as e:
            print(f"Erro ao buscar informações: {str(e)}")
            return None
    
    def obter_referencias(self, termo):
        """Obtém links relacionados ao termo"""
        try:
            # Como fallback, retorna links genéricos de busca
            return [
                f'https://www.google.com/search?q={termo}',
                f'https://www.bing.com/search?q={termo}',
                f'https://duckduckgo.com/?q={termo}'
            ]
        except Exception as e:
            print(f"Erro ao obter referências: {str(e)}")
            return []
