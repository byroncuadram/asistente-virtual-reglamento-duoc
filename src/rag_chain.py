from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.config import MISTRAL_API_KEY

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def crear_cadena_rag_con_memoria(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    llm = ChatMistralAI(model="open-mistral-7b", temperature=0, api_key=MISTRAL_API_KEY)
    
    # 1. Prompt para contextualizar la pregunta con el historial
    contextualize_q_system_prompt = (
        "Dada la conversación anterior y la última pregunta del usuario "
        "que podría hacer referencia al historial, formula una pregunta "
        "independiente que se pueda entender sin la conversación anterior. "
        "NO la respondas, solo reescríbela si es necesario, de lo contrario devuélvela tal cual."
    )
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    
    # Cadena para reformular la consulta
    contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()
    
    # Función para recuperar documentos usando la pregunta contextualizada
    def contextualized_retriever(input_dict):
        if input_dict.get("chat_history"):
            query = contextualize_q_chain.invoke(input_dict)
        else:
            query = input_dict["input"]
        return retriever.invoke(query)
        
    # 2. System Prompt principal con memoria y contexto
    system_prompt = (
        "Eres un asistente virtual de orientación académica para estudiantes de Duoc UC.\n"
        "Mantén un trato cordial, respetuoso y personalizado con el estudiante.\n"
        "Responde la consulta utilizando la información del contexto recuperado y el historial de la conversación.\n"
        "RESTRICCIÓN DE LONGITUD: Tu respuesta debe ser breve, clara y concisa (máximo 500 caracteres).\n"
        "Si la respuesta a una duda académica no está en el contexto, indica amablemente que no posees la información.\n\n"
        "Contexto recuperado:\n{context}"
    )
    
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    
    # 3. Construcción del Pipeline RAG con LCEL (LangChain Expression Language)
    rag_chain = (
        RunnablePassthrough.assign(
            context=lambda x: format_docs(contextualized_retriever(x))
        )
        | qa_prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain