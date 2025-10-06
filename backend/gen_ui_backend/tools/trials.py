"""
Herramientas para interactuar con la API de Mercadona.
Estas funciones están diseñadas para ser usadas como tools en LangGraph.
"""

import requests
import unicodedata
import time
from typing import Dict, List, Optional, Any
import json


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN Y CONSTANTES
# ═══════════════════════════════════════════════════════════════════════════════

BASE_URL = "https://tienda.mercadona.es/api/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}
REQUEST_DELAY = 0.3  # segundos entre peticiones


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES AUXILIARES
# ═══════════════════════════════════════════════════════════════════════════════

def normalizar_nombre(nombre: str) -> str:
    """
    Normaliza un nombre eliminando tildes y convirtiendo a minúsculas.
    
    Args:
        nombre: Texto a normalizar
        
    Returns:
        Texto normalizado en minúsculas sin tildes
    """
    if not nombre:
        return ""
    
    nombre = nombre.lower().strip()
    # Eliminar tildes usando Unicode
    nombre = ''.join(
        c for c in unicodedata.normalize('NFD', nombre)
        if unicodedata.category(c) != 'Mn'
    )
    return nombre


def hacer_peticion_api(url: str, timeout: int = 10) -> Optional[Dict]:
    """
    Realiza una petición GET a la API de Mercadona con manejo de errores.
    
    Args:
        url: URL completa a la que hacer la petición
        timeout: Tiempo máximo de espera en segundos
        
    Returns:
        Diccionario con la respuesta JSON o None si hay error
    """
    try:
        time.sleep(REQUEST_DELAY)
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en petición a {url}: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES PRINCIPALES (TOOLS PARA LANGGRAPH)
# ═══════════════════════════════════════════════════════════════════════════════

def crear_diccionario_categorias() -> Dict[str, int]:
    """
    Se conecta a la API de Mercadona y extrae todas las categorías y subcategorías.
    
    Crea un diccionario que mapea nombres de categorías (originales y normalizados)
    a sus IDs de la API de Mercadona.
    
    Returns:
        Diccionario con formato {nombre_categoria: id_categoria}
        Incluye tanto nombres originales como normalizados para búsqueda flexible.
        
    Example:
        >>> categorias = crear_diccionario_categorias()
        >>> print(categorias["carne"])
        3
        >>> print(categorias["Carne"])
        3
    """
    categorias_dict = {}
    
    # Obtener categorías principales
    url_categorias = f"{BASE_URL}categories/"
    data = hacer_peticion_api(url_categorias)
    
    if not data or "results" not in data:
        print("Error: No se pudieron obtener las categorías principales")
        return categorias_dict
    
    categorias_principales = data["results"]
    print(f"✅ Obtenidas {len(categorias_principales)} categorías principales")
    
    # Recorrer cada categoría principal
    for categoria in categorias_principales:
        cat_id = categoria.get("id")
        cat_nombre = categoria.get("name")
        
        if not cat_id or not cat_nombre:
            continue
        
        # Guardar categoría principal (original y normalizada)
        cat_nombre_norm = normalizar_nombre(cat_nombre)
        categorias_dict[cat_nombre] = cat_id
        categorias_dict[cat_nombre_norm] = cat_id
        
        # Las subcategorías ya vienen en la respuesta inicial
        # No hay que hacer peticiones adicionales
        if "categories" not in categoria:
            continue
        
        # Procesar subcategorías que ya están en la respuesta
        for subcat in categoria["categories"]:
            subcat_id = subcat.get("id")
            subcat_nombre = subcat.get("name")
            
            if not subcat_id or not subcat_nombre:
                continue
            
            # Guardar subcategoría (original y normalizada)
            subcat_nombre_norm = normalizar_nombre(subcat_nombre)
            categorias_dict[subcat_nombre] = subcat_id
            categorias_dict[subcat_nombre_norm] = subcat_id
    
    print(f"✅ Diccionario creado con {len(categorias_dict)} entradas")
    return categorias_dict


