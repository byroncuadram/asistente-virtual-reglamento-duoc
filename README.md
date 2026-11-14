
### 1. Archivo `requirements.txt`

# Dependencias — Ingeniería de Soluciones con IA (Evaluación RA2)
# Instalación local:   pip install -r requirements.txt
# En Google Colab:     !pip install -q -r requirements.txt
#
# Requiere Python >=3.10.

# --- Núcleo LLM / LangChain (Sintaxis LCEL Nativa) -------------------
langchain>=0.3.0
langchain-core>=0.3.0

# --- Integraciones Específicas de LangChain ---------------------------
langchain-mistralai>=0.2.0
langchain-chroma>=0.1.4
langchain-huggingface>=0.1.0

# --- Base de Datos Vectorial y Embeddings Locales ---------------------
chromadb>=0.5.0
sentence-transformers>=3.0.0

# --- Datos y Utilidades -----------------------------------------------
pandas>=2.0.0
python-dotenv>=1.0.0


---

### 2. Archivo `README.md` (Actualizado a Arquitectura Agente RA2)

Se actualizaron las rutas reales (`reglamento_academico_duoc_uc_2026.csv`), los modelos reales (`open-mistral-7b` y `sentence-transformers/all-MiniLM-L6-v2`), el límite exacto de **500 caracteres**, la recuperación **`k=8`**, las variables de entorno exactas que lee `config.py`, los comandos de salida (`salir`, `exit`, `chao`) y el ejemplo real de ejecución en consola:

