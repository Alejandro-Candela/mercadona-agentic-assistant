"""
Estado compartido entre todos los agentes del sistema multi-agente.
"""
from typing import List, Optional, TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import add_messages


class MultiAgentState(TypedDict, total=False):
    """Estado compartido entre todos los agentes."""
    input: Optional[List[HumanMessage | AIMessage | SystemMessage]]
    """Input del servidor (compatibilidad con sistema antiguo)."""
    messages: Annotated[List[HumanMessage | AIMessage | SystemMessage], add_messages]
    """Lista de mensajes para comunicación entre agentes."""
    
    # Datos del Agente 1 - Clasificador
    intencion: Optional[str]
    """Intención clasificada del usuario."""
    productos_mencionados: Optional[List[str]]
    """Lista de productos mencionados por el usuario."""
    cantidades: Optional[dict]
    """Diccionario con cantidades de cada producto."""
    
    # Datos del Agente 2 - Buscador
    productos_encontrados: Optional[List[dict]]
    """Lista de productos encontrados en Mercadona."""
    productos_no_encontrados: Optional[List[str]]
    """Lista de productos que no se encontraron."""
    
    # Datos del Agente 3 - Calculador
    precio_info: Optional[dict]
    """Información de precios calculados."""
    ticket: Optional[str]
    """Ticket de compra generado."""
    archivos_generados: Optional[dict]
    """Información de archivos descargables generados."""
    
    # Control de flujo
    current_agent: Optional[str]
    """Agente actual en ejecución."""
    final_result: Optional[str]
    """Resultado final del sistema."""

