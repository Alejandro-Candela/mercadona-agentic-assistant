"""
Definición del grafo multi-agente para el sistema de compra en Mercadona.

Este módulo contiene la lógica de construcción del grafo que coordina
los diferentes agentes del sistema.
"""
from langgraph.graph import StateGraph, START
from langgraph.graph.graph import CompiledGraph

from gen_ui_backend.agents import (
    MultiAgentState,
    agente_1_clasificador,
    agente_2_buscador,
    agente_3_calculador,
    nodo_respuesta_final,
)


def create_multi_agent_graph() -> CompiledGraph:
    """
    Crea el grafo multi-agente para el sistema de compra en Mercadona.
    
    Flujo:
    START -> Agente 1 (Clasificador) -> Agente 2 (Buscador) -> Agente 3 (Calculador) -> Respuesta Final -> END
    
    El nodo final usa el modelo de chat para generar eventos de streaming que el frontend captura.
    
    Returns:
        Grafo compilado listo para ejecutar
    """
    workflow = StateGraph(MultiAgentState)
    
    # Agregar nodos de agentes
    workflow.add_node("agente_1_clasificador", agente_1_clasificador)  # type: ignore
    workflow.add_node("agente_2_buscador", agente_2_buscador)  # type: ignore
    workflow.add_node("agente_3_calculador", agente_3_calculador)  # type: ignore
    workflow.add_node("respuesta_final", nodo_respuesta_final)  # type: ignore
    
    # Definir punto de entrada
    workflow.add_edge(START, "agente_1_clasificador")
    
    # Los edges condicionales se manejan con Command en cada agente
    # No necesitamos add_conditional_edges porque Command maneja el routing
    
    # Compilar el grafo
    graph = workflow.compile()
    
    return graph


# Mantener retrocompatibilidad con el sistema anterior
def create_graph() -> CompiledGraph:
    """
    Función legacy para mantener compatibilidad.
    Ahora usa el sistema multi-agente.
    """
    return create_multi_agent_graph()