def encontrar_numero_categoria(productos: List[str], diccionario_categorias: Optional[Dict[str, int]] = None) -> List[int]:
    """
    Encuentra los IDs de categorías cuyos nombres coinciden con los productos.
    
    Busca en el diccionario de categorías aquellas que contengan los nombres
    de productos especificados. Útil para determinar dónde buscar productos específicos.
    
    Args:
        productos: Lista de nombres de productos a buscar (ej: ["leche", "pan", "huevos"])
        diccionario_categorias: Diccionario opcional con mapeo nombre->ID.
                               Si no se proporciona, se crea uno nuevo.
        
    Returns:
        Lista de IDs de categorías encontradas (sin duplicados)
        
    Example:
        >>> categorias_dict = crear_diccionario_categorias()
        >>> ids = encontrar_numero_categoria(["leche", "pan"], categorias_dict)
        >>> print(ids)
        [6, 5]
    """
    if diccionario_categorias is None:
        print("⚠️ No se proporcionó diccionario, creando uno nuevo...")
        diccionario_categorias = crear_diccionario_categorias()
    
    if not diccionario_categorias:
        print("❌ Error: No se pudo crear el diccionario de categorías")
        return []
    
    categorias_ids = set()  # Usar set para evitar duplicados
    
    for producto in productos:
        if not producto:
            continue
        
        producto_norm = normalizar_nombre(producto)
        
        # Buscar en el diccionario
        for nombre_cat, cat_id in diccionario_categorias.items():
            nombre_cat_norm = normalizar_nombre(str(nombre_cat))
            
            # Si el nombre del producto está contenido en el nombre de la categoría
            if producto_norm in nombre_cat_norm:
                categorias_ids.add(cat_id)
                print(f"✅ '{producto}' encontrado en categoría ID: {cat_id}")
    
    return list(categorias_ids)


def extraer_productos_de_categoria(categorias: List[int]) -> List[Dict[str, Any]]:
    """
    Extrae todos los productos de las categorías especificadas.
    
    Consulta la API de Mercadona para obtener todos los productos dentro de
    las categorías dadas, incluyendo información de precios y detalles.
    
    Args:
        categorias: Lista de IDs de categorías/subcategorías de las que extraer productos
        
    Returns:
        Lista de diccionarios con información de productos. Cada producto contiene:
        - id: ID del producto
        - nombre: Nombre para mostrar
        - packaging: Información de empaquetado
        - precio_unidad: Precio por unidad
        - precio_bulk: Precio alternativo
        - precio_referencia: Precio de referencia (ej: €/kg)
        - categoria_id: ID de la categoría que lo contiene
        
    Example:
        >>> productos = extraer_productos_de_categoria([3, 6])
        >>> print(len(productos))
        125
        >>> print(productos[0]["nombre"])
        'Leche semidesnatada Hacendado'
    """
    productos_mercadona = []
    productos_unicos = set()  # Para evitar duplicados por ID
    
    # Obtener todas las categorías con sus subcategorías
    url_categorias = f"{BASE_URL}categories/"
    data = hacer_peticion_api(url_categorias)
    
    if not data or "results" not in data:
        print("❌ Error: No se pudieron obtener las categorías")
        return productos_mercadona
    
    categorias_principales = data["results"]
    
    # Procesar cada categoría principal
    for categoria in categorias_principales:
        cat_id = categoria.get("id")
        
        if "categories" not in categoria:
            continue
        
        # Verificar si alguna subcategoría o la categoría principal está en la lista solicitada
        tiene_productos_para_extraer = False
        
        # Procesar subcategorías que vienen en la respuesta
        for subcat in categoria["categories"]:
            subcat_id = subcat.get("id")
            
            # Si la subcategoría está en la lista solicitada O la categoría padre está en la lista
            if subcat_id in categorias or cat_id in categorias:
                if not tiene_productos_para_extraer:
                    print(f"🔍 Procesando categoría ID: {cat_id} - {categoria.get('name')}")
                    tiene_productos_para_extraer = True
                
                # Las subcategorías NO incluyen productos directamente
                # Hay que hacer una petición a cada subcategoría para obtener sus sub-subcategorías con productos
                print(f"   🔎 Obteniendo productos de '{subcat.get('name')}' (ID: {subcat_id})...")
                
                subcat_url = f"{BASE_URL}categories/{subcat_id}"
                subcat_data = hacer_peticion_api(subcat_url)
                
                if not subcat_data or "categories" not in subcat_data:
                    print(f"      ⚠️  No se pudieron obtener sub-subcategorías")
                    continue
                
                # Ahora SÍ tenemos las sub-subcategorías con productos
                for sub_subcat in subcat_data["categories"]:
                    if "products" not in sub_subcat:
                        continue
                    
                    productos = sub_subcat.get("products", [])
                    print(f"      📦 {sub_subcat.get('name')}: {len(productos)} productos")
                    
                    for producto in productos:
                        producto_id = producto.get("id")
                        
                        # Evitar duplicados
                        if not producto_id or producto_id in productos_unicos:
                            continue
                        
                        # Extraer información del producto
                        price_info = producto.get("price_instructions", {})
                        
                        producto_info = {
                            "id": producto_id,
                            "nombre": producto.get("display_name", ""),
                            "packaging": producto.get("packaging", ""),
                            "precio_unidad": price_info.get("unit_price", 0),
                            "precio_bulk": price_info.get("bulk_price", ""),
                            "precio_referencia": price_info.get("reference_price", ""),
                            "formato_referencia": price_info.get("reference_format", ""),
                            "categoria_id": cat_id,
                            "categoria_nombre": categoria.get("name", ""),
                            "subcategoria_id": subcat_id,
                            "subcategoria_nombre": subcat.get("name", ""),
                            "sub_subcategoria_id": sub_subcat.get("id"),
                            "sub_subcategoria_nombre": sub_subcat.get("name", "")
                        }
                        
                        productos_mercadona.append(producto_info)
                        productos_unicos.add(producto_id)
    
    print(f"✅ Total de productos extraídos: {len(productos_mercadona)}")
    return productos_mercadona


