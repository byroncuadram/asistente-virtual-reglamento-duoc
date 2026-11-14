from langchain_core.messages import HumanMessage, AIMessage
from src.rag_chain import create_rag_chain

def main():
    print("=" * 60)
    print("    ASISTENTE VIRTUAL DE REGLAMENTO ACADÉMICO DUOC UC (RA2)")
    print("=" * 60)
    print("Escribe tu consulta académica o 'salir' para finalizar.\n")

    # Inicialización de la cadena RAG en LCEL
    rag_chain = create_rag_chain()
    
    # Historial conversacional en memoria RAM durante la sesión
    chat_history = []

    while True:
        user_input = input("\nEstudiante: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ["salir", "exit", "chao"]:
            print("\nAsistente: ¡Hasta luego! Mucho éxito en tu semestre académico.")
            break

        try:
            # Ejecución de la cadena LCEL pasando la pregunta y el historial
            response = rag_chain.invoke({
                "input": user_input,
                "chat_history": chat_history
            })

            # Control adicional de longitud máxima a nivel de interfaz
            if len(response) > 500:
                response = response[:497] + "..."

            print(f"\nAsistente: {response}")

            # Actualizamos el historial de conversación en memoria
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=response))

        except Exception as e:
            print(f"\nOcurrió un error al procesar la consulta: {e}")

if __name__ == "__main__":
    main()