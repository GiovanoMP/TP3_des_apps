"""
Coordenador dos agentes de análise
Responsável por orquestrar o fluxo de análise entre os agentes
"""
from .market_analyst import AgenteAnalistaMercado
from .strategist import AgenteEstratego
from .chat_agent import AgenteChatBot

class Coordenador:
    def __init__(self):
        self.analista = AgenteAnalistaMercado()
        self.estrategista = AgenteEstratego()
        self.chatbot = AgenteChatBot()
        self.ultima_analise = None
    
    def analisar_empresa(self, dados_empresa):
        """Coordena a análise completa da empresa"""
        try:
            # Validação básica dos dados
            if not self._validar_dados(dados_empresa):
                return None
            
            # Análise de mercado
            analise_mercado = self.analista.analisar_mercado(dados_empresa)
            if not analise_mercado:
                return None
            
            # Análise SWOT
            swot = self.analista.gerar_analise_swot(dados_empresa, analise_mercado)
            if not swot:
                return None
            
            # Recomendações estratégicas
            recomendacoes = self.estrategista.gerar_recomendacoes(
                dados_empresa,
                analise_mercado,
                swot
            )
            
            if not recomendacoes:
                return None
            
            # Armazena a última análise para o chat
            self.ultima_analise = {
                'dados_empresa': dados_empresa,
                'analise_mercado': analise_mercado,
                'swot': swot,
                'recomendacoes': recomendacoes
            }
            
            # Atualiza o contexto do chatbot
            self.chatbot.memory.update_context('analise_mercado', analise_mercado)
            self.chatbot.memory.update_context('swot', swot)
            self.chatbot.memory.update_context('recomendacoes', recomendacoes)
            self.chatbot.memory.update_context('dados_empresa', dados_empresa)
            
            # Retorna resultado completo
            return self.ultima_analise
        
        except Exception as e:
            print(f"Erro na coordenação: {str(e)}")
            return None
    
    def processar_mensagem_chat(self, mensagem: str) -> str:
        """Processa uma mensagem para o chatbot"""
        if not self.ultima_analise:
            return "Por favor, realize uma análise primeiro antes de usar o chat."
        
        return self.chatbot.process_message(mensagem)
    
    def _validar_dados(self, dados):
        """Validação básica dos dados de entrada"""
        campos_obrigatorios = ['nome', 'setor', 'tamanho', 'regiao']
        
        try:
            # Verifica campos obrigatórios
            if not all(campo in dados for campo in campos_obrigatorios):
                return False
            
            # Verifica se há valores vazios
            if any(not dados[campo] for campo in campos_obrigatorios):
                return False
            
            # Verifica listas
            if not isinstance(dados.get('diferenciais', []), (list, tuple)):
                return False
            
            if not isinstance(dados.get('desafios', []), (list, tuple)):
                return False
            
            return True
            
        except Exception as e:
            print(f"Erro na validação: {str(e)}")
            return False
