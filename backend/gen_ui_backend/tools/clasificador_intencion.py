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
        
        # 3. EXTRAER CANTIDADES
        cantidades = {}
        
        # Patrón: [número] [producto] o [producto] x [número]
        # Ejemplos: "2 leches", "leche x 2", "tres panes"
        for producto in productos:
            cantidad = 1  # Por defecto
            
            # Buscar número antes del producto
            patron_antes = rf"(\d+)\s+{producto}"
            match = re.search(patron_antes, texto)
            if match:
                cantidad = int(match.group(1))
            
            # Buscar número en texto antes del producto
            patron_texto = rf"({'|'.join(NUMEROS_TEXTO.keys())})\s+{producto}"
            match = re.search(patron_texto, texto)
            if match:
                cantidad = NUMEROS_TEXTO.get(match.group(1), 1)
            
            # Buscar número después con "x"
            patron_x = rf"{producto}\s*x\s*(\d+)"
            match = re.search(patron_x, texto)
            if match:
                cantidad = int(match.group(1))
            
            cantidades[producto] = cantidad
            print(f"   📊 Cantidad de {producto}: {cantidad}")
        
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

