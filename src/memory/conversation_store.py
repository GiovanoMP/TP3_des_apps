"""
Sistema de memória conversacional para o agente de chat
"""
from typing import List, Dict
from datetime import datetime

class ConversationMemory:
    def __init__(self, max_history: int = 10):
        self.messages: List[Dict] = []
        self.max_history = max_history
        self.context = {}
    
    def add_message(self, role: str, content: str, metadata: Dict = None):
        """Adiciona uma mensagem ao histórico"""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.messages.append(message)
        
        # Mantém o histórico dentro do limite
        if len(self.messages) > self.max_history:
            self.messages.pop(0)
    
    def get_chat_history(self) -> List[Dict]:
        """Retorna o histórico de mensagens formatado para a OpenAI"""
        return [{'role': msg['role'], 'content': msg['content']} 
                for msg in self.messages]
    
    def get_context_window(self, window_size: int = 5) -> List[Dict]:
        """Retorna as últimas N mensagens do histórico"""
        return self.messages[-window_size:] if self.messages else []
    
    def update_context(self, key: str, value: any):
        """Atualiza o contexto da conversa"""
        self.context[key] = value
    
    def get_context(self, key: str) -> any:
        """Recupera um valor do contexto"""
        return self.context.get(key)
    
    def clear(self):
        """Limpa o histórico de mensagens"""
        self.messages.clear()
        self.context.clear()
