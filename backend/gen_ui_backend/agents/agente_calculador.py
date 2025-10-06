"""
Agente 3: Calculador de precios y generador del ticket de compra.

Calcula el precio total de los productos encontrados y
genera un ticket de compra formateado.
"""
from typing import Literal
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from gen_ui_backend.agents.state import MultiAgentState
from gen_ui_backend.tools.calculador_ticket import calcular_precio_total, generar_ticket_compra
from gen_ui_backend.tools.generador_archivos import generar_archivos_ticket


def agente_3_calculador(
    state: MultiAgentState,
    config: RunnableConfig  # noqa: ARG001 - Requerido por la interfaz
) -> Command[Literal["respuesta_final"]]:
    """
    Agente 3: Calculador de precios y generador del ticket de compra.
    
    Calcula el precio total de los productos encontrados y
    genera un ticket de compra formateado.
    """
    print("\n=== AGENTE 3: CALCULADOR ===")
    
    productos = state.get("productos_encontrados", [])
    cantidades = state.get("cantidades", {})
    intencion = state.get("intencion", "compra")
    productos_no_encontrados = state.get("productos_no_encontrados", [])
    
    print(f"Calculando precios para {len(productos)} productos")
    
    try:
        # Calcular precios
        precio_info = calcular_precio_total.invoke({
            "productos": productos,
            "cantidades": cantidades
        })
        
        print(f"Total calculado: {precio_info.get('total')}€")
        
        # Generar ticket
        ticket = generar_ticket_compra.invoke({
            "productos": productos,
            "cantidades": cantidades,
            "precio_info": precio_info
        })
        
        print("Ticket generado exitosamente")
        
        # Generar archivos descargables
        archivos_info = generar_archivos_ticket.invoke({
            "productos": productos,
            "cantidades": cantidades,
            "precio_info": precio_info
        })
        
        print("Archivos descargables generados exitosamente")
        
        # Preparar tabla de productos para el mensaje
        items = precio_info.get("items", [])
        tabla_productos = "\n\n📦 **LISTA DE LA COMPRA**\n\n"
        tabla_productos += "| Nº | Producto | Cantidad | Precio Unit. | Precio Total |\n"
        tabla_productos += "|---|---|---|---|---|\n"
        
        for i, item in enumerate(items, 1):
            nombre = item.get("nombre", "")
            cantidad = item.get("cantidad", 0)
            precio_unitario = item.get("precio_unitario", 0.0)
            precio_total = item.get("precio_total", 0.0)
            
            # Truncar nombre si es muy largo
            if len(nombre) > 35:
                nombre = nombre[:32] + "..."
            
            tabla_productos += f"| {i} | {nombre} | {cantidad} | {precio_unitario:.2f}€ | **{precio_total:.2f}€** |\n"
        
        # Preparar mensaje consolidado con información de los 3 agentes
        mensaje_consolidado = f"""🔄 **PROCESO COMPLETADO**

---

📋 **AGENTE 1: CLASIFICADOR**
- Intención detectada: **{intencion}**
- Productos solicitados: **{len(productos) + len(productos_no_encontrados)}**

---

🔍 **AGENTE 2: BUSCADOR**
- Productos encontrados: **{len(productos)}**
"""
        
        for prod in productos:
            mensaje_consolidado += f"\n  ✓ {prod.get('nombre')} - {prod.get('precio_unidad')}€"
        
        if productos_no_encontrados:
            mensaje_consolidado += f"\n- Productos no disponibles: **{len(productos_no_encontrados)}**"
            for prod_no in productos_no_encontrados:
                mensaje_consolidado += f"\n  ✗ {prod_no}"
        
        mensaje_consolidado += f"""

---

💰 **AGENTE 3: CALCULADOR**
- Subtotal: {precio_info.get('subtotal')}€
- Descuentos: {precio_info.get('descuentos')}€
- **TOTAL: {precio_info.get('total')}€**

---

{tabla_productos}

---

📥 **ARCHIVOS DESCARGABLES**

Los archivos del ticket han sido generados y están listos para descargar:

- 📄 **JSON**: `{archivos_info.get('json_path', 'N/A')}`
- 📝 **TXT**: `{archivos_info.get('txt_path', 'N/A')}`
- 📊 **CSV**: `{archivos_info.get('csv_path', 'N/A')}`

---

{ticket}
"""
        
        return Command(
            goto="respuesta_final",
            update={
                "precio_info": precio_info,
                "ticket": ticket,
                "archivos_generados": archivos_info,
                "final_result": mensaje_consolidado,
                "current_agent": "agente_3"
            }
        )
    
    except Exception as e:
        print(f"Error en cálculo: {e}")
        mensaje_error = f"❌ Ha ocurrido un error al calcular el total: {str(e)}"
        return Command(
            goto="respuesta_final",
            update={
                "final_result": mensaje_error,
                "current_agent": "agente_3"
            }
        )

