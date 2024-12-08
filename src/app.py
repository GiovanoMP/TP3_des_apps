"""
Aplicação Streamlit para análise de mercado usando LangChain e ReAct
"""
import streamlit as st
from langchain import OpenAI, LLMChain
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import StreamlitCallbackHandler
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(page_title="Análise de Mercado", layout="wide")

# Título e descrição
st.title("🎯 Análise de Mercado com IA")
st.markdown("""
Este sistema utiliza IA para realizar análises de mercado detalhadas.
- ✨ Framework ReAct para raciocínio e ação
- 🔧 Ferramentas especializadas
- 💭 Memória conversacional
""")

# Verifica a chave da API
if 'OPENAI_API_KEY' not in os.environ:
    st.error("⚠️ OPENAI_API_KEY não encontrada!")
    st.info("Adicione sua chave da API OpenAI no arquivo .env")
    st.stop()

# Inicializa o modelo e as ferramentas
@st.cache_resource
def initialize_chain():
    llm = OpenAI(temperature=0.7)
    
    # Ferramentas disponíveis no LangChain
    tools = load_tools(
        ['serpapi', 'llm-math'],
        llm=llm
    )
    
    # Memória conversacional
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Inicializa o agente com ReAct
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )
    
    return agent

# Interface principal
def main():
    # Inicializa o histórico se não existir
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Exibe mensagens anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Campo de entrada do usuário
    if prompt := st.chat_input("Faça uma pergunta sobre análise de mercado..."):
        # Adiciona a mensagem do usuário ao chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        try:
            # Inicializa o agente
            agent = initialize_chain()
            
            # Processa a resposta com callback do Streamlit
            with st.chat_message("assistant"):
                st_callback = StreamlitCallbackHandler(st.container())
                response = agent.run(prompt, callbacks=[st_callback])
                st.markdown(response)
                
                # Adiciona a resposta ao histórico
                st.session_state.messages.append({"role": "assistant", "content": response})
                
        except Exception as e:
            st.error(f"Erro: {str(e)}")
            if "API key" in str(e):
                st.info("Verifique se sua chave da API OpenAI está configurada corretamente no arquivo .env")

if __name__ == "__main__":
    main()
