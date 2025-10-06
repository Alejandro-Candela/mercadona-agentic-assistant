"""
Tool para buscar productos en la API de Mercadona.
"""
from typing import Any, Dict, List
from langchain_core.tools import tool


@tool
def buscar_producto_mercadona(producto: str) -> Dict[str, Any]:
    """
    Busca un producto en la API de Mercadona.
    
    Args:
        producto: Nombre del producto a buscar
        
    Returns:
        Dict con información del producto:
        - id: ID del producto
        - nombre: Nombre del producto
        - precio: Precio del producto
        - disponible: Si está disponible
        - categoria: Categoría del producto
    """
    # TODO: Implementar llamada a la API de Mercadona
    # Aquí se debe implementar:
    # 1. Llamada a la API de Mercadona
    # 2. Procesamiento de la respuesta
    # 3. Manejo de errores (producto no encontrado, etc.)
    
    return {
        "id": "",
        "nombre": producto,
        "precio": 0.0,
        "disponible": False,
        "categoria": ""
    }


@tool
def buscar_multiples_productos(productos: List[str]) -> List[Dict[str, Any]]:
    """
    Busca múltiples productos en la API de Mercadona.
    
    Args:
        productos: Lista de nombres de productos a buscar
        
    Returns:
        Lista de dicts con información de cada producto
    """
    # TODO: Implementar búsqueda múltiple
    # Optimización: realizar búsquedas en paralelo si es posible
    
    resultados = []
    for producto in productos:
        resultado = buscar_producto_mercadona.invoke(producto)
        resultados.append(resultado)
    
    return resultados

