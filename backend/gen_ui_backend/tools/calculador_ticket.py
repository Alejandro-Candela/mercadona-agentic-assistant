"""
Tool para calcular precios y generar ticket de compra.
Implementa lógica real de cálculo y formateo de tickets de Mercadona.
"""
from typing import Any, Dict, List
from datetime import datetime
from langchain_core.tools import tool


@tool
def calcular_precio_total(productos: List[Dict[str, Any]], cantidades: Dict[str, int]) -> Dict[str, Any]:
    """
    Calcula el precio total de una lista de productos con sus cantidades.
    
    Args:
        productos: Lista de productos con información (incluyendo precio_unidad)
        cantidades: Dict con producto_nombre -> cantidad o producto_buscado -> cantidad
        
    Returns:
        Dict con:
        - subtotal: Suma de precios sin descuentos
        - descuentos: Descuentos aplicados
        - total: Precio final
        - items: Lista detallada de items con precio individual y total por item
    """
    try:
        items = []
        subtotal = 0.0
        
        for producto in productos:
            # Buscar cantidad por nombre del producto o por producto_buscado
            nombre = producto.get("nombre", "")
            producto_buscado = producto.get("producto_buscado", "")
            precio_unitario = float(producto.get("precio_unidad", 0.0))
            
            # Intentar encontrar la cantidad usando diferentes claves
            cantidad = 0
            for key in cantidades:
                key_lower = str(key).lower()
                if (key_lower in nombre.lower() or 
                    key_lower in producto_buscado.lower() or
                    nombre.lower() in key_lower or
                    producto_buscado.lower() in key_lower):
                    cantidad = int(cantidades[key])
                    break
            
            # Si no se encontró cantidad, asumir 1
            if cantidad == 0:
                cantidad = 1
            
            # Calcular precio total del item
            precio_total_item = precio_unitario * cantidad
            subtotal += precio_total_item
            
            # Crear item detallado
            item = {
                "producto_id": producto.get("id", ""),
                "nombre": nombre,
                "producto_buscado": producto_buscado,
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "precio_total": round(precio_total_item, 2),
                "packaging": producto.get("packaging", ""),
                "categoria": producto.get("categoria", "")
            }
            items.append(item)
        
        # Calcular descuentos (futuro: implementar lógica de descuentos real)
        descuentos = 0.0
        
        # Calcular total final
        total = subtotal - descuentos
        
        resultado = {
            "subtotal": round(subtotal, 2),
            "descuentos": round(descuentos, 2),
            "total": round(total, 2),
            "items": items,
            "num_items": len(items),
            "num_productos": sum(item["cantidad"] for item in items)
        }
        
        print(f"✅ Precio calculado: Subtotal {resultado['subtotal']}€, Total {resultado['total']}€")
        return resultado
    
    except Exception as e:
        print(f"❌ Error al calcular precio total: {e}")
        import traceback
        traceback.print_exc()
        return {
            "subtotal": 0.0,
            "descuentos": 0.0,
            "total": 0.0,
            "items": [],
            "error": str(e)
        }


@tool
def generar_ticket_compra(
    productos: List[Dict[str, Any]], 
    cantidades: Dict[str, int],
    precio_info: Dict[str, Any]
) -> str:
    """
    Genera un ticket de compra formateado estilo Mercadona.
    
    Args:
        productos: Lista de productos
        cantidades: Cantidades de cada producto
        precio_info: Información de precios (del calcular_precio_total)
        
    Returns:
        String con el ticket formateado
    """
    try:
        # Header del ticket
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        ticket = f"""
╔═══════════════════════════════════════════════════════╗
║              MERCADONA - TICKET DE COMPRA             ║
╚═══════════════════════════════════════════════════════╝

Fecha: {fecha_hora}

───────────────────────────────────────────────────────
PRODUCTOS
───────────────────────────────────────────────────────
"""
        
        # Listar items
        items = precio_info.get("items", [])
        for i, item in enumerate(items, 1):
            nombre = item.get("nombre", "")
            cantidad = item.get("cantidad", 0)
            precio_unitario = item.get("precio_unitario", 0.0)
            precio_total = item.get("precio_total", 0.0)
            packaging = item.get("packaging", "")
            
            # Truncar nombre si es muy largo
            if len(nombre) > 40:
                nombre = nombre[:37] + "..."
            
            ticket += f"{i}. {nombre}\n"
            if packaging:
                ticket += f"   {packaging}\n"
            ticket += f"   {cantidad} x {precio_unitario:.2f}€ = {precio_total:.2f}€\n\n"
        
        # Resumen de precios
        subtotal = precio_info.get("subtotal", 0.0)
        descuentos = precio_info.get("descuentos", 0.0)
        total = precio_info.get("total", 0.0)
        num_items = precio_info.get("num_items", 0)
        num_productos = precio_info.get("num_productos", 0)
        
        ticket += f"""───────────────────────────────────────────────────────
RESUMEN
───────────────────────────────────────────────────────
Artículos diferentes: {num_items}
Unidades totales: {num_productos}

Subtotal:        {subtotal:>8.2f}€
Descuentos:      {descuentos:>8.2f}€
───────────────────────────────────────────────────────
TOTAL A PAGAR:   {total:>8.2f}€
═══════════════════════════════════════════════════════

          ¡Gracias por su compra!
          Vuelva pronto a Mercadona
          
═══════════════════════════════════════════════════════
"""
        
        print("✅ Ticket generado exitosamente")
        return ticket
    
    except Exception as e:
        print(f"❌ Error al generar ticket: {e}")
        import traceback
        traceback.print_exc()
        
        # Ticket de error
        return f"""
═══════════════════════════════════════════════════════
ERROR AL GENERAR TICKET
═══════════════════════════════════════════════════════
{str(e)}
═══════════════════════════════════════════════════════
"""