def mostrar_productos_seleccionados(productos_mercadona: List[Dict[str, Any]], productos_buscados: List[str]) -> List[Dict[str, Any]]:
    """
    Encuentra productos que coincidan con los nombres buscados y selecciona el más barato.
    
    Para cada producto buscado, encuentra todas las coincidencias en la lista de
    productos de Mercadona y devuelve el de menor precio.
    
    Args:
        productos_mercadona: Lista de productos extraídos de Mercadona
        productos_buscados: Lista de nombres de productos a buscar
        
    Returns:
        Lista de productos seleccionados (el más barato de cada coincidencia).
        Cada producto incluye toda su información más un campo "producto_buscado"
        que indica qué término de búsqueda coincidió.
        
    Example:
        >>> productos = extraer_productos_de_categoria([6])
        >>> seleccionados = mostrar_productos_seleccionados(productos, ["leche"])
        >>> print(seleccionados[0]["nombre"])
        'Leche semidesnatada Hacendado'
        >>> print(seleccionados[0]["precio_unidad"])
        0.59
    """
    productos_seleccionados = []
    
    for producto_buscado in productos_buscados:
        if not producto_buscado:
            continue
        
        producto_buscado_norm = normalizar_nombre(producto_buscado)
        coincidencias = []
        
        # Buscar todas las coincidencias
        for producto in productos_mercadona:
            nombre_producto = producto.get("nombre", "")
            nombre_norm = normalizar_nombre(nombre_producto)
            
            # Si el término buscado está en el nombre del producto
            if producto_buscado_norm in nombre_norm:
                coincidencias.append(producto)
        
        if not coincidencias:
            print(f"⚠️ No se encontraron productos para: '{producto_buscado}'")
            continue
        
        # Seleccionar el más barato
        producto_mas_barato = min(
            coincidencias, 
            key=lambda p: float(p.get("precio_unidad", float('inf')))
        )
        
        # Añadir información de búsqueda
        producto_seleccionado = producto_mas_barato.copy()
        producto_seleccionado["producto_buscado"] = producto_buscado
        producto_seleccionado["total_coincidencias"] = len(coincidencias)
        
        productos_seleccionados.append(producto_seleccionado)
        
        print(f"✅ '{producto_buscado}': {producto_mas_barato['nombre']} - {producto_mas_barato['precio_unidad']}€")
    
    return productos_seleccionados


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL INTEGRADA (TOOL COMPLETO PARA LANGGRAPH)
# ═══════════════════════════════════════════════════════════════════════════════

