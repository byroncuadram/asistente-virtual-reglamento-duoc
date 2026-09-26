# Asistente Virtual con RAG y Memoria - Reglamento Duoc UC

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Framework](https://img.shields.io/badge/LangChain-LCEL-green.svg)
![LLM Provider](https://img.shields.io/badge/Mistral%20AI-API-orange.svg)
![Vector DB](https://img.shields.io/badge/ChromaDB-v0.5%2B-purple.svg)

Prototipo de asistente conversacional inteligente basado en arquitectura **RAG (*Retrieval-Augmented Generation*)** para la orientación y consulta interactiva del Reglamento Académico Institucional de Duoc UC. 

El sistema implementa procesamiento de lenguaje natural con **LangChain Expression Language (LCEL)**, embeddings de alta densidad, base de datos vectorial local con **ChromaDB**, soporte de memoria conversacional y restricciones estrictas de extensión (máximo 300 caracteres por respuesta) para evitar alucinaciones normativas.

---

## 🏛️ Arquitectura del Sistema

El proyecto está diseñado bajo una arquitectura modular en 3 capas bien delimitadas:

```text
AsistenteVirtual/
├── data/
│   └── reglamento.csv         # Fuente de datos normativos
├── src/
│   ├── __init__.py
│   ├── config.py              # Gestión de credenciales y rutas (.env)
│   ├── database.py            # Carga del CSV, embeddings e indexación ChromaDB
│   └── rag_chain.py           # Pipeline RAG conversacional en LCEL con Mistral
├── .env                       # Credenciales de entorno (no subir al repositorio)
├── .gitignore
├── main.py                    # Interfaz de usuario interactiva por consola (CLI)
├── README.md                  # Documentación técnica e instrucciones de uso
└── requirements.txt           # Lista de dependencias del proyecto

Requisitos Previos

Python: Versión >= 3.10 y < 3.14.

API Key: Una clave activa de Mistral AI (Obtener clave en Mistral La Plateforme).

Terminal/CLI: PowerShell, Bash o Zsh.

Instalación y Configuración
Sigue estos pasos para desplegar y ejecutar el proyecto en tu entorno local:

1. Clonar el Repositorio
Bash
git clone [https://github.com/tu-usuario/AsistenteVirtual-DuocUC.git](https://github.com/tu-usuario/AsistenteVirtual-DuocUC.git)
cd AsistenteVirtual-DuocUC

2. Crear y Activar el Entorno Virtual
En Windows (PowerShell):

PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

En Linux / macOS:

Bash
python3 -m venv .venv
source .venv/bin/activate

3. Instalar Dependencias
Asegúrate de actualizar pip e instalar los paquetes desde el archivo requirements.txt:

Bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

🔑 Configuración de Variables de Entorno
Crea un archivo llamado .env en la raíz del proyecto (al mismo nivel que main.py) con el siguiente contenido:

Fragmento de código
LLM_BASE_URL="https://api.mistral.ai/v1"
# Clave API oficial de Mistral AI
MISTRAL_API_KEY=tu_api_key_aqui
LLM_MODEL="mistral-small-latest"
LLM_MODEL_SMALL="ministral-8b-latest"

⚠️ Nota de seguridad: Nunca subas el archivo .env a tu repositorio público. Asegúrate de que esté incluido en tu .gitignore.

Lista de Dependencias (requirements.txt)
El proyecto utiliza un conjunto optimizado de dependencias alineado con las últimas versiones de LangChain Core (v0.3+) para evitar conflictos de bibliotecas o rutas descontinuadas (legacy):

Plaintext
# Dependencias — Ingeniería de Soluciones con IA
# Instalación local:  pip install -r requirements.txt
# En Google Colab:     !pip install -q -r requirements.txt
#
# ⚠️ Requiere Python >=3.10.

# --- Núcleo LLM / LangChain (Sintaxis LCEL Nativa) -------------------
langchain>=0.3.0
langchain-core>=0.3.0
langchain-community>=0.3.0

# --- Proveedor LLM y Embeddings (Mistral AI) --------------------------
langchain-mistralai>=0.2.0

# --- Base de Datos Vectorial RAG --------------------------------------
chromadb>=0.5.0

# --- Datos y Utilidades -----------------------------------------------
pandas>=2.0.0
python-dotenv>=1.0.0

Ejecución del Sistema
Para iniciar la consola conversacional interactiva, ejecuta el archivo principal:

Bash
python main.py

Flujo de Uso

El sistema inicializará o cargará la base de datos vectorial local en chroma_db/.

Se cargará el pipeline RAG orquestado con ChatMistralAI (open-mistral-7b).

Podrás realizar consultas sobre causales de eliminación, convalidaciones, asistencias, notas, etc.

El sistema mantendrá la memoria del diálogo para responder a preguntas de seguimiento anafóricas.

Para finalizar la sesión, escribe salir, exit o quit.

Ejemplo de Prueba e Interacción
Plaintext
==================================================
  ASISTENTE VIRTUAL DUOC UC (CON MEMORIA RAG)    
==================================================

Inicializando base de datos vectorial...
Cargando modelo RAG con memoria...

¡Sistema listo con memoria conversacional! Escribe 'salir' para terminar.

👤 Estudiante: ¿Cuántas veces puedo reprobar una misma asignatura?
🤖 Procesando con historial y RAG...

--- RESPUESTA OBTENIDA ---
Según el Reglamento Académico de Duoc UC, puedes reprobar una asignatura hasta en 2 oportunidades. Reprobar la misma asignatura por tercera vez constituye una causal de eliminación académica.
*(Longitud de la respuesta: 212 caracteres)*
--------------------------------------------------

👤 Estudiante: ¿Y existe algún proceso de apelación para eso?
🤖 Procesando con historial y RAG...

--- RESPUESTA OBTENIDA ---
Sí, ante una causal de eliminación por tercera reprobación, el estudiante puede presentar una solicitud de apelación dentro del plazo establecido ante la Dirección de Carrera para su revisión.
*(Longitud de la respuesta: 198 caracteres)*
--------------------------------------------------
📄 Licencia y Uso Académico
Este proyecto fue desarrollado con fines exclusivamente académicos para la asignatura Soluciones de Ingeniería con IA en Duoc UC.