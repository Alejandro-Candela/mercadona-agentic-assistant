"""
Script de prueba simple para probar las tools individualmente.
"""
from gen_ui_backend.tools.clasificador_intencion import clasificar_intencion
from gen_ui_backend.tools.buscador_mercadona import buscar_multiples_productos
from gen_ui_backend.tools.calculador_ticket import calcular_precio_total, generar_ticket_compra


def test_clasificador():
    """Prueba del clasificador."""
    print("\n" + "="*80)
    print("TEST 1: CLASIFICADOR DE INTENCIÓN")
    print("="*80)
    
    mensaje = "Quiero 2 leches y un pan"
    print(f"Mensaje: '{mensaje}'")
    
    resultado = clasificar_intencion.invoke({"user_input": mensaje})
    print(f"\nResultado:")
    print(f"  Intención: {resultado.get('intencion')}")
    print(f"  Productos: {resultado.get('productos')}")
    print(f"  Cantidades: {resultado.get('cantidades')}")
    print(f"  Confianza: {resultado.get('confianza')}")
    
    return resultado


def test_buscador(productos):
    """Prueba del buscador."""
    print("\n" + "="*80)
    print("TEST 2: BUSCADOR DE PRODUCTOS")
    print("="*80)
    
    print(f"Buscando: {productos}")
    
    # Las tools de LangChain esperan un diccionario con los parámetros
    resultados = buscar_multiples_productos.invoke({"productos": productos})
    
    print(f"\nEncontrados {len(resultados)} productos:")
    for prod in resultados:
        print(f"  - {prod.get('nombre')}: {prod.get('precio_unidad')}€")
    
    return resultados


def test_calculador(productos, cantidades):
    """Prueba del calculador."""
    print("\n" + "="*80)
    print("TEST 3: CALCULADOR DE PRECIOS")
    print("="*80)
    
    # Las tools de LangChain esperan un diccionario con los parámetros
    precio_info = calcular_precio_total.invoke({
        "productos": productos,
        "cantidades": cantidades
    })
    
    print(f"\nPrecio Info:")
    print(f"  Subtotal: {precio_info.get('subtotal')}€")
    print(f"  Descuentos: {precio_info.get('descuentos')}€")
    print(f"  Total: {precio_info.get('total')}€")
    
    return precio_info


def test_ticket(productos, cantidades, precio_info):
    """Prueba del generador de tickets."""
    print("\n" + "="*80)
    print("TEST 4: GENERADOR DE TICKETS")
    print("="*80)
    
    ticket = generar_ticket_compra.invoke({
        "productos": productos,
        "cantidades": cantidades,
        "precio_info": precio_info
    })
    
    print("\nTicket generado:")
    print(ticket)
    
    return ticket


if __name__ == "__main__":
    try:
        # Test 1: Clasificador
        clasificacion = test_clasificador()
        
        # Test 2: Buscador (comentado por ahora para no hacer llamadas a la API)
        # productos_encontrados = test_buscador(clasificacion['productos'])
        
        # Usar datos mock para pruebas rápidas
        print("\n⚠️  Saltando búsqueda real de API (usar datos mock)")
        productos_encontrados = [
            {
                "id": "mock1",
                "nombre": "Leche semidesnatada Hacendado",
                "precio_unidad": 0.59,
                "disponible": True,
                "categoria": "Lácteos",
                "packaging": "1 L",
                "producto_buscado": "leche"
            },
            {
                "id": "mock2",
                "nombre": "Pan de molde integral",
                "precio_unidad": 0.85,
                "disponible": True,
                "categoria": "Panadería",
                "packaging": "450 g",
                "producto_buscado": "pan"
            }
        ]
        
        # Test 3: Calculador
        precio_info = test_calculador(
            productos_encontrados,
            clasificacion['cantidades']
        )
        
        # Test 4: Ticket
        ticket = test_ticket(
            productos_encontrados,
            clasificacion['cantidades'],
            precio_info
        )
        
        print("\n" + "="*80)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