def buscar_productos_mercadona(productos: List[str]) -> str:
    """
    Función integrada que ejecuta todo el proceso de búsqueda de productos.
    
    Esta es la función principal que debe usarse como tool en LangGraph.
    Ejecuta todo el flujo: crear diccionario -> encontrar categorías -> 
    extraer productos -> seleccionar los más baratos.
    
    Args:
        productos: Lista de nombres de productos a buscar
        
    Returns:
        String con JSON formateado conteniendo los productos encontrados
        
    Example:
        >>> resultado = buscar_productos_mercadona(["leche", "pan", "huevos"])
        >>> print(resultado)
        [
            {
                "nombre": "Leche semidesnatada Hacendado",
                "precio_unidad": 0.59,
                ...
            }
        ]
    """
    print(f"\n🔍 Iniciando búsqueda de productos: {productos}")
    
    # 1. Crear diccionario de categorías
    print("\n📚 Paso 1: Creando diccionario de categorías...")
    diccionario_categorias = crear_diccionario_categorias()
    
    if not diccionario_categorias:
        return json.dumps({"error": "No se pudo crear el diccionario de categorías"}, indent=2)
    
    # 2. Encontrar categorías relevantes
    print("\n🔎 Paso 2: Buscando categorías relevantes...")
    categorias_ids = encontrar_numero_categoria(productos, diccionario_categorias)
    
    if not categorias_ids:
        return json.dumps({"error": "No se encontraron categorías para los productos especificados"}, indent=2)
    
    # 3. Extraer productos de esas categorías
    print(f"\n📦 Paso 3: Extrayendo productos de {len(categorias_ids)} categorías...")
    productos_mercadona = extraer_productos_de_categoria(categorias_ids)
    
    if not productos_mercadona:
        return json.dumps({"error": "No se encontraron productos en las categorías"}, indent=2)
    
    # 4. Seleccionar los productos más baratos que coincidan
    print("\n💰 Paso 4: Seleccionando productos más baratos...")
    productos_seleccionados = mostrar_productos_seleccionados(productos_mercadona, productos)
    
    if not productos_seleccionados:
        return json.dumps({"error": "No se encontraron coincidencias para los productos buscados"}, indent=2)
    
    # Formatear resultado
    resultado = {
        "productos_buscados": productos,
        "total_encontrados": len(productos_seleccionados),
        "productos": productos_seleccionados
    }
    
    print(f"\n✅ Búsqueda completada: {len(productos_seleccionados)} productos encontrados")
    
    return json.dumps(resultado, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════════
# EJEMPLO DE USO
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Prueba completa del flujo
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 25 + "PRUEBA DE BÚSQUEDA EN MERCADONA" + " " * 22 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # Lista de productos a buscar
    productos_ejemplo = ["leche", "pan", "huevos"]
    
    print(f"\n📝 Productos a buscar: {productos_ejemplo}")
    print("\n" + "─" * 80)
    
    # Ejecutar búsqueda completa
    try:
        resultado_json = buscar_productos_mercadona(productos_ejemplo)
        
        # Convertir de JSON string a dict para análisis
        import json
        resultado_dict = json.loads(resultado_json)
        
        # Mostrar resumen
        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + " " * 30 + "RESULTADO FINAL" + " " * 33 + "║")
        print("╠" + "═" * 78 + "╣")
        
        if "error" in resultado_dict:
            print(f"║  ❌ Error: {resultado_dict['error']:<66} ║")
        else:
            print(f"║  📊 Productos buscados:  {len(resultado_dict['productos_buscados']):<49} ║")
            print(f"║  ✅ Productos encontrados: {resultado_dict['total_encontrados']:<47} ║")
            print("╠" + "═" * 78 + "╣")
            
            # Mostrar cada producto encontrado
            for i, producto in enumerate(resultado_dict['productos'], 1):
                print(f"║  {i}. {producto['producto_buscado'].upper():<73} ║")
                print(f"║     Producto: {producto['nombre']:<62} ║")
                
                # Manejar packaging que puede ser None
                packaging = producto.get('packaging') or 'N/A'
                print(f"║     Precio: {producto['precio_unidad']}€ | Packaging: {packaging:<39} ║")
                
                if producto.get('precio_referencia'):
                    print(f"║     Ref: {producto['precio_referencia']} {producto.get('formato_referencia', ''):<57} ║")
                print("║" + " " * 78 + "║")
        
        print("╚" + "═" * 78 + "╝")
        
        # Mostrar JSON completo
        print("\n" + "─" * 80)
        print("📄 JSON COMPLETO:")
        print("─" * 80)
        print(resultado_json)
        
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()