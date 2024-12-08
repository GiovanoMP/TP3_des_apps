from langchain.tools import BaseTool
from textblob import TextBlob
import requests
from typing import Optional

class NewsAnalyzerTool(BaseTool):
    name = "news_analyzer"
    description = "Analisa o sentimento de notícias sobre empresas ou mercados"

    def _run(self, query: str) -> str:
        try:
            # Simula busca de notícias (em produção, usaríamos uma API real de notícias)
            news_data = {
                "tecnologia": [
                    "Empresas de IA registram crescimento exponencial",
                    "Startups de tecnologia enfrentam desafios de financiamento",
                ],
                "varejo": [
                    "E-commerce continua em expansão no mercado brasileiro",
                    "Lojas físicas se adaptam ao novo cenário digital",
                ],
                "servicos": [
                    "Setor de serviços mostra recuperação pós-pandemia",
                    "Empresas investem em transformação digital",
                ]
            }
            
            # Pega notícias relevantes
            relevant_news = []
            for sector, news_list in news_data.items():
                if sector.lower() in query.lower():
                    relevant_news.extend(news_list)
            
            if not relevant_news:
                return "Nenhuma notícia encontrada para o setor especificado."
            
            # Analisa sentimento
            sentiments = []
            for news in relevant_news:
                analysis = TextBlob(news)
                sentiment = "positivo" if analysis.sentiment.polarity > 0 else "negativo" if analysis.sentiment.polarity < 0 else "neutro"
                sentiments.append(f"- {news}\n  Sentimento: {sentiment}")
            
            return "Análise de Notícias:\n" + "\n".join(sentiments)
            
        except Exception as e:
            return f"Erro na análise de notícias: {str(e)}"

    def _arun(self, query: str):
        raise NotImplementedError("Async não implementado")
