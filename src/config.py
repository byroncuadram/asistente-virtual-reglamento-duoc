import os
from dotenv import load_dotenv

# Cargamos las variables de entorno desde el archivo .env (API Keys, etc.)
load_dotenv()

# Credenciales de API para Mistral AI
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Definición de rutas absolutas/relativas del proyecto para mantener orden modular
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "reglamento_academico_duoc_uc_2026.csv")
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")