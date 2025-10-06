"""
Tool para generar archivos descargables del ticket de compra.
Crea archivos en formato JSON, TXT y CSV con la información del ticket.
"""
import os
import json
import csv
from typing import Any, Dict, List
from datetime import datetime
from langchain_core.tools import tool


@tool
def generar_archivos_ticket(
    productos: List[Dict[str, Any]],  # noqa: ARG001
    cantidades: Dict[str, int],  # noqa: ARG001
    precio_info: Dict[str, Any],
    directorio_salida: str = "tickets"
) -> Dict[str, str]:
    """
    Genera archivos descargables del ticket de compra en múltiples formatos.
    
    Args:
        productos: Lista de productos con información completa
        cantidades: Cantidades de cada producto
        precio_info: Información de precios calculados
        directorio_salida: Directorio donde guardar los archivos
        
    Returns:
        Dict con rutas de archivos generados: json_path, txt_path, csv_path
    """
    try:
        # Crear directorio si no existe
        os.makedirs(directorio_salida, exist_ok=True)
        
        # Generar timestamp para nombres únicos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"ticket_{timestamp}"
        
        # Preparar datos
        items = precio_info.get("items", [])
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # ========== GENERAR JSON ==========
        json_data = {
            "fecha": fecha_hora,
            "timestamp": timestamp,
            "resumen": {
                "articulos_diferentes": precio_info.get("num_items", 0),
                "unidades_totales": precio_info.get("num_productos", 0),
                "subtotal": precio_info.get("subtotal", 0.0),
                "descuentos": precio_info.get("descuentos", 0.0),
                "total": precio_info.get("total", 0.0)
            },
            "productos": []
        }
        
        for item in items:
            producto_json = {
                "producto_id": item.get("producto_id", ""),
                "nombre": item.get("nombre", ""),
                "cantidad": item.get("cantidad", 0),
                "precio_unitario": item.get("precio_unitario", 0.0),
                "precio_total": item.get("precio_total", 0.0),
                "packaging": item.get("packaging", ""),
                "categoria": item.get("categoria", "")
            }
            json_data["productos"].append(producto_json)
        
        json_path = os.path.join(directorio_salida, f"{base_filename}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        # ========== GENERAR TXT ==========
        txt_content = f"""╔═══════════════════════════════════════════════════════╗
║              MERCADONA - TICKET DE COMPRA             ║
╚═══════════════════════════════════════════════════════╝

Fecha: {fecha_hora}

───────────────────────────────────────────────────────
PRODUCTOS
───────────────────────────────────────────────────────
"""
        
        for i, item in enumerate(items, 1):
            nombre = item.get("nombre", "")
            cantidad = item.get("cantidad", 0)
            precio_unitario = item.get("precio_unitario", 0.0)
            precio_total = item.get("precio_total", 0.0)
            packaging = item.get("packaging", "")
            
            txt_content += f"{i}. {nombre}\n"
            if packaging:
                txt_content += f"   {packaging}\n"
            txt_content += f"   {cantidad} x {precio_unitario:.2f}€ = {precio_total:.2f}€\n\n"
        
        subtotal = precio_info.get("subtotal", 0.0)
        descuentos = precio_info.get("descuentos", 0.0)
        total = precio_info.get("total", 0.0)
        num_items = precio_info.get("num_items", 0)
        num_productos = precio_info.get("num_productos", 0)
        
        txt_content += f"""───────────────────────────────────────────────────────
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
        
        txt_path = os.path.join(directorio_salida, f"{base_filename}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(txt_content)
        
        # ========== GENERAR CSV ==========
        csv_path = os.path.join(directorio_salida, f"{base_filename}.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(["MERCADONA - TICKET DE COMPRA"])
            writer.writerow([f"Fecha: {fecha_hora}"])
            writer.writerow([])
            
            # Columnas de productos
            writer.writerow([
                "Nº", "Producto", "Cantidad", "Precio Unitario (€)", 
                "Precio Total (€)", "Packaging"
            ])
            
            # Productos
            for i, item in enumerate(items, 1):
                writer.writerow([
                    i,
                    item.get("nombre", ""),
                    item.get("cantidad", 0),
                    f"{item.get('precio_unitario', 0.0):.2f}",
                    f"{item.get('precio_total', 0.0):.2f}",
                    item.get("packaging", "")
                ])
            
            # Resumen
            writer.writerow([])
            writer.writerow(["RESUMEN"])
            writer.writerow(["Artículos diferentes", num_items])
            writer.writerow(["Unidades totales", num_productos])
            writer.writerow([])
            writer.writerow(["Subtotal", f"{subtotal:.2f}€"])
            writer.writerow(["Descuentos", f"{descuentos:.2f}€"])
            writer.writerow(["TOTAL A PAGAR", f"{total:.2f}€"])
        
        # Obtener rutas absolutas
        json_path_abs = os.path.abspath(json_path)
        txt_path_abs = os.path.abspath(txt_path)
        csv_path_abs = os.path.abspath(csv_path)
        
        resultado = {
            "json_path": json_path_abs,
            "txt_path": txt_path_abs,
            "csv_path": csv_path_abs,
            "timestamp": timestamp,
            "success": True
        }
        
        print("✅ Archivos generados exitosamente:")
        print(f"   - JSON: {json_path_abs}")
        print(f"   - TXT: {txt_path_abs}")
        print(f"   - CSV: {csv_path_abs}")
        
        return resultado
    
    except Exception as e:
        print(f"❌ Error al generar archivos: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "success": False,
            "error": str(e),
            "json_path": "",
            "txt_path": "",
            "csv_path": "",
            "timestamp": ""
        }

