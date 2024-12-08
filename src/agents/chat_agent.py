"""
Agente de Chat com framework ReAct
Implementa um agente conversacional que utiliza o framework ReAct para raciocínio interativo
"""
import os
from openai import OpenAI
from typing import Dict, List, Optional
from ..memory.conversation_store import ConversationMemory

class AgenteChatBot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.memory = ConversationMemory()
        
        # Ferramentas disponíveis para o agente
        self.tools = {
            'consultar_analise': self._consultar_analise,
            'buscar_recomendacoes': self._buscar_recomendacoes,
            'analisar_mercado': self._analisar_mercado
        }
        
        # Prompt base para o sistema
        self.system_prompt = """Você é um assistente especializado em análise de mercado e estratégia empresarial.
        Utilize o framework ReAct (Reasoning + Acting) para:
        1. Raciocinar sobre a pergunta do usuário
        2. Decidir qual ação tomar
        3. Observar os resultados
        4. Continuar o raciocínio até chegar a uma resposta satisfatória
        
        Ferramentas disponíveis:
        - consultar_analise: Busca informações da análise atual
        - buscar_recomendacoes: Obtém recomendações específicas
        - analisar_mercado: Realiza uma análise pontual do mercado
        
        Mantenha suas respostas profissionais e focadas no contexto empresarial."""
    
    def process_message(self, user_message: str, context: Dict = None) -> str:
        """Processa uma mensagem do usuário usando o framework ReAct"""
        try:
            # Atualiza o contexto se fornecido
            if context:
                for key, value in context.items():
                    self.memory.update_context(key, value)
            
            # Adiciona a mensagem do usuário ao histórico
            self.memory.add_message("user", user_message)
            
            # Prepara o histórico para o prompt
            messages = [
                {"role": "system", "content": self.system_prompt}
            ] + self.memory.get_chat_history()
            
            # Gera a resposta usando o GPT-4
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            # Processa a resposta
            assistant_message = response.choices[0].message.content
            
            # Implementa o ciclo ReAct
            if self._should_use_tool(assistant_message):
                # Extrai a ação a ser tomada
                tool_name, tool_input = self._extract_tool_call(assistant_message)
                
                # Executa a ação
                if tool_name in self.tools:
                    tool_result = self.tools[tool_name](tool_input)
                    
                    # Adiciona o resultado ao contexto
                    self.memory.add_message(
                        "system",
                        f"Resultado da ação {tool_name}: {tool_result}"
                    )
                    
                    # Gera uma nova resposta considerando o resultado
                    return self.process_message(
                        f"Com base no resultado {tool_result}, como você responderia: {user_message}"
                    )
            
            # Adiciona a resposta ao histórico
            self.memory.add_message("assistant", assistant_message)
            
            return assistant_message
            
        except Exception as e:
            print(f"Erro no processamento da mensagem: {str(e)}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem. Pode tentar novamente?"
    
    def _should_use_tool(self, message: str) -> bool:
        """Determina se deve usar uma ferramenta com base na mensagem"""
        tool_indicators = [
            "preciso consultar",
            "vou analisar",
            "deixe-me verificar",
            "necessito buscar"
        ]
        return any(indicator in message.lower() for indicator in tool_indicators)
    
    def _extract_tool_call(self, message: str) -> tuple:
        """Extrai qual ferramenta usar e seus parâmetros"""
        # Implementação simplificada - em produção, usar NLP mais robusto
        for tool_name in self.tools.keys():
            if tool_name in message.lower():
                # Extrai o contexto após o nome da ferramenta
                context = message[message.lower().find(tool_name) + len(tool_name):]
                return tool_name, context.strip()
        return None, None
    
    def _consultar_analise(self, context: str) -> str:
        """Consulta a análise atual da empresa"""
        analise = self.memory.get_context('analise_mercado')
        if not analise:
            return "Análise não disponível no momento."
        return str(analise)
    
    def _buscar_recomendacoes(self, context: str) -> str:
        """Busca recomendações específicas"""
        recomendacoes = self.memory.get_context('recomendacoes')
        if not recomendacoes:
            return "Recomendações não disponíveis no momento."
        return str(recomendacoes)
    
    def _analisar_mercado(self, context: str) -> str:
        """Realiza uma análise pontual do mercado"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um analista de mercado especializado."},
                    {"role": "user", "content": f"Faça uma análise pontual sobre: {context}"}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erro na análise: {str(e)}"
