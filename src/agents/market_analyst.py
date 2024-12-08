"""
Agente Analista de Mercado
Responsável por analisar dados de mercado e gerar insights estratégicos usando IA.
"""
import os
import google.generativeai as genai
from typing import List, Dict
import json
import yfinance as yf
from textblob import TextBlob

class AgenteAnalistaMercado:
    def __init__(self, google_api_key: str):
        # Configurar o modelo Gemini
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def get_stock_data(self, symbol: str) -> str:
        """Obtém dados em tempo real de ações."""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            current_price = info.get('currentPrice', 'N/A')
            previous_close = info.get('previousClose', 'N/A')
            volume = info.get('volume', 'N/A')
            market_cap = info.get('marketCap', 'N/A')
            if market_cap != 'N/A':
                market_cap = f"${market_cap/1000000000:.2f}B"
            
            return f"""
            Dados da ação {symbol}:
            Preço atual: ${current_price}
            Fechamento anterior: ${previous_close}
            Volume: {volume}
            Market Cap: {market_cap}
            """
        except Exception as e:
            return f"Erro ao obter dados da ação {symbol}: {str(e)}"

    def analyze_market_sentiment(self, query: str) -> str:
        """Analisa o sentimento do mercado baseado em uma consulta."""
        analysis = TextBlob(query)
        sentiment = analysis.sentiment.polarity
        
        if sentiment > 0:
            return f"Sentimento POSITIVO detectado ({sentiment:.2f}). O mercado demonstra otimismo."
        elif sentiment < 0:
            return f"Sentimento NEGATIVO detectado ({sentiment:.2f}). O mercado demonstra cautela."
        else:
            return f"Sentimento NEUTRO detectado ({sentiment:.2f}). O mercado aparenta estabilidade."

    def process_query(self, query: str) -> str:
        """Processa a query do usuário e retorna uma resposta."""
        
        # Verifica se é uma consulta de ação
        stock_symbols = [word for word in query.split() if word.isupper() and len(word) >= 2]
        if stock_symbols:
            stock_data = self.get_stock_data(stock_symbols[0])
            context = f"Dados do mercado:\n{stock_data}"
        else:
            # Analisa sentimento do mercado
            sentiment_analysis = self.analyze_market_sentiment(query)
            context = f"Análise de sentimento:\n{sentiment_analysis}"
        
        # Gera resposta com o Gemini
        prompt = f"""
        Como analista de mercado especializado, responda à seguinte pergunta:
        {query}
        
        Use estas informações como contexto:
        {context}
        
        Forneça uma análise detalhada e profissional, incluindo:
        1. Interpretação dos dados/sentimento
        2. Possíveis implicações
        3. Contexto do mercado atual
        
        Use uma linguagem clara e profissional.
        """
        
        response = self.model.generate_content(prompt)
        return response.text

def main():
    # Exemplo de uso
    api_key = os.getenv("GOOGLE_API_KEY")
    agent = AgenteAnalistaMercado(api_key)
    response = agent.process_query("Como está o mercado de tecnologia?")
    print(response)

if __name__ == "__main__":
    main()
