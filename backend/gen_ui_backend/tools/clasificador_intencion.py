"""
Tool para clasificar la intención del usuario y extraer productos mencionados.
Implementa lógica de NLP básica con regex para análisis de texto.
"""
import re
from typing import Any, Dict
from langchain_core.tools import tool


# Palabras clave para detectar intenciones
PALABRAS_COMPRA = [
    "quiero", "necesito", "comprar", "dame", "busca", "buscar",
    "añade", "añadir", "agregar", "lista", "carrito", "pedido"
]

PALABRAS_CONSULTA = [
    "cuanto", "cuánto", "cuesta", "precio", "vale", "coste",
    "disponible", "hay", "tienes", "tiene", "existe", "vende",
    "información", "info", "detalles", "dime"
]

# Palabras comunes de productos en supermercado
PRODUCTOS_COMUNES = [
    "leche", "pan", "huevos", "agua", "aceite", "arroz", "pasta",
    "tomate", "cebolla", "patata", "zanahoria", "manzana", "plátano",
    "naranja", "carne", "pollo", "pescado", "queso", "yogur",
    "mantequilla", "azúcar", "sal", "harina", "café", "té",
    "galletas", "chocolate", "cereales", "jamón", "chorizo"
]

# Números en español
NUMEROS_TEXTO = {
    "un": 1, "una": 1, "uno": 1,
    "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
    "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15,
    "dieciseis": 16, "dieciséis": 16, "diecisiete": 17, "dieciocho": 18,
    "diecinueve": 19, "veinte": 20,
    "media": 0.5, "medio": 0.5
}


