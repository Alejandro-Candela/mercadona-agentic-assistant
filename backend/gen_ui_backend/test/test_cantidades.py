"""
Test para verificar la detección correcta de cantidades en el clasificador de intención.
"""
import sys
sys.path.insert(0, '.')

from gen_ui_backend.tools.clasificador_intencion import clasificar_intencion


def test_cantidades():
    """Prueba diferentes formas de expresar cantidades."""
    
    casos_de_prueba = [
        # Formato: (entrada, productos_esperados, cantidades_esperadas)
        ("quiero 2 leches", ["leche"], {"leche": 2}),
        ("dame 3 panes y 2 leches", ["pan", "leche"], {"pan": 3, "leche": 2}),
        ("necesito tres leches, dos panes y cinco huevos", ["leche", "pan", "huevos"], {"leche": 3, "pan": 2, "huevos": 5}),
        ("comprar leche x 4 y pan x 2", ["leche", "pan"], {"leche": 4, "pan": 2}),
        ("3 de leche y 5 de pan", ["leche", "pan"], {"leche": 3, "pan": 5}),
        ("quiero cinco de leche", ["leche"], {"leche": 5}),
        ("dame 10 huevos y 6 leches", ["huevos", "leche"], {"huevos": 10, "leche": 6}),
        ("necesito leche", ["leche"], {"leche": 1}),  # Sin cantidad = 1
        ("2 leches, 3 panes, 4 huevos", ["leche", "pan", "huevos"], {"leche": 2, "pan": 3, "huevos": 4}),
    ]
    
    print("\n" + "="*80)
    print("PRUEBA DE DETECCIÓN DE CANTIDADES")
    print("="*80 + "\n")
    
    tests_pasados = 0
    tests_fallidos = 0
    
    for entrada, productos_esperados, cantidades_esperadas in casos_de_prueba:
        print(f"\n🧪 Test: '{entrada}'")
        print(f"   Esperado: productos={productos_esperados}, cantidades={cantidades_esperadas}")
        
        resultado = clasificar_intencion.invoke({"user_input": entrada})
        productos_obtenidos = resultado.get("productos", [])
        cantidades_obtenidas = resultado.get("cantidades", {})
        
        print(f"   Obtenido: productos={productos_obtenidos}, cantidades={cantidades_obtenidas}")
        
        # Verificar productos
        productos_ok = set(productos_obtenidos) == set(productos_esperados)
        
        # Verificar cantidades
        cantidades_ok = True
        for producto in productos_esperados:
            if producto in cantidades_obtenidas:
                if cantidades_obtenidas[producto] != cantidades_esperadas[producto]:
                    cantidades_ok = False
                    print(f"   ❌ Cantidad incorrecta para {producto}: esperado {cantidades_esperadas[producto]}, obtenido {cantidades_obtenidas[producto]}")
            else:
                cantidades_ok = False
                print(f"   ❌ Falta cantidad para {producto}")
        
        if productos_ok and cantidades_ok:
            print("   ✅ Test PASADO")
            tests_pasados += 1
        else:
            print("   ❌ Test FALLIDO")
            if not productos_ok:
                print(f"      - Productos no coinciden")
            tests_fallidos += 1
    
    print("\n" + "="*80)
    print(f"RESUMEN: {tests_pasados} pasados, {tests_fallidos} fallidos de {len(casos_de_prueba)} tests")
    print("="*80 + "\n")
    
    return tests_fallidos == 0


if __name__ == "__main__":
    success = test_cantidades()
    sys.exit(0 if success else 1)

