"""
Agente Analista de Mercado
Responsável por analisar dados de mercado e gerar insights estratégicos usando IA.
"""
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain.tools import Tool
from typing import List, Dict
import json

class MarketAnalystAgent:
    def __init__(self, openai_api_key: str):
        # Inicializa o modelo de linguagem
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-3.5-turbo",
            openai_api_key=openai_api_key
        )
        
        # Configura a memória
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Define as ferramentas
        self.tools = [
            Tool(
                name="market_research",
                func=self._market_research,
                description="Realiza pesquisa de mercado para um setor específico. Input deve ser o nome do setor."
            ),
            Tool(
                name="competitor_analysis",
                func=self._competitor_analysis,
                description="Analisa os principais competidores do setor. Input deve ser o nome do setor."
            )
        ]
        
        # Define o prompt do sistema
        system_message = SystemMessage(
            content="""Você é um analista de mercado especializado que ajuda a analisar mercados e competidores.
            Use as ferramentas disponíveis para fornecer insights precisos e úteis.
            Sempre explique seu raciocínio antes de usar uma ferramenta."""
        )
        
        # Cria o agente
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            system_message=system_message
        )
        
        # Cria o executor do agente
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def _market_research(self, sector: str) -> str:
        """Ferramenta para realizar pesquisa de mercado"""
        market_data = {
            "Tecnologia": {
                "market_size": "US$ 5.2 trilhões globalmente",
                "growth_rate": "5.4% ao ano",
                "trends": ["IA", "Cloud Computing", "IoT"],
                "challenges": ["Regulamentações", "Segurança Cibernética"]
            },
            "Varejo": {
                "market_size": "US$ 25 trilhões globalmente",
                "growth_rate": "4.8% ao ano",
                "trends": ["E-commerce", "Omnichannel", "Personalização"],
                "challenges": ["Logística", "Concorrência Online"]
            },
            "Serviços": {
                "market_size": "US$ 6.8 trilhões globalmente",
                "growth_rate": "3.9% ao ano",
                "trends": ["Digitalização", "Automação", "Experiência do Cliente"],
                "challenges": ["Qualificação Profissional", "Adaptação Digital"]
            }
        }
        return json.dumps(market_data.get(sector, {}), ensure_ascii=False)
    
    def _competitor_analysis(self, sector: str) -> str:
        """Ferramenta para análise de competidores"""
        competitor_data = {
            "Tecnologia": [
                {"name": "Big Tech A", "market_share": "15%", "strengths": ["Inovação", "Capital"]},
                {"name": "Tech Corp B", "market_share": "12%", "strengths": ["Alcance Global", "P&D"]}
            ],
            "Varejo": [
                {"name": "Mega Store", "market_share": "20%", "strengths": ["Preço", "Logística"]},
                {"name": "Shop Corp", "market_share": "18%", "strengths": ["Marca", "Localização"]}
            ],
            "Serviços": [
                {"name": "Service Pro", "market_share": "10%", "strengths": ["Qualidade", "Reputação"]},
                {"name": "Consult Corp", "market_share": "8%", "strengths": ["Expertise", "Network"]}
            ]
        }
        return json.dumps(competitor_data.get(sector, []), ensure_ascii=False)
    
    def analyze(self, query: str) -> str:
        """Processa uma consulta do usuário usando o framework ReAct"""
        try:
            response = self.agent_executor.invoke({"input": query})
            return response["output"]
        except Exception as e:
            return f"Erro na análise: {str(e)}"

def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY não encontrada. Configure a variável de ambiente.")
    
    agent = MarketAnalystAgent(openai_api_key)
    query = "Qual é o tamanho do mercado de tecnologia?"
    response = agent.analyze(query)
    print(response)

if __name__ == "__main__":
    main()
