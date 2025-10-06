"""
Agente 2: Buscador de productos en la API de Mercadona.

Busca cada producto mencionado en la API de Mercadona
y recopila información de precios y disponibilidad.
"""
from typing import Literal
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from gen_ui_backend.agents.state import MultiAgentState
from gen_ui_backend.tools.buscador_mercadona import buscar_multiples_productos


def agente_2_buscador(
    state: MultiAgentState,
    config: RunnableConfig  # noqa: ARG001 - Requerido por la interfaz
) -> Command[Literal["agente_3_calculador", "respuesta_final"]]:
    """
    Agente 2: Buscador de productos en la API de Mercadona.
    
    Busca cada producto mencionado en la API de Mercadona
    y recopila información de precios y disponibilidad.
    """
    print("\n=== AGENTE 2: BUSCADOR ===")
    
    productos = state.get("productos_mencionados", [])
    print(f"Buscando productos: {productos}")
    
    # Usar la herramienta de búsqueda múltiple
    productos_encontrados = []
    productos_no_encontrados = []
    
    try:
        # Invocar herramienta de búsqueda
        resultados = buscar_multiples_productos.invoke({"productos": productos})
        
        for resultado in resultados:
            if resultado.get("disponible"):
                productos_encontrados.append(resultado)
                print(f"✓ Encontrado: {resultado.get('nombre')} - {resultado.get('precio_unidad')}€")
            else:
                productos_no_encontrados.append(resultado.get("nombre"))
                print(f"✗ No disponible: {resultado.get('nombre')}")
        
        # Si encontramos productos, ir al calculador
        if productos_encontrados:
            return Command(
                goto="agente_3_calculador",
                update={
                    "productos_encontrados": productos_encontrados,
                    "productos_no_encontrados": productos_no_encontrados,
                    "current_agent": "agente_2"
                }
            )
        else:
            # No encontramos productos
            return Command(
                goto="respuesta_final",
                update={
                    "final_result": f"❌ Lo siento, no he encontrado ninguno de los productos: {', '.join(productos)}",
                    "current_agent": "agente_2"
                }
            )
    
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        return Command(
            goto="respuesta_final",
            update={
                "final_result": f"❌ Ha ocurrido un error al buscar los productos: {str(e)}",
                "current_agent": "agente_2"
            }
        )