# Agente Virtual Autónomo de Orientación Académica — Reglamento Duoc UC (RA2)

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Framework](https://img.shields.io/badge/LangChain-LCEL-green.svg)
![LLM Provider](https://img.shields.io/badge/Mistral%20AI-open--mistral--7b-orange.svg)
![Embeddings](https://img.shields.io/badge/HuggingFace-MiniLM--L6--v2-yellow.svg)
![Vector DB](https://img.shields.io/badge/ChromaDB-v0.5%2B-purple.svg)

Agente conversacional orientado a la consulta normativa institucional de Duoc UC[cite: 11]. Implementa razonamiento adaptativo mediante **LangChain Expression Language (LCEL)**[cite: 11], reformulación autónoma de consultas dependientes del contexto[cite: 11], recuperación semántica como herramienta (*Retriever Tool*) sobre **ChromaDB** con embeddings locales (**Sentence-Transformers**)[cite: 10, 11], memoria conversacional en RAM[cite: 12] y *grounding* estricto limitado a **500 caracteres** para evitar alucinaciones[cite: 11, 12].

---

## 🏛️ Arquitectura del Sistema

El proyecto sigue una arquitectura modular desacoplada en 3 capas[cite: 9, 10, 11, 12]:

```text
asistente-virtual-reglamento-duoc/
├── data/
│   └── reglamento_academico_duoc_uc_2026.csv   # Fuente de datos normativos
├── src/
│   ├── __init__.py
│   ├── config.py              # Gestión de credenciales (.env) y rutas del proyecto
│   ├── database.py            # Carga defensiva del CSV, embeddings locales e indexación ChromaDB
│   └── rag_chain.py           # Orquestación del Agente en LCEL (get_context + ChatMistralAI)
├── chroma_db/                 # Base vectorial persistente (generada automáticamente al iniciar)
├── .env                       # Credenciales de entorno (excluido en .gitignore)
├── .gitignore
├── main.py                    # Interfaz de consola interactiva (CLI) y gestión de chat_history
├── README.md                  # Documentación técnica e instrucciones de ejecución
└── requirements.txt           # Dependencias del proyecto


### Flujo de Razonamiento del Agente

1. **Gestión de Estado (`main.py`)**: Mantiene el historial de diálogo en memoria RAM mediante objetos `HumanMessage` y `AIMessage`.


2. **Planificación y Contextualización (`get_context`)**: Si existe historial previo, el agente reescribe de forma autónoma la consulta del estudiante incluyendo sinónimos normativos (ej. *"prueba"* $\rightarrow$ *"evaluación"*, *"enfermo"* $\rightarrow$ *"inasistencia médica"*) antes de buscar.


3. **Invocación de Herramienta (`Retriever Tool`)**: Consulta los **k=8** fragmentos más relevantes en ChromaDB vectorizados localmente con `all-MiniLM-L6-v2`.


4. **Inferencia Controlada (`ChatMistralAI`)**: Genera una respuesta sintética de máximo **500 caracteres** basada exclusivamente en el reglamento recuperado.



---

## 📋 Requisitos Previos

* **Python**: Versión `>= 3.10` (recomendado Python 3.11 o 3.12).


* **API Key**: Una clave activa de Mistral AI (obtener en [Mistral La Plateforme](https://console.mistral.ai/)).
* **Conexión a Internet**: Requerida en la primera ejecución para descargar el modelo local `sentence-transformers/all-MiniLM-L6-v2` (~90 MB) y para consultar la API de `open-mistral-7b`.

---

## 🚀 Instalación y Configuración Paso a Paso

### 1. Clonar el Repositorio

-bash
git clone [https://github.com/byroncuadram/asistente-virtual-reglamento-duoc.git](https://github.com/byroncuadram/asistente-virtual-reglamento-duoc.git)
cd asistente-virtual-reglamento-duoc

### 2. Crear y Activar el Entorno Virtual

**En Windows (PowerShell):**

-powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

**En Linux / macOS:**

-bash
python3 -m venv .venv
source .venv/bin/activate

### 3. Instalar Dependencias

Actualiza `pip` e instala las librerías exactas del proyecto:

-bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

### 4. Configurar Variables de Entorno

Crea un archivo llamado `.env` en la raíz del proyecto (al mismo nivel que `main.py`) y define tu clave de Mistral AI:

.env
MISTRAL_API_KEY=tu_api_key_de_mistral_aqui

> ⚠️ **Nota de seguridad:** Nunca subas el archivo `.env` ni la carpeta `chroma_db/` a tu repositorio público. Verifica que ambos estén incluidos en `.gitignore`.

### 5. Verificar Archivo de Datos

Asegúrate de que el archivo CSV del reglamento esté ubicado exactamente en la ruta esperada por `src/config.py`:

-text
data/reglamento_academico_duoc_uc_2026.csv

---

## 💻 Ejecución del Agente

Con el entorno virtual activado, inicia el agente desde la raíz del proyecto:

-bash
python main.py


### Notas sobre la Ejecución:

* **Primer arranque:** Descargará el modelo de embeddings `sentence-transformers/all-MiniLM-L6-v2`, sanitizará el CSV y creará la carpeta `chroma_db/` en disco.


* **Arranques posteriores:** Cargará directamente la base vectorial persistida en `chroma_db/` sin re-indexar.


* **Comandos de salida:** Para terminar la sesión en cualquier momento, escribe `salir`, `exit` o `chao`.



---

## 💬 Ejemplo de Interacción en Consola

============================================================
    ASISTENTE VIRTUAL DE REGLAMENTO ACADÉMICO DUOC UC (RA2)
============================================================
Escribe tu consulta académica o 'salir' para finalizar.


Estudiante: hola me llamo byron

Asistente: ¡Hola Byron! 😊 ¿En qué puedo ayudarte hoy con tu orientación académica en Duoc UC? ¿Tienes alguna duda sobre tu plan de estudios, inscripciones, cambios de carrera o algo más? Estoy aquí para apoyarte. 💪✨

Estudiante: ¿Cuántas veces puedo rendir un examen de asignatura?

Asistente: ¡Buena pregunta, Byron! 😊 Según el **Artículo N°27** del Reglamento Académico de Duoc UC, en cada asignatura **puedes rendir dos instancias de evaluación final** (ordinario y extraordinario). La nota final se calculará con **la más alta de las dos calificaciones** obtenidas.

Estudiante: ¿Y qué pasa si me enfermo el día de la prueba?

Asistente: ¡Entiendo, Byron! 😊 Si te enfermas el día de la **evaluación ordinaria o extraordinaria**, debes justificar tu inasistencia con un **certificado médico** (según el **Artículo N°48** del Título XII sobre *Retiro y Postergación*).

Puedes solicitar:
✅ **Postergación** (si es por enfermedad justificada) para rendirla en otra fecha.
✅ **Retiro** (si prefieres no rendirla en ese momento).

Estudiante: salir

Asistente: ¡Hasta luego! Mucho éxito en tu semestre académico.

---

## 📄 Licencia y Uso Académico

Proyecto desarrollado con fines académicos para la **Evaluación RA2** de la asignatura de Inteligencia Artificial en **Duoc UC - Sede Valparaíso**.