import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from src.agents.coordinator import CoordinatorAgent
from src.agents.strategist import AgenteEstrategista

def inicializar_sessao():
    """Inicializa variáveis de sessão"""
    if 'coordenador' not in st.session_state:
        st.session_state.coordenador = CoordinatorAgent()
    if 'estrategista' not in st.session_state:
        st.session_state.estrategista = AgenteEstrategista()
    if 'resultados_analise' not in st.session_state:
        st.session_state.resultados_analise = None

def exibir_analise_textual(analise):
    """Exibe a análise textual de forma organizada"""
    # Análise Setorial
    st.write("## Análise Setorial")
    st.write(analise['analise_setor'])
    
    # Análise Geral
    st.write("## Análise Geral")
    
    # Posicionamento
    st.write("### Posicionamento")
    st.write(analise['analise_geral']['posicionamento'])
    
    # Mercado
    st.write("### Análise de Mercado")
    st.write(analise['analise_geral']['mercado'])
    
    # Competitividade
    st.write("### Análise de Competitividade")
    st.write(analise['analise_geral']['competitividade'])
    
    # Recomendações
    st.write("## Recomendações Estratégicas")
    st.write(analise['recomendacoes'])

def main():
    st.title("Ferramenta de Análise Estratégica de Marketing")
    
    # Inicializa a sessão
    inicializar_sessao()
    
    # Interface do usuário
    st.write("""
    ### Sobre a Ferramenta
    Esta ferramenta realiza uma análise estratégica completa da sua empresa, 
    considerando aspectos como posicionamento, mercado, competitividade e tendências.
    
    Por favor, preencha o formulário abaixo com informações sobre sua empresa:
    """)
    
    with st.form("analise_form"):
        # Dados básicos
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome da Empresa")
            setor = st.selectbox("Setor de Atuação", 
                               ['Varejo', 'Tecnologia', 'Serviços', 'Indústria'])
            tamanho = st.selectbox("Porte da Empresa",
                                 ['Pequena', 'Média', 'Grande'])
        
        with col2:
            regiao = st.text_input("Região de Atuação")
            st.write("### Público-Alvo")
            st.write("""
            Selecione as características que melhor descrevem seu público-alvo:
            """)
            
            # Faixa Etária
            faixa_etaria = st.multiselect(
                "Faixa Etária",
                ['18-24 anos', '25-34 anos', '35-44 anos', '45-54 anos', '55+ anos'],
                help="Selecione uma ou mais faixas etárias"
            )
            
            # Classe Social
            classe_social = st.multiselect(
                "Classe Social",
                ['A', 'B', 'C', 'D', 'E'],
                help="Selecione uma ou mais classes sociais"
            )
            
            # Comportamento
            comportamento = st.multiselect(
                "Comportamento de Consumo",
                [
                    'Busca qualidade', 
                    'Sensível a preço',
                    'Valoriza conveniência',
                    'Focado em tecnologia',
                    'Preocupado com sustentabilidade',
                    'Busca status',
                    'Valoriza experiências',
                    'Compra por impulso',
                    'Pesquisa muito antes de comprar'
                ],
                help="Selecione características comportamentais"
            )
            
            # Outros aspectos específicos
            outros_aspectos = st.text_area(
                "Outros Aspectos Específicos (opcional)",
                help="Adicione outras características específicas do seu público-alvo"
            )
            
            # Consolida informações do público-alvo
            publico_alvo = {
                'faixa_etaria': faixa_etaria,
                'classe_social': classe_social,
                'comportamento': comportamento,
                'outros_aspectos': outros_aspectos
            }
        
        # Diferenciais
        st.write("### Diferenciais Competitivos")
        st.write("Liste os principais diferenciais da sua empresa:")
        diferencial1 = st.text_input("Diferencial 1")
        diferencial2 = st.text_input("Diferencial 2")
        diferencial3 = st.text_input("Diferencial 3")
        
        # Desafios
        st.write("### Desafios")
        st.write("Liste os principais desafios enfrentados:")
        desafio1 = st.text_input("Desafio 1")
        desafio2 = st.text_input("Desafio 2")
        desafio3 = st.text_input("Desafio 3")
        
        # Botão de submissão
        submitted = st.form_submit_button("Realizar Análise")
    
    if submitted:
        # Prepara os dados
        dados_empresa = {
            'nome': nome,
            'setor': setor,
            'tamanho': tamanho.lower(),
            'regiao': regiao,
            'publico_alvo': publico_alvo,  # Agora é um dicionário com informações detalhadas
            'diferenciais': [d for d in [diferencial1, diferencial2, diferencial3] if d],
            'desafios': [d for d in [desafio1, desafio2, desafio3] if d]
        }
        
        # Valida dados obrigatórios
        campos_vazios = [campo for campo, valor in dados_empresa.items() 
                        if not valor and campo not in ['diferenciais', 'desafios']]
        
        if campos_vazios:
            st.error(f"Por favor, preencha os seguintes campos: {', '.join(campos_vazios)}")
            return
        
        with st.spinner("Realizando análise estratégica..."):
            try:
                # Realiza a análise
                analise = st.session_state.estrategista.analisar_empresa(dados_empresa)
                st.session_state.resultados_analise = analise
                
                if analise:
                    # Exibe os resultados
                    st.success("Análise concluída com sucesso!")
                    exibir_analise_textual(analise)
                    
                    # Opção para download do relatório
                    st.download_button(
                        label="Baixar Relatório Completo",
                        data=str(analise),
                        file_name=f"analise_{nome.lower().replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("Não foi possível realizar a análise completa. Tente novamente.")
                
            except Exception as e:
                st.error(f"Ocorreu um erro durante a análise: {str(e)}")

if __name__ == "__main__":
    main()
