import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import yfinance as yf
from textblob import TextBlob

# Carregar variáveis de ambiente
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configurar Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Configurar página Streamlit
st.set_page_config(
    page_title="Market Analysis AI",
    page_icon="📊",
    layout="wide"
)

# Cabeçalho e Descrição
st.title("📊 Market Analysis AI")
st.markdown("""
### Bem-vindo ao seu Assistente de Análise de Mercado!

Esta ferramenta combina:
- 📈 **Dados em Tempo Real**: Acesso a informações atualizadas do mercado financeiro
- 🤖 **Inteligência Artificial**: Análises geradas pelo Google Gemini Pro
- 📰 **Análise de Sentimento**: Avaliação do sentimento do mercado sobre diferentes setores

#### Como Usar:
1. **Para Dados de Ações**: 
   - Use símbolos em maiúsculo (ex: "Como está a ação AAPL?" ou "Análise GOOGL")
   - Símbolos populares: AAPL (Apple), GOOGL (Google), MSFT (Microsoft), AMZN (Amazon)

2. **Para Análise Setorial**:
   - Faça perguntas sobre setores específicos (ex: "Como está o setor de tecnologia?")
   - Setores disponíveis: Tecnologia, Varejo, Finanças, Saúde, etc.

#### Exemplos de Perguntas:
- 💼 "Qual a situação atual da AAPL?"
- 📱 "Analise o mercado de tecnologia"
- 🏪 "Como está o setor de varejo?"
- 💰 "Me dê uma análise do setor financeiro"
""")

# Linha divisória
st.markdown("---")

# Inicializar memória de sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_stock_data(symbol: str) -> str:
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
        📊 Dados da ação {symbol}:
        💰 Preço atual: ${current_price}
        📈 Fechamento anterior: ${previous_close}
        📊 Volume: {volume}
        🏢 Market Cap: {market_cap}
        """
    except Exception as e:
        return f"❌ Erro ao obter dados da ação {symbol}: {str(e)}"

def analyze_market_sentiment(query: str) -> str:
    """Analisa o sentimento do mercado baseado em uma consulta."""
    analysis = TextBlob(query)
    sentiment = analysis.sentiment.polarity
    
    if sentiment > 0:
        return f"📈 Sentimento POSITIVO detectado ({sentiment:.2f}). O mercado demonstra otimismo."
    elif sentiment < 0:
        return f"📉 Sentimento NEGATIVO detectado ({sentiment:.2f}). O mercado demonstra cautela."
    else:
        return f"➡️ Sentimento NEUTRO detectado ({sentiment:.2f}). O mercado aparenta estabilidade."

def process_query(query: str) -> str:
    """Processa a query do usuário e retorna uma resposta."""
    
    # Verifica se é uma consulta de ação
    stock_symbols = [word for word in query.split() if word.isupper() and len(word) >= 2]
    if stock_symbols:
        stock_data = get_stock_data(stock_symbols[0])
        context = f"Dados do mercado:\n{stock_data}"
    else:
        # Analisa sentimento do mercado
        sentiment_analysis = analyze_market_sentiment(query)
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
    
    response = model.generate_content(prompt)
    return response.text

# Interface do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("💭 Como posso ajudar com sua análise de mercado?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤔 Analisando o mercado..."):
            response = process_query(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Desenvolvido com ❤️ usando Streamlit e Google Gemini Pro</p>
    <p>Dados fornecidos por Yahoo Finance | Análise de Sentimento por TextBlob</p>
</div>
""", unsafe_allow_html=True)
