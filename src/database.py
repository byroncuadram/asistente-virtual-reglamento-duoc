import os
import shutil
import pandas as pd
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import CSV_PATH, CHROMA_PATH

def get_vectorstore():
    """
    Inicializa o recupera la base de datos vectorial ChromaDB.
    Usa Embeddings locales con Sentence-Transformers para evitar errores
    de tokenización con la API de Mistral.
    """
    # 1. Instanciamos un modelo de embeddings ligero, público y local (multilingüe/robusto)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 2. Si la base vectorial existe, la cargamos directamente
    if os.path.exists(CHROMA_PATH) and len(os.listdir(CHROMA_PATH)) > 0:
        try:
            return Chroma(
                persist_directory=CHROMA_PATH,
                embedding_function=embeddings
            )
        except Exception:
            # Si la base antigua estaba dañada, la borramos para recrearla
            shutil.rmtree(CHROMA_PATH)

    # 3. Si no existe, leemos el CSV defensivamente
    df = None
    for enc in ["utf-8", "latin-1", "iso-8859-1"]:
        try:
            df = pd.read_csv(
                CSV_PATH,
                encoding=enc,
                on_bad_lines="skip",
                sep=None,
                engine="python"
            )
            break
        except Exception:
            continue

    if df is None or df.empty:
        raise ValueError(f"No se pudo cargar el archivo CSV en la ruta: {CSV_PATH}")

    # Limpiamos nombres de columnas
    df.columns = df.columns.astype(str).str.strip().str.replace('"', '').str.replace("'", "")

    # 4. Convertimos cada fila en un objeto Document validando texto estricto
    documents = []
    for _, row in df.iterrows():
        row_parts = []
        for col in df.columns:
            val = str(row[col]).strip() if pd.notna(row[col]) else ""
            if val and val.lower() != "nan":
                row_parts.append(f"{col}: {val}")

        if row_parts:
            content_str = " | ".join(row_parts)
            documents.append(Document(page_content=str(content_str)))

    if not documents:
        raise ValueError("El CSV no contiene datos válidos para procesar.")

    # 5. Creación e indexación limpia de la base vectorial
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    return vectorstore