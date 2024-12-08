"""
Ferramenta de Integração OpenAI
Gerencia todas as interações com a API da OpenAI.
"""
from openai import OpenAI
from src.config.settings import OPENAI_API_KEY

class FerramentaOpenAI:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def gerar_conteudo(self, prompt):
        """Gera conteúdo usando OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Erro ao gerar conteúdo: {e}")
            return None
