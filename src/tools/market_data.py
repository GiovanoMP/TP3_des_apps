from langchain.tools import BaseTool
import yfinance as yf
from typing import Optional

class StockDataTool(BaseTool):
    name = "stock_data"
    description = "Obtém dados de ações em tempo real usando o Yahoo Finance"

    def _run(self, symbol: str) -> str:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            return f"""
            Dados da ação {symbol}:
            Preço atual: ${info.get('currentPrice', 'N/A')}
            Volume: {info.get('volume', 'N/A')}
            Setor: {info.get('sector', 'N/A')}
            Indústria: {info.get('industry', 'N/A')}
            """
        except Exception as e:
            return f"Erro ao buscar dados da ação {symbol}: {str(e)}"

    def _arun(self, symbol: str):
        raise NotImplementedError("Async não implementado")
