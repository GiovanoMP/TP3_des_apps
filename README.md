# Market Analysis AI

[Visite o aplicativo](https://tp3desapps-un55mfy9dhtqvtfdubxvsh.streamlit.app/)


Uma ferramenta de análise de mercado alimentada por IA que combina dados em tempo real do mercado financeiro com análise de sentimento e processamento de linguagem natural.

## Características

- **Dados em Tempo Real**: Acesso a informações atualizadas do mercado financeiro via Yahoo Finance
- **IA Avançada**: Análises geradas pelo Google Gemini Pro
- **Análise de Sentimento**: Avaliação do sentimento do mercado sobre diferentes setores
- **Interface Conversacional**: Interface amigável baseada em chat para interações naturais
- **Visualização de Dados**: Apresentação clara e organizada de informações financeiras

## Começando

### Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Chave API do Google (para o Gemini Pro)

### Instalação

1. Clone o repositório:
   ```bash
   git clone [URL_DO_REPOSITÓRIO]
   cd [NOME_DO_DIRETÓRIO]
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave API do Google:
     ```
     GOOGLE_API_KEY=sua_chave_api_aqui
     ```

4. Execute a aplicação:
   ```bash
   streamlit run app.py
   ```

## Como Usar

### Consultas de Ações
- Use símbolos em maiúsculo para consultar ações específicas
- Exemplo: "Como está a ação AAPL?"
- Símbolos populares:
  - AAPL (Apple)
  - GOOGL (Google)
  - MSFT (Microsoft)
  - AMZN (Amazon)

### Análise Setorial
- Faça perguntas sobre setores específicos
- Exemplo: "Como está o setor de tecnologia?"
- Setores disponíveis:
  - Tecnologia
  - Varejo
  - Finanças
  - Saúde
  - E outros

### Exemplos de Perguntas
- "Qual a situação atual da AAPL?"
- "Analise o mercado de tecnologia"
- "Como está o setor de varejo?"
- "Me dê uma análise do setor financeiro"

## Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)**: Framework para criação da interface web
- **[Google Gemini Pro](https://ai.google.dev/)**: Motor de IA para análise e geração de respostas
- **[Yahoo Finance](https://finance.yahoo.com/)**: API para dados financeiros em tempo real
- **[TextBlob](https://textblob.readthedocs.io/)**: Biblioteca para análise de sentimento
- **[Python-dotenv](https://github.com/theskumar/python-dotenv)**: Gerenciamento de variáveis de ambiente

## Estrutura do Projeto

```
.
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências do projeto
├── .env               # Variáveis de ambiente
└── README.md          # Documentação
```

## Dependências

As principais dependências do projeto são:
- streamlit==1.29.0
- google-generativeai==0.3.1
- python-dotenv==1.0.0
- yfinance==0.2.33
- textblob==0.17.1

## Segurança

- Nunca compartilhe sua chave API do Google
- Mantenha o arquivo `.env` no `.gitignore`
- Revise regularmente as permissões de acesso

## Contribuindo

Contribuições são bem-vindas! Por favor, siga estes passos:

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Agradecimentos

- Google pela API do Gemini Pro
- Yahoo Finance pelos dados do mercado
- Comunidade Streamlit pelo excelente framework

## Contato

Para questões e sugestões, por favor abra uma issue no repositório do projeto.

---