@tool
def clasificar_intencion(user_input: str) -> Dict[str, Any]:
    """
    Clasifica la intención del usuario y extrae los productos mencionados.
    
    Usa análisis de palabras clave y regex para:
    1. Determinar si es una compra, consulta u otra acción
    2. Extraer nombres de productos mencionados
    3. Detectar cantidades asociadas a cada producto
    
    Args:
        user_input: El mensaje del usuario
        
    Returns:
        Dict con:
        - intencion: tipo de intención ("compra", "consulta", "otro")
        - productos: lista de productos mencionados
        - cantidades: dict con producto -> cantidad
        - confianza: nivel de confianza en la clasificación (0-1)
    """
    try:
        texto = user_input.lower().strip()
        
        # 1. CLASIFICAR INTENCIÓN
        score_compra = sum(1 for palabra in PALABRAS_COMPRA if palabra in texto)
        score_consulta = sum(1 for palabra in PALABRAS_CONSULTA if palabra in texto)
        
        if score_compra > score_consulta:
            intencion = "compra"
            confianza = min(score_compra / 3.0, 1.0)  # Normalizar
        elif score_consulta > 0:
            intencion = "consulta"
            confianza = min(score_consulta / 3.0, 1.0)
        else:
            intencion = "compra"  # Por defecto asumir compra
            confianza = 0.5
        
        print(f"📋 Intención detectada: {intencion} (confianza: {confianza:.2f})")
        
        # 2. EXTRAER PRODUCTOS
        productos = []
        
        # Buscar productos comunes
        for producto in PRODUCTOS_COMUNES:
            if producto in texto:
                productos.append(producto)
                print(f"   ✅ Producto encontrado: {producto}")
        
        # Buscar patrones adicionales: "de [producto]", "[producto]s"
        # Esto captura variaciones como "leches", "panes", etc.
        palabras = texto.split()
        for palabra in palabras:
            # Remover plural simple
            if palabra.endswith("s") and len(palabra) > 3:
                singular = palabra[:-1]
                if singular in PRODUCTOS_COMUNES and singular not in productos:
                    productos.append(singular)
                    print(f"   ✅ Producto encontrado (plural): {singular}")
        
        # Si no se encontraron productos, intentar extraer sustantivos potenciales
        if not productos:
            # Buscar palabras después de "de", preposiciones, etc.
            patrones = [
                r"de\s+(\w+)",
                r"un\s+(\w+)",
                r"una\s+(\w+)",
                r"comprar\s+(\w+)",
                r"quiero\s+(\w+)"
            ]
            for patron in patrones:
                matches = re.findall(patron, texto)
                for match in matches:
                    if match not in productos and len(match) > 3:
                        productos.append(match)
                        print(f"   ⚠️  Producto potencial: {match}")
        
        # 3. EXTRAER CANTIDADES CON PATRONES MEJORADOS
        cantidades = {}
        
        # Patrón mejorado: múltiples formas de expresar cantidades
        # Ejemplos: "2 leches", "leche x 2", "tres panes", "3 de leche", "leches x3"
        for producto in productos:
            cantidad = 1  # Por defecto
            cantidad_encontrada = False
            
            # Escapar caracteres especiales en el nombre del producto para regex
            producto_escaped = re.escape(producto)
            
            # Patrón 1: número + producto (ej: "2 leches", "3 panes")
            patron_numero_antes = rf"(\d+)\s*(?:de\s+)?{producto_escaped}s?"
            match = re.search(patron_numero_antes, texto)
            if match:
                cantidad = int(match.group(1))
                cantidad_encontrada = True
                print(f"   📊 [Patrón número antes] {producto}: {cantidad}")
            
            # Patrón 2: texto número + producto (ej: "dos leches", "tres panes")
            if not cantidad_encontrada:
                patron_texto_antes = rf"({'|'.join(NUMEROS_TEXTO.keys())})\s*(?:de\s+)?{producto_escaped}s?"
                match = re.search(patron_texto_antes, texto)
                if match:
                    cantidad = NUMEROS_TEXTO.get(match.group(1), 1)
                    cantidad_encontrada = True
                    print(f"   📊 [Patrón texto antes] {producto}: {cantidad}")
            
            # Patrón 3: producto + x + número (ej: "leche x 2", "pan x3")
            if not cantidad_encontrada:
                patron_x_despues = rf"{producto_escaped}s?\s*x\s*(\d+)"
                match = re.search(patron_x_despues, texto)
                if match:
                    cantidad = int(match.group(1))
                    cantidad_encontrada = True
                    print(f"   📊 [Patrón x después] {producto}: {cantidad}")
            
            # Patrón 4: "de" + producto (ej: "3 de leche", "cinco de pan")
            if not cantidad_encontrada:
                patron_de = rf"(\d+|{'|'.join(NUMEROS_TEXTO.keys())})\s+de\s+{producto_escaped}s?"
                match = re.search(patron_de, texto)
                if match:
                    cantidad_str = match.group(1)
                    if cantidad_str.isdigit():
                        cantidad = int(cantidad_str)
                    else:
                        cantidad = NUMEROS_TEXTO.get(cantidad_str, 1)
                    cantidad_encontrada = True
                    print(f"   📊 [Patrón de] {producto}: {cantidad}")
            
            # Patrón 5: coma o "y" separadores (ej: "2 leches, 3 panes y 4 huevos")
            # Buscar la cantidad más cercana antes del producto
            if not cantidad_encontrada:
                # Buscar hacia atrás desde el producto
                pos_producto = texto.find(producto)
                if pos_producto > 0:
                    texto_antes = texto[:pos_producto]
                    # Buscar el último número antes del producto (máximo 20 caracteres atrás)
                    texto_antes_cercano = texto_antes[-20:]
                    match_numero = re.search(r'(\d+)\s*$', texto_antes_cercano)
                    if match_numero:
                        cantidad = int(match_numero.group(1))
                        cantidad_encontrada = True
                        print(f"   📊 [Patrón cercano] {producto}: {cantidad}")
                    else:
                        # Buscar texto número
                        for num_texto, num_valor in NUMEROS_TEXTO.items():
                            if num_texto in texto_antes_cercano:
                                cantidad = num_valor
                                cantidad_encontrada = True
                                print(f"   📊 [Patrón texto cercano] {producto}: {cantidad}")
                                break
            
            cantidades[producto] = cantidad
            if not cantidad_encontrada:
                print(f"   📊 [Por defecto] {producto}: {cantidad}")
        
        # Si hay productos sin cantidades explícitas, asignar 1
        for producto in productos:
            if producto not in cantidades:
                cantidades[producto] = 1
        
        resultado = {
            "intencion": intencion,
            "productos": productos,
            "cantidades": cantidades,
            "confianza": round(confianza, 2),
            "num_productos": len(productos)
        }
        
        print(f"✅ Clasificación completada: {len(productos)} productos detectados")
        return resultado
    
    except Exception as e:
        print(f"❌ Error al clasificar intención: {e}")
        import traceback
        traceback.print_exc()
        
        # Retornar resultado por defecto en caso de error
        return {
            "intencion": "compra",
            "productos": [],
            "cantidades": {},
            "confianza": 0.0,
            "num_productos": 0,
            "error": str(e)
        }

