from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_mistralai import ChatMistralAI
from src.config import MISTRAL_API_KEY
from src.database import get_vectorstore

def create_rag_chain():
    """
    Construye la cadena del Agente RAG con razonamiento en LCEL.
    Se optimiza k=8 en el Retriever Tool para garantizar la captura de normativas.
    """
    # 1. Obtenemos el recuperador vectorial ampliando a k=8 para mayor cobertura
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

    # 2. Instanciamos el Modelo de Lenguaje (LLM)
    llm = ChatMistralAI(
        model="open-mistral-7b",
        mistral_api_key=MISTRAL_API_KEY,
        temperature=0.2
    )

    # 3. Prompt de Reformulación (Nodo de Planificación del Agente)
    contextualize_q_system_prompt = (
        "Dada la conversación anterior y la última pregunta del estudiante, "
        "formula una consulta de búsqueda semántica independiente en español. "
        "Incluye términos técnicos equivalentes (ejemplo: reemplazar 'prueba' por 'evaluación', "
        "'enfermo' por 'inasistencia médica / justificativo'). "
        "NO respondas la pregunta, solo entrega la consulta reformulada."
    )
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    
    contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()

    # 4. Prompt Principal de Respuesta del Agente (Grounding Semántico)
    system_prompt = (
        "Eres un asistente virtual de orientación académica para estudiantes de Duoc UC. "
        "Mantén un trato cordial, amigable y personalizado.\n"
        "Responde la consulta del estudiante analizando el contexto recuperado del reglamento.\n\n"
        "INSTRUCCIONES CLAVE:\n"
        "1. Identifica sinónimos normativos (ejemplo: 'prueba' = 'evaluación', 'enfermo' = 'inasistencia/justificativo').\n"
        "2. Sé sintético y conciso (máximo 500 caracteres).\n"
        "3. Solo si la normativa NO aborda en absoluto el tema consultado, declara amablemente que no posees la información.\n\n"
        "Contexto recuperado del Reglamento:\n{context}"
    )
    
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Función del Agente que administra el estado y la llamada a las Tools
    def get_context(input_dict):
        if input_dict.get("chat_history") and len(input_dict["chat_history"]) > 0:
            query = contextualize_q_chain.invoke(input_dict)
        else:
            query = input_dict["input"]
        
        # Invocación de la herramienta semántica ChromaDB
        docs = retriever.invoke(query)
        return format_docs(docs)

    # Pipeline LCEL
    chain = (
        RunnablePassthrough.assign(context=get_context)
        | qa_prompt
        | llm
        | StrOutputParser()
    )

    return chain