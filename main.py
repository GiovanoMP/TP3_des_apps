"""
ContentCraft AI - Ponto de Entrada Principal da Aplicação
"""
from src.agents.coordinator import CoordinatorAgent
from src.interface.app import main as app_main

def inicializar_sistema():
    """Inicializa todos os componentes necessários"""
    coordenador = CoordinatorAgent()
    return coordenador

def main():
    """Ponto de entrada principal para o sistema ContentCraft AI"""
    # Inicializa o sistema
    coordenador = inicializar_sistema()
    
    # Inicia a interface Streamlit
    app_main()

if __name__ == "__main__":
    import os
    import streamlit as st
    from dotenv import load_dotenv
    from langchain.agents import Tool, AgentType, initialize_agent
    from langchain.memory import ConversationBufferMemory
    from langchain.chat_models import ChatOpenAI
    import json

    # Carrega variáveis de ambiente
    load_dotenv()

    # Configuração da página
    st.set_page_config(
        page_title="Análise de Mercado",
        page_icon="📊",
        layout="wide"
    )

    # Verifica a chave da API
    if 'OPENAI_API_KEY' not in os.environ:
        st.error("⚠️ OPENAI_API_KEY não encontrada!")
        st.info("Por favor, configure sua chave da API OpenAI no arquivo .env")
        st.stop()

    # Dados de exemplo
    MARKET_DATA = {
        "Tecnologia": {
            "tamanho": "US$ 5.2 trilhões",
            "crescimento": "5.4% ao ano",
            "tendencias": ["IA", "Cloud Computing", "IoT"],
            "desafios": ["Regulamentações", "Segurança"]
        },
        "Varejo": {
            "tamanho": "US$ 25 trilhões",
            "crescimento": "4.8% ao ano",
            "tendencias": ["E-commerce", "Omnichannel"],
            "desafios": ["Logística", "Concorrência"]
        },
        "Serviços": {
            "tamanho": "US$ 6.8 trilhões",
            "crescimento": "3.9% ao ano",
            "tendencias": ["Digitalização", "Automação"],
            "desafios": ["Qualificação", "Adaptação"]
        }
    }

    def pesquisar_mercado(setor: str) -> str:
        """Pesquisa informações sobre um setor de mercado"""
        return json.dumps(MARKET_DATA.get(setor, {}), ensure_ascii=False)

    def analisar_competidores(setor: str) -> str:
        """Analisa os competidores de um setor"""
        competidores = {
            "Tecnologia": [
                {"nome": "Tech A", "participacao": "15%"},
                {"nome": "Tech B", "participacao": "12%"}
            ],
            "Varejo": [
                {"nome": "Mega Store", "participacao": "20%"},
                {"nome": "Shop Corp", "participacao": "18%"}
            ],
            "Serviços": [
                {"nome": "Service Pro", "participacao": "10%"},
                {"nome": "Consult Corp", "participacao": "8%"}
            ]
        }
        return json.dumps(competidores.get(setor, []), ensure_ascii=False)

    @st.cache_resource
    def criar_agente():
        """Cria e retorna um agente de análise de mercado"""
        # Configura o modelo
        llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-3.5-turbo"
        )
        
        # Define as ferramentas
        tools = [
            Tool(
                name="PesquisarMercado",
                func=pesquisar_mercado,
                description="Pesquisa informações sobre um setor de mercado específico. Input deve ser o nome do setor (Tecnologia, Varejo ou Serviços)."
            ),
            Tool(
                name="AnalisarCompetidores",
                func=analisar_competidores,
                description="Analisa os principais competidores de um setor específico. Input deve ser o nome do setor (Tecnologia, Varejo ou Serviços)."
            )
        ]
        
        # Configura a memória
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Cria o agente
        return initialize_agent(
            tools,
            llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=memory,
            verbose=True
        )

    def main():
        st.title("🤖 Assistente de Análise de Mercado")
        
        # Descrição do sistema
        st.markdown("""
        Este assistente usa LangChain e o framework ReAct para realizar análises de mercado.
        Ele pode:
        - Pesquisar informações sobre diferentes setores
        - Analisar competidores
        - Fornecer insights estratégicos
        """)
        
        # Inicializa o histórico de chat
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Exibe mensagens anteriores
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Campo de entrada do usuário
        if prompt := st.chat_input("Faça uma pergunta sobre o mercado..."):
            # Adiciona a pergunta do usuário ao chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Processa a resposta do agente
            with st.chat_message("assistant"):
                with st.spinner("Analisando..."):
                    agent = criar_agente()
                    try:
                        response = agent.run(input=prompt)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

    main()
