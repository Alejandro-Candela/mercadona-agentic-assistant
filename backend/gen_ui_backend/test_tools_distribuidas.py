"""
Script de prueba para las herramientas distribuidas del sistema multi-agente.
Demuestra el uso de las tools con la API real de Mercadona.
"""

from tools.clasificador_intencion import clasificar_intencion
from tools.buscador_mercadona import buscar_multiples_productos
from tools.calculador_ticket import calcular_precio_total, generar_ticket_compra


def test_flujo_completo():
    """
    Prueba el flujo completo del sistema multi-agente:
    1. Clasificación de intención
    2. Búsqueda de productos
    3. Cálculo de precios
    4. Generación de ticket
    """
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "PRUEBA DEL SISTEMA MULTI-AGENTE" + " " * 27 + "║")
    print("╚" + "═" * 78 + "╝\n")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PASO 1: CLASIFICAR INTENCIÓN
    # ═══════════════════════════════════════════════════════════════════════════
    
    print("─" * 80)
    print("PASO 1: CLASIFICACIÓN DE INTENCIÓN")
    print("─" * 80)
    
    mensaje_usuario = "Quiero comprar 2 leches y un pan"
    print(f"Mensaje del usuario: '{mensaje_usuario}'\n")
    
    clasificacion = clasificar_intencion.invoke(mensaje_usuario)
    
    print(f"\n📊 Resultado de clasificación:")
    print(f"   Intención: {clasificacion['intencion']}")
    print(f"   Productos detectados: {clasificacion['productos']}")
    print(f"   Cantidades: {clasificacion['cantidades']}")
    print(f"   Confianza: {clasificacion['confianza']}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PASO 2: BUSCAR PRODUCTOS
    # ═══════════════════════════════════════════════════════════════════════════
    
    print("\n" + "─" * 80)
    print("PASO 2: BÚSQUEDA DE PRODUCTOS EN MERCADONA")
    print("─" * 80)
    
    if not clasificacion['productos']:
        print("⚠️  No se detectaron productos para buscar")
        return
    
    productos_encontrados = buscar_multiples_productos.invoke(clasificacion['productos'])
    
    print(f"\n📦 Productos encontrados: {len(productos_encontrados)}")
    for i, producto in enumerate(productos_encontrados, 1):
        print(f"\n   {i}. {producto['nombre']}")
        print(f"      Precio: {producto['precio_unidad']}€")
        print(f"      Categoría: {producto['categoria']}")
        print(f"      Packaging: {producto.get('packaging', 'N/A')}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PASO 3: CALCULAR PRECIO TOTAL
    # ═══════════════════════════════════════════════════════════════════════════
    
    print("\n" + "─" * 80)
    print("PASO 3: CÁLCULO DE PRECIO TOTAL")
    print("─" * 80)
    
    precio_info = calcular_precio_total.invoke(
        productos_encontrados,
        clasificacion['cantidades']
    )
    
    print(f"\n💰 Información de precios:")
    print(f"   Subtotal: {precio_info['subtotal']}€")
    print(f"   Descuentos: {precio_info['descuentos']}€")
    print(f"   Total: {precio_info['total']}€")
    print(f"   Artículos diferentes: {precio_info['num_items']}")
    print(f"   Unidades totales: {precio_info['num_productos']}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PASO 4: GENERAR TICKET
    # ═══════════════════════════════════════════════════════════════════════════
    
    print("\n" + "─" * 80)
    print("PASO 4: GENERACIÓN DE TICKET")
    print("─" * 80)
    
    ticket = generar_ticket_compra.invoke(
        productos_encontrados,
        clasificacion['cantidades'],
        precio_info
    )
    
    print(ticket)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # RESUMEN FINAL
    # ═══════════════════════════════════════════════════════════════════════════
    
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 30 + "PRUEBA COMPLETADA" + " " * 31 + "║")
    print("╠" + "═" * 78 + "╣")
    print(f"║  ✅ Intención clasificada: {clasificacion['intencion']:<51} ║")
    print(f"║  ✅ Productos encontrados: {len(productos_encontrados):<51} ║")
    print(f"║  ✅ Precio calculado: {precio_info['total']}€{' ' * (57 - len(str(precio_info['total'])))} ║")
    print(f"║  ✅ Ticket generado correctamente{' ' * 46} ║")
    print("╚" + "═" * 78 + "╝")


def test_clasificador_simple():
    """
    Prueba simple del clasificador de intenciones.
    """
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 25 + "PRUEBA DEL CLASIFICADOR" + " " * 30 + "║")
    print("╚" + "═" * 78 + "╝\n")
    
    mensajes_prueba = [
        "Quiero 3 leches y 2 panes",
        "¿Cuánto cuesta el aceite?",
        "Dame huevos y jamón",
        "Necesito comprar arroz",
    ]
    
    for mensaje in mensajes_prueba:
        print(f"\n📝 Mensaje: '{mensaje}'")
        resultado = clasificar_intencion.invoke(mensaje)
        print(f"   Intención: {resultado['intencion']} (confianza: {resultado['confianza']})")
        print(f"   Productos: {resultado['productos']}")
        print(f"   Cantidades: {resultado['cantidades']}")


if __name__ == "__main__":
    import sys
    
    print("\n" + "═" * 80)
    print("SISTEMA DE PRUEBAS - HERRAMIENTAS DISTRIBUIDAS")
    print("═" * 80 + "\n")
    
    print("Opciones:")
    print("  1. Prueba completa del flujo multi-agente")
    print("  2. Prueba simple del clasificador")
    print()
    
    # Si se pasa argumento, usar ese
    if len(sys.argv) > 1:
        opcion = sys.argv[1]
    else:
        opcion = input("Selecciona una opción (1 o 2): ").strip()
    
    try:
        if opcion == "1":
            test_flujo_completo()
        elif opcion == "2":
            test_clasificador_simple()
        else:
            print("❌ Opción no válida")
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()

