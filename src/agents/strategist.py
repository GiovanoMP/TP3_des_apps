"""
Agente Estrategista
Responsável por gerar recomendações estratégicas com base nas análises.
"""
import json
from datetime import datetime

class AgenteEstratego:
    def __init__(self):
        # Estratégias pré-definidas por setor
        self.estrategias_setor = {
            'tecnologia': [
                'Investir em pesquisa e desenvolvimento',
                'Formar parcerias estratégicas',
                'Focar em inovação contínua',
                'Desenvolver propriedade intelectual'
            ],
            'varejo': [
                'Expandir presença online',
                'Melhorar experiência do cliente',
                'Otimizar gestão de estoque',
                'Implementar programa de fidelidade'
            ],
            'servicos': [
                'Padronizar processos',
                'Investir em treinamento',
                'Desenvolver marca forte',
                'Criar pacotes personalizados'
            ]
        }
        
        # Estratégias por região
        self.estrategias_regiao = {
            'sul': [
                'Foco em qualidade premium',
                'Adaptação a mercados maduros',
                'Diferenciação de serviços'
            ],
            'sudeste': [
                'Escala operacional',
                'Competitividade em preços',
                'Marketing intensivo'
            ],
            'nordeste': [
                'Expansão regional',
                'Adaptação local',
                'Parcerias regionais'
            ]
        }

    def gerar_recomendacoes(self, empresa, analise_mercado, analise_swot):
        """Gera recomendações estratégicas baseadas nas análises"""
        try:
            setor = empresa.get('setor', '').lower()
            regiao = empresa.get('regiao', '').lower()
            
            # Obtém estratégias base
            estrategias_base = self.estrategias_setor.get(
                setor, 
                self.estrategias_setor['servicos']
            )
            
            estrategias_regionais = self.estrategias_regiao.get(
                regiao,
                self.estrategias_regiao['sudeste']
            )
            
            # Combina análises para recomendações personalizadas
            recomendacoes = {
                'curto_prazo': self._gerar_recomendacoes_curto_prazo(
                    estrategias_base,
                    analise_swot
                ),
                'medio_prazo': self._gerar_recomendacoes_medio_prazo(
                    estrategias_regionais,
                    analise_mercado
                ),
                'longo_prazo': self._gerar_recomendacoes_longo_prazo(
                    estrategias_base,
                    analise_mercado
                ),
                'prioridades': self._definir_prioridades(
                    analise_swot,
                    analise_mercado
                )
            }
            
            return recomendacoes
            
        except Exception as e:
            return self._gerar_recomendacoes_padrao()
    
    def _gerar_recomendacoes_curto_prazo(self, estrategias_base, analise_swot):
        """Gera recomendações de curto prazo"""
        return [
            f"Implementar: {estrategias_base[0]}",
            f"Fortalecer: {analise_swot['forcas'][0]}",
            f"Mitigar: {analise_swot['fraquezas'][0]}"
        ]
    
    def _gerar_recomendacoes_medio_prazo(self, estrategias_regionais, analise_mercado):
        """Gera recomendações de médio prazo"""
        return [
            f"Desenvolver: {estrategias_regionais[0]}",
            f"Explorar tendência: {analise_mercado['tendencias'][0]}",
            f"Preparar para: {analise_mercado['desafios'][0]}"
        ]
    
    def _gerar_recomendacoes_longo_prazo(self, estrategias_base, analise_mercado):
        """Gera recomendações de longo prazo"""
        return [
            f"Consolidar: {estrategias_base[-1]}",
            f"Posicionar para: {analise_mercado['tendencias'][-1]}",
            "Desenvolver vantagens competitivas sustentáveis"
        ]
    
    def _definir_prioridades(self, analise_swot, analise_mercado):
        """Define prioridades estratégicas"""
        return [
            f"Prioridade 1: Explorar {analise_swot['oportunidades'][0]}",
            f"Prioridade 2: Fortalecer {analise_swot['forcas'][0]}",
            f"Prioridade 3: Preparar para {analise_mercado['tendencias'][0]}"
        ]
    
    def _gerar_recomendacoes_padrao(self):
        """Gera recomendações padrão em caso de erro"""
        return {
            'curto_prazo': [
                'Avaliar posição atual no mercado',
                'Identificar oportunidades imediatas',
                'Otimizar processos existentes'
            ],
            'medio_prazo': [
                'Desenvolver novos produtos/serviços',
                'Expandir base de clientes',
                'Melhorar eficiência operacional'
            ],
            'longo_prazo': [
                'Planejar expansão sustentável',
                'Investir em inovação',
                'Construir vantagens competitivas'
            ],
            'prioridades': [
                'Prioridade 1: Estabilização operacional',
                'Prioridade 2: Crescimento de receita',
                'Prioridade 3: Inovação contínua'
            ]
        }
