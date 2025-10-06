"""
Tool para clasificar la intención del usuario y extraer productos mencionados.
"""
from typing import Any, Dict, List
from langchain_core.tools import tool


@tool
def clasificar_intencion(user_input: str) -> Dict[str, Any]:
    """
    Clasifica la intención del usuario y extrae los productos mencionados.
    
    Args:
        user_input: El mensaje del usuario
        
    Returns:
        Dict con:
        - intencion: tipo de intención (compra, consulta, etc.)
        - productos: lista de productos mencionados
        - cantidad: dict con producto -> cantidad
    """
    # TODO: Implementar lógica de clasificación
    # Aquí se debe implementar la lógica para:
    # 1. Clasificar la intención del usuario
    # 2. Extraer productos mencionados
    # 3. Detectar cantidades asociadas
    
    return {
        "intencion": "compra",
        "productos": [],
        "cantidad": {}
    }

