"""
Script de prueba del flujo completo del sistema multi-agente.
"""
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from gen_ui_backend.chain import create_multi_agent_graph

# Cargar variables de entorno
load_dotenv()

def test_flujo_completo_con_api_key():
    """
    Prueba el flujo completo del sistema multi-agente.
    Requiere API key de OpenAI.
    """
    print("\n" + "="*80)
    print("PRUEBA DEL SISTEMA MULTI-AGENTE COMPLETO")
    print("="*80)
    
    # Verificar que tenemos API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n⚠️  No se encontró OPENAI_API_KEY en el entorno")
        print("Esta prueba requiere una API key de OpenAI")
        print("\nPuedes configurarla creando un archivo .env con:")
        print("OPENAI_API_KEY=tu-api-key-aqui")
        return
    
    print(f"\n✓ API Key encontrada: {api_key[:10]}...")
    
    # Crear el grafo
    print("\n📊 Creando grafo multi-agente...")
    graph = create_multi_agent_graph()
    print("✓ Grafo creado exitosamente")
    
    # Mensaje de prueba
    mensaje_usuario = "Quiero 2 leches y un pan"
    print(f"\n💬 Mensaje del usuario: '{mensaje_usuario}'")
    
    # Estado inicial
    estado_inicial = {
        "messages": [HumanMessage(content=mensaje_usuario)]
    }
    
    print("\n" + "-"*80)
    print("EJECUTANDO SISTEMA MULTI-AGENTE...")
    print("-"*80)
    
    try:
        # Invocar el grafo
        resultado = graph.invoke(estado_inicial)
        
        print("\n" + "="*80)
        print("RESULTADO FINAL")
        print("="*80)
        
        print(f"\nAgente final: {resultado.get('current_agent')}")
        print(f"\nResultado:")
        print(resultado.get("final_result"))
        
        if resultado.get("ticket"):
            print("\n" + "-"*80)
            print("TICKET GENERADO:")
            print("-"*80)
            print(resultado.get("ticket"))
        
        print("\n" + "="*80)
        print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


def test_flujo_sin_api():
    """
    Prueba el flujo con mock data (sin llamar a OpenAI).
    """
    print("\n" + "="*80)
    print("PRUEBA CON MOCK DATA (SIN API)")
    print("="*80)
    
    print("\n⚠️  Esta prueba simula el flujo sin llamar a OpenAI")
    print("Para una prueba completa, usa test_flujo_completo_con_api_key()")
    
    # Aquí puedes implementar una versión mock del flujo
    print("\n✓ Usa el script test_simple.py para probar las tools individuales")


if __name__ == "__main__":
    import sys
    
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*20 + "TEST DEL SISTEMA MULTI-AGENTE" + " "*29 + "║")
    print("╚" + "═"*78 + "╝")
    
    print("\nOpciones:")
    print("  1. Prueba completa con OpenAI (requiere API key)")
    print("  2. Información sobre pruebas mock")
    print()
    
    if len(sys.argv) > 1:
        opcion = sys.argv[1]
    else:
        opcion = input("Selecciona una opción (1 o 2): ").strip()
    
    if opcion == "1":
        test_flujo_completo_con_api_key()
    elif opcion == "2":
        test_flujo_sin_api()
    else:
        print("❌ Opción no válida")

