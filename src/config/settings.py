"""
System-wide configuration settings
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Carregar variáveis de ambiente
load_dotenv()

# Configurações das APIs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Configurações de idioma
DEFAULT_LANG = "pt-br"

# Configurações do sistema
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
MAX_RETRIES = 3
CACHE_DIR = Path(__file__).parent.parent / "memory" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DURATION = 3600  # 1 hora em segundos

# Limites de requisições
MAX_SEARCH_RESULTS = 10
MAX_NEWS_RESULTS = 5
MAX_TRENDS_RESULTS = 10
