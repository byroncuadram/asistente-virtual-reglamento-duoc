import time
from langchain_core.messages import HumanMessage, AIMessage
from src.database import inicializar_vectorstore
from src.rag_chain import crear_cadena_rag_con_memoria

LIMITE_CARACTERES = 500

def ejecutar_consulta_interactiva():
    print("==================================================")
    print("  ASISTENTE VIRTUAL DUOC UC (CON MEMORIA RAG)    ")
    print("==================================================")
    
    print("\nInicializando base de datos vectorial...")
    vectorstore = inicializar_vectorstore()

    time.sleep(2)
    
    print("Cargando modelo RAG con memoria...")
    rag_chain = crear_cadena_rag_con_memoria(vectorstore)
    
    chat_history = []
    
    print("\n¡Sistema listo con memoria conversacional! Escribe 'salir' para terminar.\n")
    
    while True:
        pregunta = input("👤 Estudiante: ")
        
        if pregunta.strip().lower() in ["salir", "exit", "quit"]:
            print("\n¡Gracias por utilizar el Asistente Académico! Hasta luego.")
            break
        
        if not pregunta.strip():
            print("Por favor, ingresa una pregunta válida.\n")
            continue
            
        print("🤖 Procesando con historial y RAG...")
        
        try:
            # Invocar pipeline LCEL
            respuesta_texto = rag_chain.invoke({
                "input": pregunta,
                "chat_history": chat_history
            })
            
            # Recorte estricto de longitud
            if len(respuesta_texto) > LIMITE_CARACTERES:
                respuesta_texto = respuesta_texto[:LIMITE_CARACTERES] + "... [Respuesta delimitada]"
            
            print("\n--- RESPUESTA OBTENIDA ---")
            print(respuesta_texto)
            print(f"*(Longitud de la respuesta: {len(respuesta_texto)} caracteres)*\n")
            print("-" * 50 + "\n")
            
            # Guardar en el historial
            chat_history.append(HumanMessage(content=pregunta))
            chat_history.append(AIMessage(content=respuesta_texto))
            
        except Exception as e:
            print(f"Ocurrió un error al procesar la consulta: {e}\n")

if __name__ == "__main__":
    ejecutar_consulta_interactiva()