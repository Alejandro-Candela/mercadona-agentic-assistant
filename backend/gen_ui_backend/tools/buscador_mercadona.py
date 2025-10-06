"""
Tool para buscar productos en la API de Mercadona.
Integra con las utilidades de mercadona_api para realizar búsquedas reales.
"""
from typing import Any, Dict, List
from langchain_core.tools import tool

from gen_ui_backend.utils.mercadona_api import (
    crear_diccionario_categorias,
    encontrar_numero_categoria,
    extraer_productos_de_categoria,
    mostrar_productos_seleccionados
)


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
        - precio_unidad: Precio del producto
        - disponible: Si está disponible
        - categoria: Categoría del producto
        - packaging: Información del empaquetado
    """
    try:
        # Usar la función integrada para buscar múltiples productos
        resultado = buscar_multiples_productos.invoke([producto])
        
        if not resultado:
            return {
                "id": "",
                "nombre": producto,
                "precio_unidad": 0.0,
                "disponible": False,
                "categoria": "",
                "error": f"No se encontró el producto: {producto}"
            }
        
        # Retornar el primer resultado encontrado
        return resultado[0]
    
    except Exception as e:
        print(f"Error al buscar producto '{producto}': {e}")
        return {
            "id": "",
            "nombre": producto,
            "precio_unidad": 0.0,
            "disponible": False,
            "categoria": "",
            "error": str(e)
        }


@tool
def buscar_multiples_productos(productos: List[str]) -> List[Dict[str, Any]]:
    """
    Busca múltiples productos en la API de Mercadona.
    
    Esta es la función principal que ejecuta todo el flujo:
    1. Crea diccionario de categorías
    2. Encuentra categorías relevantes
    3. Extrae productos de esas categorías
    4. Selecciona los más baratos que coincidan
    
    Args:
        productos: Lista de nombres de productos a buscar
        
    Returns:
        Lista de dicts con información de cada producto encontrado
    """
    try:
        print(f"\n🔍 Iniciando búsqueda de productos: {productos}")
        
        # 1. Crear diccionario de categorías
        print("\n📚 Paso 1: Creando diccionario de categorías...")
        diccionario_categorias = crear_diccionario_categorias()
        
        if not diccionario_categorias:
            print("❌ No se pudo crear el diccionario de categorías")
            return []
        
        # 2. Encontrar categorías relevantes
        print("\n🔎 Paso 2: Buscando categorías relevantes...")
        categorias_ids = encontrar_numero_categoria(productos, diccionario_categorias)
        
        if not categorias_ids:
            print("❌ No se encontraron categorías para los productos especificados")
            return []
        
        # 3. Extraer productos de esas categorías
        print(f"\n📦 Paso 3: Extrayendo productos de {len(categorias_ids)} categorías...")
        productos_mercadona = extraer_productos_de_categoria(categorias_ids)
        
        if not productos_mercadona:
            print("❌ No se encontraron productos en las categorías")
            return []
        
        # 4. Seleccionar los productos más baratos que coincidan
        print("\n💰 Paso 4: Seleccionando productos más baratos...")
        productos_seleccionados = mostrar_productos_seleccionados(productos_mercadona, productos)
        
        if not productos_seleccionados:
            print("❌ No se encontraron coincidencias para los productos buscados")
            return []
        
        # Formatear resultados para ser compatibles con el sistema multi-agente
        resultados = []
        for producto in productos_seleccionados:
            resultado = {
                "id": producto.get("id", ""),
                "nombre": producto.get("nombre", ""),
                "precio_unidad": producto.get("precio_unidad", 0.0),
                "disponible": True,
                "categoria": producto.get("categoria_nombre", ""),
                "subcategoria": producto.get("subcategoria_nombre", ""),
                "packaging": producto.get("packaging", ""),
                "precio_referencia": producto.get("precio_referencia", ""),
                "formato_referencia": producto.get("formato_referencia", ""),
                "producto_buscado": producto.get("producto_buscado", ""),
                "total_coincidencias": producto.get("total_coincidencias", 0)
            }
            resultados.append(resultado)
        
        print(f"\n✅ Búsqueda completada: {len(resultados)} productos encontrados")
        return resultados
    
    except Exception as e:
        print(f"❌ Error durante la búsqueda de productos: {e}")
        import traceback
        traceback.print_exc()
        return []

