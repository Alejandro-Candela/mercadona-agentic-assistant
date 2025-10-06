"""
Script de prueba para el sistema multi-agente de compra en Mercadona.
"""
from langchain_core.messages import HumanMessage
from gen_ui_backend.graph import create_multi_agent_graph


def test_sistema_multi_agente():
    """
    Prueba el sistema multi-agente con diferentes casos de uso.
    """
    print("="*60)
    print("PRUEBA DEL SISTEMA MULTI-AGENTE - MERCADONA")
    print("="*60)
    
    # Crear el grafo
    graph = create_multi_agent_graph()
    
    # Caso de prueba 1: Compra simple
    print("\n\n### CASO 1: Compra Simple ###\n")
    estado_inicial_1 = {
        "messages": [
            HumanMessage(content="Quiero comprar 2 litros de leche y un pan")
        ]
    }
    
    try:
        print("Ejecutando caso 1...")
        resultado_1 = graph.invoke(estado_inicial_1)
        print("\n--- RESULTADO CASO 1 ---")
        print(f"Agente final: {resultado_1.get('current_agent')}")
        print(f"Resultado: {resultado_1.get('final_result')}")
        print(f"Productos mencionados: {resultado_1.get('productos_mencionados')}")
        print(f"Productos encontrados: {len(resultado_1.get('productos_encontrados', []))}")
    except Exception as e:
        print(f"❌ Error en caso 1: {e}")
        import traceback
        traceback.print_exc()
    
    # Caso de prueba 2: Múltiples productos
    print("\n\n### CASO 2: Múltiples Productos ###\n")
    estado_inicial_2 = {
        "messages": [
            HumanMessage(content="Necesito comprar huevos, tomates, aceite de oliva y arroz")
        ]
    }
    
    try:
        print("Ejecutando caso 2...")
        resultado_2 = graph.invoke(estado_inicial_2)
        print("\n--- RESULTADO CASO 2 ---")
        print(f"Agente final: {resultado_2.get('current_agent')}")
        print(f"Resultado: {resultado_2.get('final_result')}")
        print(f"Productos mencionados: {resultado_2.get('productos_mencionados')}")
        print(f"Productos encontrados: {len(resultado_2.get('productos_encontrados', []))}")
        if resultado_2.get('ticket'):
            print(f"\nTicket generado:\n{resultado_2.get('ticket')}")
    except Exception as e:
        print(f"❌ Error en caso 2: {e}")
        import traceback
        traceback.print_exc()
    
    # Caso de prueba 3: Sin productos
    print("\n\n### CASO 3: Sin Productos ###\n")
    estado_inicial_3 = {
        "messages": [
            HumanMessage(content="¿Qué horario tiene la tienda?")
        ]
    }
    
    try:
        print("Ejecutando caso 3...")
        resultado_3 = graph.invoke(estado_inicial_3)
        print("\n--- RESULTADO CASO 3 ---")
        print(f"Agente final: {resultado_3.get('current_agent')}")
        print(f"Resultado: {resultado_3.get('final_result')}")
    except Exception as e:
        print(f"❌ Error en caso 3: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n\n" + "="*60)
    print("PRUEBAS COMPLETADAS")
    print("="*60)


def visualizar_grafo():
    """
    Visualiza la estructura del grafo multi-agente.
    """
    print("\n### ESTRUCTURA DEL GRAFO ###\n")
    graph = create_multi_agent_graph()
    
    print("Nodos del grafo:")
    print("  1. agente_1_clasificador (Clasificador de intención)")
    print("  2. agente_2_buscador (Buscador en Mercadona)")
    print("  3. agente_3_calculador (Calculador de ticket)")
    
    print("\nFlujo de ejecución:")
    print("  START → agente_1_clasificador → agente_2_buscador → agente_3_calculador → END")
    
    print("\nComunicación entre agentes:")
    print("  - Agente 1 extrae: intención, productos, cantidades")
    print("  - Agente 2 busca: productos en API y retorna lista con precios")
    print("  - Agente 3 calcula: precios totales y genera ticket")
    
    # Intentar generar imagen del grafo (si está disponible)
    try:
        from IPython.display import Image, display
        display(Image(graph.get_graph().draw_mermaid_png()))
        print("\n✓ Diagrama del grafo generado")
    except Exception as e:
        print(f"\n⚠ No se pudo generar el diagrama: {e}")
        print("  (Requiere graphviz o mermaid instalado)")


if __name__ == "__main__":
    # Visualizar estructura
    visualizar_grafo()
    
    # Ejecutar pruebas
    test_sistema_multi_agente()


