import os
import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings
from langchain_core.documents import Document
from src.config import MISTRAL_API_KEY, CHROMA_PATH, CSV_PATH

def inicializar_vectorstore():
    embeddings = MistralAIEmbeddings(model="mistral-embed", api_key=MISTRAL_API_KEY)
    
    # Si la base de datos vectorial ya existe y tiene archivos, la cargamos directamente
    if os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
        return Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    # Lectura del CSV tolerante a errores de comas en el texto
    try:
        df = pd.read_csv(CSV_PATH, encoding='utf-8', on_bad_lines='skip')
    except Exception:
        df = pd.read_csv(CSV_PATH, encoding='latin-1', sep=None, engine='python', on_bad_lines='skip')

    documentos = []
    for _, row in df.iterrows():
        # Unimos las columnas del CSV en el contenido
        contenido = " ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
        metadata = {"fuente": "Reglamento Duoc UC"}
        doc = Document(page_content=contenido, metadata=metadata)
        documentos.append(doc)

    # Crear la base de datos vectorial Chroma
    vectorstore = Chroma.from_documents(
        documents=documentos,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    return vectorstore