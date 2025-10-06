"""
Tool para calcular precios y generar ticket de compra.
"""
from typing import Any, Dict, List
from langchain_core.tools import tool


@tool
def calcular_precio_total(productos: List[Dict[str, Any]], cantidades: Dict[str, int]) -> Dict[str, Any]:
    """
    Calcula el precio total de una lista de productos con sus cantidades.
    
    Args:
        productos: Lista de productos con información (incluyendo precio)
        cantidades: Dict con producto_id -> cantidad
        
    Returns:
        Dict con:
        - subtotal: Suma de precios sin descuentos
        - descuentos: Descuentos aplicados
        - total: Precio final
        - items: Lista detallada de items
    """
    # TODO: Implementar cálculo de precios
    # 1. Calcular subtotal
    # 2. Aplicar descuentos si los hay
    # 3. Calcular total final
    
    return {
        "subtotal": 0.0,
        "descuentos": 0.0,
        "total": 0.0,
        "items": []
    }


@tool
def generar_ticket_compra(
    productos: List[Dict[str, Any]], 
    cantidades: Dict[str, int],
    precio_info: Dict[str, Any]
) -> str:
    """
    Genera un ticket de compra formateado.
    
    Args:
        productos: Lista de productos
        cantidades: Cantidades de cada producto
        precio_info: Información de precios (del calcular_precio_total)
        
    Returns:
        String con el ticket formateado
    """
    # TODO: Implementar generación de ticket
    # 1. Formatear header del ticket
    # 2. Listar productos con cantidades y precios
    # 3. Mostrar subtotal, descuentos y total
    # 4. Footer con información adicional
    
    ticket = """
    ================================
    MERCADONA - TICKET DE COMPRA
    ================================
    
    [Items aquí]
    
    --------------------------------
    Subtotal: 0.00€
    Descuentos: 0.00€
    --------------------------------
    TOTAL: 0.00€
    ================================
    """
    
    return ticket

